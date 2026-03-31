export async function analyseRequirement(text: string, useRag: boolean) {
  const response = await fetch("http://localhost:8000/api/analyse", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text,
      type: "functional",
      priority: "must",
      use_rag: useRag,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to analyse requirement");
  }

  return response.json();
}
