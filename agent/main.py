from google import genai
import os
from google.genai import types
from dotenv import load_dotenv
from google.genai.types import Part
from rich import console, print_json
from rich.markdown import Markdown
from rich.console import Console



class CalculatorTool():
    """A tool for performing mathematical calculations"""

    def get_schema(self):
        return {
            "name": "calculator",
            "description" : "performs basic mathematical calculations. use for a simple addition multiplication etc",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "expression" : {
                        "type" : "STRING",
                        "description" : "The mathematical expression to evaluate eg ('2+2', '10+5', '5*22')"
                    }
                },
                "required" :     ["expression"],
            }
        }

    

class Agent: 
    """A simple AI agent that can answer questions in a multi-turn conversation"""

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model =  "gemini-3-flash-preview"
        self.system_message = "You are a helpful expert assistant that breaks down problems into steps and solves them systematically."
        # short term memory
        self.messages = []
        self.console = Console()
        self.tools = []

    
    def _get_tool_schemas():




    def chat(self, message):
        
        """Process a user message and return a response"""

        # inject user message
        self.messages.append({
            "role" : "user",
            "parts" : [{"text": message}] 
        })

        
        response = self.client.models.generate_content(
            model=self.model,
            contents=self.messages,
            config=types.GenerateContentConfig(
                system_instruction= self.system_message,
                temperature = 0.8,
                tools=self.tools,
               # top_p = 0.95,
                #top_k = 20,
            )
        )
        print(dir(response))



        # inject llm response
        self.messages.append({
            "role" : "model",
            "parts" : [{"text": message}]
        })

        return response

    def render(self, text):
        md = Markdown(text)
        self.console.print(md)

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

    res1 =  agent.chat("I have 5 apples. How many do you have?")
    agent.render(res1.text)



    res2 = agent.chat("i ate 1 apple. how many are left now?")
    agent.render(res2.text)

    res3 = agent.chat("what is 157.09 * 493.89")
    agent.render(res3.text)




    


if __name__ == "__main__":

    main()
