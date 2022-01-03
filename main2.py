# krok 1: wczytywanie pliku w osobnym okienku - działa
# krok 2: wyświetlenie kolumn - do zrobienia z pomocą pliku table-display-test.py - more or less działa
# krok 3: wybór target kolumny - jest event do klikania w kolumnę z pomocą tamtej biblioteki
# krok 4: wyświetlenie drugiego okienka z plain textem *wynik*

from compare import build_models, CLASIFFIER_LIST
from tksheet import Sheet
from tkinter import filedialog, Toplevel
from PIL import ImageTk, Image
import tkinter as tk
import pandas as pd
import csv

class App(tk.Tk):
    def __init__(self):
        # initialize private properties
        self.root = tk.Tk.__init__(self)
        self.filename = 'D:/Projekty/Python/DataMining/example_data.csv'

        # label dla ścieżki
        path_input_label = tk.Label(self.root, text="Path:")
        path_input_label.grid(row=0, column=0, padx=10, pady=10)

        # input dla ścieżki
        path_input_box = tk.Entry(self.root, width=50, borderwidth=5)
        path_input_box.grid(row=0, column=1, columnspan=3, padx=10)

        path_input_box.insert(0, self.filename)

        button_1 = tk.Button(self.root, text="Browse", command=lambda: self.get_file_name(path_input_box))
        button_1.grid(row=0, column=5, columnspan=2, padx=10, pady=10)

        button_2 = tk.Button(self.root, text="Display data", command=lambda: self.display_data(self.filename))
        button_2.grid(row=2, column=5, padx=10, pady=10)

        button_3 = tk.Button(self.root, text="Open new window", command=lambda: self.display_computed_outcome(self.filename))
        button_3.grid(row=3, column=5, padx=10, pady=10)
        return

    # funkcja do pobierania pliku
    def get_file_name(self, output_text_box):
        # get file name
        self.filename = filedialog.askopenfilename(initialdir="", title="Wczytywanie pliku .csv", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        output_text_box.delete(0, tk.END)
        output_text_box.insert(0, self.filename)
        return

    # TODO funkcja wybierająca zmienną wyjaśniajacą
    def select_column(self, response):
        print(self.sheet.set_column_data(0, values=(0 for i in range(2050))))
        print(response)

        return

    # TODO funkcja robiąca magię w osobnym okienku
    def display_computed_outcome(self, filename):
        data = pd.read_csv(filename)
        # jeśli ta linijka wywala błąd to znaczy że potrzebuje by stworzyć folder 'matrices'
        output_data = build_models(data, data.iloc[:, -1], CLASIFFIER_LIST, 2137)
        print(output_data)
        window = Toplevel(self.root)

        file = 'matrices/SVC.jpg'
        image = Image.open(file)

        zoom = 0.2

        # multiple image size by zoom
        pixels_x, pixels_y = tuple([int(zoom * x) for x in image.size])

        img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
        label = tk.Label(window, image=img)
        label.image = img
        label.grid(row=4, column=1, columnspan=4, padx=10, pady=10)

    # TODO funkcja wyświetlająca dane + instrukcja obsługi w postaci małego tekstu
    def display_data(self, filename):
        # open file as dataframe
        data = pd.read_csv(filename)
        # zamiana csv
        file = open(filename, encoding='utf-8')
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            rows.append(row)
        print(rows)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.sheet = Sheet(self.frame,
                      page_up_down_select_row=True,
                      expand_sheet_if_paste_too_big=True,
                      # empty_vertical = 0,
                      column_width=80,
                      startup_select=(0, 1, "rows"),
                      data=rows[1:11:],
                      # data =[[f"Row {r}, Column {c}\nnewline1\nnewline2" for c in range(5)] for r in range(500)],
                      headers=rows[0],
                      height=250,  # height and width arguments are optional
                      width=800  # For full startup arguments see DOCUMENTATION.md
                      )
        self.frame.grid(row=2, column=0, columnspan=3, rowspan=2, sticky="nswe")
        self.sheet.grid(row=2, column=0, columnspan=3, rowspan=2, sticky="nswe")

        self.sheet.enable_bindings((
            "single_select",
            # "drag_select",
            # "select_all",
            # "column_select",
            # "row_select",
            # "column_width_resize",
            # "double_click_column_resize",
            # "arrowkeys",
            # "row_height_resize",
            # "double_click_row_resize",
            # "right_click_popup_menu",
            # "rc_select"
        ))
        self.sheet.extra_bindings(("column_select"), func=lambda: self.select_column("chleb"))

        # to tutaj z jakiegoś poodu nie działa


app = App()
app.title("Porównywarka klasyfikatorów")
app.resizable(False, False)
app.mainloop()