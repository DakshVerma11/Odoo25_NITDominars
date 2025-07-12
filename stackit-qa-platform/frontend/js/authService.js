import axios from 'axios';
import { API_ENDPOINTS } from '../config/api';

const authService = {
  async login(username, password) {
    try {
      const response = await axios.post(API_ENDPOINTS.AUTH.LOGIN, {
        username,
        password
      });
      
      // Store token in localStorage
      if (response.data.token) {
        localStorage.setItem('authToken', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },
  
  async register(userData) {
    try {
      const response = await axios.post(API_ENDPOINTS.AUTH.REGISTER, userData);
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },
  
  logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  },
  
  getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },
  
  isAuthenticated() {
    return !!localStorage.getItem('authToken');
  }
};

export default authService;