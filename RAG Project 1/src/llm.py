import requests


class LLM:

    def __init__(
        self,
        url="http://127.0.0.1:8080/completion"
    ):
        self.url = url


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