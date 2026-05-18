from src.evaluation.gemini_evaluator import (
    ask_gemini
)


question = (
    "Who won the FIFA World Cup in 2018?"
)

answer = ask_gemini(question)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)