import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { ErrorBoundary } from './components/ErrorBoundary'
import Dashboard from './pages/Dashboard'
import DocumentUpload from './pages/DocumentUpload'
import AnalysisView from './pages/AnalysisView'
import Reports from './pages/Reports'
import Layout from './components/Layout'

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<DocumentUpload />} />
            <Route path="/analysis/:id" element={<AnalysisView />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
          <Toaster position="top-right" />
        </Layout>
      </Router>
    </ErrorBoundary>
  )
}

export default App

