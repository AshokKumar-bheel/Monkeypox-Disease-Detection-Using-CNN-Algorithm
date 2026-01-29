# main_simple.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime
import csv
import random


class MonkeyPoxDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("MonkeyPox Detection System")
        self.root.geometry("1000x600")
        self.root.configure(bg='#f0f0f0')

        # Initialize variables
        self.image_path = None

        # Create Excel file if it doesn't exist
        self.csv_file = "predictions.csv"
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Image Path", "Prediction", "Confidence", "Monkeypox Probability"])

        self.create_sidebar()
        self.create_main_content()

    def create_sidebar(self):
        """Create the sidebar with navigation buttons"""
        sidebar = tk.Frame(self.root, bg='#2c3e50', width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Logo or title
        title_label = tk.Label(sidebar, text="MonkeyPox Detector", font=("Arial", 16, "bold"),
                               fg="white", bg="#2c3e50")
        title_label.pack(pady=20)

        # Buttons
        buttons = [
            ("Upload Image", self.upload_image),
            ("Dr. Recommendations", self.show_recommendations),
            ("Food Suggestions", self.show_food_suggestions),
            ("Medicine Info", self.show_medicine_info),
            ("View Results", self.view_results),
            ("Exit", self.exit_app)
        ]

        for text, command in buttons:
            btn = tk.Button(sidebar, text=text, font=("Arial", 12),
                            bg="#34495e", fg="white", relief=tk.FLAT,
                            command=command, width=15)
            btn.pack(pady=10)

    def create_main_content(self):
        """Create the main content area"""
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title = tk.Label(main_frame, text="MonkeyPox Detection using CNN",
                         font=("Arial", 20, "bold"), bg='#f0f0f0')
        title.pack(pady=10)

        # Image display
        self.img_label = tk.Label(main_frame, text="Upload an image for analysis",
                                  font=("Arial", 12), bg='#f0f0f0',
                                  relief=tk.SUNKEN, width=60, height=15)
        self.img_label.pack(pady=10)

        # Prediction result
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 14, "bold"),
                                     bg='#f0f0f0', fg='#2c3e50')
        self.result_label.pack(pady=10)

        # Confidence meter
        confidence_frame = tk.Frame(main_frame, bg='#f0f0f0')
        confidence_frame.pack(pady=10)

        tk.Label(confidence_frame, text="Confidence Level:",
                 font=("Arial", 12), bg='#f0f0f0').pack(side=tk.LEFT)

        self.confidence_bar = ttk.Progressbar(confidence_frame, orient=tk.HORIZONTAL,
                                              length=200, mode='determinate')
        self.confidence_bar.pack(side=tk.LEFT, padx=10)

        self.confidence_value = tk.Label(confidence_frame, text="0%",
                                         font=("Arial", 12), bg='#f0f0f0')
        self.confidence_value.pack(side=tk.LEFT)

        # Predict button
        self.predict_btn = tk.Button(main_frame, text="Predict", font=("Arial", 14),
                                     bg="#3498db", fg="white", relief=tk.RAISED,
                                     command=self.predict, state=tk.DISABLED)
        self.predict_btn.pack(pady=10)

    def upload_image(self):
        """Upload an image from file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            self.display_image_placeholder(file_path)
            self.predict_btn.config(state=tk.NORMAL)

    def display_image_placeholder(self, path):
        """Display a placeholder for the image"""
        self.img_label.configure(
            text=f"Image selected: {os.path.basename(path)}\n\n(Image preview would appear here if PIL was installed)",
            font=("Arial", 10)
        )

    def predict(self):
        """Simulate prediction (in a real app, this would use a trained model)"""
        if self.image_path:
            # Simulate prediction with random results for demonstration
            # In a real application, this would use your trained CNN model
            is_monkeypox = random.choice([True, False])
            confidence = random.uniform(80.0, 95.0) if is_monkeypox else random.uniform(5.0, 30.0)

            # Update UI
            if is_monkeypox:
                result_text = "Monkeypox Detected!"
                color = "#e74c3c"  # Red
            else:
                result_text = "No Monkeypox Detected"
                color = "#2ecc71"  # Green

            self.result_label.config(text=result_text, fg=color)
            self.confidence_bar['value'] = confidence
            self.confidence_value.config(text=f"{confidence:.2f}%")

            # Save to CSV
            self.save_to_csv(is_monkeypox, confidence)

            # Show message if confidence is high
            if confidence >= 80:
                messagebox.showinfo("High Confidence",
                                    f"Prediction made with {confidence:.2f}% confidence")

    def save_to_csv(self, is_monkeypox, confidence):
        """Save prediction results to CSV file"""
        try:
            with open(self.csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    self.image_path,
                    "Monkeypox" if is_monkeypox else "Normal",
                    f"{confidence:.2f}%",
                    f"{confidence:.2f}%"
                ])
            messagebox.showinfo("Success", "Results saved to CSV file")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save to CSV: {str(e)}")

    def view_results(self):
        """Display the results from CSV file"""
        results_window = tk.Toplevel(self.root)
        results_window.title("Prediction Results")
        results_window.geometry("800x400")

        # Create a text widget to display results
        text_widget = tk.Text(results_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Read and display CSV content
        try:
            with open(self.csv_file, 'r') as file:
                content = file.read()
                text_widget.insert(tk.END, content)
        except Exception as e:
            text_widget.insert(tk.END, f"Error reading results: {str(e)}")

        text_widget.config(state=tk.DISABLED)  # Make it read-only

    def show_recommendations(self):
        """Show doctor recommendations"""
        recommendations = """
        Doctor Recommendations for Monkeypox:

        1. Isolate immediately to prevent transmission
        2. Keep the rash dry and uncovered
        3. Avoid scratching the lesions
        4. Use topical antiseptics for symptom relief
        5. Maintain good hygiene practices
        6. Seek medical attention for severe symptoms
        7. Follow up with healthcare provider regularly

        Note: These are general recommendations. 
        Always consult with a healthcare professional for personalized advice.
        """
        messagebox.showinfo("Doctor Recommendations", recommendations)

    def show_food_suggestions(self):
        """Show food suggestions"""
        suggestions = """
        Nutritional Recommendations for Monkeypox Patients:

        1. Stay hydrated with water, electrolyte solutions
        2. Consume soft, easy-to-swallow foods if mouth sores are present
        3. Eat protein-rich foods for tissue repair
        4. Include vitamin-rich fruits and vegetables
        5. Consider foods high in zinc for immune support
        6. Opt for cool foods if fever is present
        7. Avoid spicy, acidic, or crunchy foods if mouth lesions

        Suggested foods: Yogurt, smoothies, soups, eggs, mashed potatoes, 
        cooked vegetables, oatmeal, and protein shakes.
        """
        messagebox.showinfo("Food Suggestions", suggestions)

    def show_medicine_info(self):
        """Show medicine information"""
        info = """
        Medical Information for Monkeypox:

        Currently, there are no specific treatments approved for monkeypox. 
        However, several measures can be taken:

        1. Symptomatic treatment for fever and pain
        2. Topical antibiotics for secondary bacterial infections
        3. Antiviral medications may be considered in severe cases
        4. Vaccinia Immune Globulin (VIG) may be used for severe cases
        5. Tecovirimat (TPOXX) is an antiviral approved for smallpox that may be used

        Important: Always consult a healthcare provider for proper diagnosis 
        and treatment recommendations. Do not self-medicate.
        """
        messagebox.showinfo("Medicine Information", info)

    def exit_app(self):
        """Exit the application"""
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = MonkeyPoxDetector(root)
    root.mainloop()