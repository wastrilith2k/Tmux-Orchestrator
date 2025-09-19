'use client'

import { SystemMetrics as ISystemMetrics } from '../types'
import { Cpu, HardDrive, Activity } from 'lucide-react'

interface SystemMetricsProps {
  metrics: ISystemMetrics
}

export default function SystemMetrics ({ metrics }: SystemMetricsProps) {
  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-100/50">
      <div className="p-6 border-b border-gray-200/50 bg-gradient-to-r from-green-50 to-emerald-50 rounded-t-2xl">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-bold text-gray-900">System Health</h3>
            <p className="text-sm text-gray-600 mt-1">Real-time performance metrics</p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-xs font-medium text-gray-500">Live</span>
            <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
              <Activity className="h-4 w-4 text-white" />
            </div>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl border border-blue-200/50 hover:shadow-lg transition-all duration-200">
            <div className="flex items-center justify-center w-12 h-12 bg-blue-500 rounded-xl mx-auto mb-3 shadow-lg">
              <Cpu className="h-6 w-6 text-white" />
            </div>
            <p className="text-2xl font-bold text-gray-900 mb-1">
              {metrics.system_cpu_usage?.toFixed(1) || '0'}%
            </p>
            <p className="text-sm font-medium text-gray-600">CPU Usage</p>
            <div className="mt-2 w-full bg-gray-200 rounded-full h-1.5">
              <div
                className="bg-blue-500 h-1.5 rounded-full transition-all duration-300"
                style={{ width: `${metrics.system_cpu_usage || 0}%` }}
              />
            </div>
          </div>

          <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl border border-purple-200/50 hover:shadow-lg transition-all duration-200">
            <div className="flex items-center justify-center w-12 h-12 bg-purple-500 rounded-xl mx-auto mb-3 shadow-lg">
              <HardDrive className="h-6 w-6 text-white" />
            </div>
            <p className="text-2xl font-bold text-gray-900 mb-1">
              {metrics.system_memory_usage?.toFixed(1) || '0'}%
            </p>
            <p className="text-sm font-medium text-gray-600">Memory</p>
            <div className="mt-2 w-full bg-gray-200 rounded-full h-1.5">
              <div
                className="bg-purple-500 h-1.5 rounded-full transition-all duration-300"
                style={{ width: `${metrics.system_memory_usage || 0}%` }}
              />
            </div>
          </div>

          <div className="text-center p-4 bg-gradient-to-br from-green-50 to-green-100 rounded-xl border border-green-200/50 hover:shadow-lg transition-all duration-200">
            <div className="flex items-center justify-center w-12 h-12 bg-green-500 rounded-xl mx-auto mb-3 shadow-lg">
              <Activity className="h-6 w-6 text-white" />
            </div>
            <p className="text-2xl font-bold text-gray-900 mb-1">
              {Math.floor((metrics.uptime_seconds || 0) / 3600)}h
            </p>
            <p className="text-sm font-medium text-gray-600">Uptime</p>
            <div className="mt-2 flex items-center justify-center">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="ml-2 text-xs text-green-600 font-medium">Online</span>
            </div>
          </div>
        </div>

        {/* Additional metrics */}
        <div className="pt-4 border-t border-gray-200/50">
          <div className="grid grid-cols-2 gap-6 text-sm">
            <div className="flex items-center justify-between p-3 bg-gray-50/50 rounded-lg">
              <span className="text-gray-600 font-medium">Active Agents:</span>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-gray-900">{metrics.active_agents || 0}</span>
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              </div>
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50/50 rounded-lg">
              <span className="text-gray-600 font-medium">Total Projects:</span>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-gray-900">{metrics.total_projects || 0}</span>
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}