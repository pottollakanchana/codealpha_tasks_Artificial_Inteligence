import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator

# Language dictionary (name → code)
languages = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-cn"
}

# Function to translate text
def translate_text():
    try:
        text = input_text.get("1.0", tk.END).strip()
        src_lang = languages[source_lang.get()]
        dest_lang = languages[target_lang.get()]

        if text == "":
            messagebox.showwarning("Warning", "Please enter text")
            return

        translated = GoogleTranslator(source=src_lang, target=dest_lang).translate(text)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to copy text
def copy_text():
    root.clipboard_clear()
    root.clipboard_append(output_text.get("1.0", tk.END))
    messagebox.showinfo("Copied", "Text copied to clipboard!")


# Create main window
root = tk.Tk()
root.title("Language Translator")
root.geometry("600x500")
root.config(bg="#f0f0f0")

# Title
title = tk.Label(root, text="Language Translation Tool", font=("Arial", 16, "bold"), bg="#f0f0f0")
title.pack(pady=10)

# Input Text
tk.Label(root, text="Enter Text:", bg="#f0f0f0").pack()
input_text = tk.Text(root, height=5, width=60)
input_text.pack(pady=5)

# Frame for dropdowns
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

# Source Language
tk.Label(frame, text="Source Language:", bg="#f0f0f0").grid(row=0, column=0)
source_lang = ttk.Combobox(frame, values=list(languages.keys()), width=18)
source_lang.set("Auto Detect")
source_lang.grid(row=0, column=1, padx=10)

# Target Language
tk.Label(frame, text="Target Language:", bg="#f0f0f0").grid(row=0, column=2)
target_lang = ttk.Combobox(frame, values=list(languages.keys()), width=18)
target_lang.set("English")
target_lang.grid(row=0, column=3, padx=10)

# Translate Button
translate_btn = tk.Button(root, text="Translate", command=translate_text, bg="blue", fg="white")
translate_btn.pack(pady=10)

# Output Text
tk.Label(root, text="Translated Text:", bg="#f0f0f0").pack()
output_text = tk.Text(root, height=5, width=60)
output_text.pack(pady=5)

# Copy Button
copy_btn = tk.Button(root, text="Copy Text", command=copy_text, bg="green", fg="white")
copy_btn.pack(pady=10)

# Run app
root.mainloop()
