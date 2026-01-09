import { RadialBarChart, RadialBar, ResponsiveContainer } from 'recharts'

interface RiskScoreProps {
  overallScore: number
  breakdown: {
    credit_risk: number
    legal_risk: number
    operational_risk: number
  }
}

export default function RiskScore({ overallScore, breakdown }: RiskScoreProps) {
  const getRiskColor = (score: number) => {
    if (score >= 70) return '#ef4444'
    if (score >= 40) return '#f59e0b'
    return '#10b981'
  }

  const getRiskLabel = (score: number) => {
    if (score >= 70) return 'High Risk'
    if (score >= 40) return 'Medium Risk'
    return 'Low Risk'
  }

  const data = [
    { name: 'Credit Risk', value: breakdown.credit_risk, fill: '#ef4444' },
    { name: 'Legal Risk', value: breakdown.legal_risk, fill: '#f59e0b' },
    { name: 'Operational Risk', value: breakdown.operational_risk, fill: '#3b82f6' },
  ]

  const radialData = [
    { name: 'Score', value: overallScore, fill: getRiskColor(overallScore) },
    { name: 'Max', value: 100, fill: '#e5e7eb' },
  ]

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-6">
        Risk Assessment
      </h3>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="flex flex-col items-center justify-center">
          <ResponsiveContainer width="100%" height={300}>
            <RadialBarChart
              innerRadius="60%"
              outerRadius="90%"
              data={radialData}
              startAngle={90}
              endAngle={-270}
            >
              <RadialBar dataKey="value" cornerRadius={10} />
            </RadialBarChart>
          </ResponsiveContainer>
          <div className="mt-4 text-center">
            <div
              className="text-4xl font-bold"
              style={{ color: getRiskColor(overallScore) }}
            >
              {overallScore}
            </div>
            <div className="text-sm text-gray-500 mt-1">
              {getRiskLabel(overallScore)}
            </div>
          </div>
        </div>
        <div className="space-y-4">
          <h4 className="text-sm font-medium text-gray-700">
            Risk Breakdown
          </h4>
          {data.map((item) => (
            <div key={item.name}>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">{item.name}</span>
                <span className="font-medium">{item.value}/100</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="h-2 rounded-full transition-all"
                  style={{
                    width: `${item.value}%`,
                    backgroundColor: item.fill,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

