import { useState } from "react";

export type Priority = "must" | "should" | "could" | "wont";
export type ReqType  = "functional" | "non_functional" | "constraint";

interface Props {
  onAnalyse: (
    text: string,
    useRag: boolean,
    priority: Priority,
    reqType: ReqType,
  ) => void;
  isLoading: boolean;
}

const MOSCOW_OPTIONS: { value: Priority; label: string; description: string; color: string }[] = [
  { value: "must",   label: "Must",   description: "Mandatory for this release",   color: "#dc2626" },
  { value: "should", label: "Should", description: "High priority, not critical",  color: "#d97706" },
  { value: "could",  label: "Could",  description: "Nice to have if time permits", color: "#2563eb" },
  { value: "wont",   label: "Won't",  description: "Deferred — out of scope",      color: "#6b7280" },
];

const TYPE_OPTIONS: { value: ReqType; label: string; description: string }[] = [
  { value: "functional",     label: "Functional",     description: "A system behaviour or action" },
  { value: "non_functional", label: "Non-Functional", description: "A quality attribute (performance, security…)" },
  { value: "constraint",     label: "Constraint",     description: "A design or implementation restriction" },
];

export default function RequirementInput({ onAnalyse, isLoading }: Props) {
  const [text, setText]         = useState("");
  const [useRag, setUseRag]     = useState(false);
  const [priority, setPriority] = useState<Priority>("must");
  const [reqType, setReqType]   = useState<ReqType>("functional");

  const selectedMoscow = MOSCOW_OPTIONS.find((o) => o.value === priority)!;
  const selectedType   = TYPE_OPTIONS.find((o) => o.value === reqType)!;

  return (
    <div className="input-container">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter a requirement..."
        rows={5}
        maxLength={1000}
      />

      {/* Requirement Type selector */}
      <div style={{ marginBottom: "12px" }}>
        <p style={{ margin: "0 0 6px 0", fontWeight: 600, fontSize: "0.9rem" }}>
          Requirement Type
        </p>
        <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
          {TYPE_OPTIONS.map((opt) => {
            const isActive = reqType === opt.value;
            return (
              <button
                key={opt.value}
                onClick={() => setReqType(opt.value)}
                disabled={isLoading}
                title={opt.description}
                style={{
                  padding: "6px 14px",
                  borderRadius: "4px",
                  border: "2px solid #374151",
                  background: isActive ? "#374151" : "transparent",
                  color: isActive ? "#fff" : "#374151",
                  fontWeight: 600,
                  fontSize: "0.85rem",
                  cursor: isLoading ? "not-allowed" : "pointer",
                  opacity: isLoading ? 0.6 : 1,
                  transition: "background 0.15s, color 0.15s",
                }}
              >
                {opt.label}
              </button>
            );
          })}
        </div>
        <p style={{ margin: "4px 0 0 0", fontSize: "0.8rem", color: "#6b7280" }}>
          {selectedType.description}
        </p>
      </div>

      {/* MoSCoW Priority selector */}
      <div style={{ marginBottom: "12px" }}>
        <p style={{ margin: "0 0 6px 0", fontWeight: 600, fontSize: "0.9rem" }}>
          MoSCoW Priority
        </p>
        <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
          {MOSCOW_OPTIONS.map((opt) => {
            const isActive = priority === opt.value;
            return (
              <button
                key={opt.value}
                onClick={() => setPriority(opt.value)}
                disabled={isLoading}
                title={opt.description}
                style={{
                  padding: "6px 14px",
                  borderRadius: "4px",
                  border: `2px solid ${opt.color}`,
                  background: isActive ? opt.color : "transparent",
                  color: isActive ? "#fff" : opt.color,
                  fontWeight: 600,
                  fontSize: "0.85rem",
                  cursor: isLoading ? "not-allowed" : "pointer",
                  opacity: isLoading ? 0.6 : 1,
                  transition: "background 0.15s, color 0.15s",
                }}
              >
                {opt.label}
              </button>
            );
          })}
        </div>
        <p style={{ margin: "4px 0 0 0", fontSize: "0.8rem", color: "#6b7280" }}>
          {selectedMoscow.description}
        </p>
      </div>

      <label style={{ display: "block", marginBottom: "10px" }}>
        <input
          type="checkbox"
          checked={useRag}
          onChange={(e) => setUseRag(e.target.checked)}
          disabled={isLoading}
        />{" "}
        Enable AI suggestions
      </label>

      <button
        onClick={() => onAnalyse(text, useRag, priority, reqType)}
        disabled={isLoading || !text.trim()}
      >
        {isLoading ? "Analysing..." : "Analyse Requirement"}
      </button>
    </div>
  );
}
