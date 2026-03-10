import { useState } from "react";

interface Props {
  onAnalyse: (text: string) => void;
}

export default function RequirementInput({ onAnalyse }: Props) {
  const [text, setText] = useState("");

  return (
    <div className="input-container">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter a requirement..."
        rows={5}
      />

      <button onClick={() => onAnalyse(text)}>Analyse Requirement</button>
    </div>
  );
}
