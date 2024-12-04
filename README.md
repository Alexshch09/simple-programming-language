# Simple VM IDE

This is a simple Integrated Development Environment (IDE) for a custom virtual machine and assembler. The IDE allows you to write, assemble, and execute assembly code for a basic virtual machine.

## Features
- **Code Editor**: Write assembly code with syntax highlighting.
- **Assembler**: Convert assembly code to machine code.
- **Execution**: Run the assembled code in a simple virtual machine (VM).
- **Step Execution**: Step through the code one instruction at a time.
- **State Display**: View the current state of the VM, including registers and RAM.
- **Clear State**: Reset the VM's state.

## Instructions
1. Write assembly code in the editor. Supported instructions are:
    - `STOP`: Stops the execution of the program.
    - `LOAD <data>`: Loads a value into register A.
    - `STORE <address>`: Stores register A's value into RAM at the specified address.
    - `FETCH <address>`: Loads a value from RAM into register A.
    - `ADD`: Adds values of registers A and B, stores the result in A.
    - `AND`: Performs a bitwise AND between registers A and B, stores the result in A.
    - `OR`: Performs a bitwise OR between registers A and B, stores the result in A.
    - `NOT`: Performs a bitwise NOT on register A, stores the result in A.
  
2. Click the **Assemble** button to convert the code into machine code.
3. Click **Run** to execute the entire program.
4. Click **Step** to execute one instruction at a time.
5. View the VM state in the state display.

## Requirements
- Python 3.x
- Tkinter (for GUI)
- No external dependencies are required beyond Python's standard library.

## To run:
1. Install Python 3.x from https://www.python.org/downloads/
2. Download or clone this repository.
3. Run the program with the following command:
   ```bash
   python main.py

## Example program:
```py
# This program adds 5 and 6, then stores the result in RAM address 12.

LOAD 5        # Load the value 5 into register A
LOAD 6        # Load the value 6 into register A
ADD           # Add register A and B, and store the result in A
STORE 12      # Store the result of A (11) into RAM[12]
STOP          # Stop the program
```