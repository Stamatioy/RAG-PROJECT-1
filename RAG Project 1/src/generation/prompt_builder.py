def build_prompt(question, retrieved_chunks):

    context = ""

    for i, chunk in enumerate(retrieved_chunks):

        context += f"""
Source: {chunk['source']}

{chunk['text']}

---
"""


    prompt = f"""
<|im_start|>system
- You will be provided with 3 to 5 Sources, which  are going to be your knowledge base
- Afterwards you will be given a question.
- Your task is to extract the content from the Sections that is relevant to the question, to give a complete answer.

Rules:
- Do not use outside knowledge.
- Do not invent information.
- If the sources do not contain the answer, YOU MUST reply exactly:
"I do not have enough information in my knowledge base."
<|im_end|>

<|im_start|>user

Sources:

{context}

Question:
{question}

Answer:
<|im_end|>

<|im_start|>assistant
"""

    return prompt