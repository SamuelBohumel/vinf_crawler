import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import Pillow


def search_keywords(*args):
    search_term = search_var.get()
    result_text.delete(1.0, tk.END)  # Clear previous results

    result_text.insert(tk.END, search_term)
    # with open('text_file.txt', 'r') as file:
    #     for line in file:
    #         if search_term in line:
                

app = tk.Tk()
app.title('Keyword Search App')

# Set default window size
app.geometry('800x600')

# Load and resize your logo
logo_image = Image.open('logo.png')  # Replace 'logo.png' with your image file
quantif = 0.5
logo_image = logo_image.resize((round(logo_image.width*quantif), 
                                round(logo_image.height*quantif)), 
                                Image.ANTIALIAS)  # Adjust the size as needed
logo = ImageTk.PhotoImage(logo_image)

# Create a label for the logo and use grid for centering
logo_label = ttk.Label(app, image=logo)
logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Create a frame to center the search elements
frame = ttk.Frame(app)
frame.grid(row=1, column=0, columnspan=2)

logo_label = ttk.Label(app, image=logo, anchor='center')
logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

search_label = ttk.Label(app, text='Enter search keyword:')
search_label.grid(row=1, column=0, padx=10, pady=(5, 0), sticky='w')

search_var = tk.StringVar()
search_var.trace('w', lambda name, index, mode, sv=search_var: search_keywords(search_var))
search_entry = ttk.Entry(app, textvariable=search_var)
search_entry.grid(row=2, column=0, padx=10, pady=5, sticky='ew')

search_button = ttk.Button(app, text='Next match', command=search_keywords)
search_button.grid(row=2, column=1, padx=(0, 10), pady=5, sticky='ew')

result_text = tk.Text(app, wrap=tk.WORD, height=10, width=40)
result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Column and row weights to make widgets expand correctly
app.columnconfigure(0, weight=1)
app.rowconfigure(3, weight=1)

app.mainloop()