# Python Tutorial


## Note:

### 1: Todo-List, 1.1: zip-gui
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