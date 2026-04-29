import datetime
import os

import FreeSimpleGUI as sg
import functions

# Check whether needed to create the files
TODO_FILE = "todos.txt"
if not os.path.exists(TODO_FILE):
    with open(TODO_FILE, "w") as f:
        pass

# Elements
sg.theme("Python")

welcome_text = sg.Text(
    "Welcome to the todo-list",
    font=("Helvetica", 20),
)
clock = sg.Text(
    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    font=("Helvetica", 10),
    text_color="white",
    key="clock",
)
input_text = sg.InputText(
    key="-INPUT_TEXT-",
)
add_btn = sg.Button(
    button_text="Add",
    key="-ADD_BTN-",
)
list_box = sg.Listbox(
    values=functions.read_todos(),
    size=(50, 20),
    key="-LIST_BOX-",
    enable_events=True,
)
edit_btn = sg.Button(
    button_text="Edit",
    key="-EDIT_BTN-",
)
complete_btn = sg.Button(
    button_text="Complete",
    key="-COMPLETE_BTN-",
)
exit_btn = sg.Button(
    button_text="Exit",
    key="-EXIT_BTN-",
)
status_text = sg.Text(
    "",
    key="-STATUS_TEXT-",
)


layout = [
    [welcome_text],
    [clock],
    [input_text, add_btn],
    [list_box, edit_btn, complete_btn],
    [status_text],
    [exit_btn],
]

# Initialize window
window = sg.Window("Todo", layout=layout, font=("Helvetica", 10))

# While loop
while True:
    try:
        event, values = window.read(timeout=10)
        if event in (sg.WIN_CLOSED, "-EXIT_BTN-"):
            break

        window["clock"].update(
            value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        if event == "-LIST_BOX-":
            selected_todo = values["-LIST_BOX-"][0].strip("\n")
            window["-INPUT_TEXT-"].update(value=selected_todo)

        elif event == "-ADD_BTN-":

            # Retrieve the data from the text file
            todos = functions.read_todos()

            # Format the new item to be added
            new_item = values["-INPUT_TEXT-"]
            assert new_item, "Invalid entry."
            new_item += "\n"

            # Add the new item to the internal state and rewrite the text file
            todos.append(new_item)
            functions.write_todos(todos)
            window["-LIST_BOX-"].update(values=todos)

            # Clean up
            window["-INPUT_TEXT-"].update(value="")
            window["-STATUS_TEXT-"].update(value="Added.", text_color="white")

        elif event == "-EDIT_BTN-":
            # Retrieve the data from the text file
            todos = functions.read_todos()

            # Find the index of the item to be edited in the list
            assert len(values["-LIST_BOX-"]) > 0, "There is no item to be edited."
            selected_todo = values["-LIST_BOX-"][0]
            selected_idx = todos.index(selected_todo)

            # Update the list
            edited_todo = values["-INPUT_TEXT-"]
            assert edited_todo, "Invalid entry."
            edited_todo += "\n"
            todos[selected_idx] = edited_todo

            functions.write_todos(todos)
            window["-LIST_BOX-"].update(values=todos)

            # Clean up
            window["-INPUT_TEXT-"].update(value="")
            window["-STATUS_TEXT-"].update(value="Edited.", text_color="white")

        elif event == "-COMPLETE_BTN-":
            # Retrieve the data from the text file
            todos = functions.read_todos()

            # Find the selected_todo and remove it
            assert len(values["-LIST_BOX-"]) > 0, "There is no item to be completed."
            selected_todo = values["-LIST_BOX-"][0]
            assert selected_todo, "Invalid entry."
            todos.remove(selected_todo)

            # Update the state
            functions.write_todos(todos)
            window["-LIST_BOX-"].update(values=todos)

            # Clean up
            window["-INPUT_TEXT-"].update(value="")
            window["-STATUS_TEXT-"].update(value="Completed.", text_color="white")
    except AssertionError as err:
        sg.popup(err, font=("Helvetica", 10))


window.close()
