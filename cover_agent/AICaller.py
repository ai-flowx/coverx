import datetime
import json
import os
import requests
import time

from functools import wraps
from wandb.sdk.data_types.trace_tree import Trace
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_fixed,
)

API_CHAT_COMPLETIONS = "/chat/completions"
MODEL_RETRIES = 3


def conditional_retry(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.enable_retry:
            return func(self, *args, **kwargs)

        @retry(stop=stop_after_attempt(MODEL_RETRIES), wait=wait_fixed(1))
        def retry_wrapper():
            return func(self, *args, **kwargs)

        return retry_wrapper()

    return wrapper


class AICaller:
    def __init__(
        self,
        model: str,
        api_base: str = "",
        api_key: str = "",
        enable_retry=True,
        max_tokens=16384,
    ):
        """
        Initializes an instance of the AICaller class.

        Parameters:
            model (str): The name of the model to be used.
            api_base (str): The base url of the API to be used.
            api_key (str): The key of the API to be used.
        """
        self.model = model
        self.api_base = api_base
        self.api_key = api_key
        self.api_url = self.api_base + API_CHAT_COMPLETIONS
        self.enable_retry = enable_retry
        self.max_tokens = max_tokens

    @conditional_retry  # You can access self.enable_retry here
    def call_model(self, prompt: dict, stream=True):
        """
        Call the language model with the provided prompt and retrieve the response.

        Parameters:
            prompt (dict): The prompt to be sent to the language model.
            stream (bool, optional): Whether to stream the response or not. Defaults to True.

        Returns:
            tuple: A tuple containing the response generated by the language model, the number of tokens used from the prompt, and the total number of tokens in the response.
        """
        if "system" not in prompt or "user" not in prompt:
            raise KeyError(
                "The prompt dictionary must contain 'system' and 'user' keys."
            )
        if prompt["system"] == "":
            messages = [{"role": "user", "content": prompt["user"]}]
        else:
            messages = [
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]},
            ]

        # Default completion parameters
        completion_params = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            response = requests.post(
                self.api_url, json=completion_params, headers=headers, stream=stream
            )
            response.raise_for_status()  # Raise an error for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Error calling LLM model: {e}")
            raise e

        if stream:
            chunks = []
            full_response = ""
            print("Streaming results from LLM model...")
            try:
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        chunk = line.strip()
                        print(chunk, end="", flush=True)
                        full_response += chunk
                        chunks.append(chunk)
                        time.sleep(0.01)  # Simulate natural response pacing

            except Exception as e:
                print(f"Error calling LLM model during streaming: {e}")
                if self.enable_retry:
                    raise e
            print("\n")

            # Build the final response from the streamed chunks
            model_response = {
                "model": self.model,
                "messages": messages,
                "response": full_response,
                "chunks": chunks,
            }
            content = model_response["response"]
            content_dict = json.loads(content)
            content = content_dict["choices"][0]["message"]["content"]
            print("Cleaned model response: ", content)
            prompt_tokens = len(prompt["user"])
            completion_tokens = len(full_response)
        else:
            # Non-streaming response is a CompletionResponse object
            json_response = response.json()
            content = json_response["choices"][0]["message"]["content"]
            prompt_tokens = json_response["usage"]["prompt_tokens"]
            completion_tokens = json_response["usage"]["completion_tokens"]

        if "WANDB_API_KEY" in os.environ:
            try:
                root_span = Trace(
                    name="inference_"
                    + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                    kind="llm",  # kind can be "llm", "chain", "agent", or "tool"
                    inputs={
                        "user_prompt": prompt["user"],
                        "system_prompt": prompt["system"],
                    },
                    outputs={"model_response": content},
                )
                root_span.log(name="inference")
            except Exception as e:
                print(f"Error logging to W&B: {e}")

        # Returns: Response, Prompt token count, and Completion token count
        return content, prompt_tokens, completion_tokens
