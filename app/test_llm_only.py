from rag.llm.gemini_client import get_client, generate_answer

def main():
    client = get_client()

    context = (
        "This project uses TF-IDF for text representation and "
        "Logistic Regression for classification."
    )
    question = "Explain the ML approach in simple terms."

    answer = generate_answer(
        client=client,
        context=context,
        question=question,
    )

    print("\n--- Gemini Answer ---")
    print(answer)


if __name__ == "__main__":
    main()
