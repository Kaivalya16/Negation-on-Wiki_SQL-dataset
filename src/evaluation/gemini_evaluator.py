from google import genai


client = genai.Client(
    api_key="AIzaSyC-KZr6vJBnM9ceLXPvWqAOUPiIjOuY6yA"
)


def ask_gemini(question,
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

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:

        print("GEMINI ERROR:", e)

        return None