import { useState } from "react";
import type { HistoryEntry, AnalysisResult, Priority, ReqType } from "../types/analysis";

const STORAGE_KEY = "reqcheck_history";
const MAX_ENTRIES = 20;

export function useRequirementHistory() {
  const [history, setHistory] = useState<HistoryEntry[]>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? (JSON.parse(stored) as HistoryEntry[]) : [];
    } catch {
      return [];
    }
  });

  function addEntry(entry: {
    text: string;
    reqType: ReqType;
    priority: Priority;
    result: AnalysisResult;
  }) {
    const newEntry: HistoryEntry = {
      ...entry,
      id: Date.now().toString(),
      timestamp: Date.now(),
    };
    setHistory(prev => {
      const next = [newEntry, ...prev].slice(0, MAX_ENTRIES);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }

  function clearHistory() {
    setHistory([]);
    localStorage.removeItem(STORAGE_KEY);
  }

  return { history, addEntry, clearHistory };
}
