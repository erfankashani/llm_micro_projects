# steps setup the keys in the .env file
# OPENAI_API_KEY=xxxx
# ANTHROPIC_API_KEY=xxxx
# GOOGLE_API_KEY=xxxx

import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import google.generativeai
from abc import ABC, abstractmethod

# to load the keys from the .env file
load_dotenv()

# initiate the connections
openai = OpenAI()
claude = anthropic.Anthropic()
google.generativeai.configure()

# use each llm to generate text
class AbstractLLM(ABC):
    def __init__(self, system_prompt: str, model: str, display_name: str):
        self.system_prompt = system_prompt
        self.model = model
        self.display_name = display_name
    
    @abstractmethod
    def generate_text(self, user_prompt:str) -> str:
        pass

    def generate_chat(self, user_prompt:list) -> str:
        pass


class OpenAILLM(AbstractLLM):
    def generate_text(self, user_prompt:str) -> str:
        prompts = [
            {"role": "system", "content": self.system_prompt}, 
            {"role": "user", "content": user_prompt}
            ]
        completion = openai.chat.completions.create(model=self.model, messages=prompts)
        return completion.choices[0].message.content


    def generate_chat(self, user_prompt:list) -> str:
        system_prompt = [{"role": "system", "content": self.system_prompt}]
        prompts = system_prompt + user_prompt

        completion = openai.chat.completions.create(model=self.model, messages=prompts)
        return completion.choices[0].message.content


class AnthropicLLM(AbstractLLM):
    def generate_text(self, user_prompt:str) -> str:
        message = claude.messages.create(
            model=self.model, 
            max_tokens=200, 
            temperature=0.7,
            system=self.system_prompt, 
            messages= [{"role": "user", "content": user_prompt}]
        )
        return message.content[0].text


    def generate_chat(self, user_prompt:list) -> str:
        message = claude.messages.create(
            model=self.model, 
            max_tokens=200, 
            temperature=0.7,
            system=self.system_prompt, 
            messages= user_prompt
        )
        return message.content[0].text


class GoogleLLM(AbstractLLM):
    def generate_text(self, user_prompt:list) -> str:
        model = google.generativeai.GenerativeModel(
            model_name=self.model,
            system_instruction=self.system_prompt
        )
        response = model.generate_content(user_prompt)
        return response.text


    def generate_chat(self, user_prompt:list) -> str:
        last_dialog = user_prompt.pop()
        model = google.generativeai.GenerativeModel(
            model_name=self.model,
            system_instruction=self.system_prompt
        )
        chat = model.show_chat(
            history=user_prompt
        )
        response = chat.send_message(last_dialog)
        return response.text
