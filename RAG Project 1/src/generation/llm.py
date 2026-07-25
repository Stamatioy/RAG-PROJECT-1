import requests
from config import LLAMA_URL
import json
from api.exceptions import LLMConnectionError

class LLM:

    def __init__(
        self,
        url= LLAMA_URL
    ):
        self.url = url


    def stream(self, prompt):

        try:
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
                stream=True,
                timeout=120
            )

            response.raise_for_status()


            for line in response.iter_lines():

                if line:

                    line = line.decode("utf-8")

                    if line.startswith("data:"):

                        data = line.replace(
                            "data:",
                            ""
                        ).strip()


                        if data == "[DONE]":
                            break


                        token = json.loads(data)["content"]

                        yield token


        except requests.exceptions.ConnectionError:
            raise LLMConnectionError(
                "Could not connect to the LLM server"
            )


        except requests.exceptions.Timeout:
            raise LLMConnectionError(
                "LLM server timed out"
            )


        except requests.exceptions.HTTPError:
            raise LLMConnectionError(
                "LLM server returned an error"
        )
            
                    
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