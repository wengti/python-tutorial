FILEPATH = "todos.txt"


def read_todos(filepath=FILEPATH):
    """
    Read a textfile and return the list of todo items.
    """
    todos = []
    with open(filepath, "r") as f:
        todos = f.readlines()
    return todos


def write_todos(todos_arg, filepath=FILEPATH):
    """
    Write a list of todo items into a text file.
    """
    with open(filepath, "w") as f:
        f.writelines(todos_arg)


def append_todos(todos_arg, filepath=FILEPATH):
    """
    Append a new todo item to a new line in a text file.
    """
    with open(filepath, "a") as f:
        f.writelines(todos_arg)


if __name__ == "__main__":
    print(read_todos())
