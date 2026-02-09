'use client'

import { UploadResponse } from '@/app/page'

interface ProcessingStatusProps {
  uploadResult: UploadResponse
  selectedColumn: string
  onReset: () => void
}

export default function ProcessingStatus({
  uploadResult,
  selectedColumn,
  onReset,
}: ProcessingStatusProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <div className="text-center mb-6">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
          <svg
            className="w-8 h-8 text-green-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          ESP Column Identified!
        </h2>
        <p className="text-gray-600">
          The ESP column has been successfully identified and confirmed.
        </p>
      </div>

      <div className="bg-gray-50 rounded-lg p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-sm font-medium text-gray-500">File Name</p>
            <p className="text-base text-gray-900 mt-1">{uploadResult.filename}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Total Rows</p>
            <p className="text-base text-gray-900 mt-1">
              {uploadResult.total_rows.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">ESP Column</p>
            <p className="text-base text-gray-900 mt-1 font-semibold">
              {selectedColumn}
            </p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Detection Confidence</p>
            <p className="text-base text-gray-900 mt-1 capitalize">
              {uploadResult.confidence}
            </p>
          </div>
        </div>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mb-6">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg
              className="h-5 w-5 text-blue-400"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                clipRule="evenodd"
              />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-blue-700">
              <strong>Next Step:</strong> The filtering and splitting functionality will be implemented in the next phase. 
              For now, the ESP column identification is complete.
            </p>
          </div>
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={onReset}
          className="px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
        >
          Process Another File
        </button>
      </div>
    </div>
  )
}
