import type { Finding } from "../types/analysis";

interface Props {
  findings: Finding[];
}

export default function FindingsList({ findings }: Props) {
  return (
    <div className="findings">
      <h2>Findings</h2>

      {findings.length === 0 && <p>No issues detected.</p>}

      <ul>
        {findings.map((f, index) => (
          <li key={index}>
            <strong>{f.rule_id}</strong> — {f.message}
          </li>
        ))}
      </ul>
    </div>
  );
}
