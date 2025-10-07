'use client'

import { useState, useEffect } from 'react'
import { fetchDashboardData } from '@/lib/api'

interface File {
  id: string
  fileName: string
  uploadedAt: string
  status: string
}

interface Subscription {
  planType: string
  monthlyMinutes: number
  usedMinutes: number
  remainingMinutes: number
}

interface User {
  id: string
  email: string
  handle: string
  name: string
}

interface DashboardData {
  user: User
  subscription: Subscription
  recentFiles: File[]
}

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const data = await fetchDashboardData()
      if (data) {
        setDashboardData(data)
      } else {
        setError('Failed to load dashboard data')
      }
    } catch (err) {
      setError('Error loading dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const getGreeting = () => {
    const hour = new Date().getHours()
    if (hour < 12) return 'Good Morning'
    if (hour < 18) return 'Good Afternoon'
    return 'Good Evening'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-xl font-semibold text-gray-600">Loading Dashboard...</div>
          <div className="mt-2 text-sm text-gray-500">Please wait while we load your data</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-xl font-semibold text-red-600">Error</div>
          <div className="mt-2 text-sm text-gray-500">{error}</div>
          <button 
            onClick={loadDashboardData}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  const { user, subscription, recentFiles } = dashboardData!

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-8">
              {/* Logo */}
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg"></div>
                <div className="text-xl font-bold text-gray-900">Forge Medias</div>
              </div>
              
              {/* Plan & Minutes */}
              <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-2">
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full capitalize">
                    {subscription.planType.toLowerCase()}
                  </span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-600">Remaining minutes:</span>
                  <span className="text-sm font-semibold text-gray-900">{subscription.remainingMinutes}</span>
                </div>
              </div>
            </div>

            {/* User Info */}
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <div className="text-sm font-medium text-gray-700">{user.handle}</div>
                <div className="text-xs text-gray-500">{user.email}</div>
              </div>
              <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                <span className="text-sm font-medium text-gray-600">
                  {user.name?.charAt(0) || user.handle?.charAt(0) || 'U'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-white border-r border-gray-200 min-h-[calc(100vh-73px)]">
          <nav className="p-6">
            <ul className="space-y-1">
              <li>
                <a href="#" className="flex items-center py-2 px-4 bg-blue-50 text-blue-700 rounded-md font-medium">
                  <span className="mr-3">📊</span>
                  Dashboard
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">
                  <span className="mr-3">📁</span>
                  Files
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">
                  <span className="mr-3">🔗</span>
                  Integrations
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">
                  <span className="mr-3">⚡</span>
                  Features
                </a>
              </li>
              
              <li className="pt-6">
                <div className="text-xs font-semibold text-gray-400 px-4 uppercase tracking-wider">Knowledge Base</div>
              </li>
              
              <li>
                <a href="#" className="flex items-center py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">
                  <span className="mr-3">📝</span>
                  Notes
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">
                  <span className="mr-3">📅</span>
                  Calendar
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">
                  <span className="mr-3">💼</span>
                  Workspace
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">
                  <span className="mr-3">📈</span>
                  Data Analytics
                </a>
              </li>
            </ul>

            {/* Upsell Banner */}
            <div className="mt-8 p-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white">
              <div className="text-sm font-semibold mb-1">Pro Yearly Plan</div>
              <div className="text-lg font-bold">Just $8.33/month</div>
              <div className="text-xs opacity-90 mt-1">Save 60% compared to monthly</div>
              <button className="w-full mt-3 px-3 py-2 bg-white text-blue-600 text-sm font-medium rounded-md hover:bg-gray-100 transition-colors">
                Upgrade Now
              </button>
            </div>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8">
          {/* Greeting */}
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-gray-900">
              {getGreeting()}, {user.name || 'User'}
            </h1>
            <p className="text-gray-600 mt-1">Welcome back to your media workspace</p>
          </div>

          {/* Usage Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Plan Type</p>
                  <p className="text-2xl font-bold text-gray-900 capitalize mt-1">{subscription.planType.toLowerCase()}</p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 text-xl">⚡</span>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Minutes Used</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">{subscription.usedMinutes}</p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-green-600 text-xl">⏱️</span>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Remaining Minutes</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">{subscription.remainingMinutes}</p>
                </div>
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                  <span className="text-purple-600 text-xl">🎯</span>
                </div>
              </div>
            </div>
          </div>

          {/* Feature Shortcuts */}
          <div className="mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
              {[
                { name: 'Speech to Text', icon: '🎤', color: 'blue' },
                { name: 'Calendar', icon: '📅', color: 'green' },
                { name: 'Text to Speech', icon: '🔊', color: 'purple' },
                { name: 'AI Content Generation', icon: '🤖', color: 'orange' },
                { name: 'Business Solutions', icon: '💼', color: 'indigo' }
              ].map((feature) => (
                <button
                  key={feature.name}
                  className="bg-white border border-gray-200 rounded-lg p-4 text-center hover:border-blue-500 hover:shadow-sm transition-all duration-200"
                >
                  <div className="text-2xl mb-2">{feature.icon}</div>
                  <div className="font-medium text-gray-700 text-sm">{feature.name}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Recent Files */}
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
            <div className="p-6 border-b border-gray-200">
              <div className="flex justify-between items-center">
                <h2 className="text-lg font-semibold text-gray-900">Recent Files</h2>
                <div className="flex space-x-3">
                  <button className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors">
                    Add Filter
                  </button>
                  <div className="relative">
                    <input
                      type="text"
                      placeholder="Search File Name"
                      className="pl-4 pr-10 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 w-64"
                    />
                    <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                      🔍
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Files Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">File ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {recentFiles.map((file) => (
                    <tr key={file.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{file.id}</div>
                        <div className="text-sm text-gray-500">{file.fileName}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {file.uploadedAt}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {file.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button className="text-blue-600 hover:text-blue-900 mr-4">
                          View
                        </button>
                        <button className="text-gray-600 hover:text-gray-900">
                          ⋮
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            <div className="px-6 py-4 border-t border-gray-200">
              <div className="flex justify-between items-center">
                <div className="text-sm text-gray-500">
                  Showing {recentFiles.length} files
                </div>
                <div className="flex space-x-2">
                  {[1, 2, 3].map((page) => (
                    <button
                      key={page}
                      className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
                    >
                      {page}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
