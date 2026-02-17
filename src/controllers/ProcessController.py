from .BaseController import BaseController
from .ProjectController import ProjectController
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum
import os

class ProcessController(BaseController):

    def __init__(self,project_id:str):
        super().__init__()
        
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)


    def get_file_extention(self,file_id:str):
        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self,file_id:str):

        file_ext = self.get_file_extention(file_id=file_id)
        file_path = os.path.join(
            self.project_path,
            file_id
        )

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path,encoding="utf-8")

        elif file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)

        else: None

    def get_file_content(self,file_id:str):

        loader = self.get_file_loader(file_id=file_id)

        return loader.load()
    
    def process_file_content(self, file_content: list, file_id: str,
                            chunk_size: int=100, overlap_zize: int=20):

        text_spiliter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=overlap_zize,
            length_function=len )  

        file_content_text = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_spiliter.create_documents(
            file_content_text,
            metadatas=file_content_metadata   
        )

        return chunks