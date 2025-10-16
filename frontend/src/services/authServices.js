import API from "./api";

// ✅ Register user
export const registerUser = async (userData) => {
  try {
    const response = await API.post("/auth/register", userData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// ✅ Login user
export const loginUser = async (data) => {
  const res = await API.post("/auth/login", data);
  if (res.data.access_token) {
    localStorage.setItem("token", res.data.access_token);
  }
  return res.data;
};

// ✅ Get current logged-in user profile
export const getProfile = async () => {
  return API.get("/users/me");
};

// ✅ Logout user
export const logoutUser = () => {
  localStorage.removeItem("token");
};
