'use client'

import { SystemMetrics as ISystemMetrics } from '../types'
import { Cpu, HardDrive, Activity } from 'lucide-react'

interface SystemMetricsProps {
  metrics: ISystemMetrics
}

export default function SystemMetrics ({ metrics }: SystemMetricsProps) {
  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">System Health</h2>
      </div>

      <div className="p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Cpu className="h-5 w-5 text-blue-600 mr-2" />
            <span className="text-sm font-medium text-gray-900">CPU Usage</span>
          </div>
          <span className="text-sm text-gray-600">
            {metrics.system_cpu_usage.toFixed(1)}%
          </span>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <HardDrive className="h-5 w-5 text-green-600 mr-2" />
            <span className="text-sm font-medium text-gray-900">Memory Usage</span>
          </div>
          <span className="text-sm text-gray-600">
            {metrics.system_memory_usage.toFixed(1)}%
          </span>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Activity className="h-5 w-5 text-purple-600 mr-2" />
            <span className="text-sm font-medium text-gray-900">Uptime</span>
          </div>
          <span className="text-sm text-gray-600">
            {Math.floor(metrics.uptime_seconds / 3600)}h {Math.floor((metrics.uptime_seconds % 3600) / 60)}m
          </span>
        </div>
      </div>
    </div>
  )
}