import type { HistoryEntry } from "../types/analysis";

interface Props {
  history: HistoryEntry[];
}

interface UseCaseItem {
  actor: string;
  action: string;
  priorityColor: string;
  fill: string;
  isNewest: boolean;
}

// ── Parsing ───────────────────────────────────────────────────────────────────

function parseRawUseCases(text: string): Array<{ actor: string; action: string }> {
  const sentences = text
    .split(/\.(?=\s|$)/)
    .map(s => s.trim())
    .filter(s => s.length > 2);

  const parsed = sentences.map(sentence => {
    const m1 = sentence.match(/^the\s+(.+?)\s+shall\s+(.+)$/i);
    if (m1) return { actor: m1[1].trim(), action: m1[2].replace(/[,.]$/, "").trim() };

    const m2 = sentence.match(/^(.+?)\s+(?:can|could)\s+(.+)$/i);
    if (m2) return { actor: m2[1].trim(), action: m2[2].replace(/[,.]$/, "").trim() };

    const m3 = sentence.match(/^(.+?)\s+(?:should|must|will|may)\s+(.+)$/i);
    if (m3) return { actor: m3[1].trim(), action: m3[2].replace(/[,.]$/, "").trim() };

    return { actor: "Actor", action: sentence.replace(/[,.]$/, "").trim() };
  });

  return parsed.length > 0 ? parsed : [{ actor: "Actor", action: text.trim() }];
}

// ── Filters ───────────────────────────────────────────────────────────────────

// Actor names that represent the system itself — not external actors
const SYSTEM_ACTOR_NAMES = new Set([
  "system", "the system", "application", "app", "software",
  "platform", "service", "database", "server", "backend",
]);

// Action phrases that are quality attributes, not functional user goals
const NF_ACTION_PATTERNS = [
  /\bfast\b/i, /\bquickly?\b/i, /\brapidly?\b/i,
  /\bperformance\b/i, /\bresponsive(ness)?\b/i,
  /\bscal(e|able|ability|ing)\b/i,
  /\bavailab(le|ility)\b/i, /\breliab(le|ility|ly)\b/i,
  /\buptime\b/i, /\blatency\b/i, /\bthroughput\b/i,
  /\bconcurrent(ly)?\b/i, /\bencrypt(ed|ion)?\b/i,
  /\bsecure(ly)?\b/i, /\bsecurity\b/i,
  /\b\d+(\.\d+)?%\b/, /\b\d+\s*(ms|sec|second|minute|hour)\b/i,
];

function looksNonFunctional(action: string): boolean {
  return NF_ACTION_PATTERNS.some(p => p.test(action));
}

// Use-case names that suggest passive voice or non-goal framing
const PASSIVE_PATTERNS = [
  /^(is|are|was|were)\s+\w+(ed|en)\b/i,
  /^(produced|generated|created|processed|handled|completed|given|displayed|stored|saved|imported|exported|sent|received|returned|logged|recorded)\b/i,
];

function looksPassive(action: string): boolean {
  return PASSIVE_PATTERNS.some(p => p.test(action));
}

function toTitleCase(s: string): string {
  return s.replace(/\b\w/g, c => c.toUpperCase());
}

// ── Colours ───────────────────────────────────────────────────────────────────

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

// ── Processing pipeline ───────────────────────────────────────────────────────

