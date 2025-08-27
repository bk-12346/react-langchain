from dotenv import load_dotenv
load_dotenv()

from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.tools.render import render_text_description
from langchain_openai import ChatOpenAI
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_core.agents import AgentAction, AgentFinish
from typing import Union, List
from langchain.tools import Tool
from callbacks import AgentCallBackHandler


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with: {text=}")
    text = text.strip("'\n").strip('"')


    return len(text)

def find_tool_by_name(tools: List[Tool], tool_name:str) -> Tool:
    """Helper function to find a tool by its name from a list of tools."""
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found.")

if __name__ == "__main__":
    print("Hello, World!")
    # print(get_text_length.invoke(input={"text": "Hello, World!"}))

    tools = [get_text_length]   # list of tools that we will now supply to our react agent
    # providing a prompt that will help select the right tool
    template = """
    {instructions}

    TOOLS:
    ------
    You have access to the following tools:
    {tools}

    To use a tool, please use the following format:
    ```
    Thought: Do I need to use a tool? Yes
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ```

    When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
    ```
    Thought: Do I need to use a tool? No
    Final Answer: [your response here]
    ```

    Begin!

    Previous conversation history:
    {chat_history}

    New input: {input}
    {agent_scratchpad}
    """
    # agent_scratchpad has all the history of the ReAct agent
    # define the prompt, using .partial() so that it fills all the values in the placeholders
    # input variable will come from the user
    prompt = PromptTemplate.from_template(template=template).partial(
        instructions="You are a helpful AI assistant that helps people find information.",
        # tools=tools,    # we want to give tools a string b/c llm only takes text as input, tools is not a list rather a list of tool objects
        tools= render_text_description(tools),
        tool_names=", ".join([tool.name for tool in tools]),
        chat_history="",  # no chat history for now
    )

    # define the llm which is going to be the reasoning agent
    # using stop to stop the tell the llm to stop generating words and finish working once it has outputted \n observation token
    # we need it b/c otherwise the llm will keep guessing one word after another and we want observation to come from tool
    # if it comes from the llm, it is simply a hallucination
    llm = ChatOpenAI(temperature=0, stop=["Observation:"], callbacks=[AgentCallBackHandler()])

    # if we get a parse error, issue is almost always with the indentation of the promt template we copied, adjust the stop token arguments accordingly

    agent = {"input": lambda x: x["input"], "agent_scratchpad": lambda x: x["agent_scratchpad"]} | prompt | llm | ReActSingleInputOutputParser() # we want to give it a dictionary as an input, input taken when we use invoke

    agent_step : Union[AgentAction, AgentFinish] = agent.invoke({"input": "What is the length of the text 'Hello, World!'?", "agent_scratchpad": ""})
    print(agent_step)

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input    # to call the tool

        observation = tool_to_use.func(str(tool_input))  #results of running the tool

        print(f"Observation: {observation}")
