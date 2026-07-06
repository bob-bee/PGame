import axios from 'axios';

const api = axios.create({
  baseURL: process.env.API_URL || 'http://localhost:8000'
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem('civic_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export default api;