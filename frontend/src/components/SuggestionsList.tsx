interface Props {
  suggestions: string[];
  ragError?: string | null;
}

export default function SuggestionsList({ suggestions, ragError }: Props) {
  if (!ragError && (!suggestions || suggestions.length === 0)) return null;

  return (
    <div>
      <h2>AI Suggestions</h2>
      {ragError ? (
        <p style={{ color: "#d97706" }}>⚠ {ragError}</p>
      ) : (
        <ul>
          {suggestions.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
