import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, X, CheckCircle } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { api } from '../services/api'

interface UploadedFile {
  file: File
  id: string
  status: 'pending' | 'uploading' | 'processing' | 'completed' | 'error'
  progress: number
  analysisId?: string
}

export default function DocumentUpload() {
  const [files, setFiles] = useState<UploadedFile[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const navigate = useNavigate()

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles: UploadedFile[] = acceptedFiles.map((file) => ({
      file,
      id: Math.random().toString(36).substr(2, 9),
      status: 'pending',
      progress: 0,
    }))
    setFiles((prev) => [...prev, ...newFiles])
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': [
        '.docx',
      ],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': [
        '.xlsx',
      ],
    },
    multiple: true,
  })

  const removeFile = (id: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== id))
  }

  const uploadFiles = async () => {
    if (files.length === 0) {
      toast.error('Please select at least one file')
      return
    }

    setIsUploading(true)

    for (const fileItem of files) {
      if (fileItem.status === 'completed') continue

      try {
        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileItem.id ? { ...f, status: 'uploading', progress: 10 } : f
          )
        )

        const formData = new FormData()
        formData.append('file', fileItem.file)
        formData.append('loan_name', fileItem.file.name.replace(/\.[^/.]+$/, ''))

        const response = await api.uploadDocument(formData, (progress) => {
          setFiles((prev) =>
            prev.map((f) =>
              f.id === fileItem.id ? { ...f, progress } : f
            )
          )
        })

        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileItem.id
              ? {
                  ...f,
                  status: 'processing',
                  progress: 80,
                  analysisId: response.analysis_id,
                }
              : f
          )
        )

        // Start analysis
        await api.startAnalysis(response.analysis_id)

        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileItem.id
              ? { ...f, status: 'completed', progress: 100 }
              : f
          )
        )

        toast.success(`Analysis started for ${fileItem.file.name}`)
      } catch (error: any) {
        console.error('Upload error:', error)
        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileItem.id ? { ...f, status: 'error' } : f
          )
        )
        toast.error(`Failed to upload ${fileItem.file.name}: ${error.message}`)
      }
    }

    setIsUploading(false)
  }

  const viewAnalysis = (analysisId: string) => {
    navigate(`/analysis/${analysisId}`)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold gradient-text">Upload Documents</h1>
        <p className="mt-2 text-sm text-gray-600">
          Upload loan documents for AI-powered due diligence analysis
        </p>
      </div>

      <div
        {...getRootProps()}
        className={`glass-card border-2 border-dashed rounded-2xl p-16 text-center cursor-pointer transition-all duration-300 smooth-transition ${
          isDragActive
            ? 'border-primary-400 bg-gradient-to-br from-primary-50 to-primary-100 scale-105 shadow-xl'
            : 'border-gray-300 hover:border-primary-400 hover:scale-[1.02] hover:shadow-xl'
        }`}
      >
        <input {...getInputProps()} />
        <div className={`mx-auto w-20 h-20 rounded-2xl flex items-center justify-center mb-6 transition-all duration-300 ${
          isDragActive 
            ? 'bg-gradient-to-br from-primary-500 to-primary-600 shadow-lg scale-110' 
            : 'bg-gradient-to-br from-primary-100 to-primary-200'
        }`}>
          <Upload className={`h-10 w-10 transition-all duration-300 ${
            isDragActive ? 'text-white icon-glow' : 'text-primary-600'
          }`} />
        </div>
        <div className="mt-4">
          <p className="text-xl font-bold text-gray-900 mb-2">
            {isDragActive
              ? 'Drop files here'
              : 'Drag and drop files here, or click to select'}
          </p>
          <p className="text-sm text-gray-600 font-medium">
            Supports PDF, Word, and Excel documents
          </p>
        </div>
      </div>

      {files.length > 0 && (
        <div className="glass-panel rounded-xl overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">
              Selected Files ({files.length})
            </h3>
          </div>
          <div className="p-6 space-y-4">
            {files.map((fileItem) => (
              <div
                key={fileItem.id}
                className="flex items-center justify-between p-4 glass-strong rounded-lg border border-gray-200"
              >
                <div className="flex items-center flex-1">
                  <FileText className="h-8 w-8 text-gray-600 mr-4" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">
                      {fileItem.file.name}
                    </p>
                    <p className="text-xs text-gray-600">
                      {(fileItem.file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                    {fileItem.status !== 'pending' && (
                      <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all ${
                            fileItem.status === 'error'
                              ? 'bg-red-500'
                              : fileItem.status === 'completed'
                              ? 'bg-green-500'
                              : 'bg-primary-500'
                          }`}
                          style={{ width: `${fileItem.progress}%` }}
                        />
                      </div>
                    )}
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  {fileItem.status === 'completed' && fileItem.analysisId && (
                    <button
                      onClick={() => viewAnalysis(fileItem.analysisId!)}
                      className="text-primary-600 hover:text-primary-800 text-sm font-medium transition-colors"
                    >
                      View Analysis →
                    </button>
                  )}
                  {fileItem.status === 'pending' && (
                    <button
                      onClick={() => removeFile(fileItem.id)}
                      className="text-red-600 hover:text-red-800 transition-colors"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  )}
                  {fileItem.status === 'completed' && (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  )}
                </div>
              </div>
            ))}
          </div>
          <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
            <button
              onClick={uploadFiles}
              disabled={isUploading || files.every((f) => f.status === 'completed')}
              className="w-full btn-gradient text-white px-4 py-3 rounded-lg disabled:bg-gray-300 disabled:cursor-not-allowed font-semibold"
            >
              {isUploading ? 'Uploading...' : 'Upload and Analyze'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}


