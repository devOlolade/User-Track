import React from "react";
import { Link, useLocation } from "react-router-dom";
import logo from "../assets/logo.png";

const Sidebar = () => {
  const location = useLocation();

  const links = [
    { path: "/dashboard", label: "Overview", icon: "fa-solid fa-chart-pie" },
    { path: "/users", label: "User Management", icon: "fa-regular fa-user" },
    { path: "/activities", label: "Activities", icon: "fa-regular fa-file" },
    { path: "/profile", label: "Profile", icon: "fa-regular fa-id-card" },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
              <div className="logo">
                  <img src={logo} alt="Logo" />
                </div>
      </div>
      <p className="sidebar-title">GENERAL</p>
      <nav className="sidebar-links">
        {links.map((link) => (
          <Link
            key={link.path}
            to={link.path}
            className={location.pathname === link.path ? "active" : ""}
          >
            <i className={link.icon}></i>
            {link.label}
          </Link>
        ))}
      </nav>

      <div className="sidebar-footer">
        <button className="logout-btn">
          <i className="fa-solid fa-arrow-right-from-bracket"></i> Logout
        </button>
        <p className="footer-note">
          Made by <strong>Lolade</strong> ❤️ for <a href="https://thetrybeco.org/">TheTrybeCo</a>
        </p>
      </div>
    </aside>
  );
};

export default Sidebar;
