export async function analyseRequirement(text: string) {
  const response = await fetch("http://localhost:8000/api/analyse", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: text,
      type: "functional",
      priority: "must",
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to analyse requirement");
  }

  return response.json();
}