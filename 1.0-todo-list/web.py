import os
import streamlit as st
import functions
from PIL import Image

# Create the text file if not exists
FILE_NAME = "todos.txt"
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w") as f:
        pass

# Set page layout
st.set_page_config(layout="wide")

# Title and subtitles
st.title("Todo-App")
st.subheader("This is my todo app")
st.write("This app is to increase your productivity.")


# Input to enter new todo item
def handle_add_new_todo():
    new_todo_item = st.session_state["todo_item"]
    functions.append_todos(new_todo_item + "\n")
    st.session_state["todo_item"] = ""


todo_item = st.text_input(
    label="Enter a new todo item: ",
    placeholder="i.e Exercise",
    on_change=handle_add_new_todo,
    key="todo_item",
)


# Rendering list of todos


def handle_edit_todo(todo):
    todos = functions.read_todos()
    selected_idx = todos.index(todo)
    new_todo = st.session_state[f"edited_todo_item_{todo}"]
    todos[selected_idx] = new_todo + "\n"
    functions.write_todos(todos)


def handle_complete_todo(todo):
    todos = functions.read_todos()
    todos.remove(todo)
    functions.write_todos(todos)


todos = functions.read_todos()
for idx, todo in enumerate(todos):
    col1, col2, col3 = st.columns([8, 1, 1])
    with col1:
        checked = st.checkbox(
            todo,
            on_change=handle_complete_todo,
            args=(todo,),
        )
    with col3:
        clicked = st.button(
            "Edit",
            key=f"edit_button_{todo}",
            width="stretch",
        )

    if clicked:
        st.text_input(
            label="Edit this todo item: ",
            placeholder="i.e Exercise",
            on_change=handle_edit_todo,
            args=(todo,),
            key=f"edited_todo_item_{todo}",
        )
        with col2:
            closed = st.button(
                "Close",
                key=f"close_button_{todo}",
                width="stretch",
            )
            if closed:
                pass

st.space("large")

# convert images to grayscale
st.subheader("Grayscale Image Processing Visualization")

with st.expander("Convert a uploaded image into grayscale."):
    uploaded_image = st.file_uploader("Upload an image here")
    if uploaded_image:
        pil_img = Image.open(uploaded_image)
        gray_img = pil_img.convert("L")
        col1, col2, col3 = st.columns(3)
        with col2:
            st.image(gray_img, width="stretch")
