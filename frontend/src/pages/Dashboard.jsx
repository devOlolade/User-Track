import React, { useEffect, useState } from "react";
import { getProfile, logoutUser } from "../services/authServices";

const Dashboard = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    getProfile()
      .then((res) => setUser(res.data))
      .catch(() => logoutUser());
  }, []);

  if (!user) return <p>Loading...</p>;

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Welcome, {user.name}!</h1>
      <p>Email: {user.email}</p>

      <button
        onClick={() => {
          logoutUser();
          window.location.href = "/login";
        }}
        className="mt-4 bg-red-500 text-white py-2 px-4 rounded"
      >
        Logout
      </button>
    </div>
  );
};

export default Dashboard;
