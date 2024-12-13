# steps setup the keys in the .env file
# OPENAI_API_KEY=xxxx
# ANTHROPIC_API_KEY=xxxx
# GOOGLE_API_KEY=xxxx

import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import google.generativeai
from helper.utils import validate_openai_api_key, validate_anthropic_api_key, validate_google_api_key, LLMConversation
from helper.llm_models import OpenAILLM, AnthropicLLM, GoogleLLM
from abc import ABC, abstractmethod

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
validate_openai_api_key(openai_api_key)

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
validate_anthropic_api_key(anthropic_api_key)

google_api_key = os.getenv('GOOGLE_API_KEY')
validate_google_api_key(google_api_key)



def get_jokes():
    "Ask the models to generate jokes"
    print("this function is to get jokes from different AI models:")

    system_prompt = "You are an assistant that is great at telling jokes"
    user_prompt = "Tell a light-hearted joke for an audience of Data Scientists"
    gpt_3_5_turbo = OpenAILLM(system_prompt, "gpt-3.5-turbo", "GPT-3.5 Turbo")
    print("\nGPT-3.5 Turbo:")
    print("----------------")
    print(gpt_3_5_turbo.generate_text(user_prompt=user_prompt))


    gpt_4_o_mini = OpenAILLM(system_prompt, "gpt-4o-mini", "GPT-4 O Mini")
    print("\nGPT-4 Omega Mini:")
    print("----------------")
    print(gpt_4_o_mini.generate_text(user_prompt=user_prompt))


    claude_3_5_sonnet = AnthropicLLM(system_prompt, "claude-3-5-sonnet-20240620", "Claude 3.5 Sonnet")
    print("\nClaude 3.5 Sonnet:")
    print("----------------")
    print(claude_3_5_sonnet.generate_text(user_prompt=user_prompt))


    gemini_1_5_flash = GoogleLLM(system_prompt, "gemini-1.5-flash", "Gemini 1.5 Flash")
    print("\nGemini 1.5 Flash:")
    print("----------------")
    print(gemini_1_5_flash.generate_text(user_prompt=user_prompt))


def run_conversation():
    "Run a conversation between the three models"
    print("----------------")
    print("\nthis function is to run a conversation between the three models:")

    pgt_system_prompt = "You are a chatbot who is very argumentative; \
    you disagree with anything in the conversation and you challenge everything, in a snarky way."
    gpt_3_5_turbo = OpenAILLM(pgt_system_prompt, "gpt-3.5-turbo", "Peter Griffin Turbo")

    claude_system_prompt = "You are a very polite, courteous chatbot. You try to agree with \
    everything the other person says, or find common ground. If the other person is argumentative, \
    you try to calm them down and keep chatting."
    claude_3_5_sonnet = AnthropicLLM(claude_system_prompt, "claude-3-5-sonnet-20240620", "Claudia Sunnies")

    gpt_joker_system_prompt = "You are an assistant that is great at telling jokes middle of serious conversation"
    gpt_joker = OpenAILLM(gpt_joker_system_prompt, "gpt-3.5-turbo", "Geppetto Joker")
    
    # llm_conversation = LLMConversation(model_array=[gpt_3_5_turbo, claude_3_5_sonnet, gpt_joker], initial_dialogs=["hi there", "hi", "howdey"],conversation_round=3)
    llm_conversation = LLMConversation(model_array=[gpt_3_5_turbo, claude_3_5_sonnet, gpt_joker], initial_dialogs=[],conversation_round=3)
    llm_conversation.print_conversation()
    print("\nConversation Array: ")
    print(llm_conversation.get_conversation_array())

# get the jokes
get_jokes()

# get the conversation
run_conversation()