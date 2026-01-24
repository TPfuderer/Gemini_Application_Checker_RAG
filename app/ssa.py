from rag.llm.gemini_client import load_gemini, generate_answer

client = load_gemini()

answer = generate_answer(
    client,
    context="",
    question="Say hello in one short sentence."
)

print("Gemini says:", answer)

