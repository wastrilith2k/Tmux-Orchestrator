'use client'

import { useState } from 'react'
import { X, Folder, Code, Server, CheckCircle, ArrowRight, ArrowLeft, GitBranch, Settings, Zap } from 'lucide-react'
import { ProjectCreateData } from '../types'

interface CreateProjectModalProps {
  onClose: () => void
  onSubmit: (data: ProjectCreateData) => void
}

export default function CreateProjectModal ({ onClose, onSubmit }: CreateProjectModalProps) {
  const [currentStep, setCurrentStep] = useState(1)
  const [formData, setFormData] = useState<ProjectCreateData>({
    name: '',
    description: '',
    project_type: 'auto-detect',
    project_path: '',
    cpu_limit: 2.0,
    memory_limit: '4Gi',
    auto_start: true,
    auto_scale: false,
  })

  const steps = [
    {
      id: 1,
      title: 'Project Details',
      description: 'Basic information about your project',
      icon: Folder
    },
    {
      id: 2,
      title: 'Configuration',
      description: 'Resource limits and preferences',
      icon: Settings
    },
    {
      id: 3,
      title: 'Review & Launch',
      description: 'Confirm settings and create project',
      icon: Zap
    },
  ]

  const projectTypes = [
    { value: 'auto-detect', label: 'Auto Detect', icon: '🤖', description: 'Automatically detect project type' },
    { value: 'nodejs', label: 'Node.js', icon: '🟢', description: 'JavaScript/TypeScript applications' },
    { value: 'python', label: 'Python', icon: '🐍', description: 'Python applications and scripts' },
    { value: 'go', label: 'Go', icon: '🔵', description: 'Go applications and services' },
    { value: 'rust', label: 'Rust', icon: '🦀', description: 'Rust systems programming' },
    { value: 'java', label: 'Java', icon: '☕', description: 'Java applications and Spring' },
    { value: 'react', label: 'React', icon: '⚛️', description: 'React web applications' },
    { value: 'nextjs', label: 'Next.js', icon: '▲', description: 'Next.js full-stack applications' },
  ]

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const isStepValid = () => {
    switch (currentStep) {
      case 1:
        return formData.name.trim() !== '' && formData.project_path.trim() !== ''
      case 2:
        return formData.cpu_limit > 0
      case 3:
        return true
      default:
        return false
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-t-2xl">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Create New Project</h2>
            <p className="text-gray-600 mt-1">Set up a new autonomous development project</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors p-2 hover:bg-white rounded-lg"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Step Progress */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="flex items-center justify-between">
            {steps.map((step, index) => {
              const Icon = step.icon
              return (
                <div key={step.id} className="flex items-center">
                  <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all ${currentStep >= step.id
                      ? 'bg-blue-600 border-blue-600 text-white'
                      : 'bg-white border-gray-300 text-gray-400'
                    }`}>
                    {currentStep > step.id ? (
                      <CheckCircle className="h-5 w-5" />
                    ) : (
                      <Icon className="h-5 w-5" />
                    )}
                  </div>
                  <div className="ml-3">
                    <p className={`text-sm font-medium ${currentStep >= step.id ? 'text-gray-900' : 'text-gray-500'
                      }`}>
                      {step.title}
                    </p>
                    <p className="text-xs text-gray-500">{step.description}</p>
                  </div>
                  {index < steps.length - 1 && (
                    <ArrowRight className="h-4 w-4 text-gray-300 mx-6" />
                  )}
                </div>
              )
            })}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="p-6">
          {/* Step 1: Project Details */}
          {currentStep === 1 && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Project Name *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-lg"
                  placeholder="My awesome project"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Description
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  rows={3}
                  placeholder="Describe what your project does..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Project Path *
                </label>
                <div className="relative">
                  <Folder className="absolute left-4 top-4 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    required
                    value={formData.project_path}
                    onChange={(e) => setFormData(prev => ({ ...prev, project_path: e.target.value }))}
                    className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="/path/to/your/project"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Project Type
                </label>
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
                  {projectTypes.map((type) => (
                    <button
                      key={type.value}
                      type="button"
                      onClick={() => setFormData(prev => ({ ...prev, project_type: type.value }))}
                      className={`p-4 border rounded-xl text-left transition-all hover:shadow-md ${formData.project_type === type.value
                          ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                          : 'border-gray-200 hover:border-gray-300'
                        }`}
                    >
                      <div className="text-2xl mb-2">{type.icon}</div>
                      <h3 className="font-medium text-gray-900 text-sm">{type.label}</h3>
                      <p className="text-xs text-gray-500 mt-1">{type.description}</p>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Configuration */}
          {currentStep === 2 && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    CPU Limit (cores)
                  </label>
                  <div className="relative">
                    <input
                      type="number"
                      min="0.1"
                      max="32"
                      step="0.1"
                      value={formData.cpu_limit}
                      onChange={(e) => setFormData(prev => ({ ...prev, cpu_limit: parseFloat(e.target.value) }))}
                      className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    />
                    <div className="mt-2 text-xs text-gray-500">
                      Recommended: 2-4 cores for most projects
                    </div>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Memory Limit
                  </label>
                  <select
                    value={formData.memory_limit}
                    onChange={(e) => setFormData(prev => ({ ...prev, memory_limit: e.target.value }))}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  >
                    <option value="1Gi">1 GB</option>
                    <option value="2Gi">2 GB</option>
                    <option value="4Gi">4 GB</option>
                    <option value="8Gi">8 GB</option>
                    <option value="16Gi">16 GB</option>
                    <option value="32Gi">32 GB</option>
                  </select>
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900">Project Options</h3>

                <div className="space-y-3">
                  <label className="flex items-start p-4 border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.auto_start}
                      onChange={(e) => setFormData(prev => ({ ...prev, auto_start: e.target.checked }))}
                      className="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded mt-0.5"
                    />
                    <div className="ml-3">
                      <span className="text-sm font-medium text-gray-900">Auto-start project</span>
                      <p className="text-xs text-gray-500 mt-1">Automatically start the project after creation</p>
                    </div>
                  </label>

                  <label className="flex items-start p-4 border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.auto_scale}
                      onChange={(e) => setFormData(prev => ({ ...prev, auto_scale: e.target.checked }))}
                      className="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded mt-0.5"
                    />
                    <div className="ml-3">
                      <span className="text-sm font-medium text-gray-900">Enable auto-scaling</span>
                      <p className="text-xs text-gray-500 mt-1">Automatically adjust resources based on load</p>
                    </div>
                  </label>
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Review */}
          {currentStep === 3 && (
            <div className="space-y-6">
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Review Your Project</h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-3">
                    <div>
                      <label className="text-sm font-medium text-gray-600">Project Name</label>
                      <p className="text-gray-900 font-medium">{formData.name}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-600">Type</label>
                      <p className="text-gray-900">{projectTypes.find(t => t.value === formData.project_type)?.label}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-600">Path</label>
                      <p className="text-gray-900 font-mono text-sm">{formData.project_path}</p>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <label className="text-sm font-medium text-gray-600">Resources</label>
                      <p className="text-gray-900">{formData.cpu_limit} CPU, {formData.memory_limit} RAM</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-600">Options</label>
                      <div className="space-y-1">
                        {formData.auto_start && <p className="text-sm text-green-600">✓ Auto-start enabled</p>}
                        {formData.auto_scale && <p className="text-sm text-green-600">✓ Auto-scaling enabled</p>}
                      </div>
                    </div>
                  </div>
                </div>

                {formData.description && (
                  <div className="mt-4">
                    <label className="text-sm font-medium text-gray-600">Description</label>
                    <p className="text-gray-900">{formData.description}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Footer */}
          <div className="flex justify-between items-center pt-6 border-t border-gray-200 mt-8">
            <button
              type="button"
              onClick={currentStep === 1 ? onClose : handlePrevious}
              className="px-6 py-3 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-xl transition-colors flex items-center"
            >
              {currentStep === 1 ? (
                <>
                  <X className="h-4 w-4 mr-2" />
                  Cancel
                </>
              ) : (
                <>
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Previous
                </>
              )}
            </button>

            {currentStep < 3 ? (
              <button
                type="button"
                onClick={handleNext}
                disabled={!isStepValid()}
                className="px-6 py-3 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center shadow-lg hover:shadow-xl"
              >
                Next
                <ArrowRight className="h-4 w-4 ml-2" />
              </button>
            ) : (
              <button
                type="submit"
                className="px-6 py-3 text-sm font-medium text-white bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 rounded-xl transition-all flex items-center shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                <Zap className="h-4 w-4 mr-2" />
                Create Project
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  )
}