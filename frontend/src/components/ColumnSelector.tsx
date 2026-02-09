'use client'

import { useState } from 'react'
import { UploadResponse } from '@/app/page'

interface ColumnSelectorProps {
  uploadResult: UploadResponse
  onColumnSelect: (column: string) => void
  onReset: () => void
}

export default function ColumnSelector({
  uploadResult,
  onColumnSelect,
  onReset,
}: ColumnSelectorProps) {
  const [selectedColumn, setSelectedColumn] = useState<string>('')

  const handleSubmit = () => {
    if (selectedColumn) {
      onColumnSelect(selectedColumn)
    }
  }

  const getConfidenceMessage = () => {
    if (uploadResult.confidence === 'low') {
      return 'Multiple possible ESP columns found. Please select the correct one:'
    } else if (uploadResult.confidence === 'none') {
      return 'Could not automatically detect the ESP column. Please select it from the list:'
    }
    return ''
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Select ESP Column
        </h2>
        <p className="text-gray-600">{getConfidenceMessage()}</p>
      </div>

      <div className="mb-6">
        <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mb-4">
          <p className="text-sm text-blue-800">
            <strong>File:</strong> {uploadResult.filename}
          </p>
          <p className="text-sm text-blue-800">
            <strong>Total Rows:</strong> {uploadResult.total_rows.toLocaleString()}
          </p>
          <p className="text-sm text-blue-800">
            <strong>Columns:</strong> {uploadResult.all_columns.length}
          </p>
        </div>
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Choose ESP Column
        </label>
        <select
          value={selectedColumn}
          onChange={(e) => setSelectedColumn(e.target.value)}
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md border"
        >
          <option value="">-- Select a column --</option>
          {uploadResult.candidates.map((column) => (
            <option key={column} value={column}>
              {column}
            </option>
          ))}
        </select>
      </div>

      {uploadResult.preview_data && uploadResult.preview_data.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900 mb-3">
            Data Preview (first 10 rows)
          </h3>
          <div className="overflow-x-auto border border-gray-200 rounded-md">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  {uploadResult.all_columns.slice(0, 5).map((col) => (
                    <th
                      key={col}
                      className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {col}
                    </th>
                  ))}
                  {uploadResult.all_columns.length > 5 && (
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      ...
                    </th>
                  )}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {uploadResult.preview_data.slice(0, 10).map((row, idx) => (
                  <tr key={idx}>
                    {uploadResult.all_columns.slice(0, 5).map((col) => (
                      <td
                        key={col}
                        className="px-4 py-3 text-sm text-gray-900 max-w-xs truncate"
                      >
                        {row[col] !== null && row[col] !== undefined
                          ? String(row[col])
                          : ''}
                      </td>
                    ))}
                    {uploadResult.all_columns.length > 5 && (
                      <td className="px-4 py-3 text-sm text-gray-500">...</td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {uploadResult.all_columns.length > 5 && (
            <p className="text-xs text-gray-500 mt-2">
              Showing first 5 columns. All columns will be processed.
            </p>
          )}
        </div>
      )}

      <div className="flex justify-between">
        <button
          onClick={onReset}
          className="px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
        >
          Upload Different File
        </button>
        <button
          onClick={handleSubmit}
          disabled={!selectedColumn}
          className={`px-6 py-3 border border-transparent text-base font-medium rounded-md text-white transition-colors ${
            selectedColumn
              ? 'bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
              : 'bg-gray-300 cursor-not-allowed'
          }`}
        >
          Confirm Selection
        </button>
      </div>
    </div>
  )
}
