#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code Editor UI - Simple code editing interface
"""

import pygame
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from typing import Callable, Optional

class SimpleCodeEditor:
    """Simple code editor using tkinter"""

    def __init__(self, on_run_callback: Callable[[str], None]):
        """
        Initialize code editor
        Args:
            on_run_callback: Callback function when Run button is pressed
        """
        self.on_run_callback = on_run_callback
        self.root = None
        self.text_area = None
        self.is_open = False
        
    def open_editor(self, initial_code: str = "", instructions: list = None):
        """Open code editor window"""
        if self.is_open:
            return

        self.is_open = True

        # Create tkinter window
        self.root = tk.Tk()
        self.root.title("WRO Code Editor")
        self.root.geometry("800x600")

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.close_editor)

        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Display instructions if available
        if instructions:
            self.create_instructions_panel(main_frame, instructions)
        
        # Frame for code editor
        editor_frame = tk.Frame(main_frame)
        editor_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Label
        tk.Label(editor_frame, text="Write your code:", font=("Arial", 12, "bold")).pack(anchor=tk.W)

        # Text area with scroll
        self.text_area = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Consolas", 11),
            bg="white",
            fg="black",
            insertbackground="black"
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        # Add initial code
        if initial_code:
            self.text_area.insert(tk.END, initial_code)
        
        # Frame for buttons
        button_frame = tk.Frame(editor_frame)
        button_frame.pack(fill=tk.X)

        # Buttons
        tk.Button(
            button_frame,
            text="[RUN] Code",
            command=self.run_code,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            button_frame,
            text="[CLEAR] All",
            command=self.clear_code,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            button_frame,
            text="[SAMPLE] Code",
            command=lambda: self.insert_sample_code(initial_code),
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            button_frame,
            text="[X] Close",
            command=self.close_editor,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        ).pack(side=tk.RIGHT)

        # Run tkinter mainloop
        self.root.mainloop()
    
    def create_instructions_panel(self, parent, instructions):
        """Create instructions display panel"""
        # Frame for instructions
        inst_frame = tk.Frame(parent, relief=tk.RIDGE, bd=2)
        inst_frame.pack(fill=tk.X, pady=(0, 10))

        # Label title
        tk.Label(inst_frame, text="[INFO] Instructions", font=("Arial", 12, "bold"), bg="#E3F2FD").pack(fill=tk.X, padx=5, pady=5)

        # Text area for instructions
        inst_text = tk.Text(inst_frame, height=8, wrap=tk.WORD, font=("Arial", 9), bg="#F5F5F5", state=tk.DISABLED)
        inst_text.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Add instruction content
        inst_text.config(state=tk.NORMAL)
        for line in instructions:
            inst_text.insert(tk.END, line + "\n")
        inst_text.config(state=tk.DISABLED)
    
    def run_code(self):
        """Run code and call callback"""
        if self.text_area:
            code = self.text_area.get("1.0", tk.END).strip()
            if code:
                try:
                    self.on_run_callback(code)
                    messagebox.showinfo("Success", "Code has been executed! Check the game window to see results.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error running code:\n{str(e)}")
            else:
                messagebox.showwarning("Warning", "Please enter code before running!")

    def clear_code(self):
        """Clear all code"""
        if self.text_area:
            if messagebox.askyesno("Confirm", "Are you sure you want to clear all code?"):
                self.text_area.delete("1.0", tk.END)

    def insert_sample_code(self, sample_code):
        """Insert sample code"""
        if self.text_area and sample_code:
            if messagebox.askyesno("Sample Code", "Do you want to replace current code with sample code?"):
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", sample_code)

    def close_editor(self):
        """Close code editor"""
        if self.root:
            self.root.destroy()
            self.root = None
            self.text_area = None
            self.is_open = False

class CodeEditorManager:
    """Manager to handle code editor"""

    def __init__(self):
        self.editor = None
        self.editor_thread = None

    def open_editor(self, on_run_callback: Callable[[str], None], initial_code: str = "", instructions: list = None):
        """Open code editor in separate thread"""
        if self.editor and self.editor.is_open:
            return

        def run_editor():
            self.editor = SimpleCodeEditor(on_run_callback)
            self.editor.open_editor(initial_code, instructions)

        self.editor_thread = threading.Thread(target=run_editor, daemon=True)
        self.editor_thread.start()

    def is_editor_open(self) -> bool:
        """Check if editor is currently open"""
        return self.editor and self.editor.is_open
