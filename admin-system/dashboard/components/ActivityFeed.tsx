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
    <div className="bg-white rounded-xl shadow-lg border border-gray-100">
      <div className="p-6 border-b border-gray-200 bg-gradient-to-r from-purple-50 to-pink-50 rounded-t-xl">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Recent Activity</h2>
            <p className="text-sm text-gray-600 mt-1">System events and notifications</p>
          </div>
          <MessageSquare className="h-6 w-6 text-purple-600" />
        </div>
      </div>

      <div className="p-6">
        {activities.length === 0 ? (
          <div className="text-center py-8">
            <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No recent activity</p>
          </div>
        ) : (
          <div className="space-y-4">
            {activities.map((activity) => (
              <div
                key={activity.id}
                className={`p-4 rounded-lg border transition-all hover:shadow-md ${getActivityBgColor(activity.type)}`}
              >
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 mt-1">
                    {getActivityIcon(activity.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">
                      {activity.message}
                    </p>
                    <p className="text-xs text-gray-600 mt-1">
                      {activity.details}
                    </p>
                    <div className="flex items-center mt-2 text-xs text-gray-500">
                      <Clock className="h-3 w-3 mr-1" />
                      {formatTime(activity.timestamp)}
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
