import { useEffect, useState, useCallback } from 'react'
import { getDashboard } from '../api/provider'

export function useDashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const refresh = useCallback(() => {
    setLoading(true)
    return getDashboard()
      .then((d) => {
        setData(d)
        setError(null)
      })
      .catch((err) => setError(err))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    refresh()
  }, [refresh])

  return { data, loading, error, refresh }
}
