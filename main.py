import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
from tkinter import font
from assembler import SimpleAssembler, SimpleVM


class SimpleIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple VM IDE")

        # Dark Mode Configuration
        self.dark_bg = "#2e2e2e"
        self.dark_fg = "#ffffff"
        self.button_bg = "#4e4e4e"
        self.button_fg = "#ffffff"

        # Create VM and Assembler
        self.vm = SimpleVM()
        self.assembler = SimpleAssembler()

        # Text editor for code
        self.editor_frame = tk.Frame(root)
        self.editor_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.code_editor = tk.Text(self.editor_frame, wrap=tk.NONE, font=("Consolas", 12), bg=self.dark_bg, fg=self.dark_fg)
        self.code_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Define tags for syntax highlighting
        self.code_editor.tag_configure("keyword", foreground="cyan")
        self.code_editor.tag_configure("number", foreground="yellow")
        self.code_editor.tag_configure("comment", foreground="green")
        self.code_editor.tag_configure("address", foreground="orange")
        self.code_editor.tag_configure("data", foreground="lightblue")
        self.code_editor.tag_configure("math", foreground="pink")
        self.code_editor.tag_configure("load_store", foreground="red")
        self.code_editor.tag_configure("ram_op", foreground="lightgreen")
        
        self.code_editor.bind("<KeyRelease>", self.highlight_syntax)

        self.button_frame = tk.Frame(root, bg=self.dark_bg)
        self.button_frame.pack(fill=tk.X, side=tk.TOP)

        self.assemble_button = tk.Button(self.button_frame, text="Assemble", command=self.assemble_code, bg=self.button_bg, fg=self.button_fg)
        self.assemble_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.run_button = tk.Button(self.button_frame, text="Run", command=self.run_code, bg=self.button_bg, fg=self.button_fg)
        self.run_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.step_button = tk.Button(self.button_frame, text="Step", command=self.step_code, bg=self.button_bg, fg=self.button_fg)
        self.step_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear State", command=self.clear_state, bg=self.button_bg, fg=self.button_fg)
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.output_frame = tk.Frame(root, bg=self.dark_bg)
        self.output_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        self.output_label = tk.Label(self.output_frame, text="State", font=("Arial", 14), fg=self.dark_fg, bg=self.dark_bg)
        self.output_label.pack(anchor="w", padx=5, pady=5)

        self.state_tree = ttk.Treeview(self.output_frame, columns=("Name", "Value"), show="headings")
        self.state_tree.heading("Name", text="Name")
        self.state_tree.heading("Value", text="Value")
        self.state_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.update_state_view()

    def highlight_syntax(self, event=None):
        """Highlight syntax in the code editor."""
        code = self.code_editor.get("1.0", tk.END)
        self.code_editor.mark_set("range_start", "1.0")
        self.code_editor.mark_set("range_end", "1.0")

        self.code_editor.tag_remove("keyword", "1.0", tk.END)
        self.code_editor.tag_remove("number", "1.0", tk.END)
        self.code_editor.tag_remove("comment", "1.0", tk.END)
        self.code_editor.tag_remove("address", "1.0", tk.END)
        self.code_editor.tag_remove("data", "1.0", tk.END)
        self.code_editor.tag_remove("math", "1.0", tk.END)
        self.code_editor.tag_remove("load_store", "1.0", tk.END)
        self.code_editor.tag_remove("ram_op", "1.0", tk.END)

        keywords = ["STOP", "LOAD", "STORE", "FETCH", "ADD", "AND", "OR", "NOT"]
        math_ops = ["ADD", "AND", "OR", "NOT"]
        load_store_ops = ["LOAD", "STORE"]
        ram_ops = ["FETCH", "STORE"]
        lines = code.splitlines()

        for line_no, line in enumerate(lines, 1):
            self.code_editor.mark_set("range_start", f"{line_no}.0")
            self.code_editor.mark_set("range_end", f"{line_no}.0 + {len(line)} chars")

            # Highlight comments (after '#')
            comment_start = line.find("#")
            if comment_start != -1:
                # Highlight the comment part
                self.code_editor.tag_add("comment", f"{line_no}.0 + {comment_start} chars", f"{line_no}.0 + {len(line)} chars")
                # Highlight the code part before '#'
                code_part = line[:comment_start].strip()

                # Highlight keywords in the code part before '#'
                for keyword in keywords:
                    start_index = 0
                    keyword_lower = keyword.lower()
                    while start_index < len(code_part):
                        start_index = code_part.lower().find(keyword_lower, start_index)
                        if start_index == -1:
                            break
                        end_index = start_index + len(keyword)
                        self.code_editor.tag_add("keyword", f"{line_no}.0 + {start_index} chars", f"{line_no}.0 + {end_index} chars")
                        start_index = end_index

                # Highlight math operations in the code part before '#'
                for math_op in math_ops:
                    start_index = 0
                    math_op_lower = math_op.lower()
                    while start_index < len(code_part):
                        start_index = code_part.lower().find(math_op_lower, start_index)
                        if start_index == -1:
                            break
                        end_index = start_index + len(math_op)
                        self.code_editor.tag_add("math", f"{line_no}.0 + {start_index} chars", f"{line_no}.0 + {end_index} chars")
                        start_index = end_index

                # Highlight load/store operations in the code part before '#'
                for load_op in load_store_ops:
                    start_index = 0
                    load_op_lower = load_op.lower()
                    while start_index < len(code_part):
                        start_index = code_part.lower().find(load_op_lower, start_index)
                        if start_index == -1:
                            break
                        end_index = start_index + len(load_op)
                        self.code_editor.tag_add("load_store", f"{line_no}.0 + {start_index} chars", f"{line_no}.0 + {end_index} chars")
                        start_index = end_index

                # Highlight RAM operations in the code part before '#'
                for ram_op in ram_ops:
                    start_index = 0
                    ram_op_lower = ram_op.lower()
                    while start_index < len(code_part):
                        start_index = code_part.lower().find(ram_op_lower, start_index)
                        if start_index == -1:
                            break
                        end_index = start_index + len(ram_op)
                        self.code_editor.tag_add("ram_op", f"{line_no}.0 + {start_index} chars", f"{line_no}.0 + {end_index} chars")
                        start_index = end_index

                # Highlight numbers (data) in the code part before '#'
                for word in code_part.split():
                    if word.isdigit():
                        start_index = code_part.find(word)
                        end_index = start_index + len(word)
                        self.code_editor.tag_add("data", f"{line_no}.0 + {start_index} chars", f"{line_no}.0 + {end_index} chars")

            else:
                # Highlight the whole line as code if there is no comment
                code_part = line.strip()

                # Highlight keywords in the whole line
                for keyword in keywords:
                    start_index = 0
                    keyword_lower = keyword.lower()
                    while start_index < len(code_part):
                        start_index = code_part.lower().find(keyword_lower, start_index)
                        if start_index == -1:
                            break
                        end_index = start_index + len(keyword)
                        self.code_editor.tag_add("keyword", f"{line_no}.0 + {start_index} chars", f"{line_no}.0 + {end_index} chars")
                        start_index = end_index

                # Highlight math operations in the whole line
                for math_op in math_ops:
                    start_index = 0
                    math_op_lower = math_op.lower()
                    while start_index < len(code_part):
                        start_index = code_part.lower().find(math_op_lower, start_index)
                        if start_index == -1:
                            break
                        end_index = start_index + len(math_op)
                        self.code_editor.tag_add("math", f"{line_no}.0 + {start_index} chars", f"{line_no}.0 + {end_index} chars")
                        start_index = end_index

                # Highlight load/store operations in the whole line
                for load_op in load_store_ops:
                    start_index = 0
                    load_op_lower = load_op.lower()
                    while start_index < len(code_part):
                        start_index = code_part.lower().find(load_op_lower, start_index)
                        if start_index == -1:
                            break
                        end_index = start_index + len(load_op)
                        self.code_editor.tag_add("load_store", f"{line_no}.0 + {start_index} chars", f"{line_no}.0 + {end_index} chars")
                        start_index = end_index

                # Highlight RAM operations in the whole line
                for ram_op in ram_ops:
                    start_index = 0
                    ram_op_lower = ram_op.lower()
                    while start_index < len(code_part):
                        start_index = code_part.lower().find(ram_op_lower, start_index)
                        if start_index == -1:
                            break
                        end_index = start_index + len(ram_op)
                        self.code_editor.tag_add("ram_op", f"{line_no}.0 + {start_index} chars", f"{line_no}.0 + {end_index} chars")
                        start_index = end_index

                # Highlight numbers (data) in the whole line
                for word in code_part.split():
                    if word.isdigit():
                        start_index = code_part.find(word)
                        end_index = start_index + len(word)
                        self.code_editor.tag_add("data", f"{line_no}.0 + {start_index} chars", f"{line_no}.0 + {end_index} chars")

    def assemble_code(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        if not code:
            messagebox.showerror("Error", "Code editor is empty!")
            return

        try:
            self.program = self.assembler.assemble(code)
            messagebox.showinfo("Success", "Code assembled successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Assembly failed: {e}")

    def run_code(self):
        if not hasattr(self, "program"):
            messagebox.showerror("Error", "Assemble the code first!")
            return

        try:
            self.vm.execute(self.program)
            self.update_state_view()
            messagebox.showinfo("Execution Complete", "Program executed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Execution failed: {e}")

    def step_code(self):
        if not hasattr(self, "program"):
            messagebox.showerror("Error", "Assemble the code first!")
            return

        try:
            self.vm.step(self.program)
            self.update_state_view()
        except Exception as e:
            messagebox.showerror("Error", f"Execution failed: {e}")
            print(e)

    def clear_state(self):
        """Clear the VM state."""
        self.vm.clear_state()
        self.update_state_view()
        messagebox.showinfo("State Cleared", "VM state has been cleared!")

    def update_state_view(self):
        """Update the state display for the VM."""
        state = self.vm.state()
        self.state_tree.delete(*self.state_tree.get_children())

        # Add registers
        self.state_tree.insert("", "end", values=("PC", state["pc"]))
        for reg, value in state["registers"].items():
            self.state_tree.insert("", "end", values=(f"Register {reg.upper()}", value))

        # Add RAM
        for i, value in enumerate(state["ram"]):
            self.state_tree.insert("", "end", values=(f"RAM[{i}]", value))


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleIDE(root)
    root.geometry("1200x900")
    root.mainloop()
