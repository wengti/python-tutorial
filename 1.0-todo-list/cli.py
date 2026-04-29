from functions import append_todos, read_todos, write_todos
from time import strftime

now = strftime("%b %#d, %Y %H:%M:%S")
print(now)

while True:
    user_action = input("Type add, show, edit, complete or exit: ").strip()

    # Add new todos
    if user_action.startswith("add"):
        todo = user_action[4:] + "\n"
        append_todos(todo)

    # Show
    elif user_action.startswith("show"):
        todos = read_todos()
        for idx, todo in enumerate(todos):
            print(f"{idx} - {todo.replace("\n", "")}")

    # Edit
    elif user_action.startswith("edit"):
        try:
            todos = read_todos()
            number = int(user_action[5:])
            if number >= len(todos):
                print("Invalid number.")
            else:
                item = input("Enter the edited entry: ") + "\n"
                todos[number] = item
                write_todos(todos)
        except ValueError:
            print("Your command is invalid.")

    # Complete todos
    elif user_action.startswith("complete"):
        todos = read_todos()
        number = int(user_action[9:])
        if number >= len(todos):
            print("Invalid number.")
        else:
            todos.pop(number)
            write_todos(todos)

    # Exit
    elif user_action.startswith("exit"):
        break

    # Invalid input
    else:
        print("Invalid action")
