'use client'

import { useState } from 'react'
import { Server, Activity, AlertCircle, Clock, Play, Square, Trash2 } from 'lucide-react'
import { Project } from '../types'
import { formatDistanceToNow } from 'date-fns'

interface ProjectGridProps {
  projects: Project[]
  onProjectUpdate: () => void
}

export default function ProjectGrid ({ projects, onProjectUpdate }: ProjectGridProps) {
  const [loadingActions, setLoadingActions] = useState<Set<string>>(new Set())

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return <Activity className="h-5 w-5 text-green-600" />
      case 'stopped':
        return <Server className="h-5 w-5 text-gray-400" />
      case 'error':
        return <AlertCircle className="h-5 w-5 text-red-600" />
      case 'starting':
      case 'stopping':
        return <Clock className="h-5 w-5 text-yellow-600" />
      default:
        return <Server className="h-5 w-5 text-gray-400" />
    }
  }

  const getStatusBadge = (status: string) => {
    const baseClasses = "px-2 py-1 rounded-full text-xs font-medium"
    switch (status) {
      case 'running':
        return `${baseClasses} bg-green-100 text-green-800`
      case 'stopped':
        return `${baseClasses} bg-gray-100 text-gray-800`
      case 'error':
        return `${baseClasses} bg-red-100 text-red-800`
      case 'starting':
      case 'stopping':
        return `${baseClasses} bg-yellow-100 text-yellow-800`
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`
    }
  }

  const handleProjectAction = async (projectId: string, action: string) => {
    setLoadingActions(prev => new Set(prev).add(projectId))

    try {
      const endpoint = action === 'delete'
        ? `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/projects/${projectId}`
        : `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/projects/${projectId}/${action}`

      const method = action === 'delete' ? 'DELETE' : 'POST'

      const response = await fetch(endpoint, { method })

      if (response.ok) {
        onProjectUpdate()
      } else {
        console.error(`Failed to ${action} project`)
      }
    } catch (error) {
      console.error(`Error ${action} project:`, error)
    } finally {
      setLoadingActions(prev => {
        const newSet = new Set(prev)
        newSet.delete(projectId)
        return newSet
      })
    }
  }

  if (projects.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 text-center">
          <Server className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Projects Yet</h3>
          <p className="text-gray-600 mb-4">Create your first project to get started with the orchestrator.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Projects</h2>
        <p className="text-sm text-gray-600">Manage your orchestrator projects</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-6">
        {projects.map((project) => (
          <div
            key={project.id}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center">
                {getStatusIcon(project.status)}
                <h3 className="ml-2 font-medium text-gray-900 truncate">
                  {project.name}
                </h3>
              </div>
              <span className={getStatusBadge(project.status)}>
                {project.status}
              </span>
            </div>

            <div className="space-y-2 text-sm text-gray-600 mb-4">
              <div>
                <span className="font-medium">Type:</span> {project.project_type}
              </div>
              <div>
                <span className="font-medium">Resources:</span> {project.cpu_limit} CPU, {project.memory_limit}
              </div>
              <div>
                <span className="font-medium">Created:</span>{' '}
                {formatDistanceToNow(new Date(project.created_at), { addSuffix: true })}
              </div>
              {project.last_heartbeat && (
                <div>
                  <span className="font-medium">Last seen:</span>{' '}
                  {formatDistanceToNow(new Date(project.last_heartbeat), { addSuffix: true })}
                </div>
              )}
            </div>

            <div className="flex justify-end space-x-2">
              {project.status === 'stopped' && (
                <button
                  onClick={() => handleProjectAction(project.project_id, 'start')}
                  disabled={loadingActions.has(project.project_id)}
                  className="p-2 text-green-600 hover:bg-green-50 rounded-md transition-colors disabled:opacity-50"
                  title="Start Project"
                >
                  <Play className="h-4 w-4" />
                </button>
              )}

              {project.status === 'running' && (
                <button
                  onClick={() => handleProjectAction(project.project_id, 'stop')}
                  disabled={loadingActions.has(project.project_id)}
                  className="p-2 text-yellow-600 hover:bg-yellow-50 rounded-md transition-colors disabled:opacity-50"
                  title="Stop Project"
                >
                  <Square className="h-4 w-4" />
                </button>
              )}

              <button
                onClick={() => {
                  if (confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
                    handleProjectAction(project.project_id, 'delete')
                  }
                }}
                disabled={loadingActions.has(project.project_id)}
                className="p-2 text-red-600 hover:bg-red-50 rounded-md transition-colors disabled:opacity-50"
                title="Delete Project"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}