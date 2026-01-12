import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { LogIn, Mail, Lock, Eye, EyeOff, ArrowRight, Shield } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import toast from 'react-hot-toast'
import AnimatedLogo from '../components/AnimatedLogo'

export default function Login() {
  const navigate = useNavigate()
  const { login, isAuthenticated } = useAuth()
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/')
    }
  }, [isAuthenticated, navigate])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      // Show loading message
      const loadingToast = toast.loading('Signing in...')
      
      await login(formData.username, formData.password)
      
      toast.dismiss(loadingToast)
      toast.success(`Welcome back, ${formData.username}!`)
      navigate('/')
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || error.message || 'Login failed. Please check your credentials.'
      toast.error(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col" style={{
      background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%)',
      backgroundAttachment: 'fixed'
    }}>
      {/* Header */}
      <header className="glass-nav border-b border-white/20 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <div className="flex items-center">
              <AnimatedLogo size="md" showText={false} />
              <div className="ml-3">
                <div className="text-2xl font-bold gradient-text">CrystalTrade</div>
                <div className="text-xs text-gray-600 font-medium -mt-1">Transparent Loan Trading</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
        {/* Logo and Header */}
        <div className="text-center mb-8 fade-in">
          <div className="flex justify-center mb-4">
            <AnimatedLogo size="lg" showText={false} />
          </div>
          <h1 className="text-4xl font-bold gradient-text mb-2">CrystalTrade</h1>
          <p className="text-gray-600 font-medium">Transparent Loan Trading</p>
        </div>

        {/* Login Card */}
        <div className="glass-panel rounded-3xl p-8 shadow-2xl fade-in">
          <div className="flex items-center mb-6">
            <div className="p-3 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 mr-3">
              <LogIn className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Welcome Back</h2>
          </div>
          <p className="text-gray-600 mb-8">Sign in to your account to continue</p>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Username/Email Field */}
            <div>
              <label htmlFor="username" className="block text-sm font-bold text-gray-700 mb-2">
                Username or Email
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="username"
                  type="text"
                  required
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="glass-input w-full pl-12 pr-4 py-3 rounded-xl border-2 border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 transition-all"
                  placeholder="Enter your username or email"
                />
              </div>
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-bold text-gray-700 mb-2">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="glass-input w-full pl-12 pr-12 py-3 rounded-xl border-2 border-gray-200 focus:border-primary-500 focus:ring-2 focus:ring-primary-200 transition-all"
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
                >
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="btn-gradient w-full py-4 rounded-xl font-bold text-white shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-300 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Signing in...</span>
                </>
              ) : (
                <>
                  <span>Sign In</span>
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </form>

          {/* Sign Up Link */}
          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Don't have an account?{' '}
              <Link to="/signup" className="text-primary-600 font-bold hover:text-primary-700 transition-colors">
                Sign up
              </Link>
            </p>
          </div>
        </div>

        {/* Demo Credentials */}
        <div className="mt-6 glass-strong rounded-xl p-4 border-2 border-primary-200 bg-gradient-to-br from-primary-50 to-blue-50">
          <div className="text-xs font-bold text-primary-900 uppercase tracking-wide mb-2">Demo Credentials</div>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-700 font-medium">Username:</span>
              <span className="text-gray-900 font-bold">demo</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-700 font-medium">Password:</span>
              <span className="text-gray-900 font-bold">demo123</span>
            </div>
          </div>
        </div>
      </div>
      </div>

      {/* Footer */}
      <footer className="glass-nav border-t border-white/20 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 text-sm text-gray-600 mb-4 sm:mb-0">
              <Shield className="h-4 w-4" />
              <span>Secure & Compliant</span>
              <span className="mx-2">•</span>
              <span>LMA Standards</span>
            </div>
            <div className="text-sm text-gray-600">
              © {new Date().getFullYear()} CrystalTrade. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
