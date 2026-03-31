interface Props {
  suggestions: string[];
}

export default function SuggestionsList({ suggestions }: Props) {
  if (!suggestions || suggestions.length === 0) return null;

  return (
    <div>
      <h2>AI Suggestions</h2>
      <ul>
        {suggestions.map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ul>
    </div>
  );
}
