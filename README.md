# Python Tutorial


## Note:

### 1: Todo-List, 1.1: Zip-Gui
1. How to make a .exe file?
```bash
python -m PyInstaller <file_path> --onefile --windowed --clean <name.exe>
```

* --onefile: Instead of a folder filled with many .dll, .so, and library files, it produces one single file (e.g., myscript.exe on Windows or myscript on macOS/Linux).
* --windowed: Suppressing the terminal or command prompt window that otherwise appears when the program is launched
* --clean: clears the global PyInstaller cache and removes temporary build files (located in the build/ directory)

Note:
    - the module is installed as `pyinstaller`
    - However, to run it it is spelt in `PyInstaller`


2. How to run the app? (Assuming you are in the root folder of these apps)
- Deployed on Streamlit: https://wwt-py-todo.streamlit.app/
- Local development: `python -m streamlit run web.py`
- .exe file: `python -m PyInstaller.... (refer to above)` -> execute the .exe file in dist
- command line interface: `python -m cli`

3. Deployment on streamlit
- has issue with `+cpu` from `pytorch` in `requirements.txt`
- try to remove that to resolve it.


### 3.1 Nasa-Website
* Deployment: https://wt-nasa-website.streamlit.app/


### 5.0 AI-Agent-Chat
1. Local LLM using **ollama**
* Setup guide: https://docs.langchain.com/oss/python/integrations/chat/ollama

2. Creating an agent
* Difference between agent and model is that agent can invoke tools.
* Futher references: https://docs.langchain.com/oss/python/langchain/agents
```python
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=[get_current_date, tavily_search_tool],
    system_prompt=system_prompt,
    checkpointer=checkpointer,
)
```

3. Setting up a custom tool
* Important to write docstring to provide context for the LLM to know whether to use this tool
```python
def get_current_date():
    """A function used to get the current date in yyyy-mm-dd format."""
    return date.today()
```

4. Conversation Memory
* PART 1: Setting the checkpointer
    * References: 
        * https://docs.langchain.com/oss/python/langchain/short-term-memory
        * https://docs.langchain.com/oss/python/langgraph/persistence#checkpointer-libraries
    ```python
    from langgraph.checkpoint.sqlite import SqliteSaver
    import sqlite3

    checkpointer = SqliteSaver(
        sqlite3.connect(
            "checkpoint.db",
            check_same_thread=False,
        )
    )
    ```

* PART 2: Isolating different instances accessing the chatbot to avoid leaking of conversation history
    * Assign a unique thread id for each instance of conversation.
    * References: https://docs.langchain.com/oss/python/langchain/short-term-memory
    ```python
    result = agent.invoke(
        {"messages": [HumanMessage(message)]},
        {"configurable": {"thread_id": thread_id}}, 
    )
    ```

5. Gradio for a chat interface
```python
def get_response(message, history, thread_id):
    result = agent.invoke(
        {"messages": [HumanMessage(message)]},
        {"configurable": {"thread_id": thread_id}},
    )
    return result["messages"][-1].content


with gr.Blocks() as demo:
    thread_id = gr.State(value=lambda: str(uuid.uuid4()))
    gr.Markdown("# Chatbot")
    gr.ChatInterface(fn=get_response, additional_inputs=[thread_id])

demo.launch()
```
* By default `fn` in `ChatInterface` takes in 2 arguments: `message` and `history`
* use `gr.state` to pass in additional_inputs to the `fn` of `ChatInterface`, which is a unique uuid to isolate conversation instances.
    