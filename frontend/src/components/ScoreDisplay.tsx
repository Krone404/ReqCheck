interface Props {
  clarity: number;
  testability: number;
}

export default function ScoreDisplay({ clarity, testability }: Props) {
  return (
    <div className="scores">
      <h2>Scores</h2>

      <p>Clarity Score: {clarity}</p>
      <p>Testability Score: {testability}</p>
    </div>
  );
}
