import type { Finding } from "../types/analysis";

interface Props {
  findings: Finding[];
}

const SEVERITY_BADGE: Record<Finding["severity"], { label: string; style: React.CSSProperties }> = {
  high: { label: "HIGH", style: { background: "#dc2626", color: "#fff" } },
  medium: { label: "MED", style: { background: "#d97706", color: "#fff" } },
  low: { label: "LOW", style: { background: "#2563eb", color: "#fff" } },
};

const badgeStyle: React.CSSProperties = {
  display: "inline-block",
  fontSize: "0.7rem",
  fontWeight: 700,
  padding: "1px 6px",
  borderRadius: "3px",
  marginRight: "8px",
  verticalAlign: "middle",
  letterSpacing: "0.05em",
};

export default function FindingsList({ findings }: Props) {
  return (
    <div className="findings">
      <h2>Findings</h2>

      {findings.length === 0 ? (
        <p style={{ color: "#16a34a", fontWeight: 500 }}>
          ✓ This requirement looks good — no issues detected.
        </p>
      ) : (
        <ul>
          {findings.map((f, index) => {
            const badge = SEVERITY_BADGE[f.severity];
            return (
              <li key={index}>
                <span style={{ ...badgeStyle, ...badge.style }}>{badge.label}</span>
                <strong>{f.rule_id}</strong> — {f.message}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
