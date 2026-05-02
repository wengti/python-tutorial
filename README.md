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


### 6.0 Flask-Weather-API, 6.1 Flask-Dict-API
1. Simple startup example:
* References: https://flask.palletsprojects.com/en/stable/quickstart/
```python
from flask import Flask

app = Flask(__name__)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'
```

2. What is returned in Flask?
* Plain string - an HTML element
* list or dict - automaticaly becomes JSON
* HTML template - discussed next

3. How to return a static HTML page?
* Key syntax: `render_template`
```python
@app.route("/")
def home():
    return render_template("home.html")
```

```
|_ templates
|   |_ home.html <-- where you should store the html page
|_ main.py
```

4. How to render a static image in the html?
* References: https://flask.palletsprojects.com/en/stable/tutorial/static/
* Key syntax: `{{}}` -> allowing you to write code in python/flask

```html
<body>
    <h1>Weather Data API!</h1>
    <img src="{{url_for('static', filename='icon.png')}}" />
</body>
```

```
|_ static
|   |_ icon.png <-- where you should store the html page
|_ main.py
```

5. How to pass a variable from flask to HTML?

* key syntax: `{{ | safe}}` - allows the browser to render the actual HTML tag, which otherwise will print out HTML tag as plain text.

```python
@app.route("/")
def home():
    return render_template("home.html", var_name=some_data)
```

```html
<body>
    <p>{{var_name | safe}}</p>
</body>
```

6. Catch error in Flask
```python
from Flask import abort, jsonify
@app.routes("/")
def home():
    abort(404, description="Invalid")

@app.errorhandler(404)
def handle_not_found(e):
    return jsonify(error=str(e)), 404
```

7. How to start the development of Flask App with hot-reloading
`$ flask --app hello run --debug`

### 6.2 Jupyter-Pandas
1. When using read csv files that has irrelevant rows beforehand, make use of the `skip_rows` argument.
```python
import pandas as pd
df = pd.read_csv("data_small/TG_STAID000001.txt",
                 skiprows=20)
```

2. Parse date when reading csv using pandas
* The purpose of `date_format` is only to match the date format from the data (as in to inform what is the date format only).
```python
df = pd.read_csv("data_small/TG_STAID000001.txt",
                 skiprows=20,
                 parse_dates=["    DATE"],
                 date_format="%Y%m%d", # Only to inform how is the date string format
                 )
```

3. Data indexing in Pandas



Method 1: []
* df[0] - **NOT ALLOWED*
* df[0:1] - **OK** - returned 0th row as a DataFrame
* df[0:2] - **OK** - returned 0th and 1st row as a DataFrame
* df["col_name"] - **OK** - returned the corresponding column as a series
* df[["col_name"]] - **OK** - returned the corresponding column as a DataFrame
* df[ ["col_name", "col_name2"] ] - **OK** - returned the corresponding columns as a DataFrame
* df[0:2, ["col_name", "col_name2"]] - **NOT ALLOWED**, for 2D selection, must use either loc or iloc


Method 2: loc[]
* df.loc[ [0,2], ["row2", "row3"] ] - **OK** - returned 0th and 2th row, with their "row2" and "row3" columns.
* df.loc[ :, : ] - **OK** - returned all rows and all columns
* df.loc[ 0:1, "row1":"row2" ] - **OK** - returned 0th and 1st row and their columns in "row1" and "row2"
* df.loc[ 0:1, "row2":"row1" ] - **NOT VALID** - because "row1" comes before "row2" in columns.

**VERY IMPORTANT CONCEPT** to clarify for using loc[]:
- The row label here is fixed for each row.
- Even after you filter, the first row in that filtered datafram still holds the same label as before.
- So if you already filter out 0th row and you try to reference using 0th row, it will attempt to find row with 0th label instead of the first entry in the filtered dataframe.

**To get the first row** after filtering, using [] or iloc[] where they refer to the current row position.


Method 3: iloc[]
* df.loc[ [0,2], [1,2] ] - **OK** - returned 0th and 2th row, with their "row2" and "row3" columns.
* df.loc[ :, : ] - **OK** - returned all rows and all columns
* df.loc[ 0:2, 0:2 ] - **OK** - returned 0th and 1st row and their columns in "row1" and "row2"


3.1 **Short Summary of indexing in Pandas**
a. []'s weaknesses:
* cannot do 2d query
* for row indexing, must be slicing

b. loc[]'s weaknesses
* row indexing refers to the original row index label instead of their actual row position

c. iloc[]'s weaknesses
* must use index for column indexing 


4. Selecting rows with conditioning
```python
df[df["row2"] > 3]
```

* `df["row2"] > 3` targets column "row2" and for each entry return either True or False based on the comparison which results in a sequence of `[True, False...]`
* As a result, it becomes `df[ [True, False...] ]`, where only the `True` row is returned.


5. Selecting rows with combined conditioning
* use bit operator (|, &) instead of python operator(and, or)
* wrap each condition with a parenthesis before the operation -- **IMPORTANT**
```python
df[ (df["row1"] > 1) & (df["row2"] > 0)  ]
```

6. Convert a row data into python native data
```python
df.loc[df["    DATE"] == "1860-01-01", "   TG"].squeeze().item()
```
* `.squeeze()` is to remove the index column
* `.item()` is to convet the data from numpy data to python native data

7. Conditioning by comparing year in datetime

```python
# Assuming that parse_date and date_formats are properly configured when loading the df

df_new = df[df["date"].dt.year === 2020]
```