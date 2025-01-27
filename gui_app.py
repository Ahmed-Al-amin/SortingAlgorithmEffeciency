import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List
import pandas as pd
import os

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sorting_algorithms import algorithm_functions
import generator
import time
import threading
import csv


array_input = None
results_tree = None
results = []
algo_vars = {}
size_var = None
scenario_var = None
graph_frame = None


def setup_ui(root):
    global array_input, results_tree, algo_vars, size_var, scenario_var, graph_frame
#-------------------------------------array input frame ---------------------------------

    array_frame = ttk.LabelFrame(root, text="Array Input")
    array_frame.pack(fill="x", padx=10, pady=5)

    array_input = tk.StringVar()
    array_label = ttk.Label(array_frame, text="Enter array elements (comma-separated):")
    array_label.pack(side="left", padx=5, pady=5)

    array_entry = ttk.Entry(array_frame, textvariable=array_input, width=50)
    array_entry.pack(side="left", padx=5, pady=5)

#----------------------------------------generate array frame -------------------------------------------

    ttk.Separator(root, orient='horizontal').pack(fill='x', padx=10, pady=10)

    generate_frame = ttk.LabelFrame(root, text="Generate Array")
    generate_frame.pack(fill="x", padx=10, pady=5)

    size_label = ttk.Label(generate_frame, text="Input Size:")
    size_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    size_var = tk.IntVar(value=10)
    size_spinbox = ttk.Spinbox(generate_frame, from_=1, to=10000, textvariable=size_var, width=10)
    size_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    scenario_label = ttk.Label(generate_frame, text="Scenario:")
    scenario_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

    scenario_var = tk.StringVar(value="random")
    scenarios = [("Random", "random"), ("Sorted", "sorted"), ("Reversed", "reversed")]
    for idx, (text, value) in enumerate(scenarios):
        rb = ttk.Radiobutton(generate_frame, text=text, variable=scenario_var, value=value)
        rb.grid(row=1, column=1 + idx, padx=5, pady=5, sticky='w')

    generate_button = ttk.Button(generate_frame, text="Generate Array", command=generate_array)
    generate_button.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

#--------------------------------------algortihm frame---------------------------------------------------

    ttk.Separator(root, orient='horizontal').pack(fill='x', padx=10, pady=10)

    algo_frame = ttk.LabelFrame(root, text="Select Algorithms")
    algo_frame.pack(fill="x", padx=10, pady=5)

    algorithms = list(algorithm_functions.keys())
    for idx, algo in enumerate(algorithms):
        var = tk.BooleanVar()
        chk = ttk.Checkbutton(algo_frame, text=algo, variable=var)
        chk.grid(row=0, column=idx, padx=5, pady=5, sticky='w')
        algo_vars[algo] = var


    execute_button = ttk.Button(root, text="Execute Tests", command=execute_tests)
    execute_button.pack(pady=10)

#-----------------------------------------result frame -------------------------------------------------

    results_frame = ttk.LabelFrame(root, text="Results")
    results_frame.pack(fill="both", expand=True, padx=10, pady=5)

    results_tree = ttk.Treeview(results_frame, columns=("Algorithm", "Steps", "Execution Time (ms)"), show='headings')
    results_tree.heading("Algorithm", text="Algorithm")
    results_tree.heading("Steps", text="Steps")
    results_tree.heading("Execution Time (ms)", text="Execution Time (ms)")
    results_tree.pack(fill="both", expand=True, padx=5, pady=5)

    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results_tree.yview)
    results_tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

