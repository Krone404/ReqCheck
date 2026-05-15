interface Props {
  clarity: number;
  testability: number;
}

function scoreLabel(score: number): { label: string; color: string } {
  if (score >= 75) return { label: "Good", color: "#16a34a" };
  if (score >= 50) return { label: "Fair", color: "#d97706" };
  return { label: "Needs work", color: "#dc2626" };
}

function ScoreBar({ score }: { score: number }) {
  const { label, color } = scoreLabel(score);
  return (
    <div style={{ marginBottom: "0.75rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "2px" }}>
        <span>{score} / 100</span>
        <span style={{ color, fontWeight: 600 }}>{label}</span>
      </div>
      <div style={{ background: "#e5e7eb", borderRadius: "4px", height: "8px" }}>
        <div
          style={{
            width: `${score}%`,
            background: color,
            borderRadius: "4px",
            height: "8px",
            transition: "width 0.3s ease",
          }}
        />
      </div>
    </div>
  );
}

export default function ScoreDisplay({ clarity, testability }: Props) {
  return (
    <div className="scores">
      <h2>Scores</h2>
      <p style={{ marginBottom: "4px" }}><strong>Clarity</strong></p>
      <ScoreBar score={clarity} />
      <p style={{ marginBottom: "4px" }}><strong>Testability</strong></p>
      <ScoreBar score={testability} />
    </div>
  );
}
