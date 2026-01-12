interface ExtractedTermsProps {
  terms: {
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
}

export default function ExtractedTerms({ terms }: ExtractedTermsProps) {
  return (
    <div className="glass-panel rounded-2xl p-8 fade-in">
      <div className="flex items-center mb-6">
        <div className="p-3 rounded-xl bg-gradient-to-br from-primary-100 to-primary-200 mr-4">
          <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 className="text-xl font-bold gradient-text">
          Extracted Loan Terms
        </h3>
      </div>
      <dl className="space-y-5">
        {terms.interest_rate && (
          <div className="glass-strong rounded-xl p-4 border-l-4 border-primary-500">
            <dt className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">
              Interest Rate
            </dt>
            <dd className="text-lg font-bold text-gray-900">
              {terms.interest_rate}
            </dd>
          </div>
        )}
        {terms.maturity_date && (
          <div className="glass-strong rounded-xl p-4 border-l-4 border-green-500">
            <dt className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">
              Maturity Date
            </dt>
            <dd className="text-lg font-bold text-gray-900">
              {terms.maturity_date}
            </dd>
          </div>
        )}
        {terms.principal_amount && (
          <div className="glass-strong rounded-xl p-4 border-l-4 border-blue-500">
            <dt className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">
              Principal Amount
            </dt>
            <dd className="text-lg font-bold text-gray-900">
              {terms.principal_amount}
            </dd>
          </div>
        )}
        {terms.transfer_restrictions && (
          <div className="glass-strong rounded-xl p-4 border-l-4 border-yellow-500">
            <dt className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">
              Transfer Restrictions
            </dt>
            <dd className="text-sm text-gray-900 font-medium">
              {terms.transfer_restrictions}
            </dd>
          </div>
        )}
        {terms.consent_requirements && terms.consent_requirements.length > 0 && (
          <div className="glass-strong rounded-xl p-4 border-l-4 border-purple-500">
            <dt className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-3">
              Consent Requirements
            </dt>
            <dd>
              <ul className="space-y-2">
                {terms.consent_requirements.map((req, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-primary-500 mr-2">•</span>
                    <span className="text-sm text-gray-900 font-medium">{req}</span>
                  </li>
                ))}
              </ul>
            </dd>
          </div>
        )}
        {terms.financial_covenants &&
          terms.financial_covenants.length > 0 && (
            <div className="glass-strong rounded-xl p-4 border-l-4 border-indigo-500">
              <dt className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-3">
                Financial Covenants
              </dt>
              <dd>
                <div className="space-y-3">
                  {terms.financial_covenants.map((covenant, index) => (
                    <div
                      key={index}
                      className="bg-gradient-to-r from-gray-50 to-white rounded-lg p-4 border border-gray-200"
                    >
                      <div className="text-sm font-bold text-gray-900 mb-2">
                        {covenant.name}
                      </div>
                      <div className="text-xs text-gray-600 font-medium">
                        Requirement: <span className="text-gray-900">{covenant.requirement}</span>
                      </div>
                      {covenant.current_value && (
                        <div className="text-xs text-gray-600 font-medium mt-1">
                          Current: <span className="text-gray-900">{covenant.current_value}</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </dd>
            </div>
          )}
      </dl>
    </div>
  )
}


