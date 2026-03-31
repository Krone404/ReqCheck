import { useState } from "react";

interface Props {
  onAnalyse: (text: string) => void;
  isLoading: boolean;
}

export default function RequirementInput({ onAnalyse, isLoading }: Props) {
  const [text, setText] = useState("");

  return (
    <div className="input-container">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter a requirement..."
        rows={5}
      />

      <button
        onClick={() => onAnalyse(text)}
        disabled={isLoading || !text.trim()}
      >
        {isLoading ? "Analysing..." : "Analyse Requirement"}
      </button>

      {isLoading && <p className="loading-text">Running analysis...</p>}
    </div>
  );
}