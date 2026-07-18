import React, { createContext, useContext, useState, useEffect } from 'react';
import API from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Agar localstorage me already token aur user stored hain toh restore karo
    const savedToken = localStorage.getItem('token');
    const savedUsername = localStorage.getItem('username');
    
    if (savedToken && savedUsername) {
      setToken(savedToken);
      // Backend crud.py logic: agar username me 'admin' hai toh admin component privileges milenge
      setUser({
        username: savedUsername,
        isAdmin: savedUsername.toLowerCase().includes('admin')
      });
    }
    setLoading(false);
  }, []);

  // 1. User Login Handler
  const login = async (username, password) => {
    try {
      const response = await API.post('/auth/login', { username, password });
      const { access_token } = response.data;

      localStorage.setItem('token', access_token);
      localStorage.setItem('username', username);
      
      setToken(access_token);
      const loggedInUser = {
        username: username,
        isAdmin: username.toLowerCase().includes('admin')
      };
      setUser(loggedInUser);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Invalid username or password'
      };
    }
  };

  // 2. User Registration Handler
  const register = async (username, email, password) => {
    try {
      await API.post('/auth/register', { username, email, password });
      return { success: true };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || 'Registration failed'
      };
    }
  };

  // 3. Logout Handler
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

// Custom Hook secure use karne ke liye
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};