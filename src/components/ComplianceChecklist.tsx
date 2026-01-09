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
    <div className="bg-white shadow rounded-lg p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">
        Compliance Checklist
      </h3>
      <div className="space-y-3">
        {checks.map((check, index) => (
          <div
            key={index}
            className={`border rounded-lg p-4 ${getStatusColor(check.status)}`}
          >
            <div className="flex items-start">
              <div className="flex-shrink-0">{getStatusIcon(check.status)}</div>
              <div className="ml-3 flex-1">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-medium text-gray-900">
                    {check.category}
                  </h4>
                  <span className="text-xs font-medium text-gray-500 uppercase">
                    {check.status}
                  </span>
                </div>
                <p className="mt-1 text-sm text-gray-600">
                  {check.description}
                </p>
                {check.details && (
                  <p className="mt-2 text-xs text-gray-500">{check.details}</p>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}


