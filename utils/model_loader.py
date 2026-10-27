
import os
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from utils.config_loader import load_config


class ConfigLoader:
    def __init__(self):
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]


class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    model_config = {"arbitrary_types_allowed": True}

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()

    def load_llm(self):
        if self.model_provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY is missing from .env")

            model_name = self.config["llm"]["groq"]["model_name"]
            return ChatGroq(
                model=model_name,
                api_key=api_key,
                temperature=0
            )

        if self.model_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY is missing from .env")

            model_name = self.config["llm"]["openai"]["model_name"]
            return ChatOpenAI(
                model=model_name,
                api_key=api_key,
                temperature=0
            )

        raise ValueError(
            f"Unsupported model provider: {self.model_provider}"
        )
