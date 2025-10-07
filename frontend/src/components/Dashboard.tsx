'use client'

import { useState } from 'react'

export default function Dashboard() {
  const [files, setFiles] = useState([
    {
      id: 'fdca669ab2b1628868d8c6d0e630eda1e7O0Gzqj-mp4',
      date: '07/10/2025',
      status: 'Transcription' as const,
    },
    {
      id: 'daedf9fc2f347d901b642fd857133ea9RZqhUgDf-mp4',
      date: '07/10/2025', 
      status: 'Transcription' as const,
    },
    {
      id: '2f614c69d6b1a20451bb7496066930cfIaucCP9y-mp4',
      date: '07/10/2025',
      status: 'Transcription' as const,
    },
    {
      id: '07f1a7beab540b31c299ddb9d52fe81eadiLPWTk-mp4',
      date: '06/10/2025',
      status: 'Transcription' as const,
    },
  ])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-8">
              {/* Logo Placeholder */}
              <div className="text-xl font-bold text-gray-900">
                Forge Medias Logo
              </div>
              
              {/* Plan & Minutes */}
              <div className="flex items-center space-x-6">
                <div>
                  <span className="text-sm text-gray-600">Pro</span>
                </div>
                <div>
                  <span className="text-sm text-gray-600">Remaining minutes: 2086</span>
                </div>
              </div>
            </div>

            {/* User Info */}
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <div className="text-sm font-medium">@shadcn</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-white border-r border-gray-200 min-h-[calc(100vh-80px)]">
          <nav className="p-6">
            <ul className="space-y-2">
              <li><a href="#" className="block py-2 px-4 bg-blue-50 text-blue-700 rounded-md font-medium">Dashboard</a></li>
              <li><a href="#" className="block py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">Files</a></li>
              <li><a href="#" className="block py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">Integrations</a></li>
              <li><a href="#" className="block py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">Features</a></li>
              
              <li className="pt-4"><div className="text-xs font-semibold text-gray-400 px-4">Knowledge Base</div></li>
              
              <li><a href="#" className="block py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">Notes</a></li>
              <li><a href="#" className="block py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">Calendar</a></li>
              <li><a href="#" className="block py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">Workspace</a></li>
              <li><a href="#" className="block py-2 px-4 text-gray-700 hover:bg-gray-50 rounded-md">Data Analytics</a></li>
            </ul>

            {/* Upsell Banner */}
            <div className="mt-8 p-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white">
              <div className="text-sm font-semibold">Pro Yearly:</div>
              <div className="text-lg font-bold">Just $8.33/month</div>
              <div className="text-xs opacity-90">(Save 60%)</div>
            </div>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8">
          {/* Greeting */}
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-gray-900">Good Afternoon, Godfrey</h1>
          </div>

          {/* Feature Shortcuts */}
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4 mb-8">
            {['Speech to Text', 'Calendar', 'Text to Speech', 'AI Content Generation', 'Business Solutions'].map((feature) => (
              <button
                key={feature}
                className="bg-white border border-gray-200 rounded-lg p-4 text-center hover:border-blue-500 transition-colors"
              >
                <div className="font-medium text-gray-700">{feature}</div>
              </button>
            ))}
          </div>

          {/* Recent Files */}
          <div className="bg-white rounded-lg border border-gray-200">
            <div className="p-6 border-b border-gray-200">
              <div className="flex justify-between items-center">
                <h2 className="text-lg font-semibold text-gray-900">Recent Files</h2>
                <div className="flex space-x-3">
                  <button className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50">
                    Add Filter
                  </button>
                  <div className="relative">
                    <input
                      type="text"
                      placeholder="Search File Name"
                      className="pl-4 pr-10 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Files Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <tbody className="divide-y divide-gray-200">
                  {files.map((file, index) => (
                    <tr key={file.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {file.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {file.date}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {file.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button className="text-blue-600 hover:text-blue-900">
                          Open menu
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            <div className="px-6 py-4 border-t border-gray-200">
              <div className="flex justify-center">
                <nav className="flex space-x-2">
                  {[1, 2, 3].map((page) => (
                    <button
                      key={page}
                      className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
                    >
                      {page}
                    </button>
                  ))}
                </nav>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
