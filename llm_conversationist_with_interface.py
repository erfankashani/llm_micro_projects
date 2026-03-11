# steps setup the keys in the .env file
# OPENAI_API_KEY=xxxx
# ANTHROPIC_API_KEY=xxxx
# GOOGLE_API_KEY=xxxx

import os
from dotenv import load_dotenv
from helper.utils import validate_openai_api_key, validate_anthropic_api_key, validate_google_api_key, LLMConversation
from helper.llm_models import OpenAILLM, AnthropicLLM, GoogleLLM
import gradio as gr

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
validate_openai_api_key(openai_api_key)

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
validate_anthropic_api_key(anthropic_api_key)

google_api_key = os.getenv('GOOGLE_API_KEY')
validate_google_api_key(google_api_key)



def get_jokes(model_name:str):
    "Ask the models to generate jokes"
    print("this function is to get jokes from different AI models:")
    system_prompt = "You are an assistant that is great at telling jokes"
    user_prompt = "Tell a light-hearted joke for an audience of Data Scientists"
    response = ""
    if model_name == "GPT-3.5":
        gpt_3_5_turbo = OpenAILLM(system_prompt, "gpt-3.5-turbo", "GPT-3.5 Turbo")
        print("\nGPT-3.5 Turbo:")
        print("----------------")
        response = gpt_3_5_turbo.generate_text(user_prompt=user_prompt)
    elif model_name == "GPT-4-o-mini":
        gpt_4_o_mini = OpenAILLM(system_prompt, "gpt-4o-mini", "GPT-4 O Mini")
        print("\nGPT-4 Omega Mini:")
        print("----------------")
        response = gpt_4_o_mini.generate_text(user_prompt=user_prompt)
    elif model_name == "claude-sonnet-4-6":
        claude_sonnet_4_6 = AnthropicLLM(system_prompt, "claude-sonnet-4-6", "Claude Sonnet 4.6")
        print("\nClaude 4.6 Sonnet:")
        print("----------------")
        response = claude_sonnet_4_6.generate_text(user_prompt=user_prompt)
    else:
        gemini_2_5_flash = GoogleLLM(system_prompt, "gemini-2.5-flash", "Gemini 2.5 Flash")
        print("\nGemini 2.5 Flash:")
        print("----------------")
        response = gemini_2_5_flash.generate_text(user_prompt=user_prompt)
    return response


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
    claude_sonnet_4_6 = AnthropicLLM(claude_system_prompt, "claude-sonnet-4-6", "Claudia Sunnies")

    gpt_joker_system_prompt = "You are an assistant that is great at telling jokes middle of serious conversation"
    gpt_joker = OpenAILLM(gpt_joker_system_prompt, "gpt-3.5-turbo", "Geppetto Joker")
    
    # llm_conversation = LLMConversation(model_array=[gpt_3_5_turbo, claude_sonnet_4_6, gpt_joker], initial_dialogs=["hi there", "hi", "howdey"],conversation_round=3)
    llm_conversation = LLMConversation(model_array=[gpt_3_5_turbo, claude_sonnet_4_6, gpt_joker], initial_dialogs=[],conversation_round=3)
    llm_conversation.print_conversation()
    print("\nConversation Array: ")
    print(llm_conversation.get_conversation_array())

# get the jokes
# get_jokes()
gr.Interface(fn=get_jokes, 
             inputs=[gr.Dropdown(["GPT-3.5", "GPT-4-o-mini", "claude-sonnet-4-6", "Gemini-2.5"], label="Select model", value="GPT-3.5")], 
             outputs=[gr.Markdown(label="Joke:")], 
             flagging_mode="never"
            ).launch(inbrowser=True)

# get the conversation
# run_conversation()