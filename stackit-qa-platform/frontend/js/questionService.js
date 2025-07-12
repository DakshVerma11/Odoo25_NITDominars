import axios from 'axios';
import { API_ENDPOINTS } from '../config/api';

const questionService = {
  async getQuestions(page = 1, filters = {}) {
    const params = { page, ...filters };
    try {
      const response = await axios.get(API_ENDPOINTS.QUESTIONS.LIST, { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching questions:', error);
      throw error;
    }
  },

  async getQuestionById(id) {
    try {
      const response = await axios.get(API_ENDPOINTS.QUESTIONS.DETAIL(id));
      return response.data;
    } catch (error) {
      console.error(`Error fetching question ${id}:`, error);
      throw error;
    }
  },

  async createQuestion(questionData) {
    const token = localStorage.getItem('authToken');
    try {
      const response = await axios.post(
        API_ENDPOINTS.QUESTIONS.CREATE, 
        questionData,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'  // If sending files
          }
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error creating question:', error);
      throw error;
    }
  }
};

export default questionService;