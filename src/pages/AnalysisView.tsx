import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { AlertTriangle, CheckCircle, XCircle, Clock, TrendingUp, ArrowRightLeft, FileText, Users, MessageSquare, Bell, Gavel } from 'lucide-react'
import { api } from '../services/api'
import RiskScore from '../components/RiskScore'
import ComplianceChecklist from '../components/ComplianceChecklist'
import ExtractedTerms from '../components/ExtractedTerms'
import TradeReadiness from '../components/TradeReadiness'
import AuctionRoom from '../components/AuctionRoom'

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

type TabType = 'overview' | 'trade-readiness' | 'transfer-sim' | 'lma-deviations' | 'buyer-fit' | 'negotiation' | 'monitoring' | 'auction'

export default function AnalysisView() {
  const { id } = useParams<{ id: string }>()
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<TabType>('overview')
  
  // Loan Markets feature data
  const [tradeReadiness, setTradeReadiness] = useState<any>(null)
  const [transferSim, setTransferSim] = useState<any>(null)
  const [lmaDeviations, setLmaDeviations] = useState<any>(null)
  const [buyerFit, setBuyerFit] = useState<any>(null)
  const [negotiationInsights, setNegotiationInsights] = useState<any>(null)
  const [monitoringAlerts, setMonitoringAlerts] = useState<any>(null)
  
  // Loading states for features
  const [featureLoading, setFeatureLoading] = useState<Record<string, boolean>>({})

  useEffect(() => {
    if (id) {
      fetchAnalysis(id)
      // Poll for updates if still processing - increased interval to reduce load
      const interval = setInterval(() => {
        if (analysis?.status === 'processing') {
          fetchAnalysis(id)
        }
      }, 5000) // Changed from 3000ms to 5000ms
      return () => clearInterval(interval)
    }
  }, [id, analysis?.status])

  const fetchAnalysis = async (analysisId: string) => {
    try {
      const data = await api.getAnalysis(analysisId)
      setAnalysis(data)
      // Don't load Loan Markets features here - load them lazily when tabs are clicked
    } catch (error) {
      console.error('Failed to fetch analysis:', error)
    } finally {
      setLoading(false)
    }
  }

  // Lazy load features when tab is clicked
  const loadFeatureData = async (feature: TabType) => {
    if (!id || !analysis || analysis.status !== 'completed') return
    
    // Skip if already loaded or currently loading
    const featureKey = feature
    if (featureLoading[featureKey]) return
    
    const hasData = {
      'trade-readiness': tradeReadiness,
      'transfer-sim': transferSim,
      'lma-deviations': lmaDeviations,
      'buyer-fit': buyerFit,
      'negotiation': negotiationInsights,
      'monitoring': monitoringAlerts,
    }[feature]
    
    if (hasData) return

    setFeatureLoading(prev => ({ ...prev, [featureKey]: true }))

    try {
      switch (feature) {
        case 'trade-readiness':
          const trData = await api.getTradeReadiness(id)
          setTradeReadiness(trData)
          break
        case 'transfer-sim':
          const tsData = await api.getTransferSimulation(id)
          setTransferSim(tsData)
          break
        case 'lma-deviations':
          const lmaData = await api.getLMADeviations(id)
          setLmaDeviations(lmaData)
          break
        case 'buyer-fit':
          const bfData = await api.getBuyerFit(id)
          setBuyerFit(bfData)
          break
        case 'negotiation':
          const niData = await api.getNegotiationInsights(id)
          setNegotiationInsights(niData)
          break
        case 'monitoring':
          const maData = await api.getMonitoringAlerts(id)
          setMonitoringAlerts(maData)
          break
      }
    } catch (error) {
      console.error(`Failed to load ${feature}:`, error)
    } finally {
      setFeatureLoading(prev => ({ ...prev, [featureKey]: false }))
    }
  }

  // Load feature when tab changes
  useEffect(() => {
    if (analysis?.status === 'completed' && activeTab !== 'overview' && activeTab !== 'auction' && id) {
      loadFeatureData(activeTab)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab, analysis?.status])

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
        return <Clock className="h-5 w-5 text-gray-400" />
    }
  }

  return (
    <div className="space-y-6">
      <div className="glass-card rounded-xl p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold gradient-text">
              {analysis.loan_name}
            </h1>
            <p className="mt-2 text-sm text-gray-600">
              Analysis ID: {analysis.id}
            </p>
          </div>
          <div className="flex items-center space-x-2 glass-strong px-4 py-2 rounded-lg">
            {getStatusIcon()}
            <span className="text-sm font-medium text-gray-700 capitalize">
              {analysis.status}
            </span>
          </div>
        </div>
      </div>

      {analysis.status === 'processing' && (
        <div className="glass-card rounded-xl p-4 border border-yellow-300 bg-yellow-50">
          <div className="flex">
            <Clock className="h-5 w-5 text-yellow-600 animate-spin" />
            <div className="ml-3">
              <h3 className="text-sm font-medium text-gray-900">
                Analysis in Progress
              </h3>
              <p className="mt-1 text-sm text-gray-600">
                AI is analyzing the documents. This may take a few minutes...
              </p>
            </div>
          </div>
        </div>
      )}

      {analysis.status === 'completed' && (
        <>
          {/* Tabs */}
          <div className="glass-nav rounded-xl p-2">
            <nav className="flex space-x-2 overflow-x-auto">
              {[
                { id: 'overview' as TabType, label: 'Overview', icon: FileText },
                { id: 'trade-readiness' as TabType, label: 'Trade Readiness', icon: TrendingUp },
                { id: 'transfer-sim' as TabType, label: 'Transfer Simulator', icon: ArrowRightLeft },
                { id: 'lma-deviations' as TabType, label: 'LMA Deviations', icon: FileText },
                { id: 'buyer-fit' as TabType, label: 'Buyer Fit', icon: Users },
                { id: 'negotiation' as TabType, label: 'Negotiation', icon: MessageSquare },
                { id: 'monitoring' as TabType, label: 'Monitoring', icon: Bell },
                { id: 'auction' as TabType, label: 'Auction', icon: Gavel },
              ].map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`${
                      activeTab === tab.id
                        ? 'bg-gradient-to-r from-primary-500 to-primary-700 text-white shadow-lg'
                        : 'bg-white/60 text-gray-700 hover:bg-white/80 border-transparent'
                    } whitespace-nowrap py-2 px-4 rounded-lg border font-medium text-sm flex items-center space-x-2 transition-all duration-200`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{tab.label}</span>
                  </button>
                )
              })}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="mt-6">
            {activeTab === 'overview' && (
              <>
                <RiskScore
                  overallScore={analysis.risk_score}
                  breakdown={analysis.risk_breakdown}
                />

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
                  <ExtractedTerms terms={analysis.extracted_terms} />
                  <ComplianceChecklist checks={analysis.compliance_checks} />
                </div>

                {analysis.recommendations && analysis.recommendations.length > 0 && (
                  <div className="glass-panel rounded-2xl mt-8 overflow-hidden fade-in">
                    <div className="px-8 py-6 border-b border-gray-200 bg-gradient-to-r from-yellow-50 to-white">
                      <div className="flex items-center">
                        <div className="p-3 rounded-xl bg-gradient-to-br from-yellow-100 to-yellow-200 mr-4">
                          <AlertTriangle className="h-6 w-6 text-yellow-600" />
                        </div>
                        <h3 className="text-xl font-bold gradient-text">
                          Recommendations
                        </h3>
                      </div>
                    </div>
                    <div className="p-8">
                      <ul className="space-y-4">
                        {analysis.recommendations.map((rec, index) => (
                          <li key={index} className="flex items-start glass-strong rounded-xl p-4 border-l-4 border-yellow-500">
                            <AlertTriangle className="h-6 w-6 text-yellow-500 mr-4 mt-0.5 flex-shrink-0" />
                            <span className="text-sm text-gray-800 font-medium leading-relaxed">{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}
              </>
            )}

            {activeTab === 'trade-readiness' && (
              <div>
                {tradeReadiness ? (
                  <TradeReadiness
                    score={tradeReadiness.score}
                    label={tradeReadiness.label}
                    breakdown={tradeReadiness.breakdown}
                    confidence={tradeReadiness.confidence}
                    evidence_links={tradeReadiness.evidence_links}
                  />
                ) : (
                  <div className="glass-panel rounded-xl p-12 text-center">
                    {featureLoading['trade-readiness'] ? (
                      <>
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
                        <p className="mt-4 text-gray-600">Loading trade readiness analysis...</p>
                      </>
                    ) : (
                      <p className="text-gray-600">Click to load trade readiness analysis</p>
                    )}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'transfer-sim' && (
              <div className="space-y-6 fade-in">
                <div className="glass-panel rounded-2xl p-8 overflow-hidden">
                  <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center">
                      <div className="p-4 rounded-2xl bg-gradient-to-br from-blue-400 to-blue-600 mr-4 shadow-lg">
                        <ArrowRightLeft className="w-7 h-7 text-white" />
                      </div>
                      <div>
                        <h3 className="text-3xl font-bold gradient-text">Transfer Simulation</h3>
                        <p className="text-sm text-gray-600 mt-1">Pathway analysis and timeline estimation</p>
                      </div>
                    </div>
                  </div>
                  {transferSim ? (
                    transferSim.pathways && transferSim.pathways.length > 0 ? (
                      <div className="space-y-8">
                        {/* Summary Stats */}
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-5 mb-6">
                          <div className="glass-strong rounded-2xl p-6 text-center card-hover shadow-lg">
                            <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Total Pathways</div>
                            <div className="text-4xl font-bold text-gray-900 mb-2">{transferSim.pathways.length}</div>
                            <div className="text-xs text-gray-600">Available options</div>
                          </div>
                          <div className="glass-strong rounded-2xl p-6 text-center bg-gradient-to-br from-green-50 to-green-100 border-2 border-green-200 card-hover shadow-lg">
                            <div className="text-xs font-bold text-green-700 uppercase tracking-wider mb-3">Clear Pathways</div>
                            <div className="text-4xl font-bold text-green-600 mb-2">
                              {transferSim.pathways.filter((p: any) => !p.blockers || p.blockers.length === 0).length}
                            </div>
                            <div className="text-xs text-green-600 font-medium">No blockers</div>
                          </div>
                          <div className="glass-strong rounded-2xl p-6 text-center bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-200 card-hover shadow-lg">
                            <div className="text-xs font-bold text-blue-700 uppercase tracking-wider mb-3">Fastest Timeline</div>
                            <div className="text-4xl font-bold text-blue-600 mb-2">
                              {Math.min(...transferSim.pathways.map((p: any) => p.estimated_timeline_days || 999))}
                            </div>
                            <div className="text-xs text-blue-600 font-medium">days</div>
                          </div>
                          <div className="glass-strong rounded-2xl p-6 text-center bg-gradient-to-br from-purple-50 to-purple-100 border-2 border-purple-200 card-hover shadow-lg">
                            <div className="text-xs font-bold text-purple-700 uppercase tracking-wider mb-3">Total Consents</div>
                            <div className="text-4xl font-bold text-purple-600 mb-2">
                              {transferSim.pathways.reduce((sum: number, p: any) => sum + (p.required_consents?.length || 0), 0)}
                            </div>
                            <div className="text-xs text-purple-600 font-medium">Required</div>
                          </div>
                        </div>

                        {/* Pathway Cards */}
                        {transferSim.pathways.map((pathway: any, idx: number) => {
                          const pathwayType = pathway.type?.toLowerCase() || 'unknown'
                          const isAssignment = pathwayType === 'assignment'
                          const hasBlockers = pathway.blockers && pathway.blockers.length > 0
                          const borderColor = hasBlockers ? 'border-red-500' : 'border-green-500'
                          const bgGradient = isAssignment 
                            ? 'from-blue-50 to-indigo-50' 
                            : 'from-purple-50 to-pink-50'
                          
                          return (
                            <div key={idx} className={`glass-strong border-l-4 ${borderColor} rounded-2xl p-8 mb-6 fade-in card-hover shadow-lg bg-gradient-to-br ${bgGradient}`} style={{ animationDelay: `${idx * 0.1}s` }}>
                              {/* Header */}
                              <div className="flex items-center justify-between mb-6">
                                <div className="flex items-center space-x-4">
                                  <div className={`p-4 rounded-2xl bg-gradient-to-br ${
                                    isAssignment 
                                      ? 'from-blue-500 to-indigo-600' 
                                      : 'from-purple-500 to-pink-600'
                                  } shadow-lg`}>
                                    <ArrowRightLeft className="w-6 h-6 text-white" />
                                  </div>
                                  <div>
                                    <h4 className="text-2xl font-bold text-gray-900 capitalize">
                                      {pathway.type} Pathway
                                    </h4>
                                    <p className="text-sm text-gray-600 mt-1">
                                      {isAssignment ? 'Direct transfer of loan rights' : 'Indirect participation structure'}
                                    </p>
                                  </div>
                                </div>
                                <div className={`px-5 py-2.5 rounded-xl font-bold shadow-lg ${
                                  hasBlockers
                                    ? 'bg-gradient-to-r from-red-500 to-red-600 text-white' 
                                    : 'bg-gradient-to-r from-green-500 to-green-600 text-white'
                                }`}>
                                  {hasBlockers ? 'Has Blockers' : 'Clear Pathway'}
                                </div>
                              </div>

                              {/* Key Metrics */}
                              <div className="grid grid-cols-1 md:grid-cols-4 gap-5 mb-8">
                                <div className="glass rounded-2xl p-5 text-center bg-white/80 shadow-md">
                                  <Clock className="w-6 h-6 text-blue-600 mx-auto mb-2" />
                                  <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Timeline</div>
                                  <div className="text-3xl font-bold text-gray-900 mb-1">{pathway.estimated_timeline_days || 0}</div>
                                  <div className="text-xs text-gray-600 font-medium">days</div>
                                </div>
                                <div className="glass rounded-2xl p-5 text-center bg-white/80 shadow-md">
                                  <Users className="w-6 h-6 text-purple-600 mx-auto mb-2" />
                                  <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Consents</div>
                                  <div className="text-3xl font-bold text-gray-900 mb-1">{pathway.required_consents?.length || 0}</div>
                                  <div className="text-xs text-gray-600 font-medium">required</div>
                                </div>
                                <div className={`glass rounded-2xl p-5 text-center shadow-md ${
                                  hasBlockers ? 'bg-red-50 border-2 border-red-200' : 'bg-green-50 border-2 border-green-200'
                                }`}>
                                  <AlertTriangle className={`w-6 h-6 mx-auto mb-2 ${hasBlockers ? 'text-red-600' : 'text-green-600'}`} />
                                  <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Blockers</div>
                                  <div className={`text-3xl font-bold mb-1 ${hasBlockers ? 'text-red-600' : 'text-green-600'}`}>
                                    {pathway.blockers?.length || 0}
                                  </div>
                                  <div className="text-xs text-gray-600 font-medium">issues</div>
                                </div>
                                <div className="glass rounded-2xl p-5 text-center bg-white/80 shadow-md">
                                  <CheckCircle className="w-6 h-6 text-green-600 mx-auto mb-2" />
                                  <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Actions</div>
                                  <div className="text-3xl font-bold text-gray-900 mb-1">{pathway.recommended_actions?.length || 0}</div>
                                  <div className="text-xs text-gray-600 font-medium">recommended</div>
                                </div>
                              </div>

                              {/* Required Consents */}
                              {pathway.required_consents && pathway.required_consents.length > 0 && (
                                <div className="mt-6 glass rounded-2xl p-6 bg-white/80 shadow-md">
                                  <div className="flex items-center mb-4">
                                    <Users className="w-5 h-5 text-purple-600 mr-2" />
                                    <h5 className="text-lg font-bold text-gray-900 uppercase tracking-wide">Required Consents</h5>
                                    <span className="ml-auto px-3 py-1 rounded-full bg-purple-100 text-purple-700 text-xs font-bold">
                                      {pathway.required_consents.length} {pathway.required_consents.length === 1 ? 'party' : 'parties'}
                                    </span>
                                  </div>
                                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                    {pathway.required_consents.map((consent: any, cIdx: number) => {
                                      const complexityColor = consent.complexity === 'high' ? 'from-red-500 to-red-600' :
                                                              consent.complexity === 'medium' ? 'from-yellow-500 to-yellow-600' :
                                                              'from-green-500 to-green-600'
                                      return (
                                        <div key={cIdx} className="bg-white rounded-xl p-4 border-2 border-gray-200 shadow-sm card-hover">
                                          <div className="flex items-center justify-between mb-2">
                                            <div className="font-bold text-gray-900 text-sm">{consent.party || 'Unknown Party'}</div>
                                            <span className={`px-2 py-1 rounded-lg text-xs font-bold bg-gradient-to-r ${complexityColor} text-white`}>
                                              {consent.complexity || 'low'}
                                            </span>
                                          </div>
                                          {consent.estimated_days && (
                                            <div className="text-xs text-gray-600 mt-2">
                                              <Clock className="w-3 h-3 inline mr-1" />
                                              ~{consent.estimated_days} days
                                            </div>
                                          )}
                                        </div>
                                      )
                                    })}
                                  </div>
                                </div>
                              )}

                              {/* Potential Blockers */}
                              {pathway.blockers && pathway.blockers.length > 0 && (
                                <div className="mt-6 glass rounded-2xl p-6 bg-gradient-to-br from-red-50 to-red-100 border-2 border-red-300 shadow-md">
                                  <div className="flex items-center mb-4">
                                    <AlertTriangle className="w-5 h-5 text-red-600 mr-2" />
                                    <h5 className="text-lg font-bold text-red-700 uppercase tracking-wide">Potential Blockers</h5>
                                    <span className="ml-auto px-3 py-1 rounded-full bg-red-200 text-red-800 text-xs font-bold">
                                      {pathway.blockers.length} {pathway.blockers.length === 1 ? 'blocker' : 'blockers'}
                                    </span>
                                  </div>
                                  <div className="space-y-4">
                                    {pathway.blockers.map((blocker: any, bIdx: number) => {
                                      const severityGradient = blocker.severity === 'high' ? 'from-red-500 to-red-600' :
                                                               blocker.severity === 'medium' ? 'from-yellow-500 to-yellow-600' :
                                                               'from-orange-500 to-orange-600'
                                      return (
                                        <div key={bIdx} className="bg-white rounded-xl p-5 border-2 border-red-200 shadow-sm">
                                          <div className="flex items-center justify-between mb-3">
                                            <div className="flex items-center space-x-3">
                                              <div className={`p-2 rounded-lg bg-gradient-to-r ${severityGradient}`}>
                                                <AlertTriangle className="w-4 h-4 text-white" />
                                              </div>
                                              <div className="font-bold text-lg text-gray-900">{blocker.type || 'Unknown Blocker'}</div>
                                            </div>
                                            <span className={`px-3 py-1.5 rounded-xl text-xs font-bold bg-gradient-to-r ${severityGradient} text-white shadow-md`}>
                                              {blocker.severity?.toUpperCase() || 'UNKNOWN'}
                                            </span>
                                          </div>
                                          <div className="text-sm text-gray-700 mb-3 leading-relaxed bg-gray-50 rounded-lg p-3 border border-gray-200">
                                            {blocker.description || 'No description available'}
                                          </div>
                                          {blocker.mitigation && (
                                            <div className="bg-blue-50 rounded-lg p-4 border-2 border-blue-200">
                                              <div className="flex items-center mb-2">
                                                <CheckCircle className="w-4 h-4 text-blue-600 mr-2" />
                                                <span className="text-xs font-bold text-blue-900 uppercase tracking-wide">Mitigation Strategy</span>
                                              </div>
                                              <div className="text-sm text-blue-800 leading-relaxed">{blocker.mitigation}</div>
                                            </div>
                                          )}
                                        </div>
                                      )
                                    })}
                                  </div>
                                </div>
                              )}

                              {/* Recommended Actions */}
                              {pathway.recommended_actions && pathway.recommended_actions.length > 0 && (
                                <div className="mt-6 glass rounded-2xl p-6 bg-white/80 shadow-md">
                                  <div className="flex items-center mb-4">
                                    <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                                    <h5 className="text-lg font-bold text-gray-900 uppercase tracking-wide">Recommended Actions</h5>
                                    <span className="ml-auto px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-bold">
                                      {pathway.recommended_actions.length} steps
                                    </span>
                                  </div>
                                  <ol className="space-y-3">
                                    {pathway.recommended_actions.map((action: string, aIdx: number) => (
                                      <li key={aIdx} className="flex items-start bg-white rounded-xl p-4 border-2 border-gray-200 shadow-sm card-hover">
                                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-r from-primary-500 to-primary-700 text-white flex items-center justify-center font-bold text-sm mr-4 shadow-md">
                                          {aIdx + 1}
                                        </div>
                                        <span className="text-sm text-gray-700 leading-relaxed pt-1">{action}</span>
                                      </li>
                                    ))}
                                  </ol>
                                </div>
                              )}

                              {/* Transfer Playbook */}
                              {pathway.playbook && (
                                <div className="mt-6 glass-strong rounded-2xl p-6 border-2 border-gray-300 bg-white/90 shadow-md">
                                  <div className="flex items-center mb-4">
                                    <FileText className="w-5 h-5 text-indigo-600 mr-2" />
                                    <h5 className="text-lg font-bold text-gray-900 uppercase tracking-wide">Transfer Playbook</h5>
                                  </div>
                                  <div className="text-sm font-mono whitespace-pre-wrap text-gray-700 bg-gray-50 p-5 rounded-xl border-2 border-gray-200 overflow-auto max-h-96 shadow-inner leading-relaxed">
                                    {pathway.playbook}
                                  </div>
                                </div>
                              )}
                            </div>
                          )
                        })}
                      </div>
                    ) : (
                      <div className="text-center py-16 glass-strong rounded-2xl">
                        <ArrowRightLeft className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                        <h4 className="text-xl font-bold text-gray-900 mb-2">No Pathways Available</h4>
                        <p className="text-gray-600 font-medium">Please ensure the analysis is completed to generate transfer pathways.</p>
                      </div>
                    )
                  ) : (
                    <div className="text-center py-16">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
                      <p className="text-gray-600 font-medium">Loading transfer simulation...</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'lma-deviations' && (
              <div className="space-y-6 fade-in">
                <div className="glass-panel rounded-2xl p-8 overflow-hidden">
                  <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center">
                      <div className="p-4 rounded-2xl bg-gradient-to-br from-yellow-400 to-yellow-600 mr-4 shadow-lg">
                        <FileText className="w-7 h-7 text-white" />
                      </div>
                      <div>
                        <h3 className="text-3xl font-bold gradient-text">LMA Deviations</h3>
                        <p className="text-sm text-gray-600 mt-1">Standard compliance analysis</p>
                      </div>
                    </div>
                  </div>
                  {lmaDeviations ? (
                    <div className="space-y-8">
                      {/* Summary Cards */}
                      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
                        <div className="glass-strong rounded-2xl p-6 text-center card-hover shadow-lg">
                          <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Total Deviations</div>
                          <div className="text-4xl font-bold text-gray-900 mb-2">{lmaDeviations.deviation_count || 0}</div>
                          <div className="text-xs text-gray-600">Identified issues</div>
                        </div>
                        <div className="glass-strong rounded-2xl p-6 text-center bg-gradient-to-br from-red-50 to-red-100 border-2 border-red-200 card-hover shadow-lg">
                          <div className="text-xs font-bold text-red-700 uppercase tracking-wider mb-3">High Severity</div>
                          <div className="text-4xl font-bold text-red-600 mb-2">{lmaDeviations.severity_breakdown?.high || 0}</div>
                          <div className="text-xs text-red-600 font-medium">Critical issues</div>
                        </div>
                        <div className="glass-strong rounded-2xl p-6 text-center bg-gradient-to-br from-yellow-50 to-yellow-100 border-2 border-yellow-200 card-hover shadow-lg">
                          <div className="text-xs font-bold text-yellow-700 uppercase tracking-wider mb-3">Medium Severity</div>
                          <div className="text-4xl font-bold text-yellow-600 mb-2">{lmaDeviations.severity_breakdown?.medium || 0}</div>
                          <div className="text-xs text-yellow-600 font-medium">Moderate issues</div>
                        </div>
                        <div className="glass-strong rounded-2xl p-6 text-center bg-gradient-to-br from-green-50 to-green-100 border-2 border-green-200 card-hover shadow-lg">
                          <div className="text-xs font-bold text-green-700 uppercase tracking-wider mb-3">Low Severity</div>
                          <div className="text-4xl font-bold text-green-600 mb-2">{lmaDeviations.severity_breakdown?.low || 0}</div>
                          <div className="text-xs text-green-600 font-medium">Minor issues</div>
                        </div>
                      </div>

                      {/* Deviations List */}
                      {lmaDeviations.deviations && lmaDeviations.deviations.length > 0 ? (
                        <div className="space-y-5">
                          <div className="flex items-center justify-between mb-4">
                            <h4 className="text-xl font-bold text-gray-900">Deviation Details</h4>
                            <span className="text-sm text-gray-600 font-medium">
                              {lmaDeviations.deviations.length} {lmaDeviations.deviations.length === 1 ? 'deviation' : 'deviations'}
                            </span>
                          </div>
                          {lmaDeviations.deviations.map((dev: any, idx: number) => {
                            const severityColor = dev.severity === 'high' ? 'from-red-500 to-red-600' :
                                                  dev.severity === 'medium' ? 'from-yellow-500 to-yellow-600' :
                                                  'from-blue-500 to-blue-600'
                            const borderColor = dev.severity === 'high' ? 'border-red-500' :
                                                dev.severity === 'medium' ? 'border-yellow-500' :
                                                'border-blue-500'
                            return (
                              <div key={idx} className={`glass-strong border-l-4 ${borderColor} rounded-2xl p-6 fade-in card-hover shadow-md`} style={{ animationDelay: `${idx * 0.1}s` }}>
                                <div className="flex items-start justify-between mb-4">
                                  <div className="flex-1">
                                    <div className="flex items-center space-x-3 mb-2">
                                      <div className={`px-4 py-2 rounded-xl bg-gradient-to-r ${severityColor} text-white text-xs font-bold shadow-lg`}>
                                        {dev.severity?.toUpperCase() || 'UNKNOWN'}
                                      </div>
                                      <div className="font-bold text-xl text-gray-900">{dev.clause_type || 'Unspecified Clause'}</div>
                                    </div>
                                    {dev.clause_reference && (
                                      <div className="text-sm text-gray-600 font-medium mb-3">
                                        <span className="font-semibold">Reference:</span> {dev.clause_reference}
                                      </div>
                                    )}
                                  </div>
                                </div>
                                
                                <div className="bg-white rounded-xl p-4 mb-4 border border-gray-200 shadow-sm">
                                  <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Market Impact</div>
                                  <div className="text-sm text-gray-700 leading-relaxed">{dev.market_impact || 'No impact assessment available'}</div>
                                </div>

                                {dev.deviation_details && (
                                  <div className="bg-gray-50 rounded-xl p-4 mb-4 border border-gray-200">
                                    <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Deviation Details</div>
                                    <div className="text-sm text-gray-700 leading-relaxed">{dev.deviation_details}</div>
                                  </div>
                                )}

                                {dev.recommendation && (
                                  <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-xl p-5 border-2 border-primary-200 shadow-sm">
                                    <div className="flex items-center mb-2">
                                      <CheckCircle className="w-5 h-5 text-primary-600 mr-2" />
                                      <div className="text-sm font-bold text-primary-900 uppercase tracking-wide">Recommendation</div>
                                    </div>
                                    <div className="text-sm text-primary-800 leading-relaxed mt-2">{dev.recommendation}</div>
                                  </div>
                                )}

                                {dev.lma_standard && (
                                  <div className="mt-4 pt-4 border-t border-gray-200">
                                    <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">LMA Standard</div>
                                    <div className="text-sm text-gray-700 bg-white rounded-lg p-3 border border-gray-200">{dev.lma_standard}</div>
                                  </div>
                                )}
                              </div>
                            )
                          })}
                        </div>
                      ) : (
                        <div className="text-center py-12 glass-strong rounded-2xl">
                          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                          <h4 className="text-xl font-bold text-gray-900 mb-2">No Deviations Found</h4>
                          <p className="text-gray-600">This loan document complies with LMA standards.</p>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-16">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
                      <p className="text-gray-600 font-medium">Loading LMA deviations analysis...</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'buyer-fit' && (
              <div className="space-y-6 fade-in">
                <div className="glass-panel rounded-2xl p-8 overflow-hidden">
                  <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center">
                      <div className="p-4 rounded-2xl bg-gradient-to-br from-purple-400 to-purple-600 mr-4 shadow-lg">
                        <Users className="w-7 h-7 text-white" />
                      </div>
                      <div>
                        <h3 className="text-3xl font-bold gradient-text">Buyer Fit Analysis</h3>
                        <p className="text-sm text-gray-600 mt-1">Optimal buyer matching and allocation</p>
                      </div>
                    </div>
                  </div>
                  {buyerFit ? (
                    <div className="space-y-8">
                      {/* Summary Stats */}
                      {buyerFit.buyer_fits && buyerFit.buyer_fits.length > 0 && (
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6">
                          <div className="glass-strong rounded-2xl p-6 text-center card-hover shadow-lg">
                            <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Total Buyer Types</div>
                            <div className="text-4xl font-bold text-gray-900 mb-2">{buyerFit.buyer_fits.length}</div>
                            <div className="text-xs text-gray-600">Analyzed</div>
                          </div>
                          <div className="glass-strong rounded-2xl p-6 text-center bg-gradient-to-br from-green-50 to-green-100 border-2 border-green-200 card-hover shadow-lg">
                            <div className="text-xs font-bold text-green-700 uppercase tracking-wider mb-3">High Fit (70+)</div>
                            <div className="text-4xl font-bold text-green-600 mb-2">
                              {buyerFit.buyer_fits.filter((f: any) => f.fit_score >= 70).length}
                            </div>
                            <div className="text-xs text-green-600 font-medium">Optimal matches</div>
                          </div>
                          <div className="glass-strong rounded-2xl p-6 text-center bg-gradient-to-br from-purple-50 to-purple-100 border-2 border-purple-200 card-hover shadow-lg">
                            <div className="text-xs font-bold text-purple-700 uppercase tracking-wider mb-3">Avg Fit Score</div>
                            <div className="text-4xl font-bold text-purple-600 mb-2">
                              {Math.round(buyerFit.buyer_fits.reduce((sum: number, f: any) => sum + (f.fit_score || 0), 0) / buyerFit.buyer_fits.length) || 0}
                            </div>
                            <div className="text-xs text-purple-600 font-medium">Overall average</div>
                          </div>
                        </div>
                      )}

                      {/* Buyer Fit Cards */}
                      {buyerFit.buyer_fits && buyerFit.buyer_fits.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                          {buyerFit.buyer_fits.map((fit: any, idx: number) => {
                            const scoreColor = fit.fit_score >= 70 ? 'from-green-500 to-green-600' : 
                                              fit.fit_score >= 40 ? 'from-yellow-500 to-yellow-600' : 
                                              'from-red-500 to-red-600'
                            const bgGradient = fit.fit_score >= 70 ? 'from-green-50 to-green-100' :
                                              fit.fit_score >= 40 ? 'from-yellow-50 to-yellow-100' :
                                              'from-red-50 to-red-100'
                            const borderColor = fit.fit_score >= 70 ? 'border-green-300' :
                                               fit.fit_score >= 40 ? 'border-yellow-300' :
                                               'border-red-300'
                            const fitLabel = fit.fit_score >= 70 ? 'Excellent Fit' :
                                           fit.fit_score >= 40 ? 'Moderate Fit' :
                                           'Poor Fit'
                            
                            return (
                              <div key={idx} className={`glass-strong rounded-2xl p-6 fade-in card-hover shadow-lg border-2 ${borderColor} bg-gradient-to-br ${bgGradient}`} style={{ animationDelay: `${idx * 0.1}s` }}>
                                {/* Header with Score */}
                                <div className="text-center mb-6">
                                  <div className={`inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br ${scoreColor} text-white mb-4 shadow-xl transform hover:scale-110 transition-transform`}>
                                    <span className="text-3xl font-bold">{fit.fit_score || 0}</span>
                                  </div>
                                  <div className="text-xl font-bold text-gray-900 mb-1">{fit.buyer_type || 'Unknown Buyer'}</div>
                                  <div className={`inline-block px-3 py-1 rounded-full text-xs font-bold ${
                                    fit.fit_score >= 70 ? 'bg-green-200 text-green-800' :
                                    fit.fit_score >= 40 ? 'bg-yellow-200 text-yellow-800' :
                                    'bg-red-200 text-red-800'
                                  }`}>
                                    {fitLabel}
                                  </div>
                                </div>

                                {/* Allocation Percentage */}
                                {fit.allocation_percentage && (
                                  <div className="mb-4">
                                    <div className="flex items-center justify-between mb-2">
                                      <span className="text-xs font-bold text-gray-600 uppercase tracking-wide">Recommended Allocation</span>
                                      <span className="text-sm font-bold text-gray-900">{fit.allocation_percentage}%</span>
                                    </div>
                                    <div className="w-full bg-white/80 rounded-full h-3 overflow-hidden shadow-inner">
                                      <div 
                                        className={`h-full bg-gradient-to-r ${scoreColor} rounded-full transition-all duration-500`}
                                        style={{ width: `${fit.allocation_percentage}%` }}
                                      />
                                    </div>
                                  </div>
                                )}

                                {/* Key Indicators */}
                                {fit.indicators && fit.indicators.length > 0 && (
                                  <div className="mb-4">
                                    <div className="text-xs font-bold text-gray-600 uppercase tracking-wide mb-3">Key Indicators</div>
                                    <div className="space-y-2">
                                      {fit.indicators.slice(0, 4).map((ind: string, i: number) => (
                                        <div key={i} className="flex items-start bg-white/90 rounded-lg p-3 border border-gray-200 shadow-sm">
                                          <CheckCircle className="w-4 h-4 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
                                          <span className="text-xs text-gray-700 leading-relaxed">{ind}</span>
                                        </div>
                                      ))}
                                    </div>
                                  </div>
                                )}

                                {/* Rationale */}
                                {fit.rationale && (
                                  <div className="mt-4 pt-4 border-t border-gray-300">
                                    <div className="text-xs font-bold text-gray-600 uppercase tracking-wide mb-2">Rationale</div>
                                    <div className="text-xs text-gray-700 bg-white/90 rounded-lg p-3 border border-gray-200 leading-relaxed">
                                      {fit.rationale}
                                    </div>
                                  </div>
                                )}

                                {/* Risk Factors */}
                                {fit.risk_factors && fit.risk_factors.length > 0 && (
                                  <div className="mt-4 pt-4 border-t border-gray-300">
                                    <div className="text-xs font-bold text-gray-600 uppercase tracking-wide mb-2">Risk Factors</div>
                                    <div className="space-y-1">
                                      {fit.risk_factors.slice(0, 2).map((risk: string, i: number) => (
                                        <div key={i} className="flex items-start bg-red-50 rounded-lg p-2 border border-red-200">
                                          <AlertTriangle className="w-3 h-3 text-red-600 mr-2 mt-0.5 flex-shrink-0" />
                                          <span className="text-xs text-red-700">{risk}</span>
                                        </div>
                                      ))}
                                    </div>
                                  </div>
                                )}
                              </div>
                            )
                          })}
                        </div>
                      ) : (
                        <div className="text-center py-12 glass-strong rounded-2xl">
                          <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                          <h4 className="text-xl font-bold text-gray-900 mb-2">No Buyer Fit Data</h4>
                          <p className="text-gray-600">Buyer fit analysis is not available for this loan.</p>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-16">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
                      <p className="text-gray-600 font-medium">Loading buyer fit analysis...</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'negotiation' && (
              <div className="space-y-6 fade-in">
                <div className="glass-panel rounded-2xl p-8">
                  <div className="flex items-center mb-6">
                    <div className="p-3 rounded-xl bg-gradient-to-br from-indigo-100 to-indigo-200 mr-4">
                      <MessageSquare className="w-6 h-6 text-indigo-600" />
                    </div>
                    <h3 className="text-2xl font-bold gradient-text">Negotiation Insights</h3>
                  </div>
                  {negotiationInsights ? (
                    <div className="space-y-5">
                      {negotiationInsights.insights?.map((insight: any, idx: number) => {
                        const likelihood = insight.negotiation_likelihood?.toLowerCase() || ''
                        const likelihoodColor = likelihood.includes('high') ? 'from-red-500 to-red-600' :
                                               likelihood.includes('medium') ? 'from-yellow-500 to-yellow-600' :
                                               'from-green-500 to-green-600'
                        return (
                          <div key={idx} className="glass-strong border-l-4 border-indigo-500 rounded-2xl p-6 fade-in card-hover" style={{ animationDelay: `${idx * 0.1}s` }}>
                            <div className="flex items-center justify-between mb-4">
                              <div className="font-bold text-lg text-gray-900">{insight.clause_reference}</div>
                              <div className={`px-4 py-2 rounded-xl bg-gradient-to-r ${likelihoodColor} text-white text-xs font-bold shadow-lg`}>
                                {insight.negotiation_likelihood}
                              </div>
                            </div>
                            {insight.suggested_redlines?.length > 0 && (
                              <div className="mt-4 glass rounded-xl p-4">
                                <div className="text-sm font-bold text-gray-900 mb-3 uppercase tracking-wide">Suggested Redlines</div>
                                <ul className="space-y-2">
                                  {insight.suggested_redlines.map((redline: string, i: number) => (
                                    <li key={i} className="flex items-start bg-white rounded-lg p-3 border border-gray-200">
                                      <span className="text-indigo-500 mr-3 font-bold">{i + 1}.</span>
                                      <span className="text-sm text-gray-700">{redline}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                            {insight.negotiation_strategy && (
                              <div className="mt-4 p-4 bg-indigo-50 rounded-xl border border-indigo-200">
                                <div className="text-xs font-bold text-indigo-900 mb-2">Strategy:</div>
                                <div className="text-sm text-indigo-800">{insight.negotiation_strategy}</div>
                              </div>
                            )}
                          </div>
                        )
                      })}
                    </div>
                  ) : (
                    <div className="text-center py-12">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
                      <p className="mt-4 text-gray-600">Loading negotiation insights...</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'monitoring' && (
              <div className="glass-panel rounded-xl p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Post-Trade Monitoring</h3>
                {monitoringAlerts ? (
                  <div className="space-y-4">
                    {monitoringAlerts.alerts?.length > 0 ? (
                      monitoringAlerts.alerts.map((alert: any, idx: number) => (
                        <div key={idx} className={`border-l-4 ${alert.alert_type === 'critical' ? 'border-red-500' : 'border-yellow-500'} pl-4 py-2 bg-${alert.alert_type === 'critical' ? 'red' : 'yellow'}-50 rounded`}>
                          <div className="font-medium">{alert.message}</div>
                        </div>
                      ))
                    ) : (
                      <p className="text-gray-600">No active alerts</p>
                    )}
                  </div>
                ) : (
                  <p className="text-gray-600">Loading monitoring alerts...</p>
                )}
              </div>
            )}

            {activeTab === 'auction' && (
              <AuctionRoom 
                analysisId={id || ''} 
                loanName={analysis?.loan_name || 'Unknown Loan'}
              />
            )}
          </div>
        </>
      )}
    </div>
  )
}

