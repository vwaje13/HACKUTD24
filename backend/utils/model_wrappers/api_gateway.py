import os
import requests
from typing import Any, Dict, Optional, List
from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseMessage, ChatMessage
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class SambaNovaChatModel(BaseChatModel):
    """Custom chat model for SambaNova API"""
    
    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: int = 1200,
        api_base: str = "https://api.sambanova.ai/v1",
    ):
        """Initialize SambaNova Chat Model"""
        super().__init__()
        self.model = model
        self.api_key = api_key or os.getenv("SAMBANOVA_API_KEY")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_base = api_base

        if not self.api_key:
            raise ValueError("SambaNova API key not found")

    def _call(self, messages: list[BaseMessage], stop: Optional[list[str]] = None, **kwargs: Any) -> str:
        """Call the SambaNova API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Convert messages to the format expected by SambaNova
        formatted_messages = []
        for message in messages:
            role = "user"
            if isinstance(message, SystemMessage):
                role = "system"
            elif isinstance(message, AIMessage):
                role = "assistant"
            
            formatted_messages.append({
                "role": role,
                "content": message.content
            })

        data = {
            "model": self.model,
            "messages": formatted_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        if stop:
            data["stop"] = stop

        response = requests.post(
            f"{self.api_base}/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    @property
    def _llm_type(self) -> str:
        """Return identifier for the LLM type"""
        return "sambanova_chat"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

class APIGateway:
    """Simplified API Gateway for model access"""
    
    @staticmethod
    def load_chat(
        type: str = "sncloud",
        model: str = "Meta-Llama-3.1-70B-Instruct",
        temperature: float = 0.0,
        max_tokens: int = 1200,
        do_sample: bool = False,
        process_prompt: bool = True,
        sambanova_api_key: Optional[str] = None,
        **kwargs: Any
    ) -> BaseChatModel:
        """Load chat model with specified parameters"""
        if type != "sncloud":
            raise ValueError("Only 'sncloud' type is supported in this implementation")
            
        return SambaNovaChatModel(
            model=model,
            api_key=sambanova_api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )

    @staticmethod
    def load_embedding_model(
        type: str = "cpu",
        batch_size: Optional[int] = None,
        coe: bool = False,
        select_expert: Optional[str] = None,
        **kwargs: Any
    ) -> Embeddings:
        """Load embedding model with specified parameters"""
        if type != "cpu":
            raise ValueError("Only 'cpu' type is supported in this implementation")
            
        return HuggingFaceInstructEmbeddings(
            model_name="intfloat/e5-large-v2",
            embed_instruction="",
            query_instruction="Represent this sentence for searching relevant passages: ",
            encode_kwargs={"normalize_embeddings": True}
        )