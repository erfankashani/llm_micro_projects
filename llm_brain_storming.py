# in this script we will make an llm that has multi options:
# Inputs:
# - system_prompt: str
# - user_prompt: str
# - model: str
# - toggles for adding 'mental_model'
# - section to add mental models

# system_prompt = "You are a brainstorming partner that asks questions about what the user wants to brainstom 
# based on the mental_models selected. You shall not provide final answers but ask qustions based on the mental_model 
# that applies to the brainstorming subject.

# the llm will take the user_prompt and attaches mental_models. and generate a response based on the model selected


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
from helper.prompt.prompt_params import format_response
from abc import ABC, abstractmethod
import gradio as gr

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
validate_openai_api_key(openai_api_key)

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
validate_anthropic_api_key(anthropic_api_key)

google_api_key = os.getenv('GOOGLE_API_KEY')
validate_google_api_key(google_api_key)

def brainstorm(user_prompt:str, model_name:str, mental_models:list):
    "Ask the models to brainstorm"
    print("this function is to get jokes from different AI models:")
    system_prompt = """
        You are a brainstorming partner to help consult on an idea with the user.
        You are not allowed to provide your own bais into the argument unless you can provide source for your hypothesis.
        The brainstorming will take the subject in mind and apply the chosen mental models to the idea. 
        As a partner you are not able to provide final answers/ideas based on the mental model but you are supposed to analuze the brainstorming topic
        based on the mental model and ask questions to help the user think about the subject in respect to that mental model.
        you can first itterate which mental model you considering and then ask the questions that allow the user to look at the topic from the mental models prepsective.
    """
    # user_prompt = "Tell me about the future of AI in healthcare"
    print(f"\nUser Prompt: {user_prompt}")
    print(f"\nSelected Model: {model_name}")
    print(f"\nSelected Mental Models: {mental_models}")
    user_prompt += "\n\nMental Models:\n"
    for model in mental_models:
        user_prompt += f"{model} - {mental_models_dict[model]}\n"
    
    # format the response format
    # user_prompt += format_response

    # repeat the ask to refresh the context attention
    user_prompt += "\n\nPlease ask questions based on the mental models to help brainstorm the topic."
    
    print(f"\nSystem Prompt: {system_prompt}")
    print(f"\nUser Prompt: {user_prompt}")
    
    response = ""
    if model_name == "GPT-3.5":
        gpt_3_5_turbo = OpenAILLM(system_prompt, "gpt-3.5-turbo", "GPT-3.5 Turbo")
        response = gpt_3_5_turbo.generate_text(user_prompt=user_prompt)
    elif model_name == "GPT-4-o-mini":
        gpt_4_o_mini = OpenAILLM(system_prompt, "gpt-4o-mini", "GPT-4 O Mini")
        response = gpt_4_o_mini.generate_text(user_prompt=user_prompt)
    elif model_name == "Claude-3.5":
        claude_3_5_sonnet = AnthropicLLM(system_prompt, "claude-3-5-sonnet-20240620", "Claude 3.5 Sonnet")
        response = claude_3_5_sonnet.generate_text(user_prompt=user_prompt)
    else:
        gemini_1_5_flash = GoogleLLM(system_prompt, "gemini-1.5-flash", "Gemini 1.5 Flash")
        response = gemini_1_5_flash.generate_text(user_prompt=user_prompt)
    
    return response

mental_models_dict = {
    "80/20 Rule": "Focus on the 20% of efforts that yield 80% of the results to maximize efficiency.",
    "Utilize Leverage": "Identify and use resources, skills, tools, or technologies that can amplify your results out of the same efforts you put in.",
    "lean on your strengths": "Identify your unique strengths, gifts, skills, and traits that you are good at, find who values them the most, what size of pain do the skills solve, What is the industry size, resources, margins, which your customer owns to spend on you.",
    "First Principles Thinking": "Break down complex problems into their fundamental parts and reassemble them from the ground up.",
    "Inversion": "Think about what you want to avoid or the opposite of your goal to gain clarity on your objectives.",
    "Systems Thinking": "Understand how different parts of a system interact and influence each other to identify leverage points for change.",
    "Design Thinking": "Empathize with users, define problems, ideate solutions, prototype, and test to create user-centered designs.",
    "Lean Startup": "Build, measure, learn in cycles to validate ideas quickly and efficiently.",
    "Agile Methodology": "Iterate rapidly based on feedback to adapt to changing requirements and improve outcomes. be quick to start and iterate your ideas, put out your work as soon and as much as you can. it is fine to be late in finishing the end product."
}

gr.Interface(fn=brainstorm, 
             inputs=[gr.Textbox(label="What is on your mind:"), gr.Dropdown(["GPT-3.5", "GPT-4-o-mini", "Claude-3.5", "Gemini-1.5"], label="Select model", value="GPT-3.5"), gr.Dropdown(list(mental_models_dict.keys()), label="Select Mental Model", multiselect=True)],
             outputs=[gr.Markdown(label="Brainstorm Idea:")], 
             flagging_mode="never"
            ).launch(inbrowser=True, share=True)