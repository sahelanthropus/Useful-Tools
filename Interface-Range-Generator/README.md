## Interface Range Generator
This script provides a graphical user interface for generating Cisco IOS commands to configure interface ranges. The user can enter or paste a list of interfaces into the "Enter/Paste your Interfaces" text widget, and the script will generate the corresponding interface range commands in the "Interface Range Output" text widget. The script also includes a "Clear" button to clear the contents of the text widgets.

The interface names should be in the format [interface_name][switch]/[module]/[interface], where [interface_name] is a string representing the interface type (e.g. Ethernet, FastEthernet, GigabitEthernet), [switch] is an integer representing the switch number, [module] is an integer representing the module number, and [interface] is an integer representing the interface number. The interfaces will be sorted by switch number, module number, and interface number before being processed.

The generated interface range commands will be in the format interface range [interface_name][switch]/[module]/[interface_start]-[interface_end], where [interface_start] and [interface_end] represent the first and last interface numbers in the range, respectively. The script will generate as many interface range commands as needed to include all of the interfaces, with a maximum of 5 interface ranges per command.

To use the script, run the following command:
```
python3 interface_range_generator.py
```

The script has the following dependencies:
- re: for parsing the interface names and extracting the switch number, module number, and interface number
- tkinter: for creating the graphical user interface
