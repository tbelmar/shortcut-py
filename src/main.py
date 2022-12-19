import os
import sys
from ast import literal_eval

# We want:
# shortcut go <name>
# shortcut add <name> [path]
# shortcut rm <name>
# shortcut list

shortcuts = {}

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)


# populates shortcuts from shortcuts.txt, and read CLI arguments
def init():
    f = open(application_path + "\\shortcuts.txt", "a+")
    f = open(application_path + "\\shortcuts.txt", "r")

    # escapes the characters in the file before anything
    text = f.read().split("\n")

    # populates shortcuts object
    for line in text:
        sc = line.split(" ", 1)
        if (len(sc) == 2):
            shortcuts[sc[0]] = sc[1]


# deletes duplicate shortcuts from the file
def cleanupShortcutsFile():
    f = open(application_path + "\\shortcuts.txt", "w")

    for key in shortcuts:
        f.write(key + " " + shortcuts[key] + "\n")


# opens a shortcut in the file explorer
def goto(args):
    if (len(args) < 1):
        print("Error: Please supply a shortcut to go to.")
        display_help()
        return 1

    name = args[0].lower()

    if (name not in shortcuts):
        print("Error: Shortcut does not exist.")
        return 1

    try:
        sc = shortcuts[name]
        os.system('start "" ' + '"' + sc + '"')
    except:
        print("Error: Failed to open directory.")


# deletes a shortcut
def rm(args):
    if (len(args) < 1):
        print("Error: Please supply a shortcut to remove.")
        display_help()
        return 1

    name = args[0].lower()

    if (name not in shortcuts):
        print("Error: Shortcut not found.")
        return 1

    del shortcuts[name]
    print("Shortcut successfully removed.")


# adds or updates a shortcut's path
def add(args):
    if (len(args) < 1):
        print("Error: Please supply a shortcut name and (optionally) a path.")
        display_help()
        return 1

    name = args[0].lower()
    path = repr(' '.join(args[1:]))[1:-1] if len(args) >= 2 else ""

    if (path == ""):
        path = repr(os.getcwd())[1:-1]

    f = open(application_path + "\\shortcuts.txt", "a")
    f.write(name + " " + path + "\n")
    f.close()
    shortcuts[name] = path

    path = literal_eval("'" + path + "'")

    print("Shortcut successfully added.")
    print("\t" + f'{"NAME":<16}{"PATH"}')
    print("\t" + f'{name:<16}{path}')


# displays all available shortcuts
def list(_=None):
    print("Shortcuts")
    print("\t" + f'{"NAME":<16}{"PATH"}')
    for sc in shortcuts:
        path = literal_eval("'" + shortcuts[sc] + "'")
        print("\t" + f'{sc:<16}{path}')
    print("\nTo open a directory in the path column...")
    print("\tscut go <name>")


# displays help menu
def display_help(_=None):
    print("usage:")
    print(
        "\t" + f'{"scut go <name>":<30}{"Open a shortcut in the file explorer"}')
    print(
        "\t" + f'{"scut add <name> [location]":<30}{"Add a new shortcut, or update an existing one"}')
    print(
        "\t" + f'{"scut remove <name>":<30}{"Delete a shortcut"}')
    print(
        "\t" + f'{"scut list":<30}{"Display all shortcuts"}')
    print(
        "\t" + f'{"scut help":<30}{"Display this menu"}')


def main():
    init()

    commands = {
        "goto": goto,
        "go": goto,
        "g": goto,

        "add": add,
        "a": add,

        "remove": rm,
        "rm": rm,
        "r": rm,

        "list": list,
        "ls": list,

        "help": display_help
    }

    if (len(sys.argv) < 2):
        print("Error: Please supply a command.")
        display_help()
        return 1

    command = sys.argv[1]

    if (not command in commands):
        print("Error: Command does not exist.")
        display_help()
        return 1

    
    func = commands[command]
    args = sys.argv[2:len(sys.argv)]

    func(args)

    cleanupShortcutsFile()


main()
