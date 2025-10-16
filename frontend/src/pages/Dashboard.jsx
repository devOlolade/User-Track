import React, { useEffect, useState } from "react";
import { getProfile, logoutUser } from "../services/authServices";
import DashboardLayout from "../components/DashboardLayout";
import Overview from "../components/Overview";

const Dashboard = () => {
  

  return (
    <DashboardLayout>
      <Overview />
    </DashboardLayout>
  );
};

export default Dashboard;
