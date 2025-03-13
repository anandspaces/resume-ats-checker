import axios from 'axios';
import { ApiResponse } from '../types/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

export const analyzeResume = async (formData: FormData): Promise<ApiResponse> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