#-----------------------------------------buttons frame--------------------------------------------

    buttons_frame = ttk.Frame(root)
    buttons_frame.pack(pady=10)

    save_button = ttk.Button(buttons_frame, text="Save Test Cases as CSV", command=save_user_test_cases)
    save_button.grid(row=0, column=0, padx=10, pady=5)

    save_graph_button = ttk.Button(buttons_frame, text="Save Graph as PNG", command=save_graph_as_png)
    save_graph_button.grid(row=0, column=1, padx=10, pady=5)

    compare_graph_button = ttk.Button(buttons_frame, text="Print Comparison Graphs", command=print_comparison_graphs)
    compare_graph_button.grid(row=0, column=2, padx=10, pady=5)

    efficiency_button = ttk.Button(buttons_frame, text="Algorithm Efficiency", command=show_efficiency_window)
    efficiency_button.grid(row=1, column=0, padx=10, pady=5)

    comparison_button = ttk.Button(buttons_frame, text="Steps_notation_comparison", command=show_comparison_window)
    comparison_button.grid(row=1, column=1, padx=10, pady=5)

    notation_button = ttk.Button(buttons_frame, text="Asymptotic Notation", command=show_asymptotic_notation_window)
    notation_button.grid(row=1, column=2, padx=10, pady=5)

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save Results to CSV", command=save_results)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)


#-----------------------------------------Graphs output------------------------------------------------


