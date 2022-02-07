
from compare import build_models, CLASIFFIER_LIST
from tksheet import Sheet
from tkinter import filedialog, Toplevel
from PIL import ImageTk, Image
import tkinter as tk
import pandas as pd
import csv


def state_validate(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True


class App(tk.Tk):
    def __init__(self):
        # initialize private properties
        self.root = tk.Tk.__init__(self)
        self.filename = 'D:/Projekty/Python/DataMining/example_data.csv'
        # self.filename = 'C:/Users/ewaad/Documents/GitHub/DataMining/example_data.csv'
        self.window = None
        self.selected_column = None
        self.canvas = None
        self.header = None
        self.selected_column_label = None

        # label dla ścieżki
        path_input_label = tk.Label(self.root, text="Path:")
        path_input_label.place(x=15, y=17)

        # input dla ścieżki
        path_input_box = tk.Entry(self.root, width=70, borderwidth=4)
        path_input_box.place(x=60, y=15)

        self.button_1 = tk.Button(self.root, text="Browse", command=lambda: self.get_file_name(path_input_box), width=15)
        self.button_1.place(x=506, y=15)

        # add random state input
        state_input_label = tk.Label(self.root, text="Random state:")
        state_input_label.place(x=15, y=405)
        self.state_input_box = tk.Entry(self.root, width=10, borderwidth=4, validate="key")
        self.state_input_box['validatecommand'] = (self.state_input_box.register(state_validate), '%P', '%d')
        self.state_input_box.insert(0, '100')
        self.state_input_box.place(x=110, y=405)

        self.button_3 = tk.Button(self.root, text="Compare classifiers", command=lambda: self.display_computed_outcome(self.filename), state='disabled')
        # self.button_3.grid(row=3, column=5, padx=10, pady=10)
        self.button_3.place(x=506, y=435)

        # test button lol
        # self.button_4 = tk.Button(self.root, text="test", command=lambda: self.get_file_name(path_input_box), width=15)
        # self.button_4.place(x=506, y=85)

        return

    # funkcja do pobierania pliku
    def get_file_name(self, output_text_box):
        # get file name
        self.filename = filedialog.askopenfilename(initialdir="", title="Wczytywanie pliku .csv", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

        if len(self.filename) == 0:
            return

        try:
            self.display_data(self.filename)
            # if ^this fails the path in window won't change
            output_text_box.delete(0, tk.END)
            output_text_box.insert(0, self.filename)
            self.selected_column_label = tk.Label(self.root, text="Select target column")
            self.selected_column_label.place(x=15, y=50)
        except Exception as e:
            print(e)
            tk.messagebox.showerror("Error", "There was an error loading the file.")
        return

    # funkcja wybierająca zmienną wyjaśniajacą - kolumna
    def select_column(self, e):
        print(e.column)
        # you need to unbind the event to prevent recursion
        self.sheet.extra_bindings([("column_select", None)])
        self.sheet.select_column(e.column, redraw = True)
        self.selected_column = e.column
        # selected column label
        if self.selected_column_label:
            self.selected_column_label.config(text="")
        self.selected_column_label = tk.Label(self.root, text="Target variable: "+(str(self.header[self.selected_column]) if str(self.selected_column) else "no"))
        # self.selected_column_label.grid(row=1, column=0, padx=10, pady=10)
        self.selected_column_label.place(x=15, y=50)
        self.sheet.extra_bindings([("column_select", self.select_column)])
        self.button_3["state"] = "normal"
        return

    # funkcja do scrolla w oknie wyniku
    def _on_mousewheel(self, e):
        try:
            self.canvas.yview_scroll(-1 * (e.delta // 120), "units")
        except:
            pass # TODO xD
            # bez tego try/except wywala błąd, że nie może wykonać tej linijki, a to dlatego, że okno nie istnieje
            # ale on uważa inaczej :V

    # funkcja robiąca magię w osobnym okienku
    def display_computed_outcome(self, filename):
        data = pd.read_csv(filename)
        # jeśli ta linijka wywala błąd to znaczy że potrzebuje by stworzyć folder 'matrices'
        try:
            output_data = build_models(data, data.iloc[:,self.selected_column], CLASIFFIER_LIST, int(self.state_input_box.get()) if self.state_input_box.get() else 1)
        except Exception as e:
            print(e)
            tk.messagebox.showerror("Error", "Please select a binary target column.")

        # allow to only open one window
        if self.window is not None:
            self.window.destroy()
        self.window = Toplevel(self.root, padx=10, pady=10)
        self.window.geometry('1490x990')
        # self.window.geometry('640x480')

        # configure scrollbar
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=1)
        self.canvas = tk.Canvas(main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=inner_frame, anchor="nw")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # display outcome in frames
        inner_frame.grid_columnconfigure(0, weight=1)
        i = 0
        row = 0
        for model in output_data:
            frame = tk.LabelFrame(inner_frame, text=model, padx=5, pady=5)
            # frame.pack(fill="x", expand=1)
            frame.grid(row=row, column=i % 3, sticky="we")
            if i % 3 == 2:
                row += 1
            j = 0
            for attribute in output_data[model]:
                if attribute == "confusion_matrix_path":
                    image = Image.open(output_data[model][attribute])
                    zoom = 0.2
                    pixels_x, pixels_y = tuple([int(zoom * x) for x in image.size])
                    img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
                    label = tk.Label(frame, image=img)
                    label.image = img
                    label.grid(row=0, column=0, rowspan=5)
                else:
                    attr = tk.Label(frame, text=f"{attribute}: {output_data[model][attribute]}")
                    attr.grid(row=1+j, column=1)
                    j += 1
            i += 1

    # funkcja wyświetlająca tabele z danymi  + instrukcja obsługi w postaci małego tekstu
    def display_data(self, filename):
        # zamiana csv
        file = open(filename, encoding='utf-8')
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            rows.append(row)
        self.header = rows[0]
        self.frame = tk.Frame(self, borderwidth=2, bg='grey')
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.sheet = Sheet(self.frame,
                      # page_up_down_select_row=True,
                      # expand_sheet_if_paste_too_big=True,
                      # empty_vertical = 0,
                      column_width=80,
                      startup_select=(0, 1, "rows"),
                      data=rows[1:16:],
                      headers=self.header,
                      height=300,
                      width=600
                      )
        # self.frame.grid(row=2, column=0, columnspan=3, rowspan=2, sticky="nswe")
        self.frame.place(x=15, y=85) # y=120 if button_2 exists, 85 if not
        self.sheet.grid(row=2, column=0, columnspan=3, rowspan=2, sticky="nswe")

        self.sheet.enable_bindings((
            "single_select",
            "column_select"
        ))
        self.sheet.extra_bindings([("cell_select", self.select_column)])
        # to tutaj z jakiegoś powodu nie działa


app = App()
app.title("Classifier comparator")
app.geometry('640x480')
# app.geometry('800x640')
app.resizable(False, False)
app.mainloop()