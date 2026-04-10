import { useState } from "react";
import RequirementInput from "./components/RequirementInput";
import FindingsList from "./components/FindingsList";
import ScoreDisplay from "./components/ScoreDisplay";
import SuggestionsList from "./components/SuggestionsList";
import { analyseRequirement } from "./api/reqcheck";
import type { AnalysisResult } from "./types/analysis";

function App() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleAnalyse(text: string, useRag: boolean) {
    setIsLoading(true);
    setResult(null);
    setError(null);

    try {
      const data = await analyseRequirement(text, useRag);
      setResult(data);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Something went wrong.";
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
        </>
      )}
    </div>
  );
}

export default App;
