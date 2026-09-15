def read(args):
    filename = args["file"]
    start = args["start"]
    end = -1
    try:
        end = args["end"]
    except KeyError:
        pass
    
    try:
        with open(filename, "r") as file:
            data = file.readlines()
    except UnicodeDecodeError:
        return "ERROR: File is not in text format"
    except:
        return "ERROR: Failed to open file - file may not exist or may not be accessible"
    
    try:
        return retain_newlines(data, start, end)
    except:
        return "ERROR: Invalid start or end index"
    
def retain_newlines(content, start, end):
    if end == -1:
        end = len(content)
    final = ""

    for i in range(start,end):
        final += content[i]
    
    return final