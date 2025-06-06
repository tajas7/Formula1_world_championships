# === Imports ===

import pandas as pd

# Vanilla
from src.analysis.homemade.mandatory1 import at_least_n_races_nopd
from src.analysis.homemade.mandatory2 import ranking_nopd
from src.analysis.homemade.q1 import driver_mean_grid_nopd
from src.analysis.homemade.q2 import get_driver_with_most_dnfs_nopd

# Pandas
from src.analysis.pandas.mandatory1 import at_least_n_races
from src.analysis.pandas.mandatory2 import ranking
from src.analysis.pandas.q1 import driver_mean_grid
from src.analysis.pandas.q2 import get_driver_with_most_dnfs
from src.analysis.pandas.q3 import most_dangerous_circuit
from src.analysis.pandas.q4 import constructor_winner
from src.analysis.pandas.q5_graph import most_constructor_championships_won
from src.analysis.pandas.q6_graph import nationalities
from src.analysis.pandas.q7 import most_technical_issues_constructors
from src.analysis.pandas.q8 import average_pit_stop_time
from src.analysis.compare import compare_execution_time

# Clustering function
from src.learning.clustering import cluster_driving_styles

# Interface
import tkinter as tk
import customtkinter as ctk
import inspect
from PIL import Image, ImageTk
import shutil


# Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BG_MAIN = "#1f2a38"
BG_SUB = "#2c3e50"
BTN_COLOR = "#2980b9"
BTN_HOVER = "#1f6391"

interface = ctk.CTk()
interface.geometry('950x950')
interface.title('Interface - Projet Traitement de Données')
interface.resizable(False, False)
interface.iconbitmap('f1.ico')

# Menu
menu = tk.Menu(interface)

data = tk.Menu(menu, tearoff=0)


def open_csv_preview(title):
    """
    Opens a preview window displaying the contents of a specified CSV file

    Parameters
    ----------
    title : str
        Name (not path) of the CSV file  located in the 'data/' folder

    Displays
    --------
    A table view of the first 15 rows of the selected CSV file

    """
    try:
        df = pd.read_csv(f"data/{title}.csv")
        preview_window = ctk.CTkToplevel(interface)
        preview_window.title(f"Preview – {title}")
        preview_window.geometry("900x500")
        preview_window.configure(fg_color=BG_SUB)
        preview_window.iconbitmap('f1.ico')

        ctk.CTkLabel(preview_window,
                     text=f"Aperçu de {title}.csv",
                     font=("Verdana", 15, "bold")).pack(pady=10)

        frame = tk.Frame(preview_window, bg=BG_MAIN)
        frame.pack(expand=True, fill="both", padx=20, pady=10)

        style = tk.ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2c3e50", foreground="white",
                        fieldbackground="#2c3e50", rowheight=25, font=("Verdana", 10))
        style.configure("Treeview.Heading", background="#34495e",
                        foreground="white", font=("Verdana", 10, "bold"))

        tree = tk.ttk.Treeview(frame, columns=list(df.columns), show="headings")
        hsb = tk.ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        vsb = tk.ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)

        for col in df.columns:
            tree.heading(col, text=col)
            max_len = max(df[col].astype(str).map(len).head(15).max(), len(col))
            tree.column(col,
                        anchor="center",
                        width=max(80, min(max_len * 10, 300)),
                        stretch=True)

        for _, row in df.head(15).iterrows():
            full_values = [str(val) for val in row.values]
            tree.insert("", "end", values=full_values)

        tree.pack(side="top", fill="both", expand=True)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right", fill="y")

        preview_window.grab_set()
        preview_window.focus_set()
        preview_window.wait_window()

    except Exception as e:
        tk.messagebox.showerror("Error", f"Cannot open {title}.csv : {str(e)}")


for item in [
        "driver_standings", "drivers", "circuits", "races", "results", "seasons",
        "constructor_results", "constructor_standings", "status", "lap_times",
        "pit_stops", "qualifying", "sprint_results"]:
    data.add_command(label=item, command=lambda name=item: open_csv_preview(name))

menu.add_cascade(label="Data", menu=data)


