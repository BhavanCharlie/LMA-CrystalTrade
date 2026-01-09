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
    <div className="bg-white shadow rounded-lg p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">
        Extracted Loan Terms
      </h3>
      <dl className="space-y-4">
        {terms.interest_rate && (
          <div>
            <dt className="text-sm font-medium text-gray-500">
              Interest Rate
            </dt>
            <dd className="mt-1 text-sm text-gray-900">
              {terms.interest_rate}
            </dd>
          </div>
        )}
        {terms.maturity_date && (
          <div>
            <dt className="text-sm font-medium text-gray-500">
              Maturity Date
            </dt>
            <dd className="mt-1 text-sm text-gray-900">
              {terms.maturity_date}
            </dd>
          </div>
        )}
        {terms.principal_amount && (
          <div>
            <dt className="text-sm font-medium text-gray-500">
              Principal Amount
            </dt>
            <dd className="mt-1 text-sm text-gray-900">
              {terms.principal_amount}
            </dd>
          </div>
        )}
        {terms.transfer_restrictions && (
          <div>
            <dt className="text-sm font-medium text-gray-500">
              Transfer Restrictions
            </dt>
            <dd className="mt-1 text-sm text-gray-900">
              {terms.transfer_restrictions}
            </dd>
          </div>
        )}
        {terms.consent_requirements && terms.consent_requirements.length > 0 && (
          <div>
            <dt className="text-sm font-medium text-gray-500">
              Consent Requirements
            </dt>
            <dd className="mt-1">
              <ul className="list-disc list-inside text-sm text-gray-900 space-y-1">
                {terms.consent_requirements.map((req, index) => (
                  <li key={index}>{req}</li>
                ))}
              </ul>
            </dd>
          </div>
        )}
        {terms.financial_covenants &&
          terms.financial_covenants.length > 0 && (
            <div>
              <dt className="text-sm font-medium text-gray-500">
                Financial Covenants
              </dt>
              <dd className="mt-1">
                <div className="space-y-3">
                  {terms.financial_covenants.map((covenant, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded p-3"
                    >
                      <div className="text-sm font-medium text-gray-900">
                        {covenant.name}
                      </div>
                      <div className="text-xs text-gray-600 mt-1">
                        Requirement: {covenant.requirement}
                      </div>
                      {covenant.current_value && (
                        <div className="text-xs text-gray-600 mt-1">
                          Current: {covenant.current_value}
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


