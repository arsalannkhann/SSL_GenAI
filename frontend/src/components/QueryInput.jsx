import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/Card'
import { Button } from './ui/Button'
import { Textarea, Label, Input } from './ui/Input'
import { Search, Settings2 } from 'lucide-react'

export function QueryInput({ onSubmit, isLoading }) {
  const [inputMode, setInputMode] = useState('manual')
  const [query, setQuery] = useState('')
  const [apiUrl, setApiUrl] = useState('http://localhost:8000')
  const [topK, setTopK] = useState(10)
  const [testQueries, setTestQueries] = useState([])
  const [selectedTestQuery, setSelectedTestQuery] = useState('')
  const [showSettings, setShowSettings] = useState(false)

  // Load test queries from JSON file (easier parsing than CSV with multiline entries)
  useEffect(() => {
    // Try loading from JSON first (cleaner format)
    fetch('/data/test-queries.json')
      .then(res => res.json())
      .then(data => {
        if (data.queries && Array.isArray(data.queries)) {
          setTestQueries(data.queries.filter(q => q && q.trim().length > 10))
        }
      })
      .catch(() => {
        // Fallback to CSV if JSON not available
        fetch('/data/test-set.csv')
          .then(res => res.text())
          .then(text => {
            // Proper CSV parsing for quoted fields with newlines
            const queries = []
            let currentQuery = ''
            let insideQuotes = false
            let afterHeader = false
            
            for (let i = 0; i < text.length; i++) {
              const char = text[i]
              
              if (char === '"') {
                if (insideQuotes && text[i + 1] === '"') {
                  // Escaped quote
                  currentQuery += '"'
                  i++
                } else {
                  // Toggle quote state
                  insideQuotes = !insideQuotes
                  if (!insideQuotes && currentQuery.trim() && afterHeader) {
                    // End of a quoted field, add to queries
                    queries.push(currentQuery.trim())
                    currentQuery = ''
                  }
                }
              } else if (!insideQuotes && char === '\n') {
                // Line break outside quotes
                if (!afterHeader) {
                  afterHeader = true // Skip header row
                }
                if (currentQuery.trim() && afterHeader) {
                  queries.push(currentQuery.trim())
                }
                currentQuery = ''
              } else if (insideQuotes || (afterHeader && char !== '\r')) {
                // Accumulate characters inside quotes or after header
                if (afterHeader) {
                  currentQuery += char
                }
              }
            }
            
            // Add last query if exists
            if (currentQuery.trim() && afterHeader) {
              queries.push(currentQuery.trim())
            }
            
            setTestQueries(queries.filter(q => q.length > 10)) // Filter out empty/short entries
          })
          .catch(() => {
            // Test set not available, continue with manual input only
          })
      })
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!query.trim()) return
    onSubmit({ query: query.trim(), apiUrl, topK })
  }

  const handleTestQuerySelect = (e) => {
    const selected = e.target.value
    setSelectedTestQuery(selected)
    setQuery(selected)
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>SHL Assessment Recommendation</CardTitle>
            <CardDescription className="mt-2">
              Enter a job description or requirement to find relevant SHL assessments
            </CardDescription>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowSettings(!showSettings)}
          >
            <Settings2 className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {showSettings && (
          <div className="mb-6 space-y-4 p-4 border rounded-lg bg-muted/50">
            <div className="space-y-2">
              <Label htmlFor="api-url">API URL</Label>
              <Input
                id="api-url"
                type="text"
                value={apiUrl}
                onChange={(e) => setApiUrl(e.target.value)}
                placeholder="http://localhost:8000"
              />
              <p className="text-xs text-muted-foreground">
                Ensure the backend has GOOGLE_API_KEY configured
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="top-k">Top K Results: {topK}</Label>
              <input
                id="top-k"
                type="range"
                min="1"
                max="20"
                value={topK}
                onChange={(e) => setTopK(parseInt(e.target.value))}
                className="w-full"
              />
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label>Input Mode</Label>
            <div className="flex gap-4">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  value="manual"
                  checked={inputMode === 'manual'}
                  onChange={(e) => setInputMode(e.target.value)}
                  className="h-4 w-4"
                />
                <span className="text-sm">Manual Entry</span>
              </label>
              {testQueries.length > 0 && (
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    value="test"
                    checked={inputMode === 'test'}
                    onChange={(e) => setInputMode(e.target.value)}
                    className="h-4 w-4"
                  />
                  <span className="text-sm">Select from Test Dataset</span>
                </label>
              )}
            </div>
          </div>

          {inputMode === 'test' && testQueries.length > 0 && (
            <div className="space-y-2">
              <Label htmlFor="test-query">
                Select a Test Query ({testQueries.length} available)
              </Label>
              <select
                id="test-query"
                value={selectedTestQuery}
                onChange={handleTestQuerySelect}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <option value="">Choose a query...</option>
                {testQueries.map((q, idx) => (
                  <option key={idx} value={q}>
                    Query #{idx + 1}: {q.substring(0, 80)}{q.length > 80 ? '...' : ''}
                  </option>
                ))}
              </select>
              <p className="text-xs text-muted-foreground">
                Test queries from Gen_AI Dataset.xlsx (Test-Set sheet)
              </p>
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="query">
              {inputMode === 'test' ? 'Selected Query (editable)' : 'Enter job description or query'}
            </Label>
            <Textarea
              id="query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., We need to assess candidates for analytical thinking and problem-solving skills for a data analyst position..."
              className="min-h-[150px]"
            />
          </div>

          <Button type="submit" disabled={isLoading || !query.trim()} className="w-full">
            <Search className="mr-2 h-4 w-4" />
            {isLoading ? 'Searching...' : 'Get Recommendations'}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
