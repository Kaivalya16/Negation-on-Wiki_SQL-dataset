import ollama


MODEL_NAME = "qwen2.5:7b"


def ask_ollama(question,
                table_text=""):

    prompt = f"""
You are given the following table:

{table_text}

Answer the question using ONLY the table.

Question:
{question}

Return only the answer.
"""

    try:

        response = ollama.chat(

            model=MODEL_NAME,

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ]
        )

        return (
            response["message"]["content"]
            .strip()
        )

    except Exception as e:

        print("OLLAMA ERROR:", e)

        return None