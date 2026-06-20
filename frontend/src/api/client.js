import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getProducts = () => apiClient.get('/products?limit=100');
export const getAnalyticsSummary = () => apiClient.get('/analytics/summary');
export const predictDemand = (payload) => apiClient.post('/demand/predict', payload);

export default apiClient;
