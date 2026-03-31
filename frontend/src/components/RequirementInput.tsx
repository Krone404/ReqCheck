import { useState } from "react";

interface Props {
  onAnalyse: (text: string, useRag: boolean) => void;
  isLoading: boolean;
}

export default function RequirementInput({ onAnalyse, isLoading }: Props) {
  const [text, setText] = useState("");
  const [useRag, setUseRag] = useState(false);

  return (
    <div className="input-container">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter a requirement..."
        rows={5}
      />

      <label>
        <input
          type="checkbox"
          checked={useRag}
          onChange={(e) => setUseRag(e.target.checked)}
          disabled={isLoading}
        />
        Enable AI suggestions
      </label>

      <button
        onClick={() => onAnalyse(text, useRag)}
        disabled={isLoading || !text.trim()}
      >
        {isLoading ? "Analysing..." : "Analyse Requirement"}
      </button>

      {isLoading && <p className="loading-text">Running analysis...</p>}
    </div>
  );
}
