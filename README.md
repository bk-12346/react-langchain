# ReAct Agent with LangChain and OpenAI

This project demonstrates a simple ReAct (Reasoning and Acting) agent built using the LangChain framework and OpenAI's language models. The agent is designed to use a custom tool to answer questions by thinking about the problem, deciding which tool to use, and then executing it.

Features
--------

-   **ReAct Agent:** The core of the project is a ReAct agent that reasons about a user's input before taking an action.

-   **Custom Tool:** Includes a custom `get_text_length` tool that the agent can use to perform a specific task (calculating the length of a string).

-   **LangChain Integration:** Utilizes LangChain's components like `PromptTemplate`, `ChatOpenAI`, and `ReActSingleInputOutputParser` to create the agent workflow.

-   **Custom Callback Handler:** Features a custom `AgentCallBackHandler` to log the agent's thought process and the LLM's responses, providing transparency into its operation.

Prerequisites
-------------

Before running this project, you need to have Python installed. You also need to set up your OpenAI API key.

-   **Python 3.8+**

-   **OpenAI API Key**: Sign up for an account and get your API key from the [OpenAI platform](https://platform.openai.com/).

Installation
------------

1.  **Clone the repository:**

    Bash

    ```
    git clone https://github.com/bk-12346/react-langchain
    cd react-langchain

    ```

2.  **Create and activate a virtual environment** (recommended):

    Bash

    ```
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate

    ```

3.  **Install the required packages:**

    Bash

    ```
    pip install -r requirements.txt

    ```


Setup
-----

1.  **Create a `.env` file** in the root of your project directory.

2.  **Add your OpenAI API key** to the `.env` file in the following format:

    ```
    OPENAI_API_KEY="your_api_key_here"

    ```

Usage
-----

To run the agent, simply execute the `main.py` file from your terminal:

Bash

```
python main.py

```

The script will initiate the agent with a predefined input and print out the agent's thought process, the tool it uses, and the final observation.

Code Structure
--------------

-   `main.py`: The main script that sets up the LangChain agent, defines the tools, and runs the agent's workflow.

-   `callbacks.py`: Contains the `AgentCallBackHandler` class, which logs the prompts sent to the LLM and the responses received.

-   `.env`: A file to securely store your API keys and other sensitive information.
