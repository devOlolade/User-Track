import React, { useState } from "react";
import { loginUser } from "../services/authServices";
import googleIcon from "../assets/google-icon.png"
import briefcase from "../assets/briefcase.png"
import logo from "../assets/logo.png"
import passwordIcon from "../assets/password.png"
import showPassword from "../assets/showPassword.jpg"
import "../styles/login.css";


const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await loginUser({ email, password });
      setMessage("Login successful!");
      window.location.href = "/dashboard";
    } catch (err) {
      setMessage(err.response?.data?.msg || "Login failed");
    }
  };

  return (
    <div className="login-page">
      <div className="logo">
          <img src={logo} alt="Logo" />
        </div>
      <div className="login-container">
        
        <div className="login-left">
          <h1>Tracking your users activity has never been <span>easier...</span></h1>
        </div>

        <div className="login-right">
          <div className="form-header">
            <h3>Get Started Now</h3>
            <p>Enter your credentials to access your account. Have an account?</p>
            <a href="/register">Register here</a>
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
          <form onSubmit={handleLogin}>
            <div className="input-container">
              <div className="form-input">
                <label htmlFor="">Email</label>
                <div className="input-field">
                  <i class="fa-regular fa-envelope"></i>
                  <input
                    type="email"
                    placeholder="Enter your email"  
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
              </div>
              <div className="form-input">
                <label htmlFor="">Password</label>
                <div className="input-field">
                  <img src={passwordIcon} alt="" className="passwordIcon" />
                  <input type="password" placeholder="Enter your password" value={password} onChange={(e) => setPassword(e.target.value)}
                required/>
                  <img src={showPassword} alt="" className='showPassword' />
                </div>
              </div>
            </div>
            <button>Sign in</button>
            <p>By creating an account, you agree to our <a>Terms of Service</a></p>
            
            {message && <p className="message">{message}</p>}

            </form>
          </div>
      </div>
      
      <div className="footer">
        <p>Terms of Service</p>
        <p>Made with ❤️ by Lolade for <a href="https://thetrybeco.org/">TheTrybeCo</a></p>
        <p>2025 UserTrack</p>
      </div>
    </div>
     
    

    
  );
};

export default Login;
