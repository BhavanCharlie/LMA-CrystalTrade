import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { AlertTriangle, CheckCircle, XCircle, Clock } from 'lucide-react'
import { api } from '../services/api'
import RiskScore from '../components/RiskScore'
import ComplianceChecklist from '../components/ComplianceChecklist'
import ExtractedTerms from '../components/ExtractedTerms'

interface AnalysisData {
  id: string
  loan_name: string
  status: string
  risk_score: number
  risk_breakdown: {
    credit_risk: number
    legal_risk: number
    operational_risk: number
  }
  compliance_checks: Array<{
    category: string
    status: 'pass' | 'fail' | 'warning'
    description: string
    details: string
  }>
  extracted_terms: {
    interest_rate?: string
    maturity_date?: string
    principal_amount?: string
    transfer_restrictions?: string
    consent_requirements?: string[]
    financial_covenants?: Array<{
      name: string
      requirement: string
      current_value?: string
    }>
  }
  recommendations: string[]
  created_at: string
  updated_at: string
}

export default function AnalysisView() {
  const { id } = useParams<{ id: string }>()
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (id) {
      fetchAnalysis(id)
      // Poll for updates if still processing
      const interval = setInterval(() => {
        if (analysis?.status === 'processing') {
          fetchAnalysis(id)
        }
      }, 3000)
      return () => clearInterval(interval)
    }
  }, [id])

  const fetchAnalysis = async (analysisId: string) => {
    try {
      const data = await api.getAnalysis(analysisId)
      setAnalysis(data)
    } catch (error) {
      console.error('Failed to fetch analysis:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-sm text-gray-600">Loading analysis...</p>
        </div>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="text-center py-12">
        <XCircle className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">
          Analysis not found
        </h3>
      </div>
    )
  }

  const getStatusIcon = () => {
    switch (analysis.status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'processing':
        return <Clock className="h-5 w-5 text-yellow-500 animate-spin" />
      case 'failed':
        return <XCircle className="h-5 w-5 text-red-500" />
      default:
        return <Clock className="h-5 w-5 text-gray-500" />
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            {analysis.loan_name}
          </h1>
          <p className="mt-2 text-sm text-gray-600">
            Analysis ID: {analysis.id}
          </p>
        </div>
        <div className="flex items-center space-x-2">
          {getStatusIcon()}
          <span className="text-sm font-medium text-gray-700 capitalize">
            {analysis.status}
          </span>
        </div>
      </div>

      {analysis.status === 'processing' && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex">
            <Clock className="h-5 w-5 text-yellow-600" />
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">
                Analysis in Progress
              </h3>
              <p className="mt-1 text-sm text-yellow-700">
                AI is analyzing the documents. This may take a few minutes...
              </p>
            </div>
          </div>
        </div>
      )}

      {analysis.status === 'completed' && (
        <>
          <RiskScore
            overallScore={analysis.risk_score}
            breakdown={analysis.risk_breakdown}
          />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ExtractedTerms terms={analysis.extracted_terms} />
            <ComplianceChecklist checks={analysis.compliance_checks} />
          </div>

          {analysis.recommendations.length > 0 && (
            <div className="bg-white shadow rounded-lg">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">
                  Recommendations
                </h3>
              </div>
              <div className="p-6">
                <ul className="space-y-3">
                  {analysis.recommendations.map((rec, index) => (
                    <li key={index} className="flex items-start">
                      <AlertTriangle className="h-5 w-5 text-yellow-500 mr-3 mt-0.5" />
                      <span className="text-sm text-gray-700">{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}

