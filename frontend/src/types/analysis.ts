export interface Finding {
  rule_id: string;
  message: string;
  severity: "low" | "medium" | "high";
}

export interface AnalysisResult {
  findings: Finding[];
  clarity_score: number;
  testability_score: number;
}
