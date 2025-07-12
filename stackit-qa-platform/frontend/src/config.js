const config = {
  API_URL: process.env.NODE_ENV === 'production' 
    ? '/api' 
    : 'http://localhost:5000/api'
};

export default config;