def open_about_f1():
    """
    Opens a window that shows the content of 'about_f1.md'.

    """
    try:
        with open("about_f1.md", "r", encoding="utf-8") as f:
            content = f.read()
        window = ctk.CTkToplevel(interface)
        window.title("About F1")
        window.geometry("800x600")
        window.configure(fg_color=BG_SUB)

        ctk.CTkLabel(window,
                     text="about_f1.md – Formule 1",
                     font=("Verdana", 15, "bold")).pack(pady=10)

        text_widget = tk.Text(window, wrap="word", font=("Verdana", 11),
                              bg="black", fg="white", insertbackground="white")
        text_widget.insert("1.0", content)
        text_widget.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        window.grab_set()
        window.focus_set()
        window.wait_window()
    except Exception as e:
        tk.messagebox.showerror("Error", f"Cannot open about_f1.md : {str(e)}")


menu.add_command(label="About F1", command=open_about_f1)
interface.config(menu=menu)

# Header
header = ctk.CTkFrame(interface, corner_radius=15, fg_color=BG_MAIN)
ctk.CTkLabel(header,
             text="Formula 1",
             font=("Verdana", 30, "bold")).pack(pady=(10, 5), padx=20)
ctk.CTkLabel(header,
             text="Data Processing Project",
             font=("Verdana", 15, "italic")).pack(pady=(0, 10), padx=20)
header.pack(padx=30, pady=20, fill='x')


# Windows opened when one clicks on a button "Code" or "Compare" or "Answer"
def open_code_window(title, func):
    """
    Opens a window that displays the source code of a given function

    Parameters
    ----------
    title : str
        Title for the window.
    func : function
        Python function whose source code will be displayed

    """
    window = ctk.CTkToplevel(interface)
    window.title(f"Code – {title}")
    window.geometry("800x600")
    window.configure(fg_color=BG_SUB)

    ctk.CTkLabel(window,
                 text=f"Code – {title}",
                 font=("Verdana", 15, "bold")).pack(pady=15)

    text_widget = tk.Text(window, wrap="word", font=("Courier", 10), bg="black",
                          fg="white", insertbackground="white")
    text_widget.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    try:
        text_widget.insert("1.0", inspect.getsource(func))
    except Exception as e:
        text_widget.insert("1.0", f"Unable to load source code: {str(e)}")

    window.grab_set()
    window.focus_set()
    window.wait_window()


def open_dual_code_window(title, func_pd, func_np):
    """
    Opens a window that displays the source code of both a Pandas and a Vanilla Python
    version of the same function for comparison purposes

    Parameters
    ----------
    title : str
        Title for the window
    func_pd : function
        The version of the function that uses Pandas
    func_np : function
        The version of the function that uses only base Python

    """
    window = ctk.CTkToplevel(interface)
    window.title(f"Code – {title}")
    window.geometry("800x700")
    window.configure(fg_color=BG_SUB)

    ctk.CTkLabel(window, text=f"Code – {title}",
                 font=("Verdana", 15, "bold")).pack(pady=10)

    for label, func in [("Pandas version", func_pd),
                        ("Vanilla Python version", func_np)]:
        ctk.CTkLabel(window,
                     text=label,
                     font=("Verdana", 13, "italic")).pack(pady=(10, 2))
        text_widget = tk.Text(window, wrap="word", font=("Courier", 10),
                              bg="black", fg="white", insertbackground="white",
                              height=15)
        try:
            text_widget.insert("1.0", inspect.getsource(func))
        except Exception as e:
            text_widget.insert("1.0", f"Unable to load source code: {str(e)}")
        text_widget.pack(expand=False, fill="x", padx=20, pady=(0, 10))

    window.grab_set()
    window.focus_set()
    window.wait_window()


def show_comparison_result(func_vanilla, func_pandas):
    """
    Executes both a Vanilla Python and a Pandas function and compares their
    execution time

    Parameters
    ----------
    func_vanilla : function
        The base Python implementation
    func_pandas : function
        The Pandas implementation

    Displays
    --------
    A message box with the execution time of each version and the time difference

    """
    try:
        result = compare_execution_time(func_vanilla, func_pandas)
        tk.messagebox.showinfo("Execution Time Comparison",
                               f"Vanilla Python: {result['vanilla']:.6f} s\n"
                               f"Pandas: {result['modules']:.6f} s\n"
                               f"Difference: {result['difference']:.6f} s")
    except Exception as e:
        tk.messagebox.showerror("Error", str(e))


