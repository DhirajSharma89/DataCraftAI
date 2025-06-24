from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uuid
import pandas as pd
import base64
from io import StringIO
import logging
import traceback

# Import the Ollama handler
from ollama_handler import generate_instructions_with_ollama

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "./uploads"
OUTPUT_FOLDER = "./output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.post("/generate-csv/")
async def generate_csv_endpoint(
    csv_file: UploadFile = File(...),
    user_prompt: str = Form(...)
):
    session_id = str(uuid.uuid4())
    temp_csv_filepath = os.path.join(UPLOAD_FOLDER, f"{session_id}_{csv_file.filename}")
    output_base_filename = os.path.splitext(csv_file.filename)[0]

    generated_output_csv_filepath_server = os.path.join(OUTPUT_FOLDER, f"{output_base_filename}_cleaned.csv")
    suggestions_filename_server = os.path.join(OUTPUT_FOLDER, f"{output_base_filename}_suggestions.txt")

    try:
        # Save uploaded file to disk
        with open(temp_csv_filepath, "wb") as buffer:
            shutil.copyfileobj(csv_file.file, buffer)
        logger.info(f"Saved uploaded file to: {temp_csv_filepath}")

        # Read CSV from saved file (not from memory stream)
        original_df = pd.read_csv(temp_csv_filepath)
        logger.info(f"Original DataFrame shape: {original_df.shape}")
        logger.info(f"Original columns: {list(original_df.columns)}")
        
        # Validate CSV was read properly
        if original_df.empty:
            raise HTTPException(status_code=400, detail="Uploaded CSV file is empty")

        # Get transformation instructions from Ollama
        ollama_instructions = generate_instructions_with_ollama(temp_csv_filepath, user_prompt)
        if not ollama_instructions:
            raise HTTPException(status_code=500, detail="Ollama did not return valid instructions.")
        
        logger.info("Ollama instructions received")
        logger.debug(f"Ollama response: {ollama_instructions}")

        transform_script = ollama_instructions.get("data_transform_script", "")
        processed_df = original_df.copy()  # Start with original as fallback
        
        if transform_script:
            try:
                logger.info(f"Executing transformation script:\n{transform_script}")
                
                # Create a safe execution environment
                safe_globals = {
                    'pd': pd,
                    'df': original_df.copy(),
                    '__builtins__': {k: v for k, v in __builtins__.items() 
                                     if k not in ['exec', 'eval', 'open', 'exit', 'quit']}
                }
                
                # Execute in isolated namespace
                local_vars = {}
                exec(transform_script, safe_globals, local_vars)
                
                # Check for transformed dataframe
                if 'df_transformed' in local_vars and isinstance(local_vars['df_transformed'], pd.DataFrame):
                    processed_df = local_vars['df_transformed']
                    logger.info("Transformation successful")
                    logger.info(f"New shape: {processed_df.shape}, New columns: {list(processed_df.columns)}")
                else:
                    logger.warning("Script didn't create 'df_transformed' DataFrame. Using original data.")
            except Exception as e:
                logger.error(f"Script execution failed: {str(e)}\n{traceback.format_exc()}")
        else:
            logger.info("No transformation script provided")

        # --- VALIDATE TRANSFORMATION ---
        logger.info(f"Final DataFrame shape: {processed_df.shape}")
        logger.info(f"Final columns: {list(processed_df.columns)}")

        # Save processed CSV to server
        processed_df.to_csv(generated_output_csv_filepath_server, index=False)
        logger.info(f"Saved processed CSV to: {generated_output_csv_filepath_server}")

        # Prepare CSV for API response
        csv_buffer = StringIO()
        processed_df.to_csv(csv_buffer, index=False)
        csv_string = csv_buffer.getvalue()
        encoded_csv = base64.b64encode(csv_string.encode('utf-8')).decode('utf-8')

        # Handle suggestions
        suggestions_text = ollama_instructions.get("tableau_suggestions", "")
        notes_text = ollama_instructions.get("notes", "")
        with open(suggestions_filename_server, "w", encoding="utf-8") as f:
            f.write("Tableau Visualization Suggestions:\n\n")
            f.write(suggestions_text + "\n\n")
            if notes_text:
                f.write("Additional Notes:\n\n" + notes_text + "\n")

        return JSONResponse(content={
            "status": "success",
            "message": "CSV processed and suggestions generated.",
            "csv_data": encoded_csv,
            "filename": f"{output_base_filename}_cleaned.csv",
            "tableau_suggestions": suggestions_text,
            "notes": notes_text
        })

    except pd.errors.EmptyDataError:
        error_msg = "Uploaded CSV file is empty or invalid"
        logger.error(error_msg)
        return JSONResponse(
            status_code=400,
            content={"detail": error_msg}
        )
    except Exception as e:
        logger.exception(f"Processing failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(e)}"}
        )
    finally:
        # Clean up temporary file
        if os.path.exists(temp_csv_filepath):
            os.remove(temp_csv_filepath)

@app.get("/download/{filename}")
async def download_output_file(filename: str):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='text/csv', filename=filename)
    raise HTTPException(status_code=404, detail="File not found")
