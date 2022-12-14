import subprocess
import os
import sys
# We want:
# shortcut goto <name>
# shortcut add <name> [path]
# shortcut rm <name>
# shortcut list

shortcuts = {}

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

# populate shortcuts from shortcuts.txt, and read CLI arguments


def init():
    f = open(application_path + "\\shortcuts.txt", "r")

    # escapes the characters in the file before anything
    text = f.read().split("\n")

    # populates shortcuts object
    for line in text:
        sc = line.split(" ", 1)
        if (len(sc) == 2):
            shortcuts[sc[0]] = sc[1]

    cleanupShortcuts()


def goto(args):
    if (len(args) < 1):
        return -1

    name = args[0]

    if (name not in shortcuts):
        print("Error: Shortcut does not exist.")
        return -1

    try:
        sc = shortcuts[name]
        os.system('start "" ' + '"' + sc + '"')
    except:
        print("Error: Failed to open directory.")


# deletes duplicate shortcuts from the file
def cleanupShortcuts():
    f = open(application_path + "\\shortcuts.txt", "w")

    for key in shortcuts:
        f.write(key + " " + shortcuts[key] + "\n")


# deletes a shortcut
def rm(args):
    if (len(args) < 1):
        print("Error: Please supply an shortcut to remove.")

    name = args[0]

    if (name not in shortcuts):
        print("Error: Shortcut not found.")
        return -1

    del shortcuts[name]
    cleanupShortcuts()


# adds or updates a shortcut's path
def add(args):
    name = args[0]
    path = repr(' '.join(args[1:]))[1:-1] if len(args) >= 2 else ""

    if (path == ""):
        path = repr(os.getcwd())[1:-1]
        print(path)

    f = open(application_path + "\\shortcuts.txt", "a")
    f.write(name + " " + path + "\n")
    f.close()
    shortcuts[name] = path


def list(_):
    print("SHORTCUTS")
    for sc in shortcuts:
        print("| " + sc + " => " + shortcuts[sc])
    print("\nTo open a directory...")
    print("\tscut goto <shortcut>")


def display_help():
    pass


def main():
    init()

    commands = {
        "go": goto,
        "g": goto,
        "add": add,
        "a": add,
        "remove": rm,
        "rm": rm,
        "list": list
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

    fun = commands[command]
    args = sys.argv[2:len(sys.argv)]

    fun(args)


main()
