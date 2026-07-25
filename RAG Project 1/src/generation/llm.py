import requests
from config import LLAMA_URL

class LLM:

    def __init__(
        self,
        url= LLAMA_URL
    ):
        self.url = url

    def stream(self, prompt):

        response = requests.post(
            self.url,
            json={
                "prompt": prompt,
                "temperature": 0.2,
                "n_predict": 512,
                "stop": [
                    "<|im_end|>"
                ],
                "stream": True
            },
            stream=True
        )


        response.raise_for_status()


        for line in response.iter_lines():

            if line:

                line = line.decode("utf-8")


                # llama.cpp sends:
                # data: {"content":"hello"}

                if line.startswith("data:"):

                    data = line.replace(
                        "data:",
                        ""
                    ).strip()


                    if data == "[DONE]":
                        break


                    yield data
                    
    def generate(self, prompt):

        response = requests.post(
            self.url,
            json={
                "prompt": prompt,
                "temperature": 0.2,
                "n_predict": 512,
                "stop": [
                    "<|im_end|>"
                ]
            }
        )


        response.raise_for_status()

        return response.json()["content"]