import { useState, useRef } from "react"
import "./SearchBar.css"

function SearchBar({ onSearch }) {
  const [dragOver, setDragOver] = useState(false)
  const inputRef = useRef(null)

  const handleFile = (file) => {
    if (file) onSearch(file)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files[0]
    handleFile(file)
  }

  return (
    <div
      className={`searchbar ${dragOver ? "drag-over" : ""}`}
      onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        style={{ display: "none" }}
        onChange={(e) => handleFile(e.target.files[0])}
      />
      <div className="searchbar-content">
        <span className="icon">🖼️</span>
        <p className="main-text">Glisse une image ici</p>
        <p className="sub-text">ou clique pour sélectionner</p>
        <button className="btn">Choisir une image</button>
      </div>
    </div>
  )
}

export default SearchBar