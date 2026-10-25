
import os
from typing import Literal, Optional, Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from utils.config_loader import load_config


load_dotenv()


class ConfigLoader:
    def __init__(self):
        print("Loading configuration...")
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]


class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(
        default=None,
        exclude=True
    )

    def model_post_init(self, __context: Any) -> None:
        if self.config is None:
            self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        """Load and return the selected language model."""

        print("Loading LLM...")
        print(f"Provider: {self.model_provider}")

        if self.model_provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")

            if not api_key:
                raise ValueError(
                    "GROQ_API_KEY is missing. "
                    "Check your .env file."
                )

            model_name = self.config["llm"]["groq"]["model_name"]

            print(f"Groq model: {model_name}")

            return ChatGroq(
                model=model_name,
                api_key=api_key
            )

        elif self.model_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY is missing. "
                    "Check your .env file."
                )

            model_name = self.config["llm"]["openai"]["model_name"]

            print(f"OpenAI model: {model_name}")

            return ChatOpenAI(
                model=model_name,
                api_key=api_key
            )

        raise ValueError(
            f"Unsupported model provider: {self.model_provider}"
        )
