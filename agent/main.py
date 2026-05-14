from typing import Self
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
                "type" : "OBJECT",
                "properties" : {
                    "expression" : {
                        "type" : "STRING",
                        "description" : "The mathematical expression to evaluate eg ('2+2', '10+5', '5*22')"
                    }
                },
                "required" :     ["expression"],
            }
        }

    def execute(self, expression):
        """Evaluate mathematical expressions"""

        try:
            result = eval(expression)
            return {"result": result}
        except:
            return {"error" :  "Invalid mathematical expression"}

    

class Agent:
    """A simple AI agent that can answer questions in a multi-turn conversation"""

    def __init__(self, tools):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model =  "gemma-4-26b-a4b-it"
        self.system_message = "You are a helpful expert assistant that breaks down problems into steps and solves them systematically."
        # short term memory
        self.messages = []
        self.console = Console()
        self.tools = tools
        self.tools_map = {tool.get_schema()["name"] : tool for tool in tools}


    def _get_tool_schemas(self):
        """Get tool schemas for all registered tools"""

        return types.Tool(
        function_declarations=[tool.get_schema() for tool in self.tools]
        )




    def chat(self, message):
        
        """Process a user message and return a response"""

        # inject user message
        self.messages.append({
            "role" : "user",
            "parts" : [{"text": message}] 
        })

        tool_config = types.Tool(
            function_declarations=[tool.get_schema() for tool in self.tools]
        )

        
        response = self.client.models.generate_content(
            model=self.model,
            contents=self.messages,
            config=types.GenerateContentConfig(
                system_instruction= self.system_message,
                temperature = 0.4,
                tools=[self._get_tool_schemas()],
               #top_p = 0.95,
                #top_k = 20,
            )
        )

        # Check for a function call
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            print(f"Function to call: {function_call.name}")
            print(f"ID: {function_call.id}")
            print(f"Arguments: {function_call.args}")
            #  In a real app, you would call your function here:
            #  result = schedule_meeting(**function_call.args)
        else:
            print("No function call found in the response.")
            print(response.text)
            
        for block in response:
            print(block)

        #print(dir(response))


        # inject llm response
        self.messages.append({
            "role" : "model",
            "parts" : [{"text": response.text}]
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


    calculator_tool = CalculatorTool()

    my_tools = [
        calculator_tool
    ]
    
    agent = Agent(my_tools)



    print(agent.list_available_models())

    res1 =  agent.chat("I have 5 apples. How many do you have?")
    agent.render(res1.text)



    res2 = agent.chat("i ate 1 apple. how many are left now?")
    agent.render(res2.text)

    res3 = agent.chat("what is 157.09 * 493.89")
    agent.render(res3.text)




    


if __name__ == "__main__":

    main()
