from app.rag.generator import generate

prompt = "Rewrite this requirement clearly: The system should be fast."

output = generate(prompt)

print(output)