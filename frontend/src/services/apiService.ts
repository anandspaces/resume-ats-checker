import axios from 'axios';
import { ApiResponse } from '../types/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const analyzeResume = async (formData: FormData): Promise<ApiResponse> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/resume/analyze`, formData);
    return response.data;
  } catch (error:any) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Analysis failed');
    }
    throw new Error('Network error');
  }
};
