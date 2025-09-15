'use client'

import { useState } from 'react'
import { X, Folder, Code, Server } from 'lucide-react'
import { ProjectCreateData } from '../types'

interface CreateProjectModalProps {
  onClose: () => void
  onSubmit: (data: ProjectCreateData) => void
}

export default function CreateProjectModal ({ onClose, onSubmit }: CreateProjectModalProps) {
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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const projectTypes = [
    { value: 'auto-detect', label: 'Auto Detect', icon: Code },
    { value: 'nodejs', label: 'Node.js', icon: Server },
    { value: 'python', label: 'Python', icon: Code },
    { value: 'go', label: 'Go', icon: Code },
    { value: 'rust', label: 'Rust', icon: Code },
    { value: 'java', label: 'Java', icon: Code },
  ]

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Create New Project</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Project Name *
              </label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="My awesome project"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Project Type
              </label>
              <select
                value={formData.project_type}
                onChange={(e) => setFormData(prev => ({ ...prev, project_type: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {projectTypes.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Project Path *
            </label>
            <div className="relative">
              <Folder className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <input
                type="text"
                required
                value={formData.project_path}
                onChange={(e) => setFormData(prev => ({ ...prev, project_path: e.target.value }))}
                className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="/path/to/your/project"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={3}
              placeholder="Optional description of your project"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                CPU Limit (cores)
              </label>
              <input
                type="number"
                min="0.1"
                max="32"
                step="0.1"
                value={formData.cpu_limit}
                onChange={(e) => setFormData(prev => ({ ...prev, cpu_limit: parseFloat(e.target.value) }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Memory Limit
              </label>
              <select
                value={formData.memory_limit}
                onChange={(e) => setFormData(prev => ({ ...prev, memory_limit: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="2Gi">2 GB</option>
                <option value="4Gi">4 GB</option>
                <option value="8Gi">8 GB</option>
                <option value="16Gi">16 GB</option>
              </select>
            </div>
          </div>

          <div className="flex items-center space-x-6">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={formData.auto_start}
                onChange={(e) => setFormData(prev => ({ ...prev, auto_start: e.target.checked }))}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span className="ml-2 text-sm text-gray-700">Auto-start project</span>
            </label>

            <label className="flex items-center">
              <input
                type="checkbox"
                checked={formData.auto_scale}
                onChange={(e) => setFormData(prev => ({ ...prev, auto_scale: e.target.checked }))}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span className="ml-2 text-sm text-gray-700">Enable auto-scaling</span>
            </label>
          </div>

          <div className="flex justify-end space-x-4 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md transition-colors"
            >
              Create Project
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}