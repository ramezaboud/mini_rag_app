from .providers import QdrantDBProvider
from .VectorDBEnums import VectorDBTypeEnum
from controllers.BaseController import BaseController

class VectorDBProviderFactory:
    
    def __init__(self, config: dict):
        self.config = config
        self.base_controller = BaseController()

    def create(self, provider: str):
        
        if provider ==  VectorDBTypeEnum.QDRANT.value:

            dp_path = self.base_controller.get_database_path(self.config.VECTOR_DB_PATH)

            return QdrantDBProvider(
                dp_path = dp_path,
                distance_method = self.config.VECTOR_DB_DISTANCE_METHOD
            )
        
        return None
        