'use client'

import { SystemMetrics as ISystemMetrics } from '../types'
import { Cpu, HardDrive, Activity } from 'lucide-react'

interface SystemMetricsProps {
  metrics: ISystemMetrics
}

export default function SystemMetrics ({ metrics }: SystemMetricsProps) {
  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-100">
      <div className="p-6 border-b border-gray-200 bg-gradient-to-r from-green-50 to-emerald-50 rounded-t-xl">
        <h2 className="text-xl font-semibold text-gray-900">System Health</h2>
        <p className="text-sm text-gray-600 mt-1">Real-time system performance metrics</p>
      </div>

      <div className="p-6 space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <Cpu className="h-8 w-8 text-blue-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-gray-900">
              {metrics.system_cpu_usage?.toFixed(1) || '0'}%
            </p>
            <p className="text-sm text-gray-600">CPU Usage</p>
          </div>

          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <HardDrive className="h-8 w-8 text-purple-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-gray-900">
              {metrics.system_memory_usage?.toFixed(1) || '0'}%
            </p>
            <p className="text-sm text-gray-600">Memory</p>
          </div>

          <div className="text-center p-4 bg-green-50 rounded-lg">
            <Activity className="h-8 w-8 text-green-600 mx-auto mb-2" />
            <p className="text-2xl font-bold text-gray-900">
              {Math.floor((metrics.uptime_seconds || 0) / 3600)}h
            </p>
            <p className="text-sm text-gray-600">Uptime</p>
          </div>
        </div>

        {/* Additional metrics */}
        <div className="pt-4 border-t border-gray-100">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Active Agents:</span>
              <span className="font-medium text-gray-900 ml-2">{metrics.active_agents || 0}</span>
            </div>
            <div>
              <span className="text-gray-600">Total Projects:</span>
              <span className="font-medium text-gray-900 ml-2">{metrics.total_projects || 0}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}