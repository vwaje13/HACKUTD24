from typing import List, Dict, Any
import os
import logging
from InstructorEmbedding import INSTRUCTOR
from langchain.schema import Document
from langchain_core.output_parsers import StrOutputParser  # Fixed this import
from langchain.storage import InMemoryByteStore
from langchain.vectorstores import Chroma
from chromadb.config import Settings
from unstructured.partition.pdf import partition_pdf
import uuid
from pdf2image import convert_from_path
import PyPDF2
from utils.model_wrappers.api_gateway import APIGateway
import config

logger = logging.getLogger(__name__)

class DocumentHandler:
    def __init__(self):
        try:
            # Initialize the INSTRUCTOR model without the token parameter
            self.embedding_model = INSTRUCTOR('hkunlp/instructor-base')
        except Exception as e:
            logging.error(f"Error initializing embedding model: {str(e)}")
            raise Exception(f"Failed to initialize embedding model: {str(e)}")
        self.collection_id = str(uuid.uuid4())
        self.embeddings = APIGateway.load_embedding_model(
            type=config.EMBEDDING_CONFIG["type"],
            batch_size=config.EMBEDDING_CONFIG["batch_size"],
            coe=config.EMBEDDING_CONFIG["coe"],
            select_expert=config.EMBEDDING_CONFIG["select_expert"]
        )
        self.vector_store = None
        self.initialize_vector_store()

    def initialize_vector_store(self):
        """Initialize the vector store with Chroma"""
        collection_name = f'collection_{self.collection_id}'
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            client_settings=Settings(anonymized_telemetry=False)
        )
        self.docstore = InMemoryByteStore()

    def process_pdf(self, filepath: str) -> List:
        """Process a PDF file and extract its content"""
        try:
            logger.info(f"Reading PDF for file: {filepath} ...")
            
            # First try using PyPDF2
            try:
                with open(filepath, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    documents = []
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        text = page.extract_text()
                        documents.append(Document(page_content=text, metadata={"page": page_num + 1}))
                    return documents
            except Exception as e:
                logger.warning(f"PyPDF2 failed, trying pdf2image: {str(e)}")
                
            # If PyPDF2 fails, try pdf2image
            images = convert_from_path(filepath)
            documents = []
            for i, image in enumerate(images):
                # Here you might want to use OCR (e.g., pytesseract) to extract text from images
                # For now, we'll just acknowledge we got the page
                documents.append(Document(
                    page_content=f"Page {i+1} content",
                    metadata={"page": i + 1}
                ))
            return documents
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            if "poppler" in str(e).lower():
                raise Exception(
                    "Poppler is not installed. Please install poppler-utils:\n"
                    "- For macOS: brew install poppler\n"
                    "- For Ubuntu: sudo apt-get install poppler-utils\n"
                    "- For Windows: Download from http://blog.alivate.com.au/poppler-windows/"
                )
            raise

    def process_document(self, file_path: str, metadata: Dict[str, Any] = None) -> None:
        """Process document and store in vector database"""
        documents = self.process_pdf(file_path)
        
        if metadata:
            for doc in documents:
                doc.metadata.update(metadata)

        # Generate unique IDs for documents
        doc_ids = [str(uuid.uuid4()) for _ in documents]
        
        # Add documents to vector store
        docs_for_vector_store = [
            Document(page_content=doc.page_content, metadata={'doc_id': doc_ids[i]})
            for i, doc in enumerate(documents)
        ]
        self.vector_store.add_documents(docs_for_vector_store)
        
        # Store original documents in docstore
        self.docstore.mset(list(zip(doc_ids, documents)))

    def search_documents(self, query: str, k: int = 5) -> List[Document]:
        """Search documents with a query"""
        if not self.vector_store:
            return []
        
        results = self.vector_store.similarity_search(
            query, 
            k=k
        )
        return results

    def get_all_investment_data(self) -> List[Dict[str, Any]]:
        """Retrieve all investment-related information"""
        results = self.search_documents(
            "Find all investment and stock related information", 
            k=config.K_RETRIEVED_DOCUMENTS
        )
        return [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]