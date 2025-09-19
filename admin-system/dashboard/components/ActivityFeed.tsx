'use client'

import { useState, useEffect } from 'react'
import { MessageSquare, Clock, CheckCircle, AlertTriangle, Info } from 'lucide-react'

export default function ActivityFeed () {
  const [activities, setActivities] = useState([
    {
      id: 1,
      message: 'System started successfully',
      timestamp: new Date().toISOString(),
      type: 'success',
      details: 'All core services are running'
    },
    {
      id: 2,
      message: 'Database connected',
      timestamp: new Date(Date.now() - 300000).toISOString(),
      type: 'success',
      details: 'PostgreSQL connection established'
    },
    {
      id: 3,
      message: 'Redis cache initialized',
      timestamp: new Date(Date.now() - 600000).toISOString(),
      type: 'success',
      details: 'Message broker ready for inter-agent communication'
    },
    {
      id: 4,
      message: 'Dashboard launched',
      timestamp: new Date(Date.now() - 900000).toISOString(),
      type: 'info',
      details: 'Web interface accessible at localhost:3000'
    },
  ])

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-600" />
      case 'warning':
        return <AlertTriangle className="h-4 w-4 text-yellow-600" />
      case 'error':
        return <AlertTriangle className="h-4 w-4 text-red-600" />
      default:
        return <Info className="h-4 w-4 text-blue-600" />
    }
  }

  const getActivityBgColor = (type: string) => {
    switch (type) {
      case 'success':
        return 'bg-green-50 border-green-200'
      case 'warning':
        return 'bg-yellow-50 border-yellow-200'
      case 'error':
        return 'bg-red-50 border-red-200'
      default:
        return 'bg-blue-50 border-blue-200'
    }
  }

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)

    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return `${diffHours}h ago`
    return `${Math.floor(diffHours / 24)}d ago`
  }

  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-100/50">
      <div className="p-6 border-b border-gray-200/50 bg-gradient-to-r from-purple-50 to-pink-50 rounded-t-2xl">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-bold text-gray-900">System Activity</h3>
            <p className="text-sm text-gray-600 mt-1">Real-time system events and notifications</p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-xs font-medium text-gray-500">Live</span>
            <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-600 rounded-lg flex items-center justify-center">
              <MessageSquare className="h-4 w-4 text-white" />
            </div>
          </div>
        </div>
      </div>

      <div className="p-6">
        {activities.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <MessageSquare className="h-8 w-8 text-purple-400" />
            </div>
            <h4 className="text-lg font-medium text-gray-900 mb-2">No recent activity</h4>
            <p className="text-gray-600">System events will appear here</p>
          </div>
        ) : (
          <div className="space-y-3">
            {activities.map((activity) => (
              <div
                key={activity.id}
                className={`p-4 rounded-xl border transition-all hover:shadow-md group ${getActivityBgColor(activity.type)}`}
              >
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 mt-0.5">
                    {getActivityIcon(activity.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="text-sm font-semibold text-gray-900 leading-tight">
                          {activity.message}
                        </p>
                        <p className="text-xs text-gray-600 mt-1 leading-relaxed">
                          {activity.details}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center justify-between mt-3">
                      <div className="flex items-center text-xs text-gray-500">
                        <Clock className="h-3 w-3 mr-1" />
                        {formatTime(activity.timestamp)}
                      </div>
                      <div className={`px-2 py-1 text-xs font-medium rounded-full ${activity.type === 'success' ? 'bg-green-100 text-green-700' :
                          activity.type === 'warning' ? 'bg-yellow-100 text-yellow-700' :
                            activity.type === 'error' ? 'bg-red-100 text-red-700' :
                              'bg-blue-100 text-blue-700'
                        }`}>
                        {activity.type}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
