export type Priority = "must" | "should" | "could" | "wont";
export type ReqType  = "functional" | "non_functional" | "constraint";

export interface Finding {
  rule_id: string;
  message: string;
  severity: "low" | "medium" | "high";
}

export interface AnalysisResult {
  findings: Finding[];
  clarity_score: number;
  testability_score: number;
  suggestions: string[];
  rag_error?: string | null;
}

export interface HistoryEntry {
  id: string;
  text: string;
  reqType: ReqType;
  priority: Priority;
  result: AnalysisResult;
  timestamp: number;
}