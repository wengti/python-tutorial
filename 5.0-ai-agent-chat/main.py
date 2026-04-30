import os
import sqlite3
import uuid
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.messages import SystemMessage, HumanMessage
from datetime import date
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_tavily import TavilySearch
import gradio as gr

# Load API keys
load_dotenv()


# Tools
def get_current_date():
    """A function used to get the current date in yyyy-mm-dd format."""
    return date.today()


tavily_search_tool = TavilySearch(max_results=5)


checkpointer = SqliteSaver(
    sqlite3.connect(
        "checkpoint.db",
        check_same_thread=False,
    )
)
system_prompt = SystemMessage(
    content=[
        {
            "type": "text",
            "text": """
                You are a helpful AI assistant. 
                Please make use of the available tools whenever suitable to help answering the user's query.
                You should not question the validity of the tool while responding.
                """,
        }
    ]
)
model = ChatOllama(model="qwen2.5:3b")
agent = create_agent(
    model=model,
    tools=[get_current_date, tavily_search_tool],
    system_prompt=system_prompt,
    checkpointer=checkpointer,
)


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
