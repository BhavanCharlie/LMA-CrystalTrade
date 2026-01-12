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
    <div className="glass-panel rounded-2xl p-8 fade-in">
      <div className="flex items-center justify-between mb-8">
        <h3 className="text-2xl font-bold gradient-text">
          Risk Assessment
        </h3>
        <div className={`px-4 py-2 rounded-xl font-semibold ${
          overallScore >= 70 
            ? 'bg-gradient-to-r from-red-500 to-red-600 text-white shadow-lg' 
            : overallScore >= 40 
            ? 'bg-gradient-to-r from-yellow-500 to-yellow-600 text-white shadow-lg'
            : 'bg-gradient-to-r from-green-500 to-green-600 text-white shadow-lg'
        }`}>
          {getRiskLabel(overallScore)}
        </div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="flex flex-col items-center justify-center glass-strong rounded-2xl p-8">
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
          <div className="mt-6 text-center">
            <div
              className="text-6xl font-bold mb-2"
              style={{ color: getRiskColor(overallScore) }}
            >
              {overallScore}
            </div>
            <div className="text-lg font-semibold text-gray-600">
              Overall Risk Score
            </div>
          </div>
        </div>
        <div className="space-y-6">
          <h4 className="text-lg font-bold text-gray-900 mb-4">
            Risk Breakdown
          </h4>
          {data.map((item) => (
            <div key={item.name} className="glass-strong rounded-xl p-4">
              <div className="flex justify-between items-center mb-3">
                <span className="text-sm font-semibold text-gray-700">{item.name}</span>
                <span className="text-lg font-bold" style={{ color: item.fill }}>{item.value}/100</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div
                  className="h-3 rounded-full transition-all duration-500 shadow-sm"
                  style={{
                    width: `${item.value}%`,
                    background: `linear-gradient(90deg, ${item.fill}, ${item.fill}dd)`,
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

