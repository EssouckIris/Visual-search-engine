import "./ImageCard.css"

function ImageCard({ result, index }) {
  const score = Math.round(result.score * 100)

  const scoreColor =
    score >= 80 ? "var(--blue)" :
    score >= 60 ? "var(--yellow)" :
    "var(--pink)"

  return (
    <div className="image-card">
      <div className="card-image-wrapper">
        <img src={result.image} alt={`Résultat ${index + 1}`} />
        <div className="card-overlay">
          <span className="view-btn">🔍 Voir</span>
        </div>
      </div>
      <div className="card-info">
        <div className="score-bar-wrapper">
          <div
            className="score-bar"
            style={{
              width: `${score}%`,
              backgroundColor: scoreColor
            }}
          />
        </div>
        <div className="card-meta">
          <span className="similarity" style={{ color: scoreColor }}>
            {score}% similaire
          </span>
          <span className="rank">#{index + 1}</span>
        </div>
      </div>
    </div>
  )
}

export default ImageCard