import axios from 'axios'

// In Docker, use relative path for nginx proxy. In local dev, use full URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.MODE === 'production' ? '' : 'http://localhost:8000')

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const api = {
  async uploadDocument(
    formData: FormData,
    onProgress?: (progress: number) => void
  ) {
    const response = await apiClient.post('/api/v1/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          onProgress(progress)
        }
      },
    })
    return response.data
  },

  async startAnalysis(analysisId: string) {
    const response = await apiClient.post(
      `/api/v1/analyses/${analysisId}/start`
    )
    return response.data
  },

  async getAnalysis(analysisId: string) {
    const response = await apiClient.get(`/api/v1/analyses/${analysisId}`)
    return response.data
  },

  async getDashboardStats() {
    const response = await apiClient.get('/api/v1/dashboard/stats')
    return response.data
  },

  async getReports() {
    const response = await apiClient.get('/api/v1/reports')
    return response.data
  },

  async generateReport(analysisId: string, reportType: string) {
    const response = await apiClient.post('/api/v1/reports/generate', {
      analysis_id: analysisId,
      report_type: reportType,
    })
    return response.data
  },
}

