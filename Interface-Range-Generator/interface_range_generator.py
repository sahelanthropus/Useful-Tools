import re
from tkinter import *

# Create an instance of a window
root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to 80% of the screen dimensions
root.geometry(f"{int(screen_width * 0.71)}x{int(screen_height * 0.55)}")
root.title("Interface Range Generator")

# Create separate frames
interface_frame = LabelFrame(root, padx=10, pady=10)
config_frame = LabelFrame(root, padx=10, pady=10)

# Create a Label for interface text widget
interface_label = Label(interface_frame, text="Enter/Paste your Interfaces", font=("Times New Roman", 18))

# Create a interface text widget
interface_text = Text(interface_frame, font=("Times New Roman", 12))

# Create a Label for config text widget
config_label = Label(config_frame, text="Interface Range Output", font=("Times New Roman", 18))

# Create a config text widget
config_text = Text(config_frame, font=("Times New Roman", 12))

# Place widgets in the grid
interface_frame.grid(row=1, column=0)
interface_label.grid(row=0, column=0)
interface_text.grid(row=1, column=0)
config_frame.grid(row=1, column=1)
config_label.grid(row=0, column=1)
config_text.grid(row=1, column=1)


def clear():
    """
    Clears the interface and config text widgets.

    Args:
        None

    Returns:
        None
    """
    interface_text.delete(1.0, END)
    config_text.delete(1.0, END)


def getInterfaces():
    """
    Retrieves the list of interfaces from the interface text widget.

    Args:
        None

    Returns:
        interfaces (list): A list of interfaces.
    """
    interface_input = interface_text.get("1.0", "end-1c")
    interface_list = interface_input.split("\n")
    interfaces = [i for i in interface_list if i]

    # sort the interfaces by switch number, module number, and interface number
    interfaces.sort(key=lambda x: (int(re.search(r'\d+', x.split("/")[0]).group()), int(x.split("/")[1]), int(x.split("/")[2])))

    return interfaces


def buildCommand(interfaces):
    """
    Builds the interface range command from the list of interfaces.

    Args:
        interfaces (list): A list of strings representing the interfaces.

    Returns:
        command (str): The interface range command.
    """
    command = ""
    range_start = None
    range_end = None
    switch_num_prev = None
    module_num_prev = None

    print(interfaces)

    for interface in interfaces:
        # Parse the interface name, switch number, module number, and interface number
        matches = re.findall(r"\d+", interface)
        int_name = re.search(r"[a-zA-Z]+", interface)

        if matches:
            switch_num = int(matches[0])
            module_num = int(matches[1])
            interface_num = int(matches[2])
            interface_name = int_name.group()

        # If we are not currently building a range, start a new range
        if range_start is None:
            range_start = interface_num
            range_end = interface_num
            switch_num_prev = switch_num
            module_num_prev = module_num
            continue

        # If the current interface is one more than the previous interface and on the same module and switch, continue the range
        if interface_num == range_end + 1 and switch_num == switch_num_prev and module_num == module_num_prev:
            range_end = interface_num
            continue

        # Otherwise, add the current range to the command and start a new range.
        if range_start == range_end:
            command += f"{interface_name}{switch_num_prev}/{module_num_prev}/{range_start}, "
        else:
            command += f"{interface_name}{switch_num_prev}/{module_num_prev}/{range_start}-{range_end}, "

        range_start = interface_num
        range_end = interface_num
        switch_num_prev = switch_num
        module_num_prev = module_num

    # Add the final range to the command
    if range_start == range_end:
        command += f"{interface_name}{switch_num_prev}/{module_num_prev}/{range_start}"
    else:
        command += f"{interface_name}{switch_num_prev}/{module_num_prev}/{range_start}-{range_end}"

    return command

# Generate interface range commands if more than 5 ranges in a command
def generateCommands(command):
    """
    Generate a list of commands for a list of interface ranges, with a maximum of 5 interface ranges per command.

    Args:
        command (str): a string representing a list of interface ranges, separated by ", "

    Returns:
        commands (list): a list of strings, where each string represents a command for a group of interface ranges
    """
    interface_ranges = command.split(", ")
    commands = []

    for i in range(0, len(interface_ranges), 5):
    # create a string for the current interface range command
        command_string = "interface range " + ", ".join(interface_ranges[i:i+5])
    # append the current interface range command to the list of commands
        commands.append(command_string)

    return commands

# Display the command in the config text widget
def displayCommand(commands):
    """
    Displays the interface range command.

    Args:
        commands (list): The interface range command.

    Returns:
        None
    """
    for command in commands:
        config_text.insert(END, command + '\n')

def submit():
    """
    Retrieves the list of interfaces, builds the interface range command, and displays the command.

    Args:
        None

    Returns:
        None
    """
    interfaces = getInterfaces()
    command = buildCommand(interfaces)
    commands = generateCommands(command)
    displayCommand(commands)

# Create a Clear Button
clear_button = Button(root, text="Clear", font=("Times New Roman", 18), command=clear)

# Create a Submit Button
submit_button = Button(root, text="Submit", font=("Times New Roman", 18), command=submit)

# Place buttons in the grid
clear_button.grid(row=2, column=1)
submit_button.grid(row=2, column=0)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
#root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

# Enters the Tkinter event loop, executing application
root.mainloop()
