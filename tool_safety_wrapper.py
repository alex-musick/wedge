import sys
sys.path.insert(0, "./tools")
import tool
import json
from pathlib import Path
from colorama import Fore, Back, Style # type: ignore
import difflib

tools = tool.tools

def safe_tool_call(message, safety_mode):
    tool_name = message["tool_calls"][0]["function"]["name"]
    args_string = message["tool_calls"][0]["function"]["arguments"]
    args = json.loads(args_string)

    try: #wrapping this much code in a try/except block is definitely a sin and I'm sorry
        if (tool_name not in ["update", "shell", "append"]) or (safety_mode == 2): #2 - YOLO
            return tools[tool_name].call(message)

        if safety_mode == 0: #0 - Full Supervision
            if tool_name in ["update", "append"]:
                return approve_update(message, tool_name)
            elif tool_name == "shell":
                return approve_shell(message)

        if safety_mode == 1: #1 - Quick edit locally
            if tool_name in ["update", "append"]:
                pwd = Path.cwd().resolve()
                target = (pwd / Path(args["file"]).resolve()) #Make sure the target is in pwd
                try:
                    target.relative_to(pwd)
                    return tools[tool_name].call(message)
                except ValueError:
                    response = "DENIED: You may only modify files inside the working directory."
            elif tool_name == "shell":
                return approve_shell(message)
    except KeyError as error:
        pass
    except Exception as error:
        print(Fore.RED + "ERROR during tool call. THIS IS A BUG IN WEDGE, please report!" + Style.RESET_ALL)
        print(error)
        return "ERROR: Unspecified client-side tool error. This is probably a bug in the harness."

    return "INVALID TOOL CALL"
            
def approve_append(message):
    args_string = message["tool_calls"][0]["function"]["arguments"]
    args = json.loads(args_string)
    filename = args["file"]
    content = args["content"]

    print(Fore.GREEN + content + Style.RESET_ALL)
    print()
    print(f"Appending to file {filename} - approve?")

    if get_user_approval():
        response = tools["append"].call(message)
        return response
    else:
        return "DENIED: User denied append, try doing something else."

def approve_update(message, tool):
    if tool == "append":
        return approve_append(message)
    
    args_string = message["tool_calls"][0]["function"]["arguments"]
    args = json.loads(args_string)
    filename = args["file"]
    start = args["start"]
    try:
        end = args["end"]
    except:
        end = start + 1
    content = args["content"]

    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except:
        return "ERROR: Failed to open file for reading - file may not exist or may be in a different directory"

    print_edit_for_approval(start, end, lines, content)


    # Ask for approval
    print()
    print(f"Approve file edit? - {filename}")

    if get_user_approval():
        response = tools["update"].call(message)
        return response
    else:
        return "DENIED: User denied edit, try doing something else."


def approve_shell(message):
    args_string = message["tool_calls"][0]["function"]["arguments"]
    args = json.loads(args_string)
    command = args["command"]

    print("Approve shell command?:")
    print()
    print(Fore.GREEN + command + Style.RESET_ALL)
    print()

    if get_user_approval():
        response = tools["shell"].call(message)
        return response
    else:
        return "DENIED: User denied shell command. Reconsider whether a shell command is absolutely, unambiguously necessary, then try doing something different."



def print_edit_for_approval(start, end, before, content):
    after = before.copy()

    for i in reversed(range(start, end)):
        after.pop(i)

    new_lines = content.split("\n")
    for i in reversed(range(len(new_lines))):
        line = new_lines[i]
        after.insert(start, line)

    diff_lines = difflib.unified_diff(before, after)

    skip_lines = 3
    for line in diff_lines:
        if skip_lines > 0:
            skip_lines -= 1
            continue
        if line[0] == "-":
            print(Back.RED + line + Style.RESET_ALL)
        elif line[0] == "+":
            print(Back.GREEN + line + Style.RESET_ALL)
        else:
            print(line)

    return

def get_user_approval():
    while True:
        answer = input("[y/n]")
        if answer.lower() == "y":
            return True
        elif answer.lower() == "n":
            return False
        else:
            continue