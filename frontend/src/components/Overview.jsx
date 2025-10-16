import React from "react";


const Overview = () => {
  return (
    <div className="overview">
      <h2>Overview</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <i className="fa-solid fa-users"></i>
          <div className="stat-info">
            <p>Total members</p>
            <h3>35</h3>
          </div>
        </div>
        <div className="stat-card">
          <i className="fa-regular fa-user"></i>
          <div className="stat-info">
            <p>Active members</p>
            <h3>20</h3>
          </div>
        </div>
        <div className="stat-card">
          <i className="fa-regular fa-user-xmark"></i>
          <div className="stat-info">
            <p>Inactive members</p>
            <h3>15</h3>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Overview;
