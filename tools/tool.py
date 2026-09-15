import json
import platform
import append, count_lines, listdir, read, shell, update
from colorama import Fore, Back, Style # pyright: ignore[reportMissingModuleSource]

os_name = platform.system()
if os_name == "Darwin":
    os_name = "macOS"

tools = {}

def register_tool(tool):
    global tools
    tools[tool.name] = tool

class tool:
    name = 'INVALID_TOOL'
    description = 'This tool has been misconfigured. Do not call it. Without calling this tool, you must immediately inform the user that there is an invalid tool.'
    params = {}
    required = []
    printed = []
    func = None

    def __init__(self, name, description, params, required, func, printed=[]):
        self.name = name
        self.description = description
        self.params = params
        self.required = required
        self.func = func
        self.printed = printed

    def call(self, message):
        args_string = message["tool_calls"][0]["function"]["arguments"]
        args = json.loads(args_string)

        # Print to console that the tool was called before actually calling it
        printed_output = f"Tool Called: {self.name}"
        if self.printed != []:
            printed_output += " - "
            for arg in self.printed:
                printed_output += f"{args[arg]} "

        print()
        print(Fore.MAGENTA + printed_output + Style.RESET_ALL)
        print()

        return self.func(args)

    def get_schema(self):
        schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.params,
                    "required": self.required
                }
            }
        }

        return schema

def handle_tool_call(message):
    global tools
    name = message["tool_calls"][0]["function"]["name"]
    id = message["tool_calls"][0]["id"]

    try:
        response = tools[name].call(message)
    except:
        response = "ERROR: Invalid tool call"

    json_response = json.dumps(response)

    payload = {
        "role": "tool",
        "tool_call_id": id,
        "content": json_response
    }

    return payload

# Register all the tools

register_tool(tool(
    name="append",
    description="Add new text conetnt after the last line of a file. The file will be created if it does not exist.",
    params={
        "file": {
            "type": "string",
            "description": "The relative path to the file"
        },
        "content": {
            "type": "string",
            "description": "The content to be appended to the file"
            }
    },
    required = ["file", "content"],
    func = append.append,
    printed = ["file"]
))

register_tool(tool(
    name="count_lines",
    description="Get the total number of lines in a file.",
    params={
        "file": {
            "type": "string",
            "description": "The relative path to the file"
        }
    },
    required = ["file"],
    func = count_lines.count_lines,
    printed = ["file"]
))

register_tool(tool(
    name="list_dir",
    description="Get a list of the files and directories at the specified path. Use '.' for the working directory.",
    params={
        "dir": {
            "type": "string",
            "description": "The directory to enumerate"
        }
    },
    required = ["dir"],
    func = listdir.listdir,
    printed = ["dir"]
))

register_tool(tool(
    name="read",
    description="Read a specified range of lines in a file",
    params={
        "file": {
            "type": "string",
            "description": "The relative path to the file"
        },
        "start": {
            "type": "integer",
            "description": "The first line to read, 0-indexed, inclusive"
        },
        "end": {
            "type": "integer",
            "description": "The last line to read, 0-indexed, exclusive. If ommitted, read to the end of the file."
        }
    },
    required = ["file", "start"],
    func = read.read,
    printed = ["file"]
))


register_tool(tool(
    name="shell",
    description="Use this to execute a command ONLY if ABSOLUTELY NECESSARY. YOU MAY NOT USE THIS TOOL TO EDIT, READ, OR MANIPULATE FILES. THE ECHO, CAT, AND LS/DIR COMMANDS ARE FORBIDDEN AND WILL BE REJECTED.",
    params={
        "command": {
            "type": "string",
            "description": f"The command to execute. Use syntax appropriate for {os_name}"
        }
    },
    required = ["command"],
    func = shell.shell,
    printed = ["command"]
))

register_tool(tool(
    name="update",
    description="Remove a specified range of lines in a file, and replace the removed section with the supplied content",
    params={
        "file": {
            "type": "string",
            "description": "The relative path to the file"
        },
        "start": {
            "type": "integer",
            "description": "The first line to remove, 0-indexed, inclusive. Supplied content will be written to this line."
        },
        "end": {
            "type": "integer",
            "description": "The final line to remove, 0-indexed, exclusive. If ommitted, only replace one line."
        },
        "content": {
            "type": "string",
            "description": "The new text to write to the given line"
        }
    },
    required = ["file", "start", "content"],
    func = update.update,
    printed=["file"]
))


def compact_dummy(args):
    return("ERROR: 'Compact' tool called at inappropriate time, ignoring.")
    
register_tool(tool(
    name="compact",
    description="Used to summarize the current context before clearing it. NEVER call this tool unless explicitly instructed to do so.",
    params={
        "summary": {
            "type": "string",
            "description": "The summary of the current context"
        }
    },
    required = ["summary"],
    func = compact_dummy
))