import axios from 'axios'

// In Docker, use relative path for nginx proxy. In local dev, use full URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.MODE === 'production' ? '' : 'http://localhost:8000')

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
})

// Add token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
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

  // Loan Markets Features
  async getTradeReadiness(analysisId: string) {
    const response = await apiClient.get(`/api/v1/analyses/${analysisId}/trade-readiness`)
    return response.data
  },

  async getTransferSimulation(analysisId: string) {
    const response = await apiClient.get(`/api/v1/analyses/${analysisId}/transfer-simulation`)
    return response.data
  },

  async getLMADeviations(analysisId: string) {
    const response = await apiClient.get(`/api/v1/analyses/${analysisId}/lma-deviations`)
    return response.data
  },

  async getBuyerFit(analysisId: string) {
    const response = await apiClient.get(`/api/v1/analyses/${analysisId}/buyer-fit`)
    return response.data
  },

  async getNegotiationInsights(analysisId: string) {
    const response = await apiClient.get(`/api/v1/analyses/${analysisId}/negotiation-insights`)
    return response.data
  },

  async createMonitoringRule(analysisId: string, ruleConfig: any) {
    const response = await apiClient.post(`/api/v1/analyses/${analysisId}/monitoring/rules`, ruleConfig)
    return response.data
  },

  async getMonitoringAlerts(analysisId: string) {
    const response = await apiClient.get(`/api/v1/analyses/${analysisId}/monitoring/alerts`)
    return response.data
  },

  async createAuction(auctionConfig: any) {
    const response = await apiClient.post('/api/v1/auctions', auctionConfig)
    return response.data
  },

  async placeBid(auctionId: string, bidData: any) {
    const response = await apiClient.post(`/api/v1/auctions/${auctionId}/bids`, bidData, {
      timeout: 15000, // 15 second timeout for bid placement (increased for DB operations)
    })
    return response.data
  },

  async getAuctionLeaderboard(auctionId: string) {
    const response = await apiClient.get(`/api/v1/auctions/${auctionId}/leaderboard`)
    return response.data
  },

  async closeAuction(auctionId: string) {
    const response = await apiClient.post(`/api/v1/auctions/${auctionId}/close`)
    return response.data
  },

  async getAuctionsForAnalysis(analysisId: string) {
    const response = await apiClient.get(`/api/v1/analyses/${analysisId}/auctions`)
    return response.data
  },

  async getAuction(auctionId: string) {
    const response = await apiClient.get(`/api/v1/auctions/${auctionId}`)
    return response.data
  },

  // Authentication
  async signup(userData: { email: string; username: string; password: string; full_name?: string }) {
    const response = await apiClient.post('/api/v1/auth/signup', userData)
    return response.data
  },

  async login(username: string, password: string) {
    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)
    const response = await apiClient.post('/api/v1/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      timeout: 10000, // 10 second timeout for login (bcrypt can take a moment)
    })
    return response.data
  },

  async getCurrentUser() {
    const response = await apiClient.get('/api/v1/auth/me')
    return response.data
  },
}

