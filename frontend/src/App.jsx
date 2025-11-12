import { useState } from 'react'
import axios from 'axios'
import { QueryInput } from './components/QueryInput'
import { ResultsDisplay } from './components/ResultsDisplay'
import { Sparkles } from 'lucide-react'

function App() {
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async ({ query, apiUrl, topK }) => {
    setIsLoading(true)
    setError(null)
    setResults(null)

    try {
      const response = await axios.post(
        `${apiUrl}/recommend`,
        { query, top_k: topK },
        { timeout: 120000 }
      )
      setResults(response.data)
    } catch (err) {
      if (err.response) {
        setError(`API Error ${err.response.status}: ${err.response.data?.detail || err.response.statusText}`)
      } else if (err.request) {
        setError('No response from server. Please check if the API is running.')
      } else {
        setError(`Request failed: ${err.message}`)
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <header className="mb-8 text-center">
          <div className="flex items-center justify-center gap-3 mb-2">
            <Sparkles className="h-8 w-8 text-primary" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              SHL Assessment Finder
            </h1>
          </div>
          <p className="text-muted-foreground text-lg">
            Powered by Google Gemini embeddings and FastAPI
          </p>
        </header>

        {/* Main Content */}
        <div className="space-y-6">
          <QueryInput onSubmit={handleSubmit} isLoading={isLoading} />
          <ResultsDisplay results={results} error={error} />
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-sm text-muted-foreground">
          <p>© 2024 SHL Assessment Recommendation System</p>
        </footer>
      </div>
    </div>
  )
}

export default App