function processHistory(history: HistoryEntry[]): { items: UseCaseItem[]; notes: string[] } {
  const notes: string[] = [];
  let hadSystemActor = false;
  let hadNonFunctional = false;
  let hadPassive = false;
  let hadDuplicates = false;

  const newestId = history[0]?.id;
  const raw: Array<UseCaseItem & { dedupeKey: string }> = [];

  for (const entry of history) {
    const entryIsNf = entry.reqType === "non_functional" || entry.reqType === "constraint";

    for (const uc of parseRawUseCases(entry.text)) {
      if (SYSTEM_ACTOR_NAMES.has(uc.actor.toLowerCase())) {
        hadSystemActor = true;
        continue;
      }
      if (entryIsNf || looksNonFunctional(uc.action)) {
        hadNonFunctional = true;
        continue;
      }
      const action = toTitleCase(uc.action);
      if (looksPassive(uc.action)) hadPassive = true;

      raw.push({
        actor: uc.actor,
        action,
        priorityColor: PRIORITY_COLOR[entry.priority] ?? "#374151",
        fill: TYPE_FILL[entry.reqType] ?? "#f3f4f6",
        isNewest: entry.id === newestId,
        dedupeKey: `${uc.actor.toLowerCase()}::${uc.action.toLowerCase()}`,
      });
    }
  }

  // Deduplicate — keep first occurrence (history is newest-first)
  const seen = new Set<string>();
  const items: UseCaseItem[] = [];
  for (const rawItem of raw) {
    if (seen.has(rawItem.dedupeKey)) { hadDuplicates = true; continue; }
    seen.add(rawItem.dedupeKey);
    const { dedupeKey: _key, ...item } = rawItem;
    items.push(item);
  }

  if (hadSystemActor) {
    notes.push(
      '"System" was excluded as an actor — the system boundary should not appear as an external actor. ' +
      'Requirements of the form "the system shall…" describe internal behaviour; identify the human or ' +
      'external system that triggers the goal instead.'
    );
  }
  if (hadNonFunctional) {
    notes.push(
      'Non-functional or quality-attribute requirements (e.g. "run fast", performance, availability) were ' +
      'excluded — use-case diagrams model functional user goals, not quality constraints.'
    );
  }
  if (hadPassive) {
    notes.push(
      'Some use-case names appear to use passive voice (e.g. "Produced", "Generated"). ' +
      'Rename them as active user goals such as "Generate Diagram" or "Export Report".'
    );
  }
  if (hadDuplicates) {
    notes.push('Duplicate use cases across requirements were merged into a single ellipse.');
  }

  return { items, notes };
}

// ── Layout ────────────────────────────────────────────────────────────────────

const W = 520;
const ACTOR_CX = 72;
const UC_CX = 340;
const UC_RX = 115;
const UC_RY = 33;
const ROW_H = 110;
const MARGIN_T = 30;
const MARGIN_B = 40;
const BOUNDARY_X = 150;
const MAX_ITEMS = 12;

function clamp(s: string, maxLen: number): string {
  return s.length > maxLen ? s.slice(0, maxLen - 1) + "…" : s;
}

function splitActionText(action: string): [string, string] {
  const words = action.split(" ");
  let line1 = "";
  let line2 = "";
  for (const w of words) {
    if (!line1 || line1.length + w.length + 1 <= 22) {
      line1 += (line1 ? " " : "") + w;
    } else {
      line2 += (line2 ? " " : "") + w;
    }
  }
  return [line1, line2];
}

function ActorFigure({ cx, cy, color, label }: { cx: number; cy: number; color: string; label: string }) {
  const headCY = cy - 22;
  const bodyTop = cy - 9;
  const bodyBot = cy + 29;
  return (
    <g>
      <circle cx={cx} cy={headCY} r={13} fill="white" stroke={color} strokeWidth="2" />
      <line x1={cx} y1={bodyTop} x2={cx} y2={bodyBot} stroke={color} strokeWidth="2" />
      <line x1={cx - 20} y1={cy} x2={cx + 20} y2={cy} stroke={color} strokeWidth="2" />
      <line x1={cx} y1={bodyBot} x2={cx - 14} y2={bodyBot + 22} stroke={color} strokeWidth="2" />
      <line x1={cx} y1={bodyBot} x2={cx + 14} y2={bodyBot + 22} stroke={color} strokeWidth="2" />
      <text x={cx} y={bodyBot + 36} textAnchor="middle" fontSize="11" fontWeight="600" fill="#374151">
        {clamp(label, 14)}
      </text>
    </g>
  );
}

// ── Component ─────────────────────────────────────────────────────────────────

