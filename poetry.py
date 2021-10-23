"""A poetry analyzer."""

import tkinter as tk
import tkinter.ttk
from tkinter import filedialog
from tkinter import scrolledtext
import poetry_functions
import poetry_reader

DICTIONARY_FILENAME = 'dictionary.txt'
POETRY_FORMS_FILENAME = 'poetry_forms.txt'
WELCOME_MESSAGE = '''\
Welcome to the poetry analyzer. Please select a poetry form and open a poetry
file, then click the Analyze Poem button.  Feel free to change this text in
poetry.py.  If you break it, you can always download it again.  :-)'''


# ************************
# Scrollable Frame Class
# ************************
class ScrollFrame(tk.Frame):
    """A GUI frame with a scrollbar"""

    # Credit for this class is given to
    # https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
    # with some modifications

    def __init__(self, parent: tk.Frame) -> None:
        """Initialize a frame with a scrollbar"""

        super().__init__(parent)  # create a frame (self)

        # A Canvas for the window contents, and a viewport frame
        # to hold the widgets.
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.view_port = tk.Frame(self.canvas)

        # Create scrollbars and add them to the canvas.
        self.vsb = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview)
        self.hsb = tk.Scrollbar(
            self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set,
                              xscrollcommand=self.hsb.set)

        self.vsb.pack(side="right", fill="y")  # pack scrollbar to right
        self.hsb.pack(side="bottom", fill="x")  # pack scrollbar to bottom

        # add view port frame to canvas
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window(
            (4, 4), window=self.view_port, anchor="nw", tags="self.viewPort")

        # bind events for whenever the size of the viewPort frame changes.
        self.view_port.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # perform an initial stretch on render, otherwise the scroll region has
        # a tiny border until the first resize
        self.on_frame_configure(None)

    def on_frame_configure(self, event: tk.Event) -> None:
        """Reset the scroll region to encompass the inner frame"""

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event: tk.Event) -> None:
        """Reset the canvas window to encompass inner frame when required"""

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class PoetryApp(tk.Frame):
    """A GUI for the poetry application."""

    def __init__(self, poetry_root: tk.Frame) -> None:
        """Initialize the Poetry App along with its gadgets"""

        # Read the dictionary and poetry forms files
        self.word_pronunciations = poetry_reader.read_pronouncing_dictionary(
            open(DICTIONARY_FILENAME, 'r', encoding="utf-8"))
        self.poetry_patterns = poetry_reader.read_poetry_form_descriptions(
            open(POETRY_FORMS_FILENAME, 'r', encoding="utf-8"))

        # Build the user interface
        poetry_root.title("Pure Poetry")
        screen_width = poetry_root.winfo_screenwidth()
        screen_height = poetry_root.winfo_screenheight()
        width, height = screen_width * 0.5, screen_height * 0.5
        self.width, self.height = width, height

        # calculate x and y coordinates for the Tk root window
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.annotation_height = int(self.height / 50)

        # set the dimensions of the screen and where it is placed
        poetry_root.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.master = poetry_root

        tk.Frame.__init__(self, poetry_root)
        self.scroll_frame = ScrollFrame(self)
        self.scroll_frame.width = width
        self.scroll_frame.height = height

        self.create_screen_components()

        # pack scrollFrame itself
        self.scroll_frame.pack(
            side="top", fill="both", expand=True, padx=(5, 0), pady=(5, 0))

    def create_screen_components(self) -> None:
        """Create the components of the app screen including text, text boxes,
        buttons, and so on"""

        # Put things in rows to organize gadgets.
        row_number = 0

        # The greeting at the top of the window.
        welcome_label = tk.Label(
            self.scroll_frame.view_port,
            text=WELCOME_MESSAGE,
            justify=tk.LEFT,
            font="Arial 14")
        welcome_label.grid(
            row=row_number, column=0, columnspan=1, sticky=tk.W)
        row_number += 1

        # The row of text fields containing the poetry analysis.
        self.build_poetry_analysis_frame(row_number)

        row_number += 1

        # The row of buttons along the bottom.
        self.build_bottom_button_frame(row_number)

        self.scroll_frame.columnconfigure(0, weight=0)

    def build_poetry_analysis_frame(self, row_number: int) -> None:
        """Create and add a frame for a poem/syllable count/rhyme scheme frame,
        a poetry form frame, and a pronunciation frame.
        """

        poetry_analysis_frame = tk.Frame(self.scroll_frame.view_port)
        poetry_analysis_frame.grid(
            row=row_number, column=0, columnspan=1, pady=10, sticky=tk.W)

        col_number = 0
        self.build_poem_frame(poetry_analysis_frame, col_number)

        col_number += 1
        self.build_poetry_form_frame(poetry_analysis_frame, col_number)

        col_number += 1
        self.build_pronunciation_frame(poetry_analysis_frame, col_number)

    def build_pronunciation_frame(
            self, poetry_analysis_frame: tk.Frame, col_number: int) -> None:
        """Built the frame for the pronunciation.
        """

        pronunciation_frame = tk.Frame(
            poetry_analysis_frame, borderwidth=1, relief=tk.GROOVE)
        pronunciation_frame.grid(
            row=0, column=col_number, columnspan=1, pady=10, sticky=tk.W)

        # Pronunciation header
        pronouncing_header = tk.Label(
            pronunciation_frame, text='Pronunciation')
        pronouncing_header.grid(
            row=0, column=0, columnspan=1, sticky=tk.W + tk.E + tk.N + tk.S)

        # Pronunciation
        self.pronunciation_text = tk.scrolledtext.ScrolledText(
            pronunciation_frame,
            width=int(self.width / 15),
            height=self.annotation_height)
        self.pronunciation_text.insert('1.0', 'Poem pronunciation')
        self.pronunciation_text.config(state=tk.DISABLED)
        self.pronunciation_text.grid(
            row=1, column=0, sticky=tk.W, columnspan=1, rowspan=1)

    def build_poem_frame(
            self, poetry_analysis_frame: tk.Frame, col_number: int) -> None:
        """Build the frame containing the poem."""

        poem_frame = tk.Frame(
            poetry_analysis_frame, borderwidth=1, relief=tk.GROOVE)
        poem_frame.grid(row=0, column=col_number, padx=10, pady=10, sticky=tk.W)

        row_number = 0

        self.add_poem_header(poem_frame, row_number)
        row_number += 1
        col_number = 0

        self.add_poem_text(col_number, poem_frame, row_number)
        col_number += 1

        self.add_rhyme_scheme(col_number, poem_frame, row_number)
        col_number += 1

        self.add_num_syllables(col_number, poem_frame, row_number)
        col_number += 1

    def add_num_syllables(
            self, col_number: int,
            poem_frame: tk.Frame, row_number: int) -> None:
        """Add template number of syllables text to row row_number and column
        col_number of the poem_frame."""
        self.num_syllables_text = tk.scrolledtext.ScrolledText(
            poem_frame, width=3, height=self.annotation_height)
        self.num_syllables_text.insert('1.0', '# Syllables')
        self.num_syllables_text.config(state=tk.DISABLED)
        self.num_syllables_text.grid(
            row=row_number, column=col_number,
            sticky=tk.W, columnspan=1, rowspan=1)

    def add_rhyme_scheme(
            self, col_number: int,
            poem_frame: tk.Frame, row_number: int) -> None:
        """Add template rhyme scheme text to row row_number and column
        col_number of the poem_frame."""
        self.rhyme_scheme_text = tk.scrolledtext.ScrolledText(
            poem_frame, width=3, height=self.annotation_height)
        self.rhyme_scheme_text.insert('1.0', 'Rhyme scheme')
        self.rhyme_scheme_text.config(state=tk.DISABLED)
        self.rhyme_scheme_text.grid(
            row=row_number, column=col_number,
            sticky=tk.W, columnspan=1, rowspan=1)

    def add_poem_text(
            self, col_number: int,
            poem_frame: tk.Frame, row_number: int) -> None:
        """Add template poem text to row row_number and column col_number of
        the poem_frame."""
        self.poem_text = tk.scrolledtext.ScrolledText(
            poem_frame,
            width=int(self.width / 30),
            height=self.annotation_height)
        self.poem_text.insert('1.0', 'Poem')
        self.poem_text.grid(
            row=row_number, column=col_number,
            sticky=tk.W, columnspan=1, rowspan=1)

    def add_poem_header(self, poem_frame: tk.Frame, row_number: int) -> None:
        """Add the poem header to row number row_number of poem_frame."""
        poem_header = tk.Label(poem_frame, text='Poem')
        poem_header.grid(
            row=row_number, column=0, columnspan=3,
            sticky=tk.W + tk.E + tk.N + tk.S)

    def build_poetry_form_frame(
            self, poetry_analysis_frame: tk.Frame, col_number: int) -> None:
        """Build the frame containing the poem, poetry form, and pronunciation
        subframes."""

        # The poetry form rhyme scheme and number of syllables.
        poetry_form_frame = tk.Frame(
            poetry_analysis_frame, borderwidth=1, relief=tk.GROOVE)
        poetry_form_frame.grid(
            row=0, column=col_number, padx=10, pady=10, sticky=tk.W)

        row_number = 0
        col_number = 0

        # Poetry form header
        poetry_form_header = tk.Label(poetry_form_frame, text='Poetry Form')
        poetry_form_header.grid(
            row=row_number, column=col_number,
            columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)

        row_number += 1
        col_number = 0

        # Poetry form rhyme scheme
        self.form_rhyme_scheme_text = tk.scrolledtext.ScrolledText(
            poetry_form_frame, width=3, height=self.annotation_height)
        self.form_rhyme_scheme_text.insert('1.0', 'Rhyme scheme')
        self.form_rhyme_scheme_text.config(state=tk.DISABLED)
        self.form_rhyme_scheme_text.grid(row=row_number, column=col_number,
                                         sticky=tk.W, columnspan=1, rowspan=1)
        col_number += 1

        # Poetry form number of syllables
        self.form_num_syllables_text = tk.scrolledtext.ScrolledText(
            poetry_form_frame, width=3, height=self.annotation_height)
        self.form_num_syllables_text.insert('1.0', '# Syllables')
        self.form_num_syllables_text.config(state=tk.DISABLED)
        self.form_num_syllables_text.grid(
            row=row_number, column=col_number,
            sticky=tk.W, columnspan=1, rowspan=1)
        return col_number, row_number

    def build_bottom_button_frame(self, row_number: int) -> None:
        """Build the bottom frame of buttons."""

        # A frame for the buttons and menus
        button_frame = tk.Frame(self.scroll_frame.view_port)
        button_frame.grid(
            row=row_number, column=0,
            columnspan=6, padx=10, pady=10, sticky=tk.W)

        row_number = 0
        col_number = 0

        self.add_open_poem_button(button_frame, col_number)
        col_number += 1

        self.add_analyze_poem_button(button_frame, col_number)
        col_number += 1

        self.add_form_selector_label(button_frame, col_number, row_number)
        col_number += 1

        self.add_form_dropdown_menu(button_frame, col_number, row_number)
        col_number += 1

        # Quit
        quit_btn = tk.Button(
            button_frame, text="QUIT", fg="red", width=int(self.width / 80),
            height=2, command=lambda: self.master.destroy())
        quit_btn.grid(row=0, column=col_number, padx=10, pady=2, sticky=tk.W)

    def add_form_dropdown_menu(
            self, button_frame: tk.Frame,
            col_number: int, row_number: int) -> None:
        """Create and add a dropdown menu of poetry forms to row row_number
        and column col_number of the button_frame."""

        self.poetry_form_var = tk.StringVar(button_frame)
        self.poetry_form_var.set("")  # default value
        self.poetry_pattern_menu = tk.ttk.Combobox(
            button_frame,
            state="readonly",
            textvariable=self.poetry_form_var,
            values=list(self.poetry_patterns.keys()))
        self.poetry_pattern_menu.grid(
            row=row_number, column=col_number, padx=10, pady=2, sticky=tk.W)
        self.poetry_pattern_menu.bind(
            '<<ComboboxSelected>>', self.update_poetry_form)

    def add_form_selector_label(
            self, button_frame: tk.Frame,
            col_number: int, row_number: int) -> None:
        """Create and add open poem file button to row row_number and column
        col_number of the button_frame."""
        form_selector_lbl = tk.Label(button_frame, text='Select poetry form:')
        form_selector_lbl.grid(
            row=row_number, column=col_number, padx=10, pady=2, sticky=tk.W)

    def add_analyze_poem_button(
            self, button_frame: tk.Frame, col_number: int) -> None:
        """Create and add open poem file button to column col_number of
        the button_frame."""
        analyze_btn = tk.Button(
            button_frame, text="Analyze Poem",
            width=int(self.width / 80), height=2,
            command=lambda: self.analyze_poem())
        analyze_btn.grid(
            row=0, column=col_number,
            columnspan=1, padx=10, pady=2, sticky=tk.E)

    def add_open_poem_button(
            self, button_frame: tk.Frame, col_number: int) -> None:
        """Create and add open poem file button to column col_number of
        the button_frame."""
        open_poem_btn = tk.Button(
            button_frame, text="Open Poem File",
            width=int(self.width / 80), height=2,
            command=lambda: self.choose_poem_file())
        open_poem_btn.grid(
            row=0, column=col_number,
            columnspan=1, padx=10, pady=2, sticky=tk.E)

    def update_poetry_form(self, event: tk.Event) -> None:
        """React to a new poetry form being chosen: update
        self.form_rhyme_scheme_text and self.form_num_syllables_text.
        """
        poetry_form = self.poetry_form_var.get()

        form_num_syllables = (
            str(i) for i in self.poetry_patterns[poetry_form][0])
        form_rhyme_scheme = (
            str(i) for i in self.poetry_patterns[poetry_form][1])

        syllables = '\n'.join(form_num_syllables)
        scheme = '\n'.join(form_rhyme_scheme)

        self.update_box(self.form_rhyme_scheme_text, scheme)
        self.update_box(self.form_num_syllables_text, syllables)

    def choose_poem_file(self) -> None:
        """Prompt for a text file containing a poem, read it, clean it,
        and display it in self.poem_text.
        """
        poem_filename = filedialog.askopenfilename(
            initialdir=".", title="Select poetry file",
            filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        # poem_filename = get_valid_filename("Enter a poem filename: ")
        poem_file = open(poem_filename)
        poem = poetry_reader.read_and_trim_whitespace(poem_file)
        self.update_box(self.poem_text, poem)

    def analyze_poem(self) -> None:
        """Analyze the poem in self.poem_text (which has already been cleaned!)
        and display the number of syllables per line and the rhyme scheme. Also
        display the phonetic representation.
        """
        poem = self.poem_text.get('1.0', tk.END)

        # Tokenize the words by cleaning them and extracting the phonemes.
        poem_lines = poetry_functions.clean_poem(poem)
        poem_pronunciation = poetry_functions.extract_phonemes(
            poem_lines, self.word_pronunciations)

        # Show the pronunciation.
        poem_pronunciation_str = poetry_functions.phonemes_to_str(
            poem_pronunciation)
        self.update_box(self.pronunciation_text, poem_pronunciation_str)

        # Show the rhyme scheme.
        poem_scheme = poetry_functions.get_rhyme_scheme(poem_pronunciation)
        self.update_box(self.rhyme_scheme_text, '\n'.join(poem_scheme))

        # Show the number of syllables for each line.
        poem_syllables = poetry_functions.get_num_syllables(poem_pronunciation)

        # We nearly made this next one a required function in
        # poetry_functions.py, but wanted to show you this cool trick.  :-)
        poem_syllables_text = '\n'.join((str(i) for i in poem_syllables))
        self.update_box(self.num_syllables_text, poem_syllables_text)

    def update_box(self, box: scrolledtext.ScrolledText, message: str) -> None:
        """Clear the output box in the app and put message inside it."""

        box.config(state=tk.NORMAL)
        box.delete('1.0', tk.END)
        box.insert('1.0', message)
        box.config(state=tk.DISABLED)


if __name__ == '__main__':
    root = tk.Tk()
    PoetryApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
