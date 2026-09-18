import subprocess

def shell(args):
    command = args["command"]
    out = "(None)"
    err = "(None)"

    # Explicitly deny top-level cat and echo, because models insist on it often
    command_name = command.lower().strip().split()[0]
    if command_name in ["echo", "cat", "ls", "dir"]:
        return f"ERROR: Forbidden command '{command_name}'. You MUST use the append, update, read, or list_dir tools instead."

    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    out = result.stdout
    err = result.stderr

    # This should ideally be a dict, but lots of shell outputs can make it unserializable as json...so, it's a string.
    return f"stdout: {out}\nstderr: {err}"