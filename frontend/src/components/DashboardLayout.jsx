import React from "react";
import Sidebar from "./Sidebar";
import "../styles/dashboard.css";

const DashboardLayout = ({ children }) => {
  return (
    <div className="dashboard-container">
      <Sidebar />
      <main className="dashboard-main">{children}</main>
    </div>
  );
};

export default DashboardLayout;
