'use client'

import { useState, useEffect } from 'react'
import { Activity, Server, Users, Plus, RefreshCw, BarChart3, Settings, Cpu, HardDrive, Zap, TrendingUp } from 'lucide-react'
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
  const [activeTab, setActiveTab] = useState('overview')
  const [theme, setTheme] = useState<'light' | 'dark'>('light')

  // Load theme from localStorage on component mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('dashboard-theme') as 'light' | 'dark' || 'light'
    setTheme(savedTheme)
  }, [])

  // Save theme to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('dashboard-theme', theme)
  }, [theme])

  useEffect(() => {
    loadDashboardData()
    const interval = setInterval(loadDashboardData, 30000)
    return () => clearInterval(interval)
  }, [])

  const loadDashboardData = async () => {
    try {
      const [projectsResponse, metricsResponse] = await Promise.all([
        fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/projects`),
        fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/system/status`)
      ])

      if (projectsResponse.ok) {
        const projectsData = await projectsResponse.json()
        setProjects(projectsData)
      }

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
        headers: { 'Content-Type': 'application/json' },
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

  const tabs = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'projects', label: 'Projects', icon: Server },
    { id: 'monitoring', label: 'Monitoring', icon: Activity },
    { id: 'settings', label: 'Settings', icon: Settings },
  ]

  if (loading && !systemMetrics) {
    return (
      <div className={`min-h-screen flex items-center justify-center ${theme === 'dark' ? 'bg-gray-900' : 'bg-gray-50'}`}>
        <div className="text-center">
          <div className="relative">
            <div className={`w-16 h-16 border-3 rounded-full animate-spin mx-auto mb-6 ${theme === 'dark' ? 'border-gray-700 border-t-gray-300' : 'border-gray-200 border-t-gray-900'}`}></div>
          </div>
          <h2 className={`text-xl font-semibold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>Loading Dashboard</h2>
          <p className={`${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Initializing Tmux Orchestrator...</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'bg-gray-900' : 'bg-gray-50'}`}>
      {/* Modern Header */}
      <header className={`border-b sticky top-0 z-50 ${theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}`}>
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className={`flex items-center justify-center w-12 h-12 rounded-lg mr-4 transition-colors duration-200 ${theme === 'dark' ? 'bg-gray-100 hover:bg-gray-200' : 'bg-gray-900 hover:bg-gray-800'}`}>
                <Server className={`h-6 w-6 ${theme === 'dark' ? 'text-gray-900' : 'text-white'}`} />
              </div>
              <div>
                <h1 className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                  TMUX ORCHESTRATOR
                </h1>
                <p className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>AI Development Hub</p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <button
                onClick={refreshData}
                disabled={loading}
                className={`p-2 border rounded-lg transition-all duration-200 ${theme === 'dark'
                  ? 'text-gray-300 hover:text-white border-gray-600 hover:bg-gray-700'
                  : 'text-gray-600 hover:text-gray-900 border-gray-300 hover:bg-gray-50'
                  }`}
              >
                <RefreshCw className={`h-5 w-5 ${loading ? 'animate-spin' : ''} transition-transform duration-200`} />
              </button>

              <button
                onClick={() => setShowCreateModal(true)}
                className={`px-4 py-2 rounded-lg font-medium flex items-center space-x-2 transition-all duration-200 ${theme === 'dark'
                  ? 'bg-gray-100 hover:bg-gray-200 text-gray-900'
                  : 'bg-gray-900 hover:bg-gray-800 text-white'
                  }`}
              >
                <Plus className="h-4 w-4" />
                <span>New Project</span>
              </button>
            </div>
          </div>
        </div>
      </header>      {/* Tab Navigation */}
      <div className={`border-b sticky top-16 z-40 ${theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}`}>
        <div className="max-w-7xl mx-auto px-6">
          <nav className="flex space-x-1 py-3">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all ${activeTab === tab.id
                    ? theme === 'dark' ? 'bg-gray-100 text-gray-900' : 'bg-gray-900 text-white'
                    : theme === 'dark' ? 'text-gray-300 hover:text-white hover:bg-gray-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }`}
                >
                  <Icon className="h-5 w-5" />
                  <span>{tab.label}</span>
                </button>
              )
            })}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Modern Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Projects Card */}
              <div className={`rounded-lg p-6 border transition-all duration-200 ${theme === 'dark'
                ? 'bg-gray-800 border-gray-700 hover:shadow-lg hover:shadow-gray-900/20'
                : 'bg-white border-gray-200 hover:shadow-md'
                }`}>
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-2 rounded-lg ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-100'}`}>
                    <Server className={`h-5 w-5 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`} />
                  </div>
                  <div className={`flex items-center text-xs ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                    <TrendingUp className="h-3 w-3 mr-1" />
                    <span>Active</span>
                  </div>
                </div>
                <div>
                  <p className={`text-sm font-medium mb-1 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Total Projects</p>
                  <p className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>{projects.length}</p>
                  <p className={`text-xs mt-2 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>Managed deployments</p>
                </div>
              </div>

              {/* CPU Usage Card */}
              <div className={`rounded-lg p-6 border transition-all duration-200 ${theme === 'dark'
                ? 'bg-gray-800 border-gray-700 hover:shadow-lg hover:shadow-gray-900/20'
                : 'bg-white border-gray-200 hover:shadow-md'
                }`}>
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-2 rounded-lg ${theme === 'dark' ? 'bg-blue-900/20' : 'bg-blue-50'}`}>
                    <Cpu className="h-5 w-5 text-blue-600" />
                  </div>
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                </div>
                <div>
                  <p className={`text-sm font-medium mb-1 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>CPU Usage</p>
                  <p className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>{systemMetrics?.system_cpu_usage?.toFixed(1) || '0.0'}%</p>
                  <div className="mt-3">
                    <div className={`w-full rounded-full h-2 ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`}>
                      <div
                        className="bg-blue-600 h-2 rounded-full transition-all duration-1000"
                        style={{ width: `${systemMetrics?.system_cpu_usage || 0}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Memory Usage Card */}
              <div className={`rounded-lg p-6 border transition-all duration-200 ${theme === 'dark'
                ? 'bg-gray-800 border-gray-700 hover:shadow-lg hover:shadow-gray-900/20'
                : 'bg-white border-gray-200 hover:shadow-md'
                }`}>
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-2 rounded-lg ${theme === 'dark' ? 'bg-green-900/20' : 'bg-green-50'}`}>
                    <HardDrive className="h-5 w-5 text-green-600" />
                  </div>
                  <div className={`flex items-center text-xs ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                    <Zap className="h-3 w-3 mr-1" />
                    <span>Optimal</span>
                  </div>
                </div>
                <div>
                  <p className={`text-sm font-medium mb-1 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Memory Usage</p>
                  <p className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>{systemMetrics?.system_memory_usage?.toFixed(1) || '0.0'}%</p>
                  <div className="mt-3">
                    <div className={`w-full rounded-full h-2 ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-200'}`}>
                      <div
                        className="bg-green-600 h-2 rounded-full transition-all duration-1000"
                        style={{ width: `${systemMetrics?.system_memory_usage || 0}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Active Agents Card */}
              <div className={`rounded-lg p-6 border transition-all duration-200 ${theme === 'dark'
                ? 'bg-gray-800 border-gray-700 hover:shadow-lg hover:shadow-gray-900/20'
                : 'bg-white border-gray-200 hover:shadow-md'
                }`}>
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-2 rounded-lg ${theme === 'dark' ? 'bg-orange-900/20' : 'bg-orange-50'}`}>
                    <Users className="h-5 w-5 text-orange-600" />
                  </div>
                  <div className="flex items-center space-x-1">
                    <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                    <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                  </div>
                </div>
                <div>
                  <p className={`text-sm font-medium mb-1 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Active Agents</p>
                  <p className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>{systemMetrics?.active_agents || 0}</p>
                  <p className={`text-xs mt-2 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>AI orchestrators online</p>
                </div>
              </div>
            </div>

            {/* Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className={`rounded-lg p-6 border ${theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}`}>
                <h3 className={`text-lg font-semibold mb-4 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>System Metrics</h3>
                <SystemMetrics metrics={systemMetrics} />
              </div>
              <div className={`rounded-lg p-6 border ${theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}`}>
                <h3 className={`text-lg font-semibold mb-4 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>Activity Feed</h3>
                <ActivityFeed />
              </div>
            </div>
          </div>
        )}

        {activeTab === 'projects' && (
          <div className={`rounded-lg p-6 border ${theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}`}>
            <div className="flex justify-between items-center mb-6">
              <h2 className={`text-xl font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>Projects</h2>
              <button
                onClick={() => setShowCreateModal(true)}
                className={`px-4 py-2 rounded-lg font-medium flex items-center space-x-2 transition-all duration-200 ${theme === 'dark'
                  ? 'bg-gray-100 hover:bg-gray-200 text-gray-900'
                  : 'bg-gray-900 hover:bg-gray-800 text-white'
                  }`}
              >
                <Plus className="h-4 w-4" />
                <span>New Project</span>
              </button>
            </div>
            <ProjectGrid projects={projects} onProjectUpdate={loadDashboardData} />
          </div>
        )}

        {activeTab === 'monitoring' && (
          <div className="space-y-6">
            <div className={`rounded-lg p-6 border ${theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}`}>
              <h2 className={`text-xl font-semibold mb-6 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>System Monitoring</h2>
              <SystemMetrics metrics={systemMetrics} />
            </div>
            <div className={`rounded-lg p-6 border ${theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}`}>
              <h2 className={`text-xl font-semibold mb-6 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>Activity Log</h2>
              <ActivityFeed />
            </div>
          </div>
        )}

        {activeTab === 'settings' && (
          <div className={`rounded-lg p-6 border ${theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}`}>
            <h2 className={`text-xl font-semibold mb-6 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>Settings</h2>
            <div className="space-y-6">
              <div>
                <h3 className={`text-lg font-medium mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>General Settings</h3>
                <p className={`${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Configure your Tmux Orchestrator instance</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className={`p-4 rounded-lg border ${theme === 'dark' ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
                  <h4 className={`font-medium mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>Auto-refresh</h4>
                  <select className={`rounded-lg px-3 py-2 w-full focus:ring-2 focus:border-transparent ${theme === 'dark'
                    ? 'bg-gray-600 border-gray-500 text-white focus:ring-gray-400'
                    : 'bg-white border-gray-300 text-gray-900 focus:ring-gray-500'
                    }`}>
                    <option value="30">30 seconds</option>
                    <option value="60">1 minute</option>
                    <option value="300">5 minutes</option>
                  </select>
                </div>
                <div className={`p-4 rounded-lg border ${theme === 'dark' ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'}`}>
                  <h4 className={`font-medium mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>Theme</h4>
                  <select
                    value={theme}
                    onChange={(e) => setTheme(e.target.value as 'light' | 'dark')}
                    className={`rounded-lg px-3 py-2 w-full focus:ring-2 focus:border-transparent ${theme === 'dark'
                      ? 'bg-gray-600 border-gray-500 text-white focus:ring-gray-400'
                      : 'bg-white border-gray-300 text-gray-900 focus:ring-gray-500'
                      }`}
                  >
                    <option value="light">Light Mode</option>
                    <option value="dark">Dark Mode</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        )}
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
