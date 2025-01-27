#plot_graphs.py

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os
from constant import *
from scipy.interpolate import make_interp_spline


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from constant import INPUT_SIZES

#------------------------------------line graph-----------------------------------------------

def plot_combined_steps_and_execution_line_graph(csv_file: str):
    df = pd.read_csv(csv_file)

    os.makedirs("combined_line_graphs", exist_ok=True)

    scenarios = ['sorted', 'random', 'reversed']

    for scenario in scenarios:
        for size in INPUT_SIZES:

            subset = df[(df["Scenario"] == scenario) & (df["Input Size"] == size)]

            if subset.empty:
                print(f"No data for scenario '{scenario}' with size {size}. Skipping...")
                continue

            plt.figure(figsize=(10, 6))

            algorithms = subset["Algorithm"]
            steps = subset["Steps"]
            execution_times = subset["Execution Time (ms)"]

            plt.plot(algorithms, steps, label="Steps", color="blue", marker="o", linestyle="-")

            ax1 = plt.gca()
            ax2 = ax1.twinx()
            ax2.plot(algorithms, execution_times, label="Execution Time (ms)", color="red", marker="o", linestyle="--")

            ax1.set_xlabel("Algorithms")
            ax1.set_ylabel("Steps", color="blue", labelpad=20)
            ax2.set_ylabel("Execution Time (ms)", color="red", labelpad=20)
            plt.title(f"Scenario: {scenario.capitalize()} - Input Size: {size}")
            plt.xticks(rotation=45)


            ax1.legend(loc='upper center', bbox_to_anchor=(0.05, 1.1), frameon=True)
            ax2.legend(loc='upper center', bbox_to_anchor=(.9, 1.1), frameon=True)

            plt.tight_layout()

            filename = f"combined_line_graphs/combined_{scenario}_{size}.png"
            plt.savefig(filename, bbox_inches='tight')
            plt.close()
    print("Combined line plots have been generated and saved in 'combined_graphs' directory.")


#----------------------------------------------------------------------------------------------------

def plot_combined_steps_and_execution(csv_file: str):
    df = pd.read_csv(csv_file)

    os.makedirs("combined_graphs", exist_ok=True)

    scenarios = ['sorted', 'random', 'reversed']

    INPUT_SIZES = df["Input Size"].unique()

    for scenario in scenarios:
        for size in INPUT_SIZES:

            subset = df[(df["Scenario"] == scenario) & (df["Input Size"] == size)]

            if subset.empty:
                print(f"No data for scenario '{scenario}' with size {size}. Skipping...")
                continue

            plt.figure(figsize=(10, 6))

            algorithms = subset["Algorithm"]
            steps = subset["Steps"]
            execution_times = subset["Execution Time (ms)"]

            x_indexes = np.arange(len(algorithms))
            width = 0.4

            plt.bar(x_indexes - width / 2, steps, width=width, color='blue', label="Steps")

            ax1 = plt.gca()
            ax2 = ax1.twinx()
            ax2.bar(x_indexes + width / 2, execution_times, width=width, color='red', label="Execution Time (ms)")

            ax1.set_xlabel("Algorithms")
            ax1.set_ylabel("Steps", color="blue", labelpad=20)
            ax2.set_ylabel("Execution Time (ms)", color="red", labelpad=20)
            plt.title(f"Scenario: {scenario.capitalize()} - Input Size: {size}")
            plt.xticks(x_indexes, algorithms, rotation=45)

            ax1.legend(loc='upper center', bbox_to_anchor=(0.05, 1.1), frameon=True)
            ax2.legend(loc='upper center', bbox_to_anchor=(.9, 1.1), frameon=True)

            plt.tight_layout(rect=[0, 0, 1, 0.9])

            filename = f"combined_graphs/combined_{scenario}_{size}.png"
            plt.savefig(filename, bbox_inches='tight')
            plt.close()

    print("Combined plots have been generated and saved in 'combined_graphs' directory.")


def plot_sorting_comparison(csv_file: str):
    df = pd.read_csv(csv_file)
    os.makedirs("Steps_graph", exist_ok=True)
    sns.set(style="whitegrid")

    scenarios = ['sorted', 'random', 'reversed']

    for size in INPUT_SIZES:
        for scenario in scenarios:
            scenario_data = df[(df['Scenario'] == scenario) & (df['Input Size'] == size)]

            if scenario_data.empty:
                continue

            plt.figure(figsize=(10, 6))

            #sns.barplot(x='Algorithm', y='Steps', data=scenario_data)
            sns.barplot(
                x='Algorithm',
                y='Steps',
                hue='Algorithm',
                data=scenario_data,
                palette="viridis",
                legend=False
            )

            plt.title(f'{scenario.capitalize()} Scenario - Input Size: {size}')
            plt.xlabel('Sorting Algorithm')
            plt.ylabel('Number of Steps')
            plt.xticks(rotation=45)

            if scenario_data['Steps'].max() > 1000:
                plt.yscale('log')

            plt.tight_layout()

            filename = f'Steps_graph/Steps_{scenario}_{size}.png'
            plt.savefig(filename)
            plt.close()
    print("Steps plots have been generated and saved as PNG images.")


