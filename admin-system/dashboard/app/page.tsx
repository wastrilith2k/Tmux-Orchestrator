'use client'

import { useState, useEffect } from 'react'
import { Activity, Server, Users, MessageSquare, Plus, RefreshCw } from 'lucide-react'
import ProjectGrid from '../components/ProjectGrid'
import SystemMetrics from '../components/SystemMetrics'
import ActivityFeed from '../components/ActivityFeed'
import CreateProjectModal from '../components/CreateProjectModal'
import { Project, SystemMetrics as ISystemMetrics } from '../types'
import { toast } from 'react-hot-toast'

export default function Dashboard () {
  const [projects, setProjects] = useState<Project[]>([])
  const [systemMetrics, setSystemMetrics] = useState<ISystemMetrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)

  useEffect(() => {
    loadDashboardData()

    // Refresh data every 30 seconds
    const interval = setInterval(loadDashboardData, 30000)

    return () => clearInterval(interval)
  }, [])

  const loadDashboardData = async () => {
    try {
      // Load projects
      const projectsResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/projects`)
      if (projectsResponse.ok) {
        const projectsData = await projectsResponse.json()
        setProjects(projectsData)
      }

      // Load system metrics
      const metricsResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/system/status`)
      if (metricsResponse.ok) {
        const metricsData = await metricsResponse.json()
        setSystemMetrics(metricsData)
      }
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
      toast.error('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateProject = async (projectData: any) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/projects`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(projectData),
      })

      if (response.ok) {
        const newProject = await response.json()
        setProjects(prev => [newProject, ...prev])
        setShowCreateModal(false)
        toast.success('Project created successfully!')
      } else {
        const error = await response.json()
        toast.error(`Failed to create project: ${error.detail}`)
      }
    } catch (error) {
      console.error('Failed to create project:', error)
      toast.error('Failed to create project')
    }
  }

  const refreshData = () => {
    setLoading(true)
    loadDashboardData()
  }

  if (loading && !systemMetrics) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Server className="h-8 w-8 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">
                Tmux Orchestrator Hub
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={refreshData}
                disabled={loading}
                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              >
                <RefreshCw className={`h-5 w-5 ${loading ? 'animate-spin' : ''}`} />
              </button>
              <button
                onClick={() => setShowCreateModal(true)}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors flex items-center"
              >
                <Plus className="h-4 w-4 mr-2" />
                New Project
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* System Metrics Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Server className="h-8 w-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Projects</p>
                <p className="text-2xl font-bold text-gray-900">
                  {systemMetrics?.total_projects || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Activity className="h-8 w-8 text-green-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Projects</p>
                <p className="text-2xl font-bold text-gray-900">
                  {systemMetrics?.active_projects || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Users className="h-8 w-8 text-purple-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Agents</p>
                <p className="text-2xl font-bold text-gray-900">
                  {systemMetrics?.active_agents || 0}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <MessageSquare className="h-8 w-8 text-yellow-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Messages Today</p>
                <p className="text-2xl font-bold text-gray-900">
                  {systemMetrics?.total_messages_today || 0}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Projects Grid */}
          <div className="lg:col-span-2">
            <ProjectGrid
              projects={projects}
              onProjectUpdate={loadDashboardData}
            />
          </div>

          {/* Right Sidebar */}
          <div className="space-y-8">
            {systemMetrics && (
              <SystemMetrics metrics={systemMetrics} />
            )}
            <ActivityFeed />
          </div>
        </div>
      </main>

      {/* Create Project Modal */}
      {showCreateModal && (
        <CreateProjectModal
          onClose={() => setShowCreateModal(false)}
          onSubmit={handleCreateProject}
        />
      )}
    </div>
  )
}