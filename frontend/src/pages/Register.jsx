import React, { useState } from "react";
import { registerUser } from "../services/authServices";
import googleIcon from "../assets/google-icon.png";
import briefcase from "../assets/briefcase.png";
import logo from "../assets/logo.png";
import passwordIcon from "../assets/password.png";
import showPasswordIcon from "../assets/showPassword.jpg"; // ✅ renamed for clarity
import "../styles/register.css";

const Register = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [organization, setOrganization] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [showPwd, setShowPwd] = useState(false); // ✅ renamed to avoid clash

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      const data = await registerUser({ name, email, organization, password });
      setMessage(data.message || "Registration successful! You can now log in.");
      setName("");
      setEmail("");
      setOrganization("");
      setPassword("");
    } catch (err) {
      setError(err.response?.data?.message || "Registration failed");
    }
  };

  return (
    <div className="login-page">
      <div className="logo">
        <img src={logo} alt="Logo" />
      </div>

      <div className="login-container">
        <div className="login-left">
          <h1>
            Tracking your users activity has never been <span>easier...</span>
          </h1>
        </div>

        <div className="login-right">
          <div className="form-header">
            <h3>Get Started Now</h3>
            <p>
              Enter your credentials to access your account. Have an account?
            </p>
            <a href="/login">Login here</a>
          </div>

          <div className="google-btn">
            <button>
              <img src={googleIcon} alt="" />
              Google
            </button>
          </div>

          <div className="divider">
            <hr />
            <p>or</p>
            <hr />
          </div>

          <form onSubmit={handleRegister}>
            <div className="input-container">
              <div className="form-input">
                <label>Full Name</label>
                <div className="input-field">
                  <i className="fa-regular fa-user"></i>
                  <input
                    type="text"
                    placeholder="Enter your full name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="form-input">
                <label>Email</label>
                <div className="input-field">
                  <i className="fa-regular fa-envelope"></i>
                  <input
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
              </div>
            </div>

            <div className="input-container">
              <div className="form-input">
                <label>Organization Name</label>
                <div className="input-field">
                  <img src={briefcase} alt="" className="briefcaseIcon" />
                  <input
                    type="text"
                    placeholder="e.g TheTrybeCo"
                    value={organization}
                    onChange={(e) => setOrganization(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="form-input">
                <label>Password</label>
                <div className="input-field">
                  <img src={passwordIcon} alt="" className="passwordIcon" />
                  <input
                    type={showPwd ? "text" : "password"}
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                  <img
                    src={showPasswordIcon}
                    alt="Toggle Password"
                    className="showPassword"
                    onClick={() => setShowPwd(!showPwd)}
                    style={{ cursor: "pointer" }}
                  />
                </div>
              </div>
            </div>

            <button type="submit">Sign Up</button>
            {message && <p className="text-center mt-3">{message}</p>}
            {error && <p className="error-msg">{error}</p>}
            <p>
              By creating an account, you agree to our{" "}
              <a href="#">Terms of Service</a>
            </p>
          </form>
        </div>
      </div>

      <div className="footer">
        <p>Terms of Service</p>
        <p>
          Made with ❤️ by Lolade for{" "}
          <a href="https://thetrybeco.org/">TheTrybeCo</a>
        </p>
        <p>2025 User Track</p>
      </div>
    </div>
  );
};

export default Register;
