import { useState } from "react"
import ResultsGrid from "./components/ResultsGrid"
import "./App.css"

function App() {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [preview, setPreview] = useState(null)
  const [error, setError] = useState(null)
  const [searched, setSearched] = useState(false)

  const handleFile = async (file) => {
    if (!file) return
    setLoading(true)
    setError(null)
    setResults([])
    setSearched(true)
    setPreview(URL.createObjectURL(file))

    const formData = new FormData()
    formData.append("image", file)
    formData.append("top_k", 12)

    try {
      const response = await fetch("http://localhost:5000/search", {
        method: "POST",
        body: formData,
      })
      const data = await response.json()
      if (!response.ok) {
        setError(data.error || "Erreur serveur")
        return
      }
      setResults(data.results)
    } catch {
      setError("Impossible de contacter le serveur")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      {/* HEADER */}
      <header className={searched ? "header-compact" : "header-hero"}>
        <h1 className="logo">
          <span className="logo-v">V</span>
          <span className="logo-s">S</span>
          <span className="logo-e">E</span>
        </h1>
        {!searched && (
          <p className="tagline">Recherche visuelle de vêtements</p>
        )}

        {/* BARRE DE RECHERCHE */}
        <label className="search-box">
          <input
            type="file"
            accept="image/*"
            style={{ display: "none" }}
            onChange={(e) => handleFile(e.target.files[0])}
          />
          {preview ? (
            <img src={preview} alt="query" className="search-preview" />
          ) : (
            <span className="search-placeholder">🖼️ Upload une image...</span>
          )}
          <button
            className="search-btn"
            onClick={(e) => {
              e.preventDefault()
              e.currentTarget.closest("label").querySelector("input").click()
            }}
          >
            🔍
          </button>
        </label>
      </header>

      {/* RESULTATS */}
      <main>
        {loading && (
          <div className="loading-wrapper">
            <div className="spinner" />
            <p>Recherche en cours...</p>
          </div>
        )}
        {error && <p className="error">❌ {error}</p>}
        {results.length > 0 && <ResultsGrid results={results} />}
      </main>
    </div>
  )
}

export default App