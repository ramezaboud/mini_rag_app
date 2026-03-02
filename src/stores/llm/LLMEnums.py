from enum import Enum

class LLMEnum(Enum):

    OPENAI = "OpenAI"
    COHERE = "Cohere"


class OpenAIEnums(Enum):

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
