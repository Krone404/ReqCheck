import { useState } from "react";
import RequirementInput from "./components/RequirementInput";
import type { Priority, ReqType } from "./components/RequirementInput";
import FindingsList from "./components/FindingsList";
import ScoreDisplay from "./components/ScoreDisplay";
import SuggestionsList from "./components/SuggestionsList";
import UseCaseDiagram from "./components/UseCaseDiagram";
import ExportButton from "./components/ExportButton";
import { analyseRequirement } from "./api/reqcheck";
import type { AnalysisResult } from "./types/analysis";
import { useRequirementHistory } from "./hooks/useRequirementHistory";

const MOSCOW_LABEL: Record<string, string> = {
  must: "Must", should: "Should", could: "Could", wont: "Won't",
};
const TYPE_LABEL: Record<string, string> = {
  functional: "Functional", non_functional: "Non-Functional", constraint: "Constraint",
};
const PRIORITY_COLOR: Record<string, string> = {
  must: "#dc2626", should: "#d97706", could: "#2563eb", wont: "#6b7280",
};

function App() {
  const [result, setResult]       = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError]         = useState<string | null>(null);
  const [lastText, setLastText]   = useState("");
  const [priority, setPriority]   = useState<Priority>("must");
  const [reqType, setReqType]     = useState<ReqType>("functional");

  const { history, addEntry, clearHistory } = useRequirementHistory();

  async function handleAnalyse(
    text: string,
    useRag: boolean,
    selectedPriority: Priority,
    selectedReqType: ReqType,
  ) {
    setIsLoading(true);
    setResult(null);
    setError(null);
    setLastText(text);
    setPriority(selectedPriority);
    setReqType(selectedReqType);

    try {
      const data = await analyseRequirement(text, useRag, selectedPriority, selectedReqType);
      setResult(data);
      addEntry({ text, priority: selectedPriority, reqType: selectedReqType, result: data });
    } catch (err) {
      const message = err instanceof Error ? err.message : "Something went wrong.";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="app">
      <h1>ReqCheck</h1>

      <RequirementInput onAnalyse={handleAnalyse} isLoading={isLoading} />

      {error && <p className="error-message">{error}</p>}

      {result && (
        <>
          <ScoreDisplay
            clarity={result.clarity_score}
            testability={result.testability_score}
          />
          <FindingsList findings={result.findings} />
          <SuggestionsList suggestions={result.suggestions} ragError={result.rag_error} />
          <ExportButton
            requirementText={lastText}
            reqType={reqType}
            priority={priority}
            result={result}
          />
        </>
      )}

      {/* Use-case diagram grows with each new requirement */}
      {history.length > 0 && <UseCaseDiagram history={history} />}

      {/* History list — shown once there are past entries */}
      {history.length > 1 && (
        <div style={{ marginTop: "24px" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "8px" }}>
            <h2 style={{ margin: 0 }}>Requirement History</h2>
            <button
              onClick={clearHistory}
              style={{
                padding: "4px 10px",
                fontSize: "0.8rem",
                borderRadius: "4px",
                border: "1px solid #d1d5db",
                background: "transparent",
                color: "#6b7280",
                cursor: "pointer",
              }}
            >
              Clear all
            </button>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            {history.map((entry, i) => (
              <div
                key={entry.id}
                style={{
                  padding: "10px 12px",
                  border: "1px solid #e5e7eb",
                  borderRadius: "6px",
                  background: i === 0 ? "#f9fafb" : "white",
                  borderLeft: `3px solid ${PRIORITY_COLOR[entry.priority] ?? "#9ca3af"}`,
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "8px" }}>
                  <p style={{ margin: 0, fontSize: "0.9rem", color: "#111827", flex: 1 }}>
                    {entry.text.length > 120 ? entry.text.slice(0, 118) + "…" : entry.text}
                    {i === 0 && (
                      <span style={{ marginLeft: "6px", fontSize: "0.75rem", color: "#6b7280" }}>(latest)</span>
                    )}
                  </p>
                  <div style={{ display: "flex", gap: "4px", flexShrink: 0 }}>
                    <span style={{
                      padding: "2px 7px", borderRadius: "4px", fontSize: "0.75rem", fontWeight: 600,
                      background: PRIORITY_COLOR[entry.priority] ?? "#9ca3af", color: "white",
                    }}>
                      {MOSCOW_LABEL[entry.priority] ?? entry.priority}
                    </span>
                    <span style={{
                      padding: "2px 7px", borderRadius: "4px", fontSize: "0.75rem",
                      border: "1px solid #d1d5db", color: "#374151",
                    }}>
                      {TYPE_LABEL[entry.reqType] ?? entry.reqType}
                    </span>
                  </div>
                </div>
                <p style={{ margin: "4px 0 0 0", fontSize: "0.8rem", color: "#6b7280" }}>
                  Clarity {entry.result.clarity_score}/10 · Testability {entry.result.testability_score}/10
                  {" · "}{new Date(entry.timestamp).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