def plot_execution_time_graph(csv_file: str):
    df = pd.read_csv(csv_file)

    os.makedirs("execution_time_graph", exist_ok=True)
    scenarios = ['sorted', 'random', 'reversed']

    sns.set(style="whitegrid")

    for scenario in scenarios:
        for size in INPUT_SIZES:
            subset = df[(df["Scenario"] == scenario) & (df["Input Size"] == size)]

            if subset.empty:
                print(f"No data for scenario '{scenario}' with size {size}. Skipping...")
                continue

            plt.figure(figsize=(10, 6))
            sns.barplot(
                x='Algorithm',
                y='Execution Time (ms)',
                hue='Algorithm',
                data=subset,
                palette="viridis",
                legend=False
            )

            plt.title(f'Execution Time for {scenario.capitalize()} Scenario (Size {size})')
            plt.xlabel('Algorithm')
            plt.ylabel('Execution Time (ms)')
            plt.xticks(rotation=45)

            filename = f'execution_time_graph/execution_time_{scenario}_{size}.png'
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
    print("Execution time graphs have been saved in 'execution_time_graph' directory.")


def plot_asymptotic_notation():

    complexities = {
        "Bubble Sort": {
            'Sorted': lambda n: n,
            'Random': lambda n: n ** 2,
            'Reversed': lambda n: n ** 2
        },
        "Insertion Sort": {
            'Sorted': lambda n: n,
            'Random': lambda n: n ** 2,
            'Reversed': lambda n: n ** 2
        },
        "Merge Sort": {
            'Sorted': lambda n: n * np.log2(n),
            'Random': lambda n: n * np.log2(n),
            'Reversed': lambda n: n * np.log2(n)
        },
        "Quick Sort": {
            'Sorted': lambda n: n * np.log2(n),
            'Random': lambda n: n * np.log2(n),
            'Reversed': lambda n: n ** 2
        },
        "Heap Sort": {
            'Sorted': lambda n: n * np.log2(n),
            'Random': lambda n: n * np.log2(n),
            'Reversed': lambda n: n * np.log2(n)
        },
        "Selection Sort": {
            'Sorted': lambda n: n ** 2,
            'Random': lambda n: n ** 2,
            'Reversed': lambda n: n ** 2
        },
        "Radix Sort": {
            'Sorted': lambda n: n * np.log2(n),
            'Random': lambda n: n * np.log2(n),
            'Reversed': lambda n: n * np.log2(n)
        },
        "Counting Sort": {
            'Sorted': lambda n: n,
            'Random': lambda n: n + n,
            'Reversed': lambda n: n + n
        }
    }

    complexity_notation = {
        "Bubble Sort": "O(n²)",
        "Insertion Sort": "O(n²)",
        "Merge Sort": "O(n log n)",
        "Quick Sort": "O(n log n) / O(n²)",
        "Heap Sort": "O(n log n)",
        "Selection Sort": "O(n²)",
        "Radix Sort": "O(n * d)",
        "Counting Sort": "O(n + k)"
    }

    scenarios = ['Sorted', 'Random', 'Reversed']
    line_styles = ['-', '--', '-.']
    colors = ['blue', 'orange', 'green']

    os.makedirs("asymptotic_notation_graphs", exist_ok=True)

    for algorithm, scenario_complexities in complexities.items():
        plt.figure(figsize=(10, 6))

        for i, scenario in enumerate(scenarios):
            time_complexity = [scenario_complexities[scenario](n) for n in INPUT_SIZES]
            plt.plot(
                INPUT_SIZES,
                time_complexity,
                label=f"{scenario} ({complexity_notation[algorithm]})",
                linestyle=line_styles[i],
                color=colors[i]
            )

        plt.title(f"Asymptotic Notation for {algorithm}", fontsize=14)
        plt.xlabel("Input Size (n)", fontsize=12)
        plt.ylabel("Theoretical Steps", fontsize=12)
        plt.legend()
        plt.grid(True)

        filename = f"asymptotic_notation_graphs/{algorithm.replace(' ', '_').lower()}_complexity.png"
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

    print("Enhanced asymptotic notation graphs have been saved in 'asymptotic_notation_graphs' directory.")


