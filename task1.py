

import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import urllib.parse
import json
import threading

# Language names and their API language codes
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Russian": "ru",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Gujarati": "gu",
    "Punjabi": "pa"
}


def translate_text():
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "Input Required",
            "Please enter some text to translate."
        )
        return

    source_name = source_language.get()
    target_name = target_language.get()

    if source_name == target_name:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, text)
        return

    translate_button.config(state=tk.DISABLED, text="Translating...")
    status_label.config(text="Connecting to translation service...")

    thread = threading.Thread(
        target=do_translation,
        args=(text, source_name, target_name),
        daemon=True
    )
    thread.start()


def do_translation(text, source_name, target_name):
    try:
        source_code = LANGUAGES[source_name]
        target_code = LANGUAGES[target_name]

        parameters = urllib.parse.urlencode({
            "q": text,
            "langpair": source_code + "|" + target_code
        })

        url = (
            "https://api.mymemory.translated.net/get?"
            + parameters
        )

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "PythonTranslationTool/1.0"}
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        if data.get("responseStatus") != 200:
            error_message = data.get(
                "responseDetails",
                "The translation service could not translate this text."
            )
            raise ValueError(str(error_message))

        translated = data.get("responseData", {}).get(
            "translatedText", ""
        )

        if not translated:
            raise ValueError("No translated text was returned.")

        root.after(0, show_translation, translated)

    except Exception as error:
        root.after(0, show_error, str(error))


def show_translation(translated):
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, translated)
    status_label.config(text="Translation completed.")
    translate_button.config(state=tk.NORMAL, text="Translate")


def show_error(error):
    status_label.config(text="Translation unsuccessful.")
    translate_button.config(state=tk.NORMAL, text="Translate")

    messagebox.showerror(
        "Translation Error",
        "The online translation service could not complete "
        "your request.\n\n"
        "Please check your internet connection and try again.\n\n"
        "Details: " + error[:400]
    )


def copy_translation():
    translated = output_text.get("1.0", tk.END).strip()

    if not translated:
        messagebox.showwarning(
            "Nothing to Copy",
            "Please translate some text first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(translated)
    status_label.config(text="Translation copied to clipboard.")


def clear_text():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    status_label.config(text="Ready")


# Main application window
root = tk.Tk()
root.title("AI Language Translation Tool")
root.geometry("720x650")
root.minsize(600, 550)

title_label = tk.Label(
    root,
    text="AI Language Translation Tool",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=15)

# Language selection
language_frame = tk.Frame(root)
language_frame.pack(pady=5)

tk.Label(
    language_frame,
    text="Translate from:",
    font=("Arial", 11)
).grid(row=0, column=0, padx=5, pady=5)

source_language = ttk.Combobox(
    language_frame,
    values=list(LANGUAGES.keys()),
    state="readonly",
    width=15
)
source_language.set("English")
source_language.grid(row=0, column=1, padx=5)

tk.Label(
    language_frame,
    text="Translate to:",
    font=("Arial", 11)
).grid(row=0, column=2, padx=5)

target_language = ttk.Combobox(
    language_frame,
    values=list(LANGUAGES.keys()),
    state="readonly",
    width=15
)
target_language.set("Hindi")
target_language.grid(row=0, column=3, padx=5)

# Input section
tk.Label(
    root,
    text="Enter Text:",
    font=("Arial", 12, "bold")
).pack(anchor="w", padx=25, pady=(15, 5))

input_text = tk.Text(
    root,
    height=7,
    width=75,
    font=("Arial", 11),
    wrap=tk.WORD
)
input_text.pack(padx=25, fill="x")

# Translate button
translate_button = tk.Button(
    root,
    text="Translate",
    font=("Arial", 12, "bold"),
    command=translate_text
)
translate_button.pack(pady=12)

# Output section
tk.Label(
    root,
    text="Translated Text:",
    font=("Arial", 12, "bold")
).pack(anchor="w", padx=25, pady=5)

output_text = tk.Text(
    root,
    height=7,
    width=75,
    font=("Arial", 11),
    wrap=tk.WORD
)
output_text.pack(padx=25, fill="x")

# Copy and clear buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=12)

tk.Button(
    button_frame,
    text="Copy Translation",
    font=("Arial", 10),
    command=copy_translation
).grid(row=0, column=0, padx=8)

tk.Button(
    button_frame,
    text="Clear All",
    font=("Arial", 10),
    command=clear_text
).grid(row=0, column=1, padx=8)

status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 9),
    fg="gray"
)
status_label.pack(pady=5)

root.mainloop()
