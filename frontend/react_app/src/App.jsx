import React, { useState, useEffect } from 'react'
import './App.css'

const App = () => {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
      .then(response => response.json())
      .then(json => setData(json))
      .catch(() => setData(null))
  }, [])

  return (
    <div style={{ padding: '20px' }}>
      <h1>hello!world</h1>
      {data ? <p>message: {data.message}</p> : <p>loading...</p>}
    </div>
  )
}

export default App
