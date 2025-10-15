import API from "./api";

// Register
export const registerUser = async (data) => {
  return API.post("/auth/register", data);
};

// Login
export const loginUser = async (data) => {
  const res = await API.post("/auth/login", data);
  if (res.data.access_token) {
    localStorage.setItem("token", res.data.access_token);
  }
  return res.data;
};

// Get current user profile
export const getProfile = async () => {
  return API.get("/users/me");
};

// Logout
export const logoutUser = () => {
  localStorage.removeItem("token");
};
