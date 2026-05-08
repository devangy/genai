from google import genai
import os
from google.genai import types
from dotenv import load_dotenv
from google.genai.chats import Part


class Agent:

    def __init__(self):
        self.client = genai.Client()
        self.model =  "ge"
        self.system_message = "You are a lot helpful assistant that can break down problems into steps and solves them systematically"



    def chat(self, message):
        response = self.client.models.generate_content(
            model=self.model
            config=types.types.GenerateContentConfig(
                
            )
        )








def main():

    load_dotenv()
    print("Agent starting!")


    


if __name__ == "__main__":

    main()