def open_question_window_with_input(title, func_pandas, func_nopd, param_info,
                                    allow_toggle):
    """
    Opens a dynamic input window for a question, allowing the user to provide
    parameters and run either the Pandas or Vanilla version of a function

    Parameters
    ----------
    title : str
        The title of the question
    func_pandas : function
        The Pandas version of the function to execute
    func_nopd : function
        The Vanilla Python version
    param_info : list
        List of dictionaries describing expected parameters (label, default value, type)
    allow_toggle : bool
        If True, allows the user to select which implementation to run

    """
    if title in [
        "Which constructors have won the most Constructors’ Championships?",
        "Which nationality has the highest number of F1 drivers?"
    ]:
        try:
            func_pandas()
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))
        return

    window = ctk.CTkToplevel(interface)
    window.title(title)
    window.geometry("700x750")
    window.configure(fg_color=BG_SUB)

    ctk.CTkLabel(window, text=title, font=("Verdana", 15, "bold")).pack(pady=15)

    use_pandas = tk.BooleanVar(value=True)
    if allow_toggle:
        toggle = ctk.CTkFrame(window, fg_color="transparent")
        ctk.CTkLabel(toggle,
                     text="Use Pandas:",
                     font=("Verdana", 11)).pack(side="left", padx=10)
        ctk.CTkRadioButton(toggle,
                           text="Yes",
                           variable=use_pandas,
                           value=True).pack(side="left", padx=5)
        ctk.CTkRadioButton(toggle,
                           text="No",
                           variable=use_pandas,
                           value=False).pack(side="left", padx=5)
        toggle.pack(pady=10)

    entries = []
    for info in param_info:
        frame = ctk.CTkFrame(window, fg_color="transparent")
        frame.pack(pady=5, padx=20, anchor="w")
        ctk.CTkLabel(frame, text=info["label"], font=("Verdana", 11)).pack(side='left')
        entry = ctk.CTkEntry(frame, width=180)
        entry.insert(0, str(info["default"]) if info["default"] is not None else "")
        entry.pack(side='left', padx=8)
        entries.append((entry, info["type"]))

    result_frame = ctk.CTkFrame(window, fg_color=BG_MAIN)
    result_frame.pack(pady=20, fill='x', padx=30)
    result_label = ctk.CTkLabel(result_frame, text="", font=("Courier", 12))
    result_label.pack(padx=10, pady=10)

    def run():
        try:
            values = []
            for entry, typ in entries:
                val = entry.get().strip()
                if val == "" and typ != str:
                    val = None
                elif typ == int:
                    val = int(val)
                elif typ == bool:
                    val = val.lower() == "true"
                values.append(val)
            if allow_toggle and use_pandas.get():
                chosen_func = func_pandas
            else:
                chosen_func = func_nopd
            result = chosen_func(*values)
            result_label.configure(text=f"{result}")
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

    ctk.CTkButton(window, text="Run", command=run).pack(pady=10)

    window.grab_set()
    window.focus_set()
    window.wait_window()


