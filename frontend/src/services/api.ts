import axios from 'axios';
import type { EventLog, AnalysisResult } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = {
  getHistory: async (): Promise<EventLog[]> => {
    const response = await axios.get(`${API_BASE_URL}/history`);
    return response.data;
  },
  
  analyze: async (labelId: number): Promise<AnalysisResult> => {
    const response = await axios.post(`${API_BASE_URL}/analyze/${labelId}`);
    return response.data;
  },
  
  startVoyage: async (): Promise<void> => {
    await axios.post(`${API_BASE_URL}/start-voyage`);
  }
};

export const WS_URL = 'ws://localhost:8000/ws/stream';
