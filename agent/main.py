from google import genai
import os
from google.genai import types
from dotenv import load_dotenv
from google.genai.types import Part
from rich import print_json

class Agent:
    """A simple AI agent that can answer questions in a multi-turn conversation"""

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model =  "gemini-2.5-flash"
        self.system_message = "You are a helpful assistant that breaks down problems into steps and solves them systematically"
        # short term memory
        self.messages = []

    
    def chat(self, message):
        
        """Process a user message and return a response"""

        # inject user message
        self.messages.append({
            "role" : "user",
            "content" : message
        })

        response = self.client.models.generate_content(
            model=self.model,
            contents=types.Part.from_text(text=message),
            config=types.GenerateContentConfig(
                temperature = 0,
                top_p = 0.95,
                top_k = 20,
            )
        )


        # inject llm response
        self.messages.append({
            "role" : "assistant",
            "content" : response.text
        })

        return response

    def list_available_models(self):
        print("Available Models:")  
        model_names = [m.name for m in self.client.models.list()]
        for name in model_names:
            print(f"- {name}")
            return model_names
    


def main():

    load_dotenv()

    print("Agent starting!")
    
    agent = Agent()

    

    #print(agent.list_available_models())

    response1 =  agent.chat("I have 5 apples. How many do you have?")
    print_json(data=response1.text)

    response2 = agent.chat("i ate 1 apple. how many are left now?")
    print_json(data=response2.text)



    


if __name__ == "__main__":

    main()
