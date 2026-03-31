import { useState } from "react";
import RequirementInput from "./components/RequirementInput";
import FindingsList from "./components/FindingsList";
import ScoreDisplay from "./components/ScoreDisplay";
import { analyseRequirement } from "./api/reqcheck";
import type { AnalysisResult } from "./types/analysis";


function App() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleAnalyse(text: string) {
    setIsLoading(true);
    setResult(null);

    try {
      const data = await analyseRequirement(text);
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="app">
      <h1>ReqCheck</h1>

      <RequirementInput onAnalyse={handleAnalyse} isLoading={isLoading} />

      {result && (
        <>
          <ScoreDisplay
            clarity={result.clarity_score}
            testability={result.testability_score}
          />

          <FindingsList findings={result.findings} />
        </>
      )}
    </div>
  );
}

export default App;
