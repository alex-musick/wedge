import ai_interface as ai
import sys
from colorama import Fore, Back, Style # pyright: ignore[reportMissingModuleSource]
import compact

version = "1.0.0"
safety_mode = 0

safety_descriptions = [
    Fore.GREEN + "0: All destructive operations need approval." + Style.RESET_ALL,
    Fore.YELLOW + "1: Writes to pwd are auto-approved. Commands need approval." + Style.RESET_ALL,
    Fore.RED + "2: All tool calls are auto-approved. Use with a container." + Style.RESET_ALL,
]

try:
    model_name = sys.argv[1]
    ai.change_model(model_name)
except:
    ai.change_model(ai.settings.default_model)

def parse_input(input_str):
    global safety_mode
    if input_str[0] != "/":
        ai.enter_work_loop(input_str, safety_mode)
        return

    try:
        parts = input_str.split(" ")
        command = parts[0]
        arg = parts[1]
    except:
        command = input_str

    if command.lower() == "/model":
        ai.change_model(arg)
        print(f"Changed model: {arg}")
        return

    if command.lower() == "/danger" or command.lower() == "/safety":
        if arg in ["0", "1", "2"]:
            safety_mode = int(arg)
            return

    if command.lower() == "/compact":
        compact.compact()
        return

    if command.lower() == "/clear":
        ai.init_messages()
        print('Cleared Context')
        return

    if command.lower() == "/exit" or command.lower() == "/quit":
        print("Bye")
        exit()

    print(Fore.RED + "Invalid command" + Style.RESET_ALL)
    return

def main():
    global safety_mode
    global safety_descriptions
    global version

    print()
    print(f"wedge v{version}")
    print("\n")

    while True:
        print(Fore.LIGHTBLUE_EX + f"Model: {ai.model_name} | Context: {ai.used_ctx} / {ai.total_ctx} | Auto-compact: {ai.settings.get_compact_threshold(ai.total_ctx)}" + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + f"Safety Mode {safety_descriptions[safety_mode]}" + Style.RESET_ALL)
        user_input = input("> ").strip()
        print(Style.RESET_ALL)
        parse_input(user_input)
        print()
        continue

if __name__ == "__main__":
    main()
    exit()