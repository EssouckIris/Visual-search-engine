import ImageCard from "./ImageCard"
import "./ResultsGrid.css"

function ResultsGrid({ results }) {
  return (
    <div className="results-section">
      <div className="results-header">
        <span className="results-count">
          {results.length} résultats similaires trouvés
        </span>
      </div>
      <div className="results-grid">
        {results.map((result, index) => (
          <ImageCard key={index} result={result} index={index} />
        ))}
      </div>
    </div>
  )
}

export default ResultsGrid