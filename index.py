import tkinter as tk
from tkinter import messagebox
import time
import threading

class AlgorithmVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Visualizer")
        self.root.geometry("800x600")
        
        # Variables to control execution
        self.stop_flag = False
        self.current_algorithm = None
        
        # Create intro screen
        self.create_intro_screen()

    def create_intro_screen(self):
        """Create the introductory interface with algorithm selection."""
        self.clear_screen()

        # Title
        title = tk.Label(self.root, text="Algorithm Visualizer", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Description
        desc = tk.Label(self.root, text="Select an algorithm to visualize:", font=("Arial", 12))
        desc.pack(pady=10)

        # Algorithm Buttons
        algorithms = [
            ("Odd Numbers", self.visualize_odd_numbers),
            ("Prime and Composite", self.visualize_prime_and_composite),
            ("Insertion Sort", self.visualize_insertion_sort),
            ("Bubble Sort", self.visualize_bubble_sort),
            ("Selection Sort", self.visualize_selection_sort),
            ("Shell Sort", self.visualize_shell_sort),
            ("Quick Sort", self.visualize_quick_sort),
        ]

        for algo, command in algorithms:
            btn = tk.Button(self.root, text=algo, width=25, command=command)
            btn.pack(pady=5)

    def clear_screen(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def stop_execution(self):
        """Stop the currently running algorithm."""
        self.stop_flag = True

    def setup_algorithm_screen(self, title_text, desc_text):
        """Set up the screen for a specific algorithm."""
        self.clear_screen()
        self.stop_flag = False

        # Title
        title = tk.Label(self.root, text=title_text, font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Description
        desc = tk.Label(self.root, text=desc_text, font=("Arial", 12))
        desc.pack(pady=10)

        # Input Section
        input_label = tk.Label(self.root, text="Enter numbers separated by commas:", font=("Arial", 10))
        input_label.pack(pady=5)

        self.input_entry = tk.Entry(self.root, width=50)
        self.input_entry.insert(0, "64, 34, 25, 12, 22, 11, 90")  # Default values
        self.input_entry.pack(pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        start_btn = tk.Button(btn_frame, text="Start", command=self.start_execution)
        start_btn.pack(side=tk.LEFT, padx=5)

        stop_btn = tk.Button(btn_frame, text="Stop", command=self.stop_execution)
        stop_btn.pack(side=tk.LEFT, padx=5)

        back_btn = tk.Button(btn_frame, text="Back", command=self.create_intro_screen)
        back_btn.pack(side=tk.LEFT, padx=5)

        # Canvas for Animation
        self.canvas = tk.Canvas(self.root, width=700, height=300, bg="white")
        self.canvas.pack(pady=10)

    def start_execution(self):
        """Start the selected algorithm in a separate thread."""
        if not self.current_algorithm:
            return
            
        self.stop_flag = False
        input_text = self.input_entry.get()

        try:
            numbers = [int(x.strip()) for x in input_text.split(',')]
            threading.Thread(target=self.current_algorithm, args=(numbers,), daemon=True).start()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers separated by commas.")

    def visualize_numbers(self, numbers, highlight_indices=None, color_map=None):
        """Helper to visualize numbers on the canvas with optional highlighting."""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Calculate bar width and spacing
        n = len(numbers)
        bar_width = min(50, (width - 100) // n)
        spacing = 5
        
        # Find max value for scaling
        max_val = max(abs(min(numbers)), abs(max(numbers)))
        scale_factor = (height - 100) / max_val if max_val > 0 else 1

        # Draw bars
        x = 50
        for i, num in enumerate(numbers):
            # Determine bar color
            if color_map and i in color_map:
                color = color_map[i]
            elif highlight_indices and i in highlight_indices:
                color = "red"
            else:
                color = "blue"

            # Calculate bar height
            bar_height = abs(num) * scale_factor
            y_bottom = height - 50
            y_top = y_bottom - bar_height

            # Draw bar
            self.canvas.create_rectangle(x, y_bottom, x + bar_width, y_top, fill=color)
            self.canvas.create_text(x + bar_width/2, y_bottom + 15, text=str(num))
            
            x += bar_width + spacing

        self.root.update()

    # Algorithm Implementations
    def visualize_insertion_sort(self):
        """Visualize the Insertion Sort algorithm."""
        self.current_algorithm = self.run_insertion_sort
        self.setup_algorithm_screen(
            "Insertion Sort",
            "Sorts the numbers using the Insertion Sort algorithm."
        )

    def run_insertion_sort(self, numbers):
        """Execute the Insertion Sort algorithm."""
        numbers = numbers.copy()
        for i in range(1, len(numbers)):
            if self.stop_flag:
                break
            key = numbers[i]
            j = i - 1
            while j >= 0 and numbers[j] > key:
                if self.stop_flag:
                    break
                numbers[j + 1] = numbers[j]
                j -= 1
                self.visualize_numbers(numbers, highlight_indices=[j+1])
                time.sleep(0.5)
            numbers[j + 1] = key
            self.visualize_numbers(numbers)
            time.sleep(0.5)

    def visualize_bubble_sort(self):
        """Visualize the Bubble Sort algorithm."""
        self.current_algorithm = self.run_bubble_sort
        self.setup_algorithm_screen(
            "Bubble Sort",
            "Sorts the numbers using the Bubble Sort algorithm."
        )

    def run_bubble_sort(self, numbers):
        """Execute the Bubble Sort algorithm."""
        numbers = numbers.copy()
        n = len(numbers)
        for i in range(n):
            if self.stop_flag:
                break
            for j in range(0, n-i-1):
                if self.stop_flag:
                    break
                if numbers[j] > numbers[j+1]:
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
                self.visualize_numbers(numbers, highlight_indices=[j, j+1])
                time.sleep(0.5)

    def visualize_selection_sort(self):
        """Visualize the Selection Sort algorithm."""
        self.current_algorithm = self.run_selection_sort
        self.setup_algorithm_screen(
            "Selection Sort",
            "Sorts the numbers using the Selection Sort algorithm."
        )

    def run_selection_sort(self, numbers):
        """Execute the Selection Sort algorithm."""
        numbers = numbers.copy()
        for i in range(len(numbers)):
            if self.stop_flag:
                break
            min_idx = i
            for j in range(i+1, len(numbers)):
                if self.stop_flag:
                    break
                if numbers[j] < numbers[min_idx]:
                    min_idx = j
                self.visualize_numbers(numbers, highlight_indices=[min_idx, j])
                time.sleep(0.5)
            numbers[i], numbers[min_idx] = numbers[min_idx], numbers[i]

    def visualize_shell_sort(self):
        """Visualize the Shell Sort algorithm."""
        self.current_algorithm = self.run_shell_sort
        self.setup_algorithm_screen(
            "Shell Sort",
            "Sorts the numbers using the Shell Sort algorithm."
        )

    def run_shell_sort(self, numbers):
        """Execute the Shell Sort algorithm."""
        numbers = numbers.copy()
        n = len(numbers)
        gap = n // 2

        while gap > 0:
            if self.stop_flag:
                break
            for i in range(gap, n):
                if self.stop_flag:
                    break
                temp = numbers[i]
                j = i
                while j >= gap and numbers[j-gap] > temp:
                    if self.stop_flag:
                        break
                    numbers[j] = numbers[j-gap]
                    j -= gap
                    self.visualize_numbers(numbers, highlight_indices=[j, j+gap])
                    time.sleep(0.5)
                numbers[j] = temp
            gap //= 2

    def visualize_quick_sort(self):
        """Visualize the Quick Sort algorithm."""
        self.current_algorithm = self.run_quick_sort
        self.setup_algorithm_screen(
            "Quick Sort",
            "Sorts the numbers using the Quick Sort algorithm."
        )

    def run_quick_sort(self, numbers):
        """Execute the Quick Sort algorithm."""
        def partition(low, high):
            i = low - 1
            pivot = numbers[high]
            
            for j in range(low, high):
                if self.stop_flag:
                    return i + 1
                if numbers[j] <= pivot:
                    i += 1
                    numbers[i], numbers[j] = numbers[j], numbers[i]
                    self.visualize_numbers(numbers, highlight_indices=[i, j, high])
                    time.sleep(0.5)
            
            numbers[i + 1], numbers[high] = numbers[high], numbers[i + 1]
            return i + 1

        def quick_sort_recursive(low, high):
            if low < high and not self.stop_flag:
                pi = partition(low, high)
                quick_sort_recursive(low, pi - 1)
                quick_sort_recursive(pi + 1, high)

        numbers = numbers.copy()
        quick_sort_recursive(0, len(numbers) - 1)

    def run_odd_numbers(self, numbers):
        """Execute the Odd Numbers algorithm."""
        numbers = numbers.copy()
        for i, num in enumerate(numbers):
            if self.stop_flag:
                break
            color_map = {i: "green" if num % 2 != 0 else "red"}
            self.visualize_numbers(numbers, color_map=color_map)
            time.sleep(0.5)

    def run_prime_and_composite(self, numbers):
        """Execute the Prime and Composite algorithm."""
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True

        numbers = numbers.copy()
        for i, num in enumerate(numbers):
            if self.stop_flag:
                break
            color_map = {i: "blue" if is_prime(num) else "orange"}
            self.visualize_numbers(numbers, color_map=color_map)
            time.sleep(0.5)

    def visualize_odd_numbers(self):
        """Visualize the Odd Numbers algorithm."""
        self.current_algorithm = self.run_odd_numbers
        self.setup_algorithm_screen(
            "Odd Numbers",
            "This algorithm identifies odd numbers in the list."
        )

    def visualize_prime_and_composite(self):
        """Visualize the Prime and Composite algorithm."""
        self.current_algorithm = self.run_prime_and_composite
        self.setup_algorithm_screen(
            "Prime and Composite",
            "This algorithm identifies prime and composite numbers in the list."
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmVisualizer(root)
    root.mainloop()
