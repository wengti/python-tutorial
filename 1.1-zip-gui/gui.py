import os
from os import path
import zipfile
from pathlib import Path
import FreeSimpleGUI as sg
from FreeSimpleGUI import WIN_CLOSED

# A list of file names, values for the list box
file_names = []

# Setting theme
sg.theme("DarkGreen3")

# Setting layout
layout = [
    # File selection to be zipped
    [
        sg.Text("Select files to be zipped: "),
    ],
    [
        sg.Listbox(values=file_names, key="file_lists", size=(60, 20)),
        sg.FilesBrowse(target="files"),
        sg.InputText(key="files", visible=False, enable_events=True),
    ],
    # Selecting folder where the zipped folder will be saved to
    [
        sg.Text("Select zipped destination: "),
    ],
    [
        sg.InputText(key="destination", size=(60, 1)),
        sg.FolderBrowse(target="destination", size=(10, 1)),
    ],
    # Provide the zip folder name
    [
        sg.Text("Enter the destination zip folder name (without zip): "),
    ],
    [
        sg.InputText(key="save_dir_name", size=(60, 1)),
        sg.Button(button_text="Zip", key="zip", size=(10, 1)),
    ],
    # Status
    [
        sg.Text("Status: ", key="status"),
    ],
    # Close button
    [
        sg.Push(),
        sg.Button(button_text="Close", key="close"),
    ],
]

# Initialize the window
window = sg.Window("Zipper", layout)


# While loop
while True:
    # Read events
    event, values = window.read()

    # Close windows
    if event in (WIN_CLOSED, "close"):
        break

    # Refresh status
    window["status"].update("Status: ", text_color="white")

    # When browsing files button is clicked
    if event == "files":
        new_files = values["files"].split(";")
        for file in new_files:
            file_names.append(Path(file))
        window["file_lists"].update(values=file_names)

    # When destination folder selection button is clicked
    elif event == "destination":
        window["destination"].update(values[event])

    # When zip button is clicked
    elif event == "zip":
        try:
            # Data sanitization
            assert len(file_names) > 0, "There is no file to be zipped."
            assert values["destination"], "Destination folder is emtpy."
            assert values["save_dir_name"], "File name to be zipped to cannot be empty."

            # Zipping files
            destination_dir = Path(values["destination"])
            save_dir = destination_dir / f"{values["save_dir_name"]}.zip"
            with zipfile.ZipFile(save_dir, "w") as zip_ref:
                for file in file_names:
                    if os.path.exists(Path(file)):
                        zip_ref.write(
                            Path(file), Path(file).name
                        )  # Second argument is to set the path in the zipped folder

            # Clean up
            window["status"].update(value="Status: Success!", text_color="green")
            window["destination"].update(value="")
            file_names = []
            window["file_lists"].update(values=file_names)
            window["save_dir_name"].update(value="")

        except AssertionError as err:
            window["status"].update(value=f"Status: {err}!", text_color="red")


window.close()
