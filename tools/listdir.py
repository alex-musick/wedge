import os

def listdir(args):
    dir = "."
    try:
        dir = args["dir"]
    except:
        dir = "." # This is redundant but safe

    try:
        entries = os.listdir(dir)
    except FileNotFoundError:
        return "ERROR: Directory does not exist"
    except OSError:
        return "ERROR: Access denied"

    files = []
    dirs = []
    for entry in entries:
        if os.path.isdir(entry):
            dirs.append(entry)
        else:
            files.append(entry)

    if files == []:
        files = "(None)"
    if dirs == []:
        dirs = "(None)"

    return f"files:{files}\ndirectories:{dirs}"