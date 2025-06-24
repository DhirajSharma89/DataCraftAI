import ollama
import pandas as pd
import json
import os
import io # For capturing df.info() output
import re # For regex for string cleanup

def generate_instructions_with_ollama(csv_filepath: str, user_prompt: str) -> dict:
    """
    Connects to Ollama (Mistral), provides CSV data/schema and user prompt,
    and requests structured instructions for data transformation and Tableau suggestions.

    Args:
        csv_filepath (str): Path to the uploaded CSV file.
        user_prompt (str): The user's natural language prompt.

    Returns:
        dict: A dictionary containing parsed instructions (e.g., 'data_transform_script', 'tableau_suggestions').
              Returns an empty dict if parsing fails or no valid instructions are found.
    """
    try:
        # 1. Read CSV to get schema and a sample of data
        df = pd.read_csv(csv_filepath)
        csv_head = df.head(3).to_string(index=False) # Get first 3 rows, without pandas index
        csv_columns = ", ".join(df.columns.tolist()) # Get all column names as a comma-separated string
        
        # Use StringIO to capture df.info() output
        buffer = io.StringIO()
        df.info(buf=buffer)
        csv_info_str = buffer.getvalue() # Get the string content of df.info()

        # Construct an EXTREMELY strict prompt for Mistral.
        # This prompt is designed to guide the AI very precisely on generating the Python script.
        prompt_template = f"""
**STRICT INSTRUCTIONS FOR AI:**
YOU ARE AN EXPERT AT GENERATING JSON FOR DATA PREPARATION AND VISUALIZATION SUGGESTIONS.
**YOUR ONLY OUTPUT MUST BE A SINGLE, PERFECTLY VALID JSON OBJECT.**
**DO NOT** include any conversational text, explanations, or comments (// or /* */) ANYWHERE in the output.
**DO NOT** include any Python code to generate the JSON. Just provide the JSON directly.
**DO NOT** add any extra characters, spaces, or newlines before or after the JSON block.
**ALL STRING VALUES IN THE JSON MUST USE STRAIGHT DOUBLE QUOTES ("). NO CURLY/SMART QUOTES.**

**CSV Data Context:**
- **Data Columns:** {csv_columns}
- **First 3 Rows (for data context):**
```csv
{csv_head}
```
- **Column Data Types and Non-Null Counts (from pandas df.info()):**
```
{csv_info_str}
```

**User's Specific Request:** "{user_prompt}"

**JSON SCHEMA TO ADHERE TO (NO DEVIATIONS):**
```json
{{
    "data_transform_script": "Python script (using pandas) to clean, transform, or aggregate data. **The script MUST BEGIN EXACTLY AND ONLY WITH: `import pandas as pd\\ndf_transformed = df.copy()`**. After this line, implement *only* the specific transformation logic requested by the user. **Crucially, if a transformation involves operations like sorting or filtering that require certain columns, perform these operations on `df_transformed` FIRST, ensuring all necessary columns are available for those steps. The final selection of columns (if requested) MUST be the VERY LAST step, applied to the already transformed `df_transformed`.** For example, if the request is 'top 100 by Unit price, show only City and Gender', the script must be: `df_transformed = df_transformed.sort_values('Unit price', ascending=False).head(100)` THEN `df_transformed = df_transformed[['City', 'Gender']]`. **DO NOT simply leave `df_transformed = df.copy()` if changes are needed. The final `df_transformed` MUST reflect the user's prompt.** If the user's prompt implies no data transformation (e.g., \"just analyze the data\"), then the script should remain simply `import pandas as pd\\ndf_transformed = df.copy()`.",
    "tableau_suggestions": "Provide clear, concise suggestions for how the user can visualize this data in Tableau Desktop, based on their prompt and the *transformed* data. For example: 'To show total sales by product category, drag [Product Category] to Columns and SUM([Total]) to Rows, then select a Bar Chart. Use [Date] for filtering trends.' Be specific with field names exactly as they appear in the CSV (or the transformed DataFrame). If no specific visualization is requested, provide general tips like: 'Explore trends using Date, and breakdowns by Category and Gender.' If empty, use an empty string.",
    "notes": "Optional: Any brief, non-critical notes or advice regarding the data or visualization process. If empty, use an empty string."
}}
```
**YOUR FINAL OUTPUT IS THE JSON OBJECT ABOVE, WRAPPED IN ```json AND ```. THIS IS THE ONLY CONTENT YOU SHOULD GENERATE.**
        """

        # 2. Call Ollama with the constructed prompt
        print("Sending prompt to Ollama...")
        response = ollama.chat(
            model='mistral',
            messages=[{'role': 'user', 'content': prompt_template}],
            options={'temperature': 0.0, 'num_predict': 4000} # Even lower temperature (0.0 for max determinism)
        )

        ollama_output_raw = response['message']['content']
        print(f"Ollama Raw Output:\n{ollama_output_raw}")

        # 3. Parse Ollama's output using the resilient extraction strategy
        json_str = ""
        
        # Strategy 1: Look for ```json ... ``` block explicitly
        start_marker = "```json"
        end_marker = "```"
        if start_marker in ollama_output_raw and ollama_output_raw.count(start_marker) == 1:
            json_start = ollama_output_raw.find(start_marker) + len(start_marker)
            json_end = ollama_output_raw.find(end_marker, json_start)
            if json_end != -1:
                json_str = ollama_output_raw[json_start:json_end].strip()
                print("Strategy 1: Extracted JSON from ```json block.")
            else:
                print("Strategy 1: ```json found, but no matching closing ```. Attempting full string.")
                json_str = ollama_output_raw[json_start:].strip()
        
        # Strategy 2: If Strategy 1 failed or if the output is not strictly block-formatted,
        # try to find the outermost JSON object by braces.
        if not json_str: # Only if json_str is still empty
            print("Strategy 2: ```json block not found or incomplete. Searching for outermost JSON object by braces.")
            first_brace = ollama_output_raw.find('{')
            last_brace = ollama_output_raw.rfind('}')
            
            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                potential_json_str = ollama_output_raw[first_brace : last_brace + 1].strip()
                # Aggressively remove common LLM junk like python code wrappers or comments
                potential_json_str = re.sub(r'```[a-zA-Z]*', '', potential_json_str) # Remove ```python, ```json, etc.
                potential_json_str = re.sub(r'//.*$', '', potential_json_str, flags=re.MULTILINE) # Remove // comments
                potential_json_str = re.sub(r'/\*.*?\*/', '', potential_json_str, flags=re.DOTALL) # Remove /* */ comments
                potential_json_str = "\n".join([line for line in potential_json_str.splitlines() if line.strip()]) # Remove empty lines
                
                json_str = potential_json_str
                print(f"Strategy 2: Attempted to extract JSON from braces. Potential JSON:\n{json_str}")
            else:
                print("Strategy 2: Could not find a valid JSON-like structure by braces. Returning empty.")
                return {} # No JSON found at all, return empty

        try:
            # Final cleanup: Replace smart quotes with straight quotes for robust parsing
            json_str_cleaned = json_str.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
            
            parsed_instructions = json.loads(json_str_cleaned)
            
            # Basic validation: check if all expected top-level keys are present
            expected_keys = ["data_transform_script", "tableau_suggestions", "notes"]
            if not all(k in parsed_instructions for k in expected_keys):
                print(f"Warning: Ollama output JSON missing one or more expected keys: {expected_keys}. Found: {list(parsed_instructions.keys())}")
                return {} # Return empty if validation fails
                
            return parsed_instructions
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from Ollama: {e}")
            print(f"Malformed JSON (after initial cleanup):\n{json_str_cleaned}")
            return {}

    except Exception as e:
        print(f"Error in Ollama handler: {e}")
        # Re-raise the exception to be caught by the main FastAPI endpoint
        raise