# Questions
question_data = [
    ("Which drivers have won 30 or more races in their careers?",
     at_least_n_races, at_least_n_races_nopd,
     [{"label": "Minimum wins:", "default": 30, "type": int}], True),

    ("What was the final drivers ranking for the 2023 season?",
     ranking, ranking_nopd,
     [{"label": "Year:", "default": 2023, "type": int}], True),

    ("What is Lewis Hamilton's average starting position?",
     driver_mean_grid, driver_mean_grid_nopd,
     [{"label": "First name:", "default": "Lewis", "type": str},
      {"label": "Last name:", "default": "Hamilton", "type": str}], True),

    ("Which drivers have recorded the most DNFs in their careers?",
     get_driver_with_most_dnfs, get_driver_with_most_dnfs_nopd,
     [], True),

    ("Which circuit has been the most dangerous historically?",
     most_dangerous_circuit, most_dangerous_circuit,
     [{"label": "Country:", "default": "", "type": str}], False),

    ("Which constructor won the Constructors’ Championship in 2023?",
     constructor_winner, constructor_winner,
     [{"label": "Year:", "default": 2023, "type": int}], False),

    ("Which constructors have won the most Constructors’ Championships?",
     most_constructor_championships_won, most_constructor_championships_won,
     [], False),

    ("Which nationality has the highest number of F1 drivers?",
     nationalities, nationalities,
     [], False),

    ("Which constructors have encountered the most technical failures?",
     most_technical_issues_constructors, most_technical_issues_constructors,
     [{"label": "Top:", "default": 5, "type": int}], False),

    ("What is the average pit stop time across races?",
     average_pit_stop_time, average_pit_stop_time,
     [{"label": "Outliers:", "default": "False", "type": bool},
      {"label": "Sup:", "default": 60, "type": int}], False)
]

# Display
questions = ctk.CTkFrame(interface, corner_radius=15, fg_color=BG_MAIN)
questions.pack(padx=30, pady=20, fill='x', expand=True)

for i, (title, func_pd, func_np, params, toggle) in enumerate(question_data):
    frame = ctk.CTkFrame(questions, corner_radius=10, fg_color=BG_SUB)
    frame.columnconfigure(0, weight=1)

    ctk.CTkLabel(frame, text=title, font=("Verdana", 14), anchor="w").grid(
        row=0, column=0, sticky="w", padx=10, pady=5)

    if i < 4:
        def make_compare_callback(f_np=func_np, f_pd=func_pd, p=params):
            def callback():
                args = [arg["default"] for arg in p]
                show_comparison_result(lambda: f_np(*args), lambda: f_pd(*args))
            return callback

        ctk.CTkButton(
            frame, text="Compare", corner_radius=8, width=100, height=30,
            fg_color="#e91e63", hover_color="#ad1457",
            command=make_compare_callback()
        ).grid(row=0, column=1, padx=(5, 5), pady=5, sticky="e")

        ctk.CTkButton(
            frame, text="Code", corner_radius=8, width=100, height=30,
            fg_color="#16a085", hover_color="#117864",
            command=lambda t=title,
            fpd=func_pd,
            fnp=func_np: open_dual_code_window(t, fpd, fnp)
        ).grid(row=0, column=2, padx=(5, 5), pady=5, sticky="e")
    else:
        ctk.CTkButton(
            frame, text="Code", corner_radius=8, width=100, height=30,
            fg_color="#16a085", hover_color="#117864",
            command=lambda t=title, f=func_pd: open_code_window(t, f)
        ).grid(row=0, column=2, padx=(5, 5), pady=5, sticky="e")

    ctk.CTkButton(
        frame, text="Answer", corner_radius=8, width=100, height=30,
        fg_color=BTN_COLOR, hover_color=BTN_HOVER,
        command=lambda t=title, fpd=func_pd, fnp=func_np, p=params, tog=toggle:
            open_question_window_with_input(t, fpd, fnp, p, tog)
    ).grid(row=0, column=3, padx=(5, 10), pady=5, sticky="e")

    frame.pack(pady=8, padx=10, fill='x', expand=True)


# Export results

