def append(args):
    filename = args["file"]
    content = args["content"]
    try:
        with open(filename, "r") as file:
            data = file.readlines()
    except UnicodeDecodeError:
        return "ERROR: File is not in text format"
    except:
        pass

    try:
        with open(filename, "w") as file:
            file.writelines([content])
    except:
        return "ERROR: Failed to open file for writing - you may lack needed permissions"
    
    return "success"