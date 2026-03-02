from .providers import CoHereProvider, OpenAIProvider
from .LLMEnums import LLMEnum

class LLMProviderFactory:

    def __init__(self, config: dict):
        self.config = config

    def create(self, provider: str):

        if provider == LLMEnum.OPENAI.value:
            return OpenAIProvider(
                api_key = self.config.OPENAI_API_KEY,
                api_url = self.config.OPENAI_API_URL,
                default_input_max_characters = self.config.OPENAI_DEFAULT_INPUT_MAX_CHARACTERS,
                default_generation_max_output_tokens = self.config.OPENAI_DEFAULT_GENERATION_MAX_OUTPUT_TOKENS,
                default_generation_temperature = self.config.OPENAI_DEFAULT_GENERATION_TEMPERATURE
            )

        if provider == LLMEnum.COHERE.value:
            return CoHereProvider(
                api_key = self.config.COHERE_API_KEY,
                default_input_max_characters = self.config.COHERE_DEFAULT_INPUT_MAX_CHARACTERS,
                default_generation_max_output_tokens = self.config.COHERE_DEFAULT_GENERATION_MAX_OUTPUT_TOKENS,
                default_generation_temperature = self.config.COHERE_DEFAULT_GENERATION_TEMPERATURE
            )

        return None
    