export default function UseCaseDiagram({ history }: Props) {
  if (history.length === 0) return null;

  const { items: allItems, notes } = processHistory(history);
  const displayItems = allItems.slice(0, MAX_ITEMS);
  const uniqueActors = [...new Set(displayItems.map(uc => uc.actor))];

  const N = displayItems.length;
  const H = MARGIN_T + Math.max(N, 1) * ROW_H + MARGIN_B;
  const bW = W - BOUNDARY_X - 10;

  const rowCY = (i: number) => MARGIN_T + i * ROW_H + ROW_H / 2;

  const actorRefY = (actor: string) => {
    const rows = displayItems
      .map((uc, i) => (uc.actor === actor ? i : -1))
      .filter(i => i >= 0);
    if (rows.length === 0) return H / 2;
    return MARGIN_T + (rows.reduce((a, b) => a + b, 0) / rows.length) * ROW_H + ROW_H / 2;
  };

  const actorColor = (actor: string) =>
    displayItems.find(uc => uc.actor === actor)?.priorityColor ?? "#374151";

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Use-Case Diagram</h2>
      <p style={{ fontSize: "0.8rem", color: "#6b7280", marginBottom: "8px" }}>
        Draft — extracted from requirement text.{" "}
        {N > 0
          ? `${N} use case${N !== 1 ? "s" : ""} from ${history.length} requirement${history.length !== 1 ? "s" : ""}.`
          : "No eligible use cases found after filtering."
        }
      </p>

      {N > 0 && (
        <svg
          viewBox={`0 0 ${W} ${H}`}
          xmlns="http://www.w3.org/2000/svg"
          role="img"
          aria-label="Use case diagram"
          style={{ width: "100%", maxWidth: `${W}px`, border: "1px solid #e5e7eb", borderRadius: "8px" }}
        >
          <title>Use-case diagram</title>

          {/* System boundary */}
          <rect
            x={BOUNDARY_X} y="10" width={bW} height={H - 18} rx="6"
            fill="#f9fafb" stroke="#9ca3af" strokeWidth="1.5" strokeDasharray="6 3"
          />
          <text x={BOUNDARY_X + bW / 2} y="8" textAnchor="middle" fontSize="11" fill="#6b7280">
            System Boundary
          </text>

          {/* Association lines + use case ellipses */}
          {displayItems.map((uc, i) => {
            const cy = rowCY(i);
            const refY = actorRefY(uc.actor);
            const [line1, line2] = splitActionText(clamp(uc.action, 38));
            return (
              <g key={i}>
                <line
                  x1={ACTOR_CX + 20} y1={refY}
                  x2={UC_CX - UC_RX} y2={cy}
                  stroke="#9ca3af" strokeWidth="1.5"
                />
                <ellipse
                  cx={UC_CX} cy={cy} rx={UC_RX} ry={UC_RY}
                  fill={uc.fill} stroke={uc.priorityColor}
                  strokeWidth={uc.isNewest ? 2.5 : 1.5}
                  opacity={uc.isNewest ? 1 : 0.7}
                />
                {line2 ? (
                  <>
                    <text x={UC_CX} y={cy - 7} textAnchor="middle" fontSize="11" fill="#111827" opacity={uc.isNewest ? 1 : 0.7}>{line1}</text>
                    <text x={UC_CX} y={cy + 9} textAnchor="middle" fontSize="11" fill="#111827" opacity={uc.isNewest ? 1 : 0.7}>{line2}</text>
                  </>
                ) : (
                  <text x={UC_CX} y={cy + 4} textAnchor="middle" fontSize="11" fill="#111827" opacity={uc.isNewest ? 1 : 0.7}>{line1}</text>
                )}
              </g>
            );
          })}

          {/* Actor stick figures */}
          {uniqueActors.map(actor => (
            <ActorFigure
              key={actor}
              cx={ACTOR_CX}
              cy={actorRefY(actor)}
              color={actorColor(actor)}
              label={actor}
            />
          ))}
        </svg>
      )}

      {/* Review notes — always shown when there are issues to flag */}
      {notes.length > 0 && (
        <div style={{
          marginTop: "12px",
          padding: "12px 16px",
          background: "#fffbeb",
          border: "1px solid #f59e0b",
          borderLeft: "4px solid #f59e0b",
          borderRadius: "6px",
        }}>
          <p style={{ margin: "0 0 6px 0", fontWeight: 600, fontSize: "0.85rem", color: "#92400e" }}>
            Review Notes — diagram needs attention
          </p>
          <ul style={{ margin: 0, paddingLeft: "16px" }}>
            {notes.map((note, i) => (
              <li key={i} style={{ fontSize: "0.82rem", color: "#78350f", marginBottom: i < notes.length - 1 ? "4px" : 0 }}>
                {note}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
