from retrieval.retriever import retrieve
from generation.prompt_builder import build_prompt
from generation.llm import LLM



def main():

    llm = LLM()

    print("Ancient Greece RAG")
    print("Type exit to quit\n")


    while True:

        question = input("Question: ")


        if question.lower() == "exit":
            break


        results = retrieve(
            question,
            k=5
        )


        prompt = build_prompt(
            question,
            results
        )


        answer = llm.generate(
            prompt
        )


        print("\nAnswer:")
        print(answer)

        print("\nFurther reading:")

        shown = set()

        for result in results:

            key = (result["source"], result["section"])

            if key in shown:
                continue

            shown.add(key)

            print(
                f"'{result['section']}' section of the "
                f"'{result['source']}' Wikipedia page:"
            )

            print(result["url"])

        print("\n" + "=" * 80)



if __name__ == "__main__":
    main()