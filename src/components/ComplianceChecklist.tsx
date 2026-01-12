import { CheckCircle, XCircle, AlertTriangle } from 'lucide-react'

interface ComplianceCheck {
  category: string
  status: 'pass' | 'fail' | 'warning'
  description: string
  details: string
}

interface ComplianceChecklistProps {
  checks: ComplianceCheck[]
}

export default function ComplianceChecklist({
  checks,
}: ComplianceChecklistProps) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pass':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'fail':
        return <XCircle className="h-5 w-5 text-red-500" />
      case 'warning':
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />
      default:
        return null
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pass':
        return 'bg-green-50 border-green-200'
      case 'fail':
        return 'bg-red-50 border-red-200'
      case 'warning':
        return 'bg-yellow-50 border-yellow-200'
      default:
        return 'bg-gray-50 border-gray-200'
    }
  }

  return (
    <div className="glass-panel rounded-2xl p-8 fade-in">
      <div className="flex items-center mb-6">
        <div className="p-3 rounded-xl bg-gradient-to-br from-green-100 to-green-200 mr-4">
          <CheckCircle className="w-6 h-6 text-green-600" />
        </div>
        <h3 className="text-xl font-bold gradient-text">
          Compliance Checklist
        </h3>
      </div>
      <div className="space-y-4">
        {checks.map((check, index) => (
          <div
            key={index}
            className={`glass-strong rounded-xl p-5 border-l-4 transition-all duration-300 hover:scale-[1.02] ${
              check.status === 'pass' 
                ? 'border-green-500 bg-gradient-to-r from-green-50 to-white' 
                : check.status === 'fail'
                ? 'border-red-500 bg-gradient-to-r from-red-50 to-white'
                : 'border-yellow-500 bg-gradient-to-r from-yellow-50 to-white'
            }`}
          >
            <div className="flex items-start">
              <div className="flex-shrink-0 p-2 rounded-lg bg-white shadow-sm">{getStatusIcon(check.status)}</div>
              <div className="ml-4 flex-1">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-base font-bold text-gray-900">
                    {check.category}
                  </h4>
                  <span className={`text-xs font-bold px-3 py-1 rounded-full uppercase ${
                    check.status === 'pass'
                      ? 'bg-green-100 text-green-800'
                      : check.status === 'fail'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {check.status}
                  </span>
                </div>
                <p className="text-sm text-gray-700 font-medium mb-2">
                  {check.description}
                </p>
                {check.details && (
                  <p className="text-xs text-gray-600 bg-white/60 rounded-lg p-2 mt-2">{check.details}</p>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}


