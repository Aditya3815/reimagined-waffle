import { createContext, useState, useEffect } from "react";
import { setTokens, clearTokens, getUserData, getUserRole, setUserData } from "../utils/tokenManager";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [role, setRole] = useState(null); // 'doctor' or 'patient'

  // Check if user is logged in on mount
  useEffect(() => {
    const userData = getUserData();
    const userRole = getUserRole();
    if (userData && userRole) {
      setUser(userData);
      setRole(userRole);
      setIsLoggedIn(true);
    }
  }, []);

  const login = (userData, tokens, userRole) => {
    setTokens(tokens.access, tokens.refresh);
    setUserData(userData, userRole);
    setUser(userData);
    setRole(userRole);
    setIsLoggedIn(true);
  };

  const logout = () => {
    clearTokens();
    setUser(null);
    setRole(null);
    setIsLoggedIn(false);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