def open_export_window():
    """
    Opens a window allowing the user to select questions' parameters and export
    their results to a chosen directory

    """
    window = ctk.CTkToplevel(interface)
    window.title("Export Results")
    window.geometry("850x750")
    window.configure(fg_color=BG_SUB)
    window.grab_set()
    window.focus_set()
    window.lift()

    ctk.CTkLabel(window,
                 text="Export Selected Results",
                 font=("Verdana", 18, "bold"),
                 text_color="white").pack(pady=15)

    outer_frame = ctk.CTkFrame(window, fg_color=BG_MAIN)
    outer_frame.pack(expand=True, fill="both", padx=20, pady=10)

    canvas = tk.Canvas(outer_frame, bg=BG_MAIN, highlightthickness=0)
    scrollbar = tk.ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas, fg_color=BG_MAIN)

    scrollable_frame.bind("<Configure>",
                          lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    export_data = []

    def make_selector(title, func_pd, func_np, param_info, allow_toggle):
        frame = ctk.CTkFrame(scrollable_frame, fg_color=BG_SUB, corner_radius=10)
        frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(frame,
                     text=title,
                     font=("Verdana", 14, "bold"),
                     text_color="white").pack(anchor="w", pady=(5, 2), padx=10)

        use_pd = tk.BooleanVar(value=True)
        if allow_toggle:
            toggle_frame = ctk.CTkFrame(frame, fg_color="transparent")
            toggle_frame.pack(anchor="w", padx=10)
            ctk.CTkRadioButton(toggle_frame,
                               text="Pandas",
                               variable=use_pd,
                               value=True).pack(side="left", padx=5)
            ctk.CTkRadioButton(toggle_frame,
                               text="Python pur",
                               variable=use_pd,
                               value=False).pack(side="left", padx=5)

        param_entries = []
        for param in param_info:
            entry_frame = ctk.CTkFrame(frame, fg_color="transparent")
            entry_frame.pack(anchor="w", pady=4, padx=10)
            ctk.CTkLabel(entry_frame, text=param["label"], font=("Verdana", 11),
                         text_color="white").pack(side="left")
            entry = ctk.CTkEntry(entry_frame, width=140)
            entry.insert(0, str(param["default"]))
            entry.pack(side="left", padx=10)
            param_entries.append((entry, param["type"]))

        export_data.append((title, func_pd, func_np, use_pd,
                            param_entries, allow_toggle))

    for title, fpd, fnp, params, toggle in question_data:
        make_selector(title, fpd, fnp, params, toggle)

    def export():
        import os
        import matplotlib.pyplot as plt
        rows = []
        dir_path = tk.filedialog.askdirectory(title="Select folder to save results")
        if not dir_path:
            return

        for title, fpd, fnp, use_pd, entries, allow_toggle in export_data:
            try:
                args = []
                for entry, typ in entries:
                    val = entry.get().strip()
                    if typ == int:
                        val = int(val)
                    elif typ == bool:
                        val = val.lower() == "true"
                    args.append(val)
                func = fpd if allow_toggle and use_pd.get() else fnp

                if func.__name__ in ["most_constructor_championships_won",
                                     "nationalities"]:
                    graph_path = os.path.join(dir_path, f"{func.__name__}.png")
                    plt.clf()
                    func(save_path=graph_path)
                    rows.append((title, f"Graph saved to {graph_path}"))
                else:
                    result = func(*args)
                    rows.append((title, str(result)))
            except Exception as e:
                rows.append((title, f"Error: {str(e)}"))

        filename = os.path.join(dir_path, "results.txt")
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    for title, res in rows:
                        f.write(f"{title}\n{res}\n\n")
                tk.messagebox.showinfo("Export",
                                       f"Exported successfully to folder:{dir_path}")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error during export : {str(e)}")

    ctk.CTkButton(window,
                  text="Go",
                  command=export,
                  fg_color=BTN_COLOR,
                  hover_color=BTN_HOVER,
                  font=("Verdana", 13, "bold"),
                  corner_radius=10,
                  height=35,
                  width=140).pack(pady=20)


ctk.CTkButton(
    interface,
    text="Export",
    font=("Verdana", 13, "bold"),
    command=open_export_window,
    corner_radius=8,
    width=160,
    height=35,
    fg_color="#9b59b6",
    hover_color="#6c3483"
).pack(pady=(10, 20))


# Clustering
machine_learning = ctk.CTkFrame(interface, corner_radius=15, fg_color=BG_MAIN)
machine_learning.pack(padx=30, pady=20, anchor='nw', fill='x')

machine_learning.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(machine_learning,
             text="Classification non supervisée",
             font=("Verdana", 18, "bold")).grid(row=0,
                                                column=0,
                                                sticky="w",
                                                padx=20,
                                                pady=(10, 5))
ctk.CTkLabel(machine_learning,
             text=("Can we identify distinct groups of "
                   "drivers based on their driving styles?"),
             font=("Verdana", 15, "italic")).grid(row=1,
                                                  column=0,
                                                  sticky="w",
                                                  padx=20,
                                                  pady=(0, 10))


def open_kmeans_window():
    """
    Executes KMeans clustering on driver data and displays:
    - The elbow method graph
    - The PCA projection of clusters
    - The contributions of features to the principal components
    - A preview of the clusters

    Exports results to a folder chosen by the user.

    """
    window = ctk.CTkToplevel(interface)
    window.title("Résultats du clustering KMeans")

    canvas = tk.Canvas(window, bg=BG_SUB, highlightthickness=0)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=BG_SUB)

    scrollable_frame.bind("<Configure>",
                          lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    window.geometry("1000x800")
    window.configure(fg_color=BG_SUB)

    try:
        folder = tk.filedialog.askdirectory(title="Choisir un dossier d'export")
        if not folder:
            return

        cluster_driving_styles(save_outputs=True)

        shutil.move("elbow_method.png", f"{folder}/elbow_method.png")
        shutil.move("pca_visualization.png", f"{folder}/pca_visualization.png")
        shutil.move("pca_contributions.csv", f"{folder}/pca_contributions.csv")
        shutil.move("clusters.csv", f"{folder}/clusters.csv")

        pca_contrib = pd.read_csv(f"{folder}/pca_contributions.csv", index_col=0)
        cluster_sample = pd.read_csv(f"{folder}/clusters.csv")

        # Elbow method graph
        frame1 = ctk.CTkFrame(scrollable_frame)
        frame1.pack(pady=10)
        img1 = Image.open(f"{folder}/elbow_method.png")
        img1 = img1.resize((600, 400))
        photo1 = ImageTk.PhotoImage(img1)
        label1 = tk.Label(frame1, image=photo1)
        label1.image = photo1
        label1.pack()

        # PCA
        frame2 = ctk.CTkFrame(scrollable_frame)
        frame2.pack(pady=10)
        img2 = Image.open(f"{folder}/pca_visualization.png")
        img2 = img2.resize((600, 400))
        photo2 = ImageTk.PhotoImage(img2)
        label2 = tk.Label(frame2, image=photo2)
        label2.image = photo2
        label2.pack()

        # PCA Contributions
        contrib_text = tk.Text(scrollable_frame, height=1 + len(pca_contrib),
                               font=("Courier", 10), bg="black", fg="white")
        contrib_text.insert("1.0", "PCA Contributions (PC1 / PC2):\n")
        for var, row in pca_contrib.iterrows():
            line = f"{var:<30} : {row['PC1']:.4f} / {row['PC2']:.4f}\n"
            contrib_text.insert("end", line)
        contrib_text.config(state="disabled")
        contrib_text.pack(padx=20, pady=20, fill="x")

        # Preview of clusters
        cluster_sample = cluster_sample.head(10)
        preview_text = tk.Text(scrollable_frame,
                               height=12,
                               font=("Courier New", 11),
                               bg="black", fg="white")
        preview_text.insert("1.0",
                            f"{'Cluster 0':<30}{'Cluster 1':<30}{'Cluster 2':<30}\n")
        preview_text.insert("end", f"{'-'*30}{'-'*30}{'-'*30}\n")
        for row in cluster_sample.itertuples(index=False):
            line = "".join(f"{str(col) if pd.notna(col) else '':<30}" for col in row)
            preview_text.insert("end", line + "\n")
        preview_text.config(state="disabled")
        preview_text.pack(padx=20, pady=20, fill="x")

        tk.messagebox.showinfo("Success",
                               f"Clustering finished. Results exported to : {folder}")

    except Exception as e:
        tk.messagebox.showerror("Error",
                                f"Error during clustering execution : {str(e)}")

    window.grab_set()
    window.focus_set()
    window.wait_window()


ctk.CTkButton(machine_learning,
              text="Export & View Clustering",
              font=("Verdana", 13, "bold"),
              command=open_kmeans_window,
              corner_radius=8,
              width=160,
              height=35,
              fg_color="#e67e22",
              hover_color="#d35400").grid(row=0, column=1, rowspan=2,
                                          padx=(10, 30), pady=10,
                                          sticky="e")

interface.mainloop()
