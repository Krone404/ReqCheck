interface Props {
  requirementText: string;
  reqType: string;
  priority: string;
}

function parseRequirement(text: string): { actor: string; action: string } {
  const match = text.match(/^the\s+(.+?)\s+shall\s+(.+?)[\.,]?$/i);
  if (match) {
    return {
      actor:  match[1].trim(),
      action: match[2].trim(),
    };
  }
  return { actor: "System", action: text.trim() };
}

const PRIORITY_COLOR: Record<string, string> = {
  must:   "#dc2626",
  should: "#d97706",
  could:  "#2563eb",
  wont:   "#6b7280",
};

const TYPE_FILL: Record<string, string> = {
  functional:     "#dbeafe",
  non_functional: "#dcfce7",
  constraint:     "#fef9c3",
};

const TYPE_BADGE_LABEL: Record<string, string> = {
  functional:     "Functional",
  non_functional: "Non-Functional",
  constraint:     "Constraint",
};

export default function UseCaseDiagram({ requirementText, reqType, priority }: Props) {
  const { actor, action } = parseRequirement(requirementText);
  const priorityColor = PRIORITY_COLOR[priority] ?? "#374151";
  const useCaseFill   = TYPE_FILL[reqType]        ?? "#f3f4f6";

  const displayAction = action.length > 48 ? action.slice(0, 45) + "…" : action;
  const displayActor  = actor.length > 16  ? actor.slice(0, 13)  + "…" : actor;

  const actionLine1 = displayAction.length > 24 ? displayAction.slice(0, 24) : displayAction;
  const actionLine2 = displayAction.length > 24 ? displayAction.slice(24)    : "";

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Use-Case Diagram</h2>
      <p style={{ fontSize: "0.8rem", color: "#6b7280", marginBottom: "8px" }}>
        Extracted from requirement text — review for accuracy.
      </p>
      <svg
        viewBox="0 0 480 200"
        xmlns="http://www.w3.org/2000/svg"
        role="img"
        aria-label={`Use case diagram: ${displayActor} — ${displayAction}`}
        style={{
          width: "100%",
          maxWidth: "480px",
          border: "1px solid #e5e7eb",
          borderRadius: "8px",
        }}
      >
        <title>{`Use case: ${displayActor} shall ${displayAction}`}</title>
        {/* System boundary */}
        <rect
          x="160" y="20" width="280" height="160" rx="6"
          fill="#f9fafb" stroke="#9ca3af" strokeWidth="1.5" strokeDasharray="6 3"
        />
        <text x="300" y="14" textAnchor="middle" fontSize="11" fill="#6b7280">
          System Boundary
        </text>

        {/* Actor — stick figure */}
        <circle cx="70" cy="70" r="16" fill="white" stroke={priorityColor} strokeWidth="2" />
        <line x1="70" y1="86"  x2="70" y2="130" stroke={priorityColor} strokeWidth="2" />
        <line x1="44" y1="100" x2="96" y2="100" stroke={priorityColor} strokeWidth="2" />
        <line x1="70" y1="130" x2="50" y2="158" stroke={priorityColor} strokeWidth="2" />
        <line x1="70" y1="130" x2="90" y2="158" stroke={priorityColor} strokeWidth="2" />
        <text x="70" y="178" textAnchor="middle" fontSize="11" fontWeight="600" fill="#374151">
          {displayActor}
        </text>

        {/* Association line */}
        <line x1="90" y1="100" x2="190" y2="100" stroke="#9ca3af" strokeWidth="1.5" />

        {/* Use case ellipse */}
        <ellipse
          cx="300" cy="100" rx="100" ry="44"
          fill={useCaseFill} stroke={priorityColor} strokeWidth="2"
        />
        {actionLine2 ? (
          <>
            <text x="300" y="94"  textAnchor="middle" fontSize="11" fill="#111827">{actionLine1}</text>
            <text x="300" y="110" textAnchor="middle" fontSize="11" fill="#111827">{actionLine2}</text>
          </>
        ) : (
          <text x="300" y="104" textAnchor="middle" fontSize="11" fill="#111827">
            {actionLine1}
          </text>
        )}

        {/* MoSCoW priority badge */}
        <rect x="376" y="22" width="52" height="18" rx="4" fill={priorityColor} />
        <text x="402" y="34" textAnchor="middle" fontSize="9" fontWeight="700" fill="white">
          {priority.toUpperCase()}
        </text>

        {/* Type badge */}
        <rect
          x="162" y="22" width="86" height="18" rx="4"
          fill={useCaseFill} stroke={priorityColor} strokeWidth="1"
        />
        <text x="205" y="34" textAnchor="middle" fontSize="9" fill="#374151">
          {TYPE_BADGE_LABEL[reqType] ?? reqType}
        </text>
      </svg>
    </div>
  );
}
