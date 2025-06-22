import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
from helper.utils import validate_openai_api_key, validate_anthropic_api_key, validate_google_api_key, LLMConversation
from helper.llm_models import OpenAILLM, AnthropicLLM, GoogleLLM
from abc import ABC, abstractmethod
from pydantic import BaseModel

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
validate_openai_api_key(openai_api_key)

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
validate_anthropic_api_key(anthropic_api_key)

google_api_key = os.getenv('GOOGLE_API_KEY')
validate_google_api_key(google_api_key)

system_prompt = "You are an assistant that is great at telling jokes"
user_prompt = "Tell 3 light-hearted jokes for an audience of Data Scientists"

class Joke(BaseModel):
    joke_topic: str
    joke_list: list[str]
    joke_count: int


# gemini_1_5_flash = GoogleLLM(system_prompt, "gemini-1.5-flash", "Gemini 1.5 Flash")
# print("\nGemini 1.5 Flash:")
# print("----------------")
# # print(gemini_1_5_flash.generate_text(user_prompt=user_prompt))
# print(type(gemini_1_5_flash.generate_json(user_prompt=user_prompt, json_schema=Joke)))


gpt_4_o_mini = OpenAILLM(system_prompt, "gpt-4o-mini", "GPT-4 O Mini")
print("\nGPT-4 Omega Mini:")
print("----------------")
# print(gpt_4_o_mini.generate_text(user_prompt=user_prompt))
print(gpt_4_o_mini.generate_json(user_prompt=user_prompt, json_schema=Joke))