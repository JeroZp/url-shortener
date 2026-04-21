import { useState } from 'react'
import { Link } from 'react-router-dom'
import { isValidUrl } from '../utils/helpers.js'

export default function Home() {
  const [url, setUrl] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setResult(null)

    if (!url.trim()) {
      setError('Please enter a URL.')
      return
    }
    if (!isValidUrl(url.trim())) {
      setError('Please enter a valid URL (e.g. https://example.com).')
      return
    }

    setLoading(true)
    try {
      const res = await fetch('/api/shorten', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url.trim() }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => null)
        throw new Error(data?.detail || `Server error (${res.status})`)
      }
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  function handleCopy() {
    navigator.clipboard.writeText(result.short_url)
  }

  return (
    <>
      <form onSubmit={handleSubmit} className="shorten-form">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Paste a long URL here..."
          className="url-input"
        />
        <button type="submit" disabled={loading} className="btn">
          {loading ? 'Shortening...' : 'Shorten'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result">
          <p>
            <a href={result.short_url} target="_blank" rel="noopener noreferrer">
              {result.short_url}
            </a>
            <button onClick={handleCopy} className="btn-copy">Copy</button>
          </p>
          <Link to={`/stats/${result.short_code}`}>View stats →</Link>
        </div>
      )}
    </>
  )
}
