from enum import Enum

class LLMEnum(Enum):

    OPENAI = "OPENAI"
    COHERE = "COHERE"


class OpenAIEnums(Enum):

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "CHATBOT"

class CohereEnums(Enum):

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    DOCUMENT = "search_document"
    QUERY = "search_query"


class DocumentTypeEnum(Enum):

    DOCUMENT = "search_document"
    QUERY = "search_query"