import { FileText, Zap, Shield, TrendingUp, Users, Target, CheckCircle, AlertTriangle, BarChart3, ArrowRightLeft, Gavel, Bell, Search, Lightbulb, Clock, DollarSign, Upload, Briefcase, Home, ArrowLeft } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import AnimatedLogo from '../components/AnimatedLogo'
import { useAuth } from '../contexts/AuthContext'

export default function About() {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()
  const features = [
    {
      icon: FileText,
      title: "AI-Powered Document Analysis",
      description: "Automatically extracts key loan terms, interest rates, maturity dates, and principal amounts from complex loan documents using GPT-4.",
      benefit: "Reduces manual review time from hours to minutes"
    },
    {
      icon: BarChart3,
      title: "Risk Assessment",
      description: "Comprehensive risk scoring with breakdown by credit, legal, and operational risks. Visual charts and explainable analysis.",
      benefit: "Standardized, objective risk evaluation"
    },
    {
      icon: Shield,
      title: "Automated Compliance Checking",
      description: "Verifies compliance against LMA standards, checks transfer restrictions, consent requirements, and financial covenants.",
      benefit: "Ensures regulatory compliance automatically"
    },
    {
      icon: TrendingUp,
      title: "Trade Readiness Scoring",
      description: "0-100 score assessing how ready a loan is for trading based on documentation, transferability, consent complexity, and covenants.",
      benefit: "Quick visibility into tradeability"
    },
    {
      icon: ArrowRightLeft,
      title: "Transfer Simulation",
      description: "Simulates assignment and participation pathways, identifies required consents, estimates timelines, and highlights blockers.",
      benefit: "Understand transfer mechanics before committing"
    },
    {
      icon: Search,
      title: "LMA Deviation Detection",
      description: "Identifies deviations from LMA standard templates with severity ratings and recommendations for standardization.",
      benefit: "Maintains consistency with market standards"
    },
    {
      icon: Users,
      title: "Buyer Fit Analysis",
      description: "Matches loans to suitable buyer types (CLO, Bank, Distressed Fund) with fit scores and allocation recommendations.",
      benefit: "Faster, more accurate buyer identification"
    },
    {
      icon: Lightbulb,
      title: "Negotiation Insights",
      description: "AI-powered analysis identifies negotiation leverage points, suggests redlines, and predicts likely negotiation areas.",
      benefit: "Data-driven negotiation strategy"
    },
    {
      icon: Bell,
      title: "Post-Trade Monitoring",
      description: "Rule-based alerting system for covenant compliance, payment obligations, and key dates with automated notifications.",
      benefit: "Proactive covenant management"
    },
    {
      icon: Gavel,
      title: "Auction Room",
      description: "English and sealed-bid auction functionality for loan trading with real-time bidding, leaderboards, and winner selection.",
      benefit: "Streamlined auction process"
    }
  ]

  const problems = [
    {
      problem: "Time-Consuming Manual Review",
      impact: "Loan documents are 100+ pages, requiring hours of manual review by legal and credit teams",
      solution: "AI-powered extraction reduces review time by 80-90%, processing documents in minutes instead of hours"
    },
    {
      problem: "Inconsistent Risk Assessment",
      impact: "Risk evaluation varies between analysts, lacks standardization, and is subjective",
      solution: "Standardized risk scoring algorithm provides consistent, objective risk evaluation with explainable breakdowns"
    },
    {
      problem: "Missed Transfer Restrictions",
      impact: "Transfer restrictions buried in legal documents are easy to miss, leading to failed trades or delays",
      solution: "Automated detection identifies transfer restrictions early, preventing costly mistakes"
    },
    {
      problem: "Compliance Complexity",
      impact: "Ensuring compliance with LMA standards requires deep expertise and manual checking",
      solution: "Automated compliance verification against LMA standards with evidence logging for audit trails"
    },
    {
      problem: "Buyer Matching Challenges",
      impact: "Finding the right buyer requires understanding buyer preferences and loan characteristics",
      solution: "Buyer fit analysis automatically matches loans to suitable buyers (CLO, Bank, Distressed Fund)"
    },
    {
      problem: "Lack of Trade Readiness Visibility",
      impact: "Traders don't know if a loan is ready to trade until deep into the process",
      solution: "Trade readiness scoring provides early visibility with actionable recommendations"
    }
  ]

  const userTypes = [
    {
      type: "Loan Traders & Trading Desks",
      icon: Users,
      painPoints: ["Manual review takes hours", "Subjective risk assessment", "Easy to miss restrictions"],
      benefits: ["Instant AI analysis", "Automated risk scoring", "Early blocker identification"]
    },
    {
      type: "Investment Banks",
      icon: Briefcase,
      painPoints: ["High document volume", "Need quick tradeability assessment", "Compliance requirements"],
      benefits: ["Batch processing", "Trade readiness scoring", "Automated compliance"]
    },
    {
      type: "CLO Managers",
      icon: Target,
      painPoints: ["Need CLO-eligible loans", "Transfer restrictions block acquisitions", "Speed is critical"],
      benefits: ["CLO-specific buyer fit", "Transfer pathway simulation", "Quick assessment"]
    },
    {
      type: "Asset Management Firms",
      icon: BarChart3,
      painPoints: ["Evaluate multiple opportunities", "Covenant monitoring burden", "Due diligence consistency"],
      benefits: ["Portfolio-wide dashboard", "Automated monitoring", "Standardized reports"]
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-gray-100">
      {/* Header Navigation */}
      <header className="glass-nav sticky top-0 z-50 border-b border-white/20 shadow-lg bg-white/95 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo and Branding */}
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <AnimatedLogo size="md" showText={false} />
                <div className="ml-3">
                  <div className="text-2xl font-bold gradient-text">CrystalTrade</div>
                  <div className="text-xs text-gray-600 font-medium -mt-1">Transparent Loan Trading</div>
                </div>
              </div>
            </div>

            {/* Navigation Links */}
            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <>
                  <Link
                    to="/"
                    className="inline-flex items-center px-4 py-2 rounded-xl text-sm font-semibold text-gray-700 hover:bg-gray-100 transition-all"
                  >
                    <Home className="h-4 w-4 mr-2" />
                    Dashboard
                  </Link>
                  <Link
                    to="/upload"
                    className="inline-flex items-center px-4 py-2 rounded-xl text-sm font-semibold text-gray-700 hover:bg-gray-100 transition-all"
                  >
                    <Upload className="h-4 w-4 mr-2" />
                    Upload
                  </Link>
                  <Link
                    to="/reports"
                    className="inline-flex items-center px-4 py-2 rounded-xl text-sm font-semibold text-gray-700 hover:bg-gray-100 transition-all"
                  >
                    <FileText className="h-4 w-4 mr-2" />
                    Reports
                  </Link>
                </>
              ) : (
                <Link
                  to="/login"
                  className="inline-flex items-center px-4 py-2 rounded-xl text-sm font-semibold bg-primary-600 text-white hover:bg-primary-700 transition-all"
                >
                  Login
                </Link>
              )}
              <button
                onClick={() => navigate(-1)}
                className="inline-flex items-center px-4 py-2 rounded-xl text-sm font-semibold text-gray-700 hover:bg-gray-100 transition-all"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-primary-600 via-primary-700 to-primary-800 text-white">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <AnimatedLogo size="lg" showText={false} />
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              CrystalTrade
            </h1>
            <p className="text-xl md:text-2xl text-primary-100 mb-8 max-w-3xl mx-auto">
              Transparent Loan Trading Platform
            </p>
            <p className="text-lg text-primary-200 max-w-2xl mx-auto">
              Automating due diligence for secondary loan market transactions with AI-powered analysis, 
              bringing transparency and efficiency to loan trading.
            </p>
          </div>
        </div>
      </div>

      {/* Overview Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">What is CrystalTrade?</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              CrystalTrade is an AI-powered platform that automates and streamlines due diligence checks 
              for secondary loan market transactions. It analyzes loan documents, assesses risks, verifies 
              compliance, and provides comprehensive insights to help traders make informed decisions.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mt-12">
            <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-blue-50 to-blue-100">
              <Clock className="h-12 w-12 text-primary-600 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">80-90% Time Savings</h3>
              <p className="text-gray-600">Reduce manual review time from hours to minutes</p>
            </div>
            <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-green-50 to-green-100">
              <CheckCircle className="h-12 w-12 text-green-600 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">Automated Compliance</h3>
              <p className="text-gray-600">Real-time verification against LMA standards</p>
            </div>
            <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-purple-50 to-purple-100">
              <DollarSign className="h-12 w-12 text-purple-600 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">Better Decisions</h3>
              <p className="text-gray-600">Data-driven insights for smarter trading</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Key Features</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive tools designed to streamline every aspect of loan trading and due diligence
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <div
                  key={index}
                  className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-200"
                >
                  <div className="flex items-start">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center">
                        <Icon className="h-6 w-6 text-white" />
                      </div>
                    </div>
                    <div className="ml-4 flex-1">
                      <h3 className="text-lg font-bold text-gray-900 mb-2">{feature.title}</h3>
                      <p className="text-gray-600 text-sm mb-3">{feature.description}</p>
                      <div className="flex items-center text-sm text-primary-600 font-semibold">
                        <Zap className="h-4 w-4 mr-1" />
                        <span>{feature.benefit}</span>
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Problems & Solutions Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Solving Real-World Problems</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              CrystalTrade addresses critical challenges in the secondary loan market
            </p>
          </div>

          <div className="space-y-8">
            {problems.map((item, index) => (
              <div
                key={index}
                className="bg-gradient-to-r from-gray-50 to-blue-50 rounded-2xl p-8 shadow-md"
              >
                <div className="flex items-start">
                  <AlertTriangle className="h-8 w-8 text-red-500 flex-shrink-0 mr-4 mt-1" />
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">{item.problem}</h3>
                    <p className="text-gray-600 mb-4">{item.impact}</p>
                    <div className="flex items-start bg-white rounded-xl p-4 border-l-4 border-primary-500">
                      <CheckCircle className="h-6 w-6 text-green-500 flex-shrink-0 mr-3 mt-0.5" />
                      <p className="text-gray-700 font-medium">{item.solution}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* User Types Section */}
      <section className="py-16 bg-gradient-to-br from-primary-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Who Benefits from CrystalTrade?</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Designed for professionals across the loan trading ecosystem
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {userTypes.map((user, index) => {
              const Icon = user.icon
              return (
                <div
                  key={index}
                  className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200"
                >
                  <div className="flex items-center mb-6">
                    <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center mr-4">
                      <Icon className="h-8 w-8 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900">{user.type}</h3>
                  </div>
                  
                  <div className="mb-6">
                    <h4 className="text-sm font-semibold text-red-600 uppercase mb-3">Pain Points</h4>
                    <ul className="space-y-2">
                      {user.painPoints.map((point, i) => (
                        <li key={i} className="flex items-start text-gray-600">
                          <AlertTriangle className="h-5 w-5 text-red-400 mr-2 flex-shrink-0 mt-0.5" />
                          <span>{point}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="text-sm font-semibold text-green-600 uppercase mb-3">How CrystalTrade Helps</h4>
                    <ul className="space-y-2">
                      {user.benefits.map((benefit, i) => (
                        <li key={i} className="flex items-start text-gray-700">
                          <CheckCircle className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                          <span className="font-medium">{benefit}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Technology Stack Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Built with Modern Technology</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Leveraging cutting-edge AI and web technologies for optimal performance
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Frontend</h3>
              <ul className="space-y-3">
                <li className="flex items-center text-gray-700">
                  <CheckCircle className="h-5 w-5 text-blue-600 mr-3" />
                  <span>React + TypeScript for type-safe, modern UI</span>
                </li>
                <li className="flex items-center text-gray-700">
                  <CheckCircle className="h-5 w-5 text-blue-600 mr-3" />
                  <span>Tailwind CSS for beautiful, responsive design</span>
                </li>
                <li className="flex items-center text-gray-700">
                  <CheckCircle className="h-5 w-5 text-blue-600 mr-3" />
                  <span>Recharts for interactive data visualization</span>
                </li>
                <li className="flex items-center text-gray-700">
                  <CheckCircle className="h-5 w-5 text-blue-600 mr-3" />
                  <span>Electron for desktop application support</span>
                </li>
              </ul>
            </div>

            <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Backend & AI</h3>
              <ul className="space-y-3">
                <li className="flex items-center text-gray-700">
                  <CheckCircle className="h-5 w-5 text-green-600 mr-3" />
                  <span>FastAPI for high-performance API</span>
                </li>
                <li className="flex items-center text-gray-700">
                  <CheckCircle className="h-5 w-5 text-green-600 mr-3" />
                  <span>OpenAI GPT-4 for intelligent document analysis</span>
                </li>
                <li className="flex items-center text-gray-700">
                  <CheckCircle className="h-5 w-5 text-green-600 mr-3" />
                  <span>LangChain for advanced document processing</span>
                </li>
                <li className="flex items-center text-gray-700">
                  <CheckCircle className="h-5 w-5 text-green-600 mr-3" />
                  <span>SQLAlchemy for robust data management</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Transform Your Loan Trading Process?</h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Start using CrystalTrade today and experience the power of AI-driven loan analysis
          </p>
          <div className="flex justify-center space-x-4">
            <Link
              to="/upload"
              className="inline-flex items-center px-8 py-4 bg-white text-primary-600 rounded-xl font-bold text-lg hover:bg-primary-50 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              <Upload className="h-5 w-5 mr-2" />
              Upload Documents
            </Link>
            <Link
              to="/"
              className="inline-flex items-center px-8 py-4 bg-primary-500 text-white rounded-xl font-bold text-lg hover:bg-primary-400 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 border-2 border-white/30"
            >
              <BarChart3 className="h-5 w-5 mr-2" />
              View Dashboard
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
