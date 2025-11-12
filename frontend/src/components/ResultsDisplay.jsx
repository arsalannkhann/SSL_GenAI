import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/Card'
import { Alert, AlertDescription } from './ui/Alert'
import { ExternalLink, Clock, Award } from 'lucide-react'

export function ResultsDisplay({ results, error }) {
  if (error) {
    return (
      <Alert variant="error">
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    )
  }

  if (!results) {
    return null
  }

  if (results.recommendations.length === 0) {
    return (
      <Alert variant="info">
        <AlertDescription>No recommendations found for your query.</AlertDescription>
      </Alert>
    )
  }

  return (
    <div className="space-y-4">
      <Alert variant="success">
        <AlertDescription>
          Found {results.total_results} relevant assessment{results.total_results !== 1 ? 's' : ''}
        </AlertDescription>
      </Alert>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {results.recommendations.map((rec, idx) => (
          <Card key={idx} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between gap-2">
                <CardTitle className="text-lg leading-tight">
                  {rec.assessment_name}
                </CardTitle>
                <div className="flex-shrink-0 bg-primary/10 text-primary px-2 py-1 rounded text-xs font-semibold">
                  {(rec.relevance_score * 100).toFixed(1)}%
                </div>
              </div>
              {rec.test_type && (
                <CardDescription className="flex items-center gap-1 mt-2">
                  <Award className="h-3 w-3" />
                  {rec.test_type}
                </CardDescription>
              )}
            </CardHeader>
            <CardContent className="space-y-3">
              {rec.duration && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Clock className="h-4 w-4" />
                  <span>{rec.duration}</span>
                </div>
              )}
              <a
                href={rec.assessment_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 text-sm text-primary hover:underline"
              >
                View Assessment
                <ExternalLink className="h-3 w-3" />
              </a>
            </CardContent>
          </Card>
        ))}
      </div>

      <details className="mt-6">
        <summary className="cursor-pointer text-sm font-medium text-muted-foreground hover:text-foreground">
          Show API Response
        </summary>
        <pre className="mt-2 p-4 bg-muted rounded-lg overflow-auto text-xs">
          {JSON.stringify(results, null, 2)}
        </pre>
      </details>
    </div>
  )
}
