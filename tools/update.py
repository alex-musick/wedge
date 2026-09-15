def update(args):
    filename = args["file"]
    start = args["start"]
    content = args["content"]

    end = -1
    try:
        end = args["end"]
    except ValueError:
        pass
    
    try:
        with open(filename, "r") as file:
            data = file.readlines()
    except UnicodeDecodeError:
        return "ERROR: File is not in text format"
    except:
        return "ERROR: Failed to open file for reading - file may not exist or may be in a different directory"

    if end != -1:
        try:
            for i in range(start, end, reversed=True):
                data.pop(i)
        except:
            return "ERROR: Could not clear specified lines - end value is likely invalid"

    try:
        data[start] = content
        if start != len(data):
            data[start] += "\n"
    except:
        return "ERROR: Failed to update line - line number may not exist"

    try:
        with open(filename, "w") as file:
            file.writelines(data)
    except:
        return "ERROR: Failed to open file for writing - you may lack needed permissions"
    
    return "success"