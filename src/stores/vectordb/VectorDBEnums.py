from enum import Enum

class VectorDBTypeEnum(Enum):
    QDRANT = "qdrant"


class DistanceMethodEnum(Enum):
    COSINE = "cosine"
    DOT = "dot"