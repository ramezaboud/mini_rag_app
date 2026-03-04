from enum import Enum

class VectorDBTypeEnum(Enum):
    QDRANT = "QDRANT"


class DistanceMethodEnum(Enum):
    COSINE = "cosine"
    DOT = "dot"