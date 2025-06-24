import React, { useState } from 'react';
import './Sidebar.css';
import { FaChartBar, FaHistory, FaInfoCircle, FaBars } from 'react-icons/fa';

const Sidebar = ({ activePage, setActivePage }) => {
  const [collapsed, setCollapsed] = useState(false);

  const handleToggle = () => {
    setCollapsed(!collapsed);
  };

  return (
    <div className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="top-section">
        <div className="logo">{!collapsed && '⚡ DataSpeak'}</div>
        <FaBars className="toggle-btn" onClick={handleToggle} />
      </div>

      <ul className="nav">
        <li className={activePage === 'Dashboard' ? 'active' : ''} onClick={() => setActivePage('Dashboard')}>
          <FaChartBar className="icon" />
          {!collapsed && <span>Dashboard</span>}
        </li>
        <li className={activePage === 'History' ? 'active' : ''} onClick={() => setActivePage('History')}>
          <FaHistory className="icon" />
          {!collapsed && <span>History</span>}
        </li>
       <li onClick={() => setActivePage('About')} style={{ cursor: 'pointer' }}>
  <FaInfoCircle className="icon" />
  {!collapsed && <span>About</span>}
</li>

      </ul>
    </div>
  );
};

export default Sidebar;
