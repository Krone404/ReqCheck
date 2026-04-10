const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

import type { AnalysisResult } from "../types/analysis";

export async function analyseRequirement(
  text: string,
  useRag: boolean
): Promise<AnalysisResult> {
  const response = await fetch(`${BASE}/api/analyse`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text,
      use_rag: useRag,
    }),
  });

  let data: AnalysisResult | null = null;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const errData = data as unknown as { detail?: string; message?: string } | null;
    const message =
      errData?.detail ||
      errData?.message ||
      `Request failed with status ${response.status}`;
    throw new Error(message);
  }

  return data as AnalysisResult;
}
