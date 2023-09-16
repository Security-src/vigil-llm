import logging
import litellm

from typing import List, Optional, Union, Dict, Any


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLM:
    def __init__(self, model_name: str, api_key: Optional[str] = None, api_base: Optional[str] = None) -> None:
        self.name = 'llm'
        litellm.api_key = api_key
        self.api_base = api_base

        if model_name not in litellm.model_list:
            logger.error(f'[{self.name}] Model name not supported: {model_name}')
            raise ValueError("Model name not supported")

        if not litellm.check_valid_key(model=model_name, api_key=api_key):
            logger.error(f'[{self.name}] Invalid API key for model: {model_name}')
            raise ValueError("Invalid API key for model")

        self.model_name = model_name
        logger.info(f'[{self.name}] Loaded LLM API.')

    def generate(self, prompt: str, content_only: Optional[bool] = False) -> Union[str, Dict[str, Any]]:
        """Call configured LLM model with litellm"""
        logger.info(f'[{self.name}] Calling model: {self.model_name}')

        messages = [{"content": prompt, "role": "user"}]

        try:
            output = litellm.completion(
                model=self.model_name,
                messages=messages,
                api_base=self.api_base if self.api_base else None
            )
        except Exception as err:
            logger.error(f'[{self.name}] Failed to generate output for input data: {err}')
            raise

        return output['choices'][0]['message']['content'] if content_only else output
