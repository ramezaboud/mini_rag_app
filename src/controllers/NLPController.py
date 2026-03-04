from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import List
import json

class NLPController(BaseController):

    def __init__(self, vectordb_client, 
                 generation_client, embedding_client, ):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client


    def create_collection_name(self, project_id: str):
        return f"collection_{self.vectordb_client.default_vector_size}_{project_id}".strip()
    

    async def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return await self.vectordb_client.delete_collection(collection_name=collection_name)
    

    def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    

    async def index_into_vector_db(self, project: Project,
                                   chunks: List[DataChunk],
                                   chunks_ids: List[int],
                                   do_rest: bool = False):
        
        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: manage items
        tests = [
            chunk.chunk_text
            for chunk in chunks
        ]
        metadata = [
            chunk.chunk_metadata
            for chunk in chunks
        ]
        vectors = self.embedding_client.embed_text(text = tests,
                                                   document_id=DocumentTypeEnum.DOCUMENT.value)

        # step3: create collection if not exists
        _ = await self.vectordb_client.create_collection(collection_name = collection_name,
                                                         embedding_size = self.embedding_client.embedding_size,
                                                         do_rest = do_rest)

        # step4: insert into vector db
        _ = await self.vectordb_client.insert_many(collection_name = collection_name,
                                                  tests = tests,
                                                  metadata = metadata,
                                                  vectors = vectors,
                                                  record_ids = chunks_ids
                                                  )
        
        return True
            
        
        