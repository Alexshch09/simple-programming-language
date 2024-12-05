class SimpleVM:
    def __init__(self):
        self.ram = [0] * 16  # 16 bytes of RAM
        self.registers = {"a": 0, "b": 0, "c": 0, "d": 0}  # Registers
        self.pc = 0  # Program counter
        self.running = True  # VM running state

    def execute(self, program):
        """Execute the given program."""
        self.pc = 0
        self.running = True

        while self.running and self.pc < len(program):
            instruction = program[self.pc]
            opcode = instruction >> 4  # Upper 4 bits
            data = instruction & 0xF  # Lower 4 bits

            self.pc += 1
            self.run_instruction(opcode, data)

    def step(self, program):
        """Execute one step of the program."""
        if self.pc >= len(program):
            raise ValueError("No more instructions to execute.")
        
        instruction = program[self.pc]
        opcode = instruction >> 4
        data = instruction & 0xF
        self.pc += 1
        self.run_instruction(opcode, data)

    def run_instruction(self, opcode, data):
        if opcode == 1:  # Stop
            self.running = False
        elif opcode == 2:  # Load data to A
            self.registers["d"] = self.registers["c"]
            self.registers["c"] = self.registers["b"]
            self.registers["b"] = self.registers["a"]
            self.registers["a"] = data
        elif opcode == 3:  # Load A to RAM
            if data < len(self.ram):
                self.ram[data] = self.registers["a"]
        elif opcode == 4:  # Load RAM to A
            if data < len(self.ram):
                self.registers["d"] = self.registers["c"]
                self.registers["c"] = self.registers["b"]
                self.registers["b"] = self.registers["a"]
                self.registers["a"] = self.ram[data]
        elif opcode == 5:  # A + B > A
            self.registers["a"] = (self.registers["a"] + self.registers["b"]) & 0xF
            self.registers["b"] = self.registers["c"]
            self.registers["c"] = self.registers["d"]
            self.registers["d"] = 0
        elif opcode == 6:  # A & B > A
            self.registers["a"] = self.registers["a"] & self.registers["b"]
            self.registers["b"] = self.registers["c"]
            self.registers["c"] = self.registers["d"]
            self.registers["d"] = 0
        elif opcode == 7:  # A || B > A
            self.registers["a"] = self.registers["a"] | self.registers["b"]
            self.registers["b"] = self.registers["c"]
            self.registers["c"] = self.registers["d"]
            self.registers["d"] = 0
        elif opcode == 8:  # !A > A
            self.registers["a"] = (~self.registers["a"]) & 0xF
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    def state(self):
        """Return the current state of the VM."""
        return {
            "registers": self.registers.copy(),
            "ram": self.ram[:],
            "pc": self.pc,
        }

    def clear_state(self):
        """Reset the VM state."""
        self.ram = [0] * 16
        self.registers = {"a": 0, "b": 0, "c": 0, "d": 0}
        self.pc = 0
        self.running = True


class SimpleAssembler:
    INSTRUCTIONS = {
        "STOP": 1,
        "LOAD": 2,
        "STORE": 3,
        "FETCH": 4,
        "ADD": 5,
        "AND": 6,
        "OR": 7,
        "NOT": 8,
    }

    @staticmethod
    def assemble(assembly_code):
        """Convert assembly code into machine code."""
        program = []
        for line in assembly_code.splitlines():
            line = line.strip()
            # Remove comments by splitting at the first '#'
            line = line.split("#")[0].strip()
            if not line:
                continue  # Skip empty or comment-only lines
            parts = line.split()
            instruction = parts[0].upper()
            data = int(parts[1]) if len(parts) > 1 else 0

            if instruction not in SimpleAssembler.INSTRUCTIONS:
                raise ValueError(f"Unknown instruction: {instruction}")
            opcode = SimpleAssembler.INSTRUCTIONS[instruction]
            program.append((opcode << 4) | (data & 0xF))
        return program