def compare_algorithm_steps_and_onotation(csv_file: str):
    df = pd.read_csv(csv_file)

    output_dir = "sorting_comparison"
    os.makedirs(output_dir, exist_ok=True)

    algorithms = df["Algorithm"].unique()

    complexities = {
        "Bubble Sort": ("O(n^2)", lambda n: n ** 2),
        "Insertion Sort": ("O(n^2)", lambda n: n ** 2),
        "Merge Sort": ("O(n log n)", lambda n: n * np.log2(n)),
        "Quick Sort": ("O(n log n)", lambda n: n * np.log2(n)),
        "Heap Sort": ("O(n log n)", lambda n: n * np.log2(n)),
        "Selection Sort": ("O(n^2)", lambda n: n ** 2),
        "Radix Sort": ("O(n * d)", lambda n: n * np.log2(n)),
        "Counting Sort": ("O(n + k)", lambda n: n + n),
    }

    for algorithm in algorithms:
        plt.figure(figsize=(10, 6))

        algorithm_data = df[df["Algorithm"] == algorithm]


        grouped_data = (
            algorithm_data.groupby("Input Size", as_index=False)[["Input Size", "Steps"]]
            .mean()
        )
        input_sizes = grouped_data["Input Size"].values
        steps = grouped_data["Steps"].values

        smooth_input_sizes = np.linspace(min(input_sizes), max(input_sizes), 500)
        smooth_steps = make_interp_spline(input_sizes, steps)(smooth_input_sizes)

        notation, complexity_fn = complexities[algorithm]
        theoretical_complexity = complexity_fn(smooth_input_sizes)


        plt.plot(smooth_input_sizes, smooth_steps, label=f"{algorithm} Steps", color="blue")
        plt.plot(
            smooth_input_sizes,
            theoretical_complexity,
            label=f"{algorithm} {notation}",
            color="orange",
            linestyle="--",
        )

        plt.title(f"{algorithm} - Steps vs {notation}", fontsize=14)
        plt.xlabel("Input Size", fontsize=12)
        plt.ylabel("f(n)", fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True)

        file_path = os.path.join(output_dir, f"{algorithm.replace(' ', '_').lower()}_comparison.png")
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()

    print(f"Comparison graphs with asymptotic notation saved in '{output_dir}' directory.")


def plot_case_comparison_individual(csv_file: str, output_dir: str = "case_comparison_graphs"):
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(csv_file)

    grouped = df.groupby(['Algorithm', 'Scenario', 'Input Size'])['Steps'].mean().reset_index()

    algorithms = df['Algorithm'].unique()
    scenarios = ['sorted', 'random', 'reversed']

    for algo in algorithms:
        algo_data = grouped[grouped['Algorithm'] == algo]
        input_sizes = sorted(df['Input Size'].unique())

        best_case = []
        worst_case = []
        average_case = []

        for size in input_sizes:
            size_data = algo_data[algo_data['Input Size'] == size]
            best_case.append(size_data[size_data['Scenario'] == 'sorted']['Steps'].mean())
            worst_case.append(size_data[size_data['Scenario'] == 'reversed']['Steps'].mean())
            average_case.append(size_data[size_data['Scenario'] == 'random']['Steps'].mean())

        plt.figure(figsize=(8, 6))
        plt.plot(input_sizes, best_case, label='Best Case', linestyle='-', marker='o', color='green')
        plt.plot(input_sizes, worst_case, label='Worst Case', linestyle='--', marker='x', color='red')
        plt.plot(input_sizes, average_case, label='Average Case', linestyle='-.', marker='s', color='blue')

        plt.title(f"{algo} - Case Comparison", fontsize=14)
        plt.xlabel("Input Size", fontsize=12)
        plt.ylabel("Steps", fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        file_path = os.path.join(output_dir, f"{algo.replace(' ', '_').lower()}_case_comparison.png")
        plt.savefig(file_path)
        plt.close()

    print(f"Graphs saved in directory: {output_dir}")


def main():
    plot_execution_time_graph("sorting_efficiency_comparison.csv")
    plot_sorting_comparison("sorting_efficiency_comparison.csv")
    plot_combined_steps_and_execution("sorting_efficiency_comparison.csv")
    compare_algorithm_steps_and_onotation("sorting_efficiency_comparison.csv")
    plot_combined_steps_and_execution_line_graph("sorting_efficiency_comparison.csv")
    plot_case_comparison_individual("sorting_efficiency_comparison.csv")
    plot_asymptotic_notation()



if __name__ == "__main__":
    main()
