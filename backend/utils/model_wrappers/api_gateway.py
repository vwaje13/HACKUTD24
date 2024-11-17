import logging
import os
import sys
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.llms import LLM
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.abspath(os.path.join(current_dir, '..'))
repo_dir = os.path.abspath(os.path.join(utils_dir, '..'))
sys.path.append(utils_dir)
sys.path.append(repo_dir)

from utils.model_wrappers.langchain_chat_models import ChatSambaNovaCloud, ChatSambaStudio
from utils.model_wrappers.langchain_embeddings import SambaStudioEmbeddings
from utils.model_wrappers.langchain_llms import SambaNovaCloud, SambaStudio

EMBEDDING_MODEL = 'intfloat/e5-large-v2'
NORMALIZE_EMBEDDINGS = True

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class APIGateway:
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

    @staticmethod
    def load_llm(
        type: str = "sncloud",
        model: str = "Meta-Llama-3.1-70B-Instruct",
        temperature: float = 0.0,
        max_tokens: int = 1200,
        do_sample: bool = False,
        coe: bool = False,
        streaming: bool = True,
        select_expert: Optional[str] = None,
        **kwargs: Any
    ) -> BaseChatModel:
        """Load chat model with specified parameters"""
        from langchain_chat_models import ChatSambaNovaCloud
        
        if type != "sncloud":
            raise ValueError("Only 'sncloud' type is supported in this implementation")
        
        # Get API key from environment
        api_key = os.getenv("SAMBANOVA_API_KEY")
        if not api_key:
            raise ValueError("SAMBANOVA_API_KEY environment variable not found")
            
        return ChatSambaNovaCloud(
            model=model,
            streaming=streaming,
            temperature=temperature,
            max_tokens=max_tokens,
            sambanova_api_key=SecretStr(api_key),  # Convert to SecretStr
            **kwargs
        )

    @staticmethod
    def load_chat(
        type: str,
        model: str,
        streaming: bool = False,
        max_tokens: int = 1024,
        temperature: Optional[float] = 0.0,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        do_sample: Optional[bool] = None,
        process_prompt: Optional[bool] = True,
        stream_options: Optional[Dict[str, bool]] = {'include_usage': True},
        special_tokens: Optional[Dict[str, str]] = {
            'start': '<|begin_of_text|>',
            'start_role': '<|begin_of_text|><|start_header_id|>{role}<|end_header_id|>',
            'end_role': '<|eot_id|>',
            'end': '<|start_header_id|>assistant<|end_header_id|>\n',
        },
        model_kwargs: Optional[Dict[str, Any]] = None,
        sambanova_url: Optional[str] = None,
        sambanova_api_key: Optional[str] = None,
        sambastudio_url: Optional[str] = None,
        sambastudio_api_key: Optional[str] = None,
    ) -> BaseChatModel:
        """
        Loads a langchain Sambanova chat model given some parameters
        Args:
            type (str): whether to use sambastudio, or SambaNova Cloud chat model "sncloud"
            model (str): The name of the model to use, e.g., llama3-8b.
            streaming (bool): whether to use streaming method. Defaults to False.
            max_tokens (int): Optional max number of tokens to generate.
            temperature (float): Optional model temperature.
            top_p (float): Optional model top_p.
            top_k (int): Optional model top_k.
            do_sample (bool): whether to do sampling
            process_prompt (bool): whether use API process prompt (for CoE generic v1 and v2 endpoints)
            stream_options (dict): stream options, include usage to get generation metrics
            special_tokens (dict): start, start_role, end_role and end special tokens
            (set for CoE generic v1 and v2 endpoints when process prompt set to false
            or for StandAlone v1 and v2 endpoints)
            default to llama3 special tokens
            model_kwargs (dict): Key word arguments to pass to the model.


            sambanova_url (str): Optional SambaNova Cloud URL",
            sambanova_api_key (str): Optional SambaNovaCloud API key.
            sambastudio_url (str): Optional SambaStudio URL",
            sambastudio_api_key (str): Optional SambaStudio API key.

        Returns:
            langchain BaseChatModel
        """

        if type == 'sambastudio':
            envs = {
                'sambastudio_url': sambastudio_url,
                'sambastudio_api_key': sambastudio_api_key,
            }
            envs = {k: v for k, v in envs.items() if v is not None}
            model = ChatSambaStudio(
                **envs,
                model=model,
                streaming=streaming,
                max_tokens=max_tokens,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                do_sample=do_sample,
                process_prompt=process_prompt,
                stream_options=stream_options,
                special_tokens=special_tokens,
                model_kwargs=model_kwargs,
            )

        elif type == 'sncloud':
            envs = {
                'sambanova_url': sambanova_url,
                'sambanova_api_key': sambanova_api_key,
            }
            envs = {k: v for k, v in envs.items() if v is not None}
            model = ChatSambaNovaCloud(
                **envs,
                model=model,
                streaming=streaming,
                max_tokens=max_tokens,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                stream_options=stream_options,
            )

        else:
            raise ValueError(f"Invalid LLM API: {type}, only 'sncloud' and 'sambastudio' are supported.")

        return model