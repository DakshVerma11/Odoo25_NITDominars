/**
 * API Utility for making requests to the backend
 */

class ApiService {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
    }
    
    /**
     * Make a request to the API
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Fetch options
     * @returns {Promise<any>} - Response data
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        
        // Default options
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin' // Include cookies in requests
        };
        
        // Merge options
        const fetchOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, fetchOptions);
            
            // Handle unauthorized responses
            if (response.status === 401) {
                // Redirect to login page if not authenticated
                window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname);
                return null;
            }
            
            // Parse JSON response
            const data = await response.json();
            
            // Check for error responses
            if (!response.ok) {
                throw new Error(data.error || `Request failed with status ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    }
    
    /**
     * Make a GET request
     * @param {string} endpoint - API endpoint
     * @param {Object} params - Query parameters
     * @returns {Promise<any>} - Response data
     */
    async get(endpoint, params = {}) {
        // Build query string from params
        const queryString = Object.keys(params)
            .filter(key => params[key] !== undefined && params[key] !== null)
            .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
            .join('&');
            
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        
        return this.request(url, { method: 'GET' });
    }
    
    /**
     * Make a POST request
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Request body
     * @returns {Promise<any>} - Response data
     */
    async post(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    /**
     * Make a PUT request
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Request body
     * @returns {Promise<any>} - Response data
     */
    async put(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    /**
     * Make a DELETE request
     * @param {string} endpoint - API endpoint
     * @returns {Promise<any>} - Response data
     */
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
    
    /**
     * Upload a file
     * @param {string} endpoint - API endpoint
     * @param {FormData} formData - Form data with file
     * @returns {Promise<any>} - Response data
     */
    async uploadFile(endpoint, formData) {
        return this.request(endpoint, {
            method: 'POST',
            body: formData,
            headers: {} // Let browser set content-type with boundary
        });
    }
    
    // Question-specific API methods
    
    /**
     * Get questions with optional filtering
     * @param {number} page - Page number
     * @param {number} perPage - Items per page
     * @param {string} tag - Filter by tag
     * @param {string} search - Search term
     * @returns {Promise<Object>} - Questions data
     */
    async getQuestions(page = 1, perPage = 10, tag = null, search = null) {
        return this.get('/questions', { page, per_page: perPage, tag, search });
    }
    
    /**
     * Get a specific question with answers
     * @param {number} questionId - Question ID
     * @returns {Promise<Object>} - Question data
     */
    async getQuestion(questionId) {
        return this.get(`/questions/${questionId}`);
    }
    
    /**
     * Create a new question
     * @param {Object} questionData - Question data
     * @returns {Promise<Object>} - Created question
     */
    async createQuestion(questionData) {
        return this.post('/questions', questionData);
    }
    
    /**
     * Update a question
     * @param {number} questionId - Question ID
     * @param {Object} questionData - Updated question data
     * @returns {Promise<Object>} - Updated question
     */
    async updateQuestion(questionId, questionData) {
        return this.put(`/questions/${questionId}`, questionData);
    }
    
    /**
     * Post an answer to a question
     * @param {number} questionId - Question ID
     * @param {Object} answerData - Answer data
     * @returns {Promise<Object>} - Created answer
     */
    async createAnswer(questionId, answerData) {
        return this.post(`/questions/${questionId}/answers`, answerData);
    }
    
    /**
     * Vote on an answer
     * @param {number} answerId - Answer ID
     * @param {string} voteType - Vote type ('up' or 'down')
     * @returns {Promise<Object>} - Updated vote count
     */
    async voteAnswer(answerId, voteType) {
        return this.post(`/answers/${answerId}/vote`, { vote_type: voteType });
    }
    
    /**
     * Accept an answer
     * @param {number} answerId - Answer ID
     * @returns {Promise<Object>} - Updated answer
     */
    async acceptAnswer(answerId) {
        return this.post(`/answers/${answerId}/accept`);
    }
    
    /**
     * Upload an image
     * @param {File} imageFile - Image file
     * @returns {Promise<Object>} - Image URL
     */
    async uploadImage(imageFile) {
        const formData = new FormData();
        formData.append('image', imageFile);
        
        return this.uploadFile('/questions/upload-image', formData);
    }
    
    /**
     * Get user notifications
     * @param {boolean} unreadOnly - Get only unread notifications
     * @returns {Promise<Array>} - Notifications
     */
    async getNotifications(unreadOnly = false) {
        return this.get('/notifications', { unread_only: unreadOnly });
    }
    
    /**
     * Mark notification as read
     * @param {number} notificationId - Notification ID
     * @returns {Promise<Object>} - Updated notification
     */
    async markNotificationAsRead(notificationId) {
        return this.put(`/notifications/${notificationId}/read`);
    }
}

// Create global API instance
window.api = new ApiService();