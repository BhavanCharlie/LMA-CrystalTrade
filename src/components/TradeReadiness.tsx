import { CheckCircle, AlertTriangle, XCircle } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface TradeReadinessProps {
  score: number
  label: string
  breakdown: {
    [key: string]: {
      score: number
      contribution: number
      weight?: number
      friction_level?: number
      complexity_level?: number
    }
  }
  confidence: number
  evidence_links?: Array<any>
}

export default function TradeReadiness({
  score,
  label,
  breakdown,
  confidence,
  evidence_links = [],
}: TradeReadinessProps) {
  const getLabelColor = () => {
    if (label === 'Green') return 'text-green-600 bg-green-100'
    if (label === 'Amber') return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getLabelIcon = () => {
    if (label === 'Green') return <CheckCircle className="h-5 w-5" />
    if (label === 'Amber') return <AlertTriangle className="h-5 w-5" />
    return <XCircle className="h-5 w-5" />
  }

  const chartData = Object.entries(breakdown).map(([key, value]) => ({
    name: key.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase()),
    score: value.score,
    contribution: value.contribution,
  }))

  const scoreColor = getLabelColor().includes('green') ? '#10b981' : getLabelColor().includes('yellow') ? '#f59e0b' : '#ef4444'
  
  return (
    <div className="glass-panel rounded-2xl p-8 fade-in">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center">
          <div className="p-3 rounded-xl bg-gradient-to-br from-primary-100 to-primary-200 mr-4">
            <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold gradient-text">Trade Readiness Score</h3>
        </div>
        <div className={`flex items-center space-x-2 px-6 py-3 rounded-xl shadow-lg font-bold ${getLabelColor()}`}>
          {getLabelIcon()}
          <span>{label}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="flex flex-col items-center justify-center glass-strong rounded-2xl p-8">
          <div className="text-8xl font-bold mb-4" style={{ color: scoreColor }}>
            {score}
          </div>
          <div className="text-lg font-semibold text-gray-600 mb-2">out of 100</div>
          <div className="mt-4 px-4 py-2 rounded-lg bg-gradient-to-r from-gray-100 to-gray-50">
            <span className="text-sm font-bold text-gray-700">
              Confidence: <span className="text-primary-600">{(confidence * 100).toFixed(0)}%</span>
            </span>
          </div>
        </div>

        <div className="glass-strong rounded-2xl p-6">
          <h4 className="text-lg font-bold text-gray-900 mb-4">Score Breakdown</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                }} 
              />
              <Bar dataKey="score" fill="url(#colorGradient)" radius={[8, 8, 0, 0]}>
                <defs>
                  <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#0ea5e9" />
                    <stop offset="100%" stopColor="#0284c7" />
                  </linearGradient>
                </defs>
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-8">
        <h4 className="text-xl font-bold text-gray-900 mb-6">Detailed Breakdown</h4>
        <div className="space-y-4">
          {Object.entries(breakdown).map(([key, value]) => (
            <div key={key} className="glass-strong rounded-xl p-5 border-l-4 border-primary-500">
              <div className="flex justify-between items-center mb-3">
                <span className="text-base font-bold text-gray-900">
                  {key.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
                </span>
                <span className="text-lg font-bold text-primary-600">{value.score}/100</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 mb-2 overflow-hidden">
                <div
                  className="h-3 rounded-full transition-all duration-500 shadow-sm"
                  style={{ 
                    width: `${value.score}%`,
                    background: 'linear-gradient(90deg, #0ea5e9, #0284c7)'
                  }}
                />
              </div>
              <div className="grid grid-cols-2 gap-4 mt-3">
                {value.friction_level !== undefined && (
                  <div className="text-xs">
                    <span className="font-semibold text-gray-600">Friction: </span>
                    <span className="font-bold text-gray-900">{value.friction_level}/100</span>
                  </div>
                )}
                {value.complexity_level !== undefined && (
                  <div className="text-xs">
                    <span className="font-semibold text-gray-600">Complexity: </span>
                    <span className="font-bold text-gray-900">{value.complexity_level}/100</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {evidence_links.length > 0 && (
        <div className="mt-8 glass-strong rounded-2xl p-6">
          <h4 className="text-lg font-bold text-gray-900 mb-4">Evidence Links</h4>
          <div className="space-y-2">
            {evidence_links.slice(0, 5).map((link, idx) => (
              <div key={idx} className="flex items-center p-3 rounded-lg bg-gradient-to-r from-gray-50 to-white">
                <span className="text-primary-500 mr-2 font-bold">•</span>
                <span className="text-sm text-gray-700 font-medium">
                  <span className="font-bold">{link.type}:</span> {link.document || 'N/A'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

