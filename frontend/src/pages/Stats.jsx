import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { formatDate, formatClicks } from '../utils/helpers.js'

export default function Stats() {
  const { shortCode } = useParams()
  const [stats, setStats] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch(`/api/stats/${shortCode}`)
      .then((res) => {
        if (!res.ok) throw new Error(`Not found (${res.status})`)
        return res.json()
      })
      .then(setStats)
      .catch((err) => setError(err.message))
  }, [shortCode])

  if (error) return <p className="error">{error}</p>
  if (!stats) return <p>Loading...</p>

  return (
    <div className="stats">
      <table>
        <tbody>
          <tr><td>Short code</td><td>{stats.short_code}</td></tr>
          <tr><td>Original URL</td><td><a href={stats.original_url} target="_blank" rel="noopener noreferrer">{stats.original_url}</a></td></tr>
          <tr><td>Total clicks</td><td>{formatClicks(stats.total_clicks)}</td></tr>
          <tr><td>Created</td><td>{formatDate(stats.created_at)}</td></tr>
          <tr><td>Last click</td><td>{formatDate(stats.last_click_at)}</td></tr>
        </tbody>
      </table>
      <Link to="/">← Back</Link>
    </div>
  )
}
