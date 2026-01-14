import { Link, useLocation, useNavigate } from 'react-router-dom'
import { FileText, Upload, BarChart3, FileCheck, HelpCircle, Settings, Bell, Shield, Github, Linkedin, Mail, LogOut, User } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import toast from 'react-hot-toast'
import AnimatedLogo from './AnimatedLogo'

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuth()

  const navItems = [
    { path: '/', icon: BarChart3, label: 'Dashboard' },
    { path: '/upload', icon: Upload, label: 'Upload Documents' },
    { path: '/reports', icon: FileCheck, label: 'Reports' },
    { path: '/about', icon: HelpCircle, label: 'About' },
  ]

  const currentYear = new Date().getFullYear()

  const handleLogout = () => {
    logout()
    toast.success('Logged out successfully')
    navigate('/login')
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Enhanced Header */}
      <header className="glass-nav sticky top-0 z-50 border-b border-white/20 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Logo and Branding */}
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <AnimatedLogo size="md" showText={false} />
                <div className="ml-3">
                  <div className="text-2xl font-bold gradient-text">
                    CrystalTrade
                  </div>
                  <div className="text-xs text-gray-600 font-medium -mt-1">
                    Transparent Loan Trading
                  </div>
                </div>
              </div>
              
              {/* Navigation Links */}
              <div className="hidden md:ml-8 md:flex md:space-x-2">
                {navItems.map((item) => {
                  const Icon = item.icon
                  const isActive = location.pathname === item.path
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      className={`inline-flex items-center px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300 smooth-transition ${
                        isActive
                          ? 'bg-gradient-to-r from-primary-500 to-primary-700 text-white shadow-lg scale-105'
                          : 'text-gray-700 hover:bg-white/80 hover:text-primary-600 hover:scale-105'
                      }`}
                    >
                      <Icon className={`h-5 w-5 mr-2 ${isActive ? 'icon-glow' : ''}`} />
                      {item.label}
                    </Link>
                  )
                })}
              </div>
            </div>

            {/* Right Side Actions */}
            <div className="flex items-center space-x-3">
              <button className="hidden sm:flex items-center justify-center w-10 h-10 rounded-xl text-gray-600 hover:bg-white/80 hover:text-primary-600 transition-all duration-300 smooth-transition">
                <Bell className="h-5 w-5" />
              </button>
              <button className="hidden sm:flex items-center justify-center w-10 h-10 rounded-xl text-gray-600 hover:bg-white/80 hover:text-primary-600 transition-all duration-300 smooth-transition">
                <HelpCircle className="h-5 w-5" />
              </button>
              <button className="hidden sm:flex items-center justify-center w-10 h-10 rounded-xl text-gray-600 hover:bg-white/80 hover:text-primary-600 transition-all duration-300 smooth-transition">
                <Settings className="h-5 w-5" />
              </button>
              <div className="hidden sm:flex items-center ml-2 pl-4 border-l border-gray-300 space-x-3">
                <div className="flex items-center space-x-2">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center text-white font-bold text-sm shadow-lg">
                    {user?.username?.charAt(0).toUpperCase() || 'U'}
                  </div>
                  <div className="hidden lg:block">
                    <div className="text-sm font-semibold text-gray-900">{user?.username || 'User'}</div>
                    <div className="text-xs text-gray-600">{user?.is_admin ? 'Admin' : 'User'}</div>
                  </div>
                </div>
                <button
                  onClick={handleLogout}
                  className="p-2 rounded-xl text-gray-600 hover:bg-white/80 hover:text-red-600 transition-all duration-300 smooth-transition"
                  title="Logout"
                >
                  <LogOut className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full py-8 px-4 sm:px-6 lg:px-8">
        {children}
      </main>

      {/* Enhanced Footer */}
      <footer className="glass-nav border-t border-white/20 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            {/* Brand Column */}
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center mb-4">
                <AnimatedLogo size="sm" showText={false} />
                <div className="ml-2">
                  <div className="text-xl font-bold gradient-text">
                    CrystalTrade
                  </div>
                  <div className="text-xs text-gray-600">
                    Transparent Loan Trading
                  </div>
                </div>
              </div>
              <p className="text-sm text-gray-600 mb-4 max-w-md">
                Automating due diligence checks for secondary loan market transactions. 
                Bringing crystal-clear transparency to loan trading with AI-powered analysis.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="w-10 h-10 rounded-xl bg-white/80 flex items-center justify-center text-gray-600 hover:bg-primary-600 hover:text-white transition-all duration-300 smooth-transition">
                  <Github className="h-5 w-5" />
                </a>
                <a href="#" className="w-10 h-10 rounded-xl bg-white/80 flex items-center justify-center text-gray-600 hover:bg-primary-600 hover:text-white transition-all duration-300 smooth-transition">
                  <Linkedin className="h-5 w-5" />
                </a>
                <a href="#" className="w-10 h-10 rounded-xl bg-white/80 flex items-center justify-center text-gray-600 hover:bg-primary-600 hover:text-white transition-all duration-300 smooth-transition">
                  <Mail className="h-5 w-5" />
                </a>
              </div>
            </div>

            {/* Quick Links */}
            <div>
              <h3 className="text-sm font-bold text-gray-900 mb-4 uppercase tracking-wide">Quick Links</h3>
              <ul className="space-y-2">
                <li>
                  <Link to="/" className="text-sm text-gray-600 hover:text-primary-600 transition-colors">
                    Dashboard
                  </Link>
                </li>
                <li>
                  <Link to="/upload" className="text-sm text-gray-600 hover:text-primary-600 transition-colors">
                    Upload Documents
                  </Link>
                </li>
                <li>
                  <Link to="/reports" className="text-sm text-gray-600 hover:text-primary-600 transition-colors">
                    Reports
                  </Link>
                </li>
                <li>
                  <a href="#" className="text-sm text-gray-600 hover:text-primary-600 transition-colors">
                    Documentation
                  </a>
                </li>
              </ul>
            </div>

            {/* Support */}
            <div>
              <h3 className="text-sm font-bold text-gray-900 mb-4 uppercase tracking-wide">Support</h3>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="text-sm text-gray-600 hover:text-primary-600 transition-colors">
                    Help Center
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-gray-600 hover:text-primary-600 transition-colors">
                    Contact Us
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-gray-600 hover:text-primary-600 transition-colors">
                    Privacy Policy
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-gray-600 hover:text-primary-600 transition-colors">
                    Terms of Service
                  </a>
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="border-t border-gray-200 pt-6 mt-6">
            <div className="flex flex-col sm:flex-row justify-between items-center">
              <div className="flex items-center space-x-2 text-sm text-gray-600 mb-4 sm:mb-0">
                <Shield className="h-4 w-4" />
                <span>Secure & Compliant</span>
                <span className="mx-2">•</span>
                <span>LMA Standards</span>
              </div>
              <div className="text-sm text-gray-600">
                © {currentYear} CrystalTrade. All rights reserved.
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