def show_asymptotic_notation_window():

    algorithms = {
        "Bubble Sort": {
            "description": "Bubble Sort is a simple comparison-based sorting algorithm that repeatedly steps through the list, compares adjacent items, and swaps them if they are in the wrong order.",
            "best_case": "O(n) (when the array is already sorted)",
            "average_case": "O(n²)",
            "worst_case": "O(n²)",
            "space_complexity": "O(1) (in-place)",
            "key_points": [
                "Inefficient on large datasets.",
                "Useful for small data or as an educational tool."
            ]
        },
        "Insertion Sort": {
            "description": "Insertion Sort builds the sorted array one item at a time by repeatedly taking the next element from the input and inserting it into the correct position.",
            "best_case": "O(n) (when the array is already sorted)",
            "average_case": "O(n²)",
            "worst_case": "O(n²)",
            "space_complexity": "O(1) (in-place)",
            "key_points": [
                "Efficient for small datasets or nearly sorted arrays.",
                "Works well in online sorting applications."
            ]
        },
        "Merge Sort": {
            "description": "Merge Sort is a divide-and-conquer algorithm that divides the input array into halves, sorts each half, and then merges the sorted halves back together.",
            "best_case": "O(n log n)",
            "average_case": "O(n log n)",
            "worst_case": "O(n log n)",
            "space_complexity": "O(n) (auxiliary space for merging)",
            "key_points": [
                "Stable sorting algorithm.",
                "Preferred for large datasets and linked lists."
            ]
        },
        "Quick Sort": {
            "description": "Quick Sort is a divide-and-conquer algorithm that selects a pivot and partitions the array into two halves: one with elements smaller than the pivot and one with elements larger.",
            "best_case": "O(n log n)",
            "average_case": "O(n log n)",
            "worst_case": "O(n²) (when the pivot is poorly chosen)",
            "space_complexity": "O(log n) (for recursion stack)",
            "key_points": [
                "Efficient for large datasets.",
                "Can be optimized with a good pivot selection strategy."
            ]
        },
        "Heap Sort": {
            "description": "Heap Sort builds a max heap from the input data and repeatedly extracts the largest element from the heap to build the sorted array.",
            "best_case": "O(n log n)",
            "average_case": "O(n log n)",
            "worst_case": "O(n log n)",
            "space_complexity": "O(1) (in-place)",
            "key_points": [
                "Not stable but works in-place.",
                "Suitable for applications requiring constant space usage."
            ]
        },
        "Selection Sort": {
            "description": "Selection Sort repeatedly finds the minimum element from the unsorted part of the array and moves it to the beginning.",
            "best_case": "O(n²)",
            "average_case": "O(n²)",
            "worst_case": "O(n²)",
            "space_complexity": "O(1) (in-place)",
            "key_points": [
                "Inefficient for large datasets.",
                "Simple to implement and requires minimal swaps."
            ]
        },
        "Radix Sort": {
            "description": "Radix Sort sorts numbers by processing individual digits. It works by sorting based on the least significant digit, then the next least significant, and so on.",
            "best_case": "O(n * d)",
            "average_case": "O(n * d)",
            "worst_case": "O(n * d)",
            "space_complexity": "O(n + k) (where k is the range of digits)",
            "key_points": [
                "Efficient for sorting numbers or strings.",
                "Not comparison-based, depends on digit count."
            ]
        },
        "Counting Sort": {
            "description": "Counting Sort is a non-comparison sorting algorithm that counts the occurrences of each element and uses this count to place elements in the correct position.",
            "best_case": "O(n + k)",
            "average_case": "O(n + k)",
            "worst_case": "O(n + k)",
            "space_complexity": "O(n + k)",
            "key_points": [
                "Fast for small ranges of integers.",
                "Not suitable for sorting negative numbers or floating-point values."
            ]
        }
    }

    output_dir = "asymptotic_notation_graphs"

    notation_window = tk.Toplevel()
    notation_window.title("Asymptotic Notation")
    notation_window.geometry("800x600")

    algorithm_list_frame = ttk.Frame(notation_window)
    algorithm_list_frame.pack(side="left", fill="y", padx=10, pady=10)

    info_frame = ttk.Frame(notation_window)
    info_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    info_label = tk.Label(info_frame, text="", justify="left", anchor="w", wraplength=400)
    info_label.pack(fill="both", expand=True, padx=10, pady=10)

    def display_asymptotic_graph(algorithm_name):

        details = algorithms.get(algorithm_name, {})
        graph_path = os.path.join(output_dir, f"{algorithm_name.replace(' ', '_').lower()}_complexity.png")


        info_text = (
            f"Algorithm: {algorithm_name}\n\n"
            f"Description:\n{details.get('description', 'N/A')}\n\n"
            f"Best Case: {details.get('best_case', 'N/A')}\n"
            f"Average Case: {details.get('average_case', 'N/A')}\n"
            f"Worst Case: {details.get('worst_case', 'N/A')}\n"
            f"Space Complexity: {details.get('space_complexity', 'N/A')}\n\n"
            f"Key Points:\n- " + "\n- ".join(details.get("key_points", []))
        )
        info_label.config(text=info_text)

        if os.path.exists(graph_path):
            graph_window = tk.Toplevel()
            graph_window.title(f"{algorithm_name} Asymptotic Notation Graph")
            graph_window.geometry("800x600")

            figure = Figure(figsize=(8, 6), dpi=100)
            ax = figure.add_subplot(111)
            img = plt.imread(graph_path)
            ax.imshow(img)
            ax.axis('off')

            canvas = FigureCanvasTkAgg(figure, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            messagebox.showerror("Graph Not Found", f"No graph found for {algorithm_name}. Please generate it first.")

    for algo in algorithms.keys():
        algo_button = ttk.Button(algorithm_list_frame, text=algo, command=lambda a=algo: display_asymptotic_graph(a))
        algo_button.pack(fill="x", pady=5)

    notation_window.mainloop()


def show_comparison_window():

    algorithms = list(algorithm_functions.keys())
    output_dir = "sorting_comparison"

    comparison_window = tk.Toplevel()
    comparison_window.title("Algorithm Steps Comparison")
    comparison_window.geometry("400x400")

    def show_comparison_graph(algorithm_name):

        graph_path = os.path.join(output_dir, f"{algorithm_name.replace(' ', '_').lower()}_comparison.png")
        if not os.path.exists(graph_path):
            messagebox.showerror("Graph Not Found", f"No graph found for {algorithm_name}. Please generate it first.")
            return


        graph_window = tk.Toplevel()
        graph_window.title(f"{algorithm_name} Comparison Graph")
        graph_window.geometry("800x600")

        figure = Figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111)
        img = plt.imread(graph_path)
        ax.imshow(img)
        ax.axis('off')

        canvas = FigureCanvasTkAgg(figure, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


    for algo in algorithms:
        algo_button = ttk.Button(comparison_window, text=algo, command=lambda a=algo: show_comparison_graph(a))
        algo_button.pack(pady=5, fill="x")

    comparison_window.mainloop()


def show_efficiency_window():

    algorithms = list(algorithm_functions.keys())
    output_dir = "case_comparison_graphs"


    efficiency_window = tk.Toplevel()
    efficiency_window.title("Algorithm Efficiency")
    efficiency_window.geometry("400x400")

    def show_algorithm_graph(algorithm_name):

        graph_path = os.path.join(output_dir, f"{algorithm_name.replace(' ', '_').lower()}_case_comparison.png")
        if not os.path.exists(graph_path):
            messagebox.showerror("Graph Not Found", f"No graph found for {algorithm_name}. Please generate it first.")
            return

        graph_window = tk.Toplevel()
        graph_window.title(f"{algorithm_name} Case Comparison Graph")
        graph_window.geometry("800x600")

        figure = Figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111)
        img = plt.imread(graph_path)
        ax.imshow(img)
        ax.axis('off')

        canvas = FigureCanvasTkAgg(figure, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    for algo in algorithms:
        algo_button = ttk.Button(efficiency_window, text=algo, command=lambda a=algo: show_algorithm_graph(a))
        algo_button.pack(pady=5, fill="x")
    efficiency_window.mainloop()

#---------------------------------------------------------------------------------------------------------


def print_comparison_graphs():
    global results

    if not results:
        messagebox.showwarning("No Results", "Please execute tests before printing comparison graphs.")
        return

    algorithms = [result["Algorithm"] for result in results]
    steps = [result["Steps"] for result in results]
    execution_times = [result["Execution Time (ms)"] for result in results]

    graph_window = tk.Toplevel()
    graph_window.title("Sorting Comparison Graphs")
    graph_window.geometry("1000x600")

    figure = Figure(figsize=(12, 6), dpi=100)
    ax1 = figure.add_subplot(111)

    width = 0.4
    x_indexes = range(len(algorithms))
    ax1.bar(x_indexes, steps, width=width, color='royalblue', label="Steps")

    ax1.set_xlabel("Algorithms", fontsize=12)
    ax1.set_ylabel("Steps", color="blue", fontsize=12)
    ax1.set_xticks(x_indexes)
    ax1.set_xticklabels(algorithms, rotation=45, ha="right", fontsize=10)

    ax2 = ax1.twinx()
    ax2.bar([x + width for x in x_indexes], execution_times, width=width, color='tomato', label="Execution Time (ms)")
    ax2.set_ylabel("Execution Time (ms)", color="red", fontsize=12)

    ax1.set_title("Steps and Execution Time Comparison", fontsize=14)
    figure.legend(loc="upper right")

    canvas = FigureCanvasTkAgg(figure, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)



def save_graph_as_png():
    global results

    if not results:
        messagebox.showwarning("No Graph", "Please generate and display a graph before saving.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Save Graph as PNG"
    )
    if not file_path:
        return

    try:
        algorithms = [result["Algorithm"] for result in results]
        steps = [result["Steps"] for result in results]
        execution_times = [result["Execution Time (ms)"] for result in results]

        figure = Figure(figsize=(12, 6), dpi=100)
        ax1 = figure.add_subplot(111)

        width = 0.4
        x_indexes = range(len(algorithms))
        ax1.bar(x_indexes, steps, width=width, color='royalblue', label="Steps")

        ax1.set_xlabel("Algorithms", fontsize=12)
        ax1.set_ylabel("Steps", color="blue", fontsize=12)
        ax1.set_xticks(x_indexes)
        ax1.set_xticklabels(algorithms, rotation=45, ha="right", fontsize=10)

        ax2 = ax1.twinx()
        ax2.bar([x + width for x in x_indexes], execution_times, width=width, color='tomato', label="Execution Time (ms)")
        ax2.set_ylabel("Execution Time (ms)", color="red", fontsize=12)

        ax1.set_title("Steps and Execution Time Comparison", fontsize=14)
        figure.legend(loc="upper right")

        figure.savefig(file_path)
        messagebox.showinfo("Saved", f"Graph has been saved as {file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the graph: {e}")




def execute_tests():
    global array_input, results_tree, algo_vars, results

    array_str = array_input.get()
    if not array_str:
        messagebox.showerror("No Input", "Please enter or generate an array to test.")
        return

    try:
        arr = [int(x.strip()) for x in array_str.split(",")]
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid array of integers, separated by commas.")
        return

    selected_algos = [algo for algo, var in algo_vars.items() if var.get()]
    if not selected_algos:
        messagebox.showwarning("No Algorithms Selected", "Please select at least one algorithm to execute.")
        return

    for item in results_tree.get_children():
        results_tree.delete(item)

    results = []
    for algo in selected_algos:
        start_time = time.time()
        steps = algorithm_functions[algo](arr.copy())
        end_time = time.time()

        execution_time = round((end_time - start_time) * 1000, 3)
        results.append({"Algorithm": algo, "Steps": steps, "Execution Time (ms)": execution_time})
        results_tree.insert("", "end", values=(algo, steps, execution_time))

    messagebox.showinfo("Tests Completed", "Selected algorithms have been executed. Results are displayed below.")


def save_user_test_cases():
    global results


    if not results:
        messagebox.showwarning("No Results", "Please run the tests before saving the results.")
        return


    folder_name = "user_test_cases"
    os.makedirs(folder_name, exist_ok=True)


    file_path = filedialog.asksaveasfilename(
        initialdir=folder_name,
        title="Save Test Cases",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="user_test_cases.csv"
    )

    if not file_path:
        messagebox.showinfo("Cancelled", "File saving was cancelled.")
        return

    try:

        file_exists = os.path.isfile(file_path)


        with open(file_path, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)

            if not file_exists:
                writer.writerow(["Algorithm", "Scenario", "Input Size", "Steps", "Execution Time (ms)"])


            for result in results:
                writer.writerow([
                    result["Algorithm"],
                    scenario_var.get(),
                    len(array_input.get().split(",")),
                    result["Steps"],
                    result["Execution Time (ms)"]
                ])

        messagebox.showinfo("Success", f"Test cases appended successfully to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {e}")


def save_results():
    global results

    if not results:
        messagebox.showwarning("No Results", "There are no results to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save Results")
    if not file_path:
        return

    df = pd.DataFrame(results)
    df.to_csv(file_path, index=False)
    messagebox.showinfo("Saved", f"Results have been saved to {file_path}")


def generate_array():
    global array_input, size_var, scenario_var

    size = size_var.get()
    scenario = scenario_var.get()

    if size <= 0:
        messagebox.showerror("Invalid Size", "Input size must be a positive integer.")
        return

    try:
        if scenario == "random":
            arr = generator.generate_random_array(size)
        elif scenario == "sorted":
            arr = generator.generate_sorted_array(size)
        elif scenario == "reversed":
            arr = generator.generate_reversed_array(size)
        else:
            messagebox.showerror("Invalid Scenario", "Please select a valid scenario.")
            return

        array_str = ", ".join(map(str, arr))
        array_input.set(array_str)
        messagebox.showinfo("Array Generated", f"Array generated with size {size} in '{scenario}' scenario.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def run_generator():
    try:
        generator.main()
    except Exception as e:
        print(f"Error while running generator: {e}")


def main():
    generator_thread = threading.Thread(target=run_generator)
    generator_thread.daemon = True
    generator_thread.start()

    root = tk.Tk()
    root.title("Sorting Algorithms Tester")
    root.geometry("800x800")
    setup_ui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
