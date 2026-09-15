def count_lines(args):
    filename = args["filename"]
    try:
        with open(filename, "r") as file:
            data = file.readlines()
    except:
        return "ERROR: Failed to open file - file may not exist or may be in a different directory"
    
    return len(data)