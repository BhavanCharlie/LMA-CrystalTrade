import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { AlertTriangle, CheckCircle, Clock } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { api } from '../services/api'

interface DashboardStats {
  total_analyses: number
  completed: number
  in_progress: number
  high_risk: number
  low_risk: number
  medium_risk: number
  recent_analyses: Array<{
    id: string
    loan_name: string
    risk_score: number
    status: string
    created_at: string
  }>
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const data = await api.getDashboardStats()
      setStats(data)
    } catch (error) {
      console.error('Failed to fetch dashboard stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-sm text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  const riskData = stats
    ? [
        { name: 'Low Risk', value: stats.low_risk, color: '#10b981' },
        { name: 'Medium Risk', value: stats.medium_risk, color: '#f59e0b' },
        { name: 'High Risk', value: stats.high_risk, color: '#ef4444' },
      ]
    : []

  const statusData = stats
    ? [
        { name: 'Completed', value: stats.completed },
        { name: 'In Progress', value: stats.in_progress },
      ]
    : []

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold gradient-text">Dashboard</h1>
        <p className="mt-2 text-sm text-gray-600">
          Overview of loan due diligence analyses
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div className="glass-card overflow-hidden rounded-2xl card-hover fade-in">
          <div className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="p-4 rounded-xl bg-gradient-to-br from-primary-100 to-primary-200 shadow-lg">
                    <FileText className="h-6 w-6 text-primary-600 icon-glow" />
                  </div>
                </div>
                <div className="ml-4 w-0 flex-1">
                  <dl>
                    <dt className="text-xs font-semibold text-gray-500 uppercase tracking-wide truncate">
                      Total Analyses
                    </dt>
                    <dd className="text-3xl font-bold text-gray-900 mt-2">
                      {stats?.total_analyses || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="glass-card overflow-hidden rounded-2xl card-hover fade-in" style={{ animationDelay: '0.1s' }}>
          <div className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="p-4 rounded-xl bg-gradient-to-br from-green-100 to-green-200 shadow-lg">
                    <CheckCircle className="h-6 w-6 text-green-600 icon-glow" />
                  </div>
                </div>
                <div className="ml-4 w-0 flex-1">
                  <dl>
                    <dt className="text-xs font-semibold text-gray-500 uppercase tracking-wide truncate">
                      Completed
                    </dt>
                    <dd className="text-3xl font-bold text-gray-900 mt-2">
                      {stats?.completed || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="glass-card overflow-hidden rounded-2xl card-hover fade-in" style={{ animationDelay: '0.2s' }}>
          <div className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="p-4 rounded-xl bg-gradient-to-br from-yellow-100 to-yellow-200 shadow-lg">
                    <Clock className="h-6 w-6 text-yellow-600 icon-glow" />
                  </div>
                </div>
                <div className="ml-4 w-0 flex-1">
                  <dl>
                    <dt className="text-xs font-semibold text-gray-500 uppercase tracking-wide truncate">
                      In Progress
                    </dt>
                    <dd className="text-3xl font-bold text-gray-900 mt-2">
                      {stats?.in_progress || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="glass-card overflow-hidden rounded-2xl card-hover fade-in" style={{ animationDelay: '0.3s' }}>
          <div className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="p-4 rounded-xl bg-gradient-to-br from-red-100 to-red-200 shadow-lg">
                    <AlertTriangle className="h-6 w-6 text-red-600 icon-glow" />
                  </div>
                </div>
                <div className="ml-4 w-0 flex-1">
                  <dl>
                    <dt className="text-xs font-semibold text-gray-500 uppercase tracking-wide truncate">
                      High Risk
                    </dt>
                    <dd className="text-3xl font-bold text-gray-900 mt-2">
                      {stats?.high_risk || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="glass-panel rounded-2xl p-8 fade-in">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-gray-900">
              Risk Distribution
            </h3>
            <div className="w-2 h-2 rounded-full bg-primary-500 pulse-slow"></div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={riskData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) =>
                  `${name}: ${(percent * 100).toFixed(0)}%`
                }
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {riskData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="glass-panel rounded-2xl p-8 fade-in" style={{ animationDelay: '0.1s' }}>
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-gray-900">
              Status Overview
            </h3>
            <div className="w-2 h-2 rounded-full bg-primary-500 pulse-slow"></div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={statusData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.2)" />
              <XAxis dataKey="name" stroke="rgba(255,255,255,0.8)" />
              <YAxis stroke="rgba(255,255,255,0.8)" />
              <Tooltip />
              <Bar dataKey="value" fill="#0ea5e9" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="glass-panel rounded-2xl overflow-hidden fade-in">
        <div className="px-8 py-6 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-white">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold text-gray-900">
              Recent Analyses
            </h3>
            <span className="text-sm text-gray-500 font-medium">
              {stats?.recent_analyses?.length || 0} items
            </span>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gradient-to-r from-gray-50 to-gray-100">
              <tr>
                <th className="px-8 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Loan Name
                </th>
                <th className="px-8 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Risk Score
                </th>
                <th className="px-8 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-8 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-8 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {stats?.recent_analyses?.map((analysis, idx) => (
                <tr key={analysis.id} className="hover:bg-gradient-to-r hover:from-primary-50 hover:to-transparent transition-all duration-200 smooth-transition" style={{ animationDelay: `${idx * 0.05}s` }}>
                  <td className="px-8 py-5 whitespace-nowrap">
                    <div className="text-sm font-semibold text-gray-900">{analysis.loan_name}</div>
                  </td>
                  <td className="px-8 py-5 whitespace-nowrap">
                    <span
                      className={`px-4 py-2 text-xs font-bold rounded-lg shadow-sm ${
                        analysis.risk_score >= 70
                          ? 'bg-gradient-to-r from-red-100 to-red-50 text-red-800 border border-red-200'
                          : analysis.risk_score >= 40
                          ? 'bg-gradient-to-r from-yellow-100 to-yellow-50 text-yellow-800 border border-yellow-200'
                          : 'bg-gradient-to-r from-green-100 to-green-50 text-green-800 border border-green-200'
                      }`}
                    >
                      {analysis.risk_score}/100
                    </span>
                  </td>
                  <td className="px-8 py-5 whitespace-nowrap">
                    <span className="text-sm text-gray-600 capitalize font-medium">{analysis.status}</span>
                  </td>
                  <td className="px-8 py-5 whitespace-nowrap">
                    <span className="text-sm text-gray-500">{new Date(analysis.created_at).toLocaleDateString()}</span>
                  </td>
                  <td className="px-8 py-5 whitespace-nowrap">
                    <Link
                      to={`/analysis/${analysis.id}`}
                      className="inline-flex items-center text-primary-600 hover:text-primary-800 transition-all duration-200 font-semibold group"
                    >
                      View Details
                      <span className="ml-1 group-hover:translate-x-1 transition-transform">→</span>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

function FileText(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
      />
    </svg>
  )
}

