'use client'

import { useState, useEffect } from 'react'
import { MessageSquare, Clock } from 'lucide-react'

export default function ActivityFeed () {
  const [activities, setActivities] = useState([
    { id: 1, message: 'System started', timestamp: new Date().toISOString(), type: 'info' },
    { id: 2, message: 'Database connected', timestamp: new Date().toISOString(), type: 'success' },
    { id: 3, message: 'Redis connected', timestamp: new Date().toISOString(), type: 'success' },
  ])

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">Recent Activity</h2>
      </div>

      <div className="p-6">
        {activities.length === 0 ? (
          <div className="text-center text-gray-500">
            <MessageSquare className="h-8 w-8 mx-auto mb-2" />
            <p>No recent activity</p>
          </div>
        ) : (
          <div className="space-y-3">
            {activities.map((activity) => (
              <div key={activity.id} className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <Clock className="h-4 w-4 text-gray-400 mt-1" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900">{activity.message}</p>
                  <p className="text-xs text-gray-500">
                    {new Date(activity.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}