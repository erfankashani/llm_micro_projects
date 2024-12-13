from bs4 import BeautifulSoup
import requests
import markdown
from helper.llm_models import AbstractLLM

class Website:
    """
    A utility class to represent a Website that we have scraped
    """

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.body = response.content
        soup = self.get_soup(body=self.body)
        self.title = soup.title.string if soup.title else "No title found"
        self.text = soup.body.get_text(strip=True) if soup.body else ""
        self.links = self.get_links(soup=soup)


    def get_soup(self, body , page_type: str = 'html.parser') -> BeautifulSoup:
        soup = BeautifulSoup(body, page_type)
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
        return soup


    def get_links(self, soup: BeautifulSoup) -> list:
        return [link.get('href') for link in soup.find_all('a')]


    def get_contents(self) -> str:
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"


def generate_html_page(markdown_str: str, file_name: str) -> None:
    """
        Generate an HTML page from a markdown string
    """
    html = markdown.markdown(markdown_str)
    try:
        with open(file_name, 'w') as file:
            file.write(html)
        print(f"HTML page generated successfully in the path: {file_name}")
    except Exception as e:
        print(f"Error writing to file: {e}")


def validate_openai_api_key(api_key: str):
    """
    Check if the OpenAI API key is valid
    """
    if not api_key:
        raise ValueError("No API key was found; please set an OPENAI_API_KEY environment variable")
    elif not api_key.startswith("sk-proj"):
        raise ValueError("An API key was found, but it doesn't start sk-proj-; please check you're using the right key")
    elif api_key.strip() != api_key:
        raise ValueError("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them")
    else:
        print(f"OpenAI API Key exists and begins {api_key[:8]}")


def validate_anthropic_api_key(api_key: str):
    """
    Check if the Anthropic API key is valid
    """
    if api_key:
        print(f"Anthropic API Key exists and begins {api_key[:7]}")
    else:
        raise ValueError("No API key was found; please set an ANTHROPIC_API_KEY environment variable")


def validate_google_api_key(api_key: str):
    """
    Check if the Google API key is valid
    """
    if api_key:
        print(f"Google API Key exists and begins {api_key[:8]}")
    else:
        raise ValueError("No API key was found; please set a GOOGLE_API_KEY environment variable")


class LLMConversation():
    """
        This class constructs a conversation between multiple models regardless of type (OpenAI, Anthropic, Google)
        model_array: list of AbstractLLM objects
        initial_dialogs: list of strings which is the first user_prompt sent to each model. if this is empty, the conversation starts with no initial user_prompt.
        NOTE: the length of the initial_dialogs should be the same as the model_array
        conversation_round: number of rounds the conversation should last
    """
    def __init__(self, model_array: list[AbstractLLM], initial_dialogs: list[str], conversation_round: int):
        self.model_array = model_array #[gpt_3_5_turbo, claude_3_5_sonnet, gemini_1_5_flash]
        self.initial_dialogs = initial_dialogs # ["Hi there", "Hi", "Hey"]
        self.conversation_array = self.initiate_conversation_array() # integrate the initial dialogs
        self.conversation_round = conversation_round # 3


    def initiate_conversation_array(self):
        if len(self.initial_dialogs) == 0:
            return [[] for _ in range(len(self.model_array))] #[["a", "b", "c"], ["x", "y", "z"], ["i", "ii", "iii"]]
        else:
            if len(self.initial_dialogs) != len(self.model_array):
                raise ValueError("Initial dialogs should be the same length as the model array")
            return [[self.initial_dialogs[_]] for _ in range(len(self.model_array))]


    def print_conversation(self):
        skip_counter = 0
        for i in range(self.conversation_round):
            for seat_order, model in enumerate(self.model_array):
                # skip if we dealing with the initial dialogs
                if skip_counter >= len(self.initial_dialogs):
                    # print(f"conv_itter: {i}, seat_order: {seat_order}, asking model: {model.display_name}")
                    user_prompt = self.get_user_prompt(conv_itteration=i, seat_order=seat_order)
                    response = self.model_array[seat_order].generate_chat(user_prompt=user_prompt)
                    self.conversation_array[seat_order].append(response)
                
                skip_counter += 1
                print(f"\n{self.model_array[seat_order].display_name} (answer_{i}):")
                print(self.conversation_array[seat_order][i])


    def get_user_prompt(self, conv_itteration: int, seat_order: int):
        user_prompt = []
        for i in range(conv_itteration+1):
            for model_id, model in enumerate(self.model_array):
                if i == conv_itteration and model_id == seat_order:
                    # break if we reached the model that is answering the question
                    break
                conv = {"role": "assistant" if model_id == seat_order else "user", 
                        "content": self.conversation_array[model_id][i]
                        }
                user_prompt.append(conv)

        return user_prompt


    def get_conversation_array(self):
        return self.conversation_array