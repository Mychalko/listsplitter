'use client'

import { useState } from 'react'
import FileUpload from '@/components/FileUpload'
import ColumnSelector from '@/components/ColumnSelector'
import ProcessingStatus from '@/components/ProcessingStatus'

export type DetectionConfidence = 'high' | 'low' | 'none'

export interface UploadResponse {
  confidence: DetectionConfidence
  detected_column: string | null
  candidates: string[]
  preview_data: Record<string, any>[] | null
  total_rows: number
  all_columns: string[]
  filename: string
}

export default function Home() {
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null)
  const [selectedColumn, setSelectedColumn] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)

  const handleUploadSuccess = (result: UploadResponse) => {
    setUploadResult(result)
    if (result.confidence === 'high' && result.detected_column) {
      setSelectedColumn(result.detected_column)
    }
  }

  const handleColumnSelect = (column: string) => {
    setSelectedColumn(column)
  }

  const handleReset = () => {
    setUploadResult(null)
    setSelectedColumn(null)
    setIsProcessing(false)
  }

  return (
    <main className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            ESP List Processing
          </h1>
          <p className="text-lg text-gray-600">
            Upload your CSV or XLSX file to process and filter ESP lists
          </p>
        </div>

        {!uploadResult && (
          <FileUpload
            onUploadSuccess={handleUploadSuccess}
            isProcessing={isProcessing}
            setIsProcessing={setIsProcessing}
          />
        )}

        {uploadResult && !selectedColumn && (
          <ColumnSelector
            uploadResult={uploadResult}
            onColumnSelect={handleColumnSelect}
            onReset={handleReset}
          />
        )}

        {uploadResult && selectedColumn && (
          <ProcessingStatus
            uploadResult={uploadResult}
            selectedColumn={selectedColumn}
            onReset={handleReset}
          />
        )}
      </div>
    </main>
  )
}
