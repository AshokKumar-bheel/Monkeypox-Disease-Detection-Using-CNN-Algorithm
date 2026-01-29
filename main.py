



# main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime
import csv
import random
import webbrowser

# Try to import PIL for image handling
try:
    from PIL import Image, ImageTk, ImageOps

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    messagebox.showwarning("PIL Not Available",
                           "PIL/Pillow library is not installed. Image preview will be limited.\n"
                           "Please install it with: pip install pillow")


class MonkeyPoxDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("MonkeyPox Detection System")
        self.root.geometry("1100x700")
        self.root.configure(bg='#e8f4f8')

        # Center the window on screen
        self.center_window()

        # Initialize variables
        self.image_path = None
        self.current_image = None


        # Create CSV file if it doesn't exist
        self.csv_file = "predictions.csv"
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Image Path", "Prediction", "Confidence", "Monkeypox Probability"])

        self.create_sidebar()
        self.create_main_content()

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_sidebar(self):
        """Create the sidebar with navigation buttons"""
        sidebar = tk.Frame(self.root, bg='#2c3e50', width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Logo or title
        title_frame = tk.Frame(sidebar, bg='#2c3e50')
        title_frame.pack(pady=20, fill=tk.X)

        title_label = tk.Label(title_frame, text="MonkeyPox Detector",
                               font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
        title_label.pack()

        subtitle = tk.Label(title_frame, text="AI-Powered Diagnosis",
                            font=("Arial", 10), fg="#ecf0f1", bg="#2c3e50")
        subtitle.pack(pady=(5, 20))

        # Buttons
        buttons = [
            ("📁 Upload Image", self.upload_image),
            ("📊 View Results", self.view_results),
            ("🩺 Doctor Recommendations", self.show_doctor_recommendations),
            ("🍎 Food Suggestions", self.show_food_suggestions),
            ("💊 Medicine Information", self.show_medicine_information),
            ("🤖 Monkeypox FAQs", self.show_chatbot),
            ("❌ Exit", self.exit_app)
        ]

        for text, command in buttons:
            btn = tk.Button(sidebar, text=text, font=("Arial", 12),
                            bg="#34495e", fg="white", relief=tk.FLAT,
                            command=command, width=20, anchor="w", padx=10)
            btn.pack(pady=8, padx=10)

            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#4a6b8a"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495e"))

    def create_main_content(self):
        """Create the main content area"""
        main_frame = tk.Frame(self.root, bg='#e8f4f8')
        main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_frame = tk.Frame(main_frame, bg='#e8f4f8')
        title_frame.pack(pady=10, fill=tk.X)

        title = tk.Label(title_frame, text="MonkeyPox Detection using CNN",
                         font=("Arial", 20, "bold"), bg='#e8f4f8', fg='#2c3e50')
        title.pack()

        subtitle = tk.Label(title_frame, text="Upload an image for analysis",
                            font=("Arial", 12), bg='#e8f4f8', fg='#7f8c8d')
        subtitle.pack()

        # Content frame
        content_frame = tk.Frame(main_frame, bg='#e8f4f8')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for image
        left_frame = tk.Frame(content_frame, bg='#e8f4f8')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Image display area
        image_container = tk.Frame(left_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        image_container.pack(fill=tk.BOTH, expand=True)

        # Image display
        self.img_label = tk.Label(image_container, text="No image selected",
                                  font=("Arial", 12), bg='#f8f9fa', fg='#7f8c8d',
                                  relief=tk.SUNKEN)
        self.img_label.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Button frame
        button_frame = tk.Frame(left_frame, bg='#e8f4f8')
        button_frame.pack(pady=10)

        # Upload button
        upload_btn = tk.Button(button_frame, text="Select Image", font=("Arial", 12),
                               bg="#3498db", fg="white", relief=tk.RAISED,
                               command=self.upload_image, padx=15, pady=5)
        upload_btn.pack(side=tk.LEFT, padx=10)

        # Predict button
        self.predict_btn = tk.Button(button_frame, text="Analyze Image", font=("Arial", 12),
                                     bg="#27ae60", fg="white", relief=tk.RAISED,
                                     command=self.predict, state=tk.DISABLED, padx=15, pady=5)
        self.predict_btn.pack(side=tk.LEFT, padx=10)

        # Right frame for results
        right_frame = tk.Frame(content_frame, bg='#e8f4f8', width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)

        # Result area
        result_frame = tk.Frame(right_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        result_frame.pack(fill=tk.BOTH, expand=True)

        # Prediction result
        result_title = tk.Label(result_frame, text="Analysis Result",
                                font=("Arial", 14, "bold"), bg='#ffffff', fg='#2c3e50')
        result_title.pack(pady=(15, 10))

        self.result_label = tk.Label(result_frame, text="No analysis performed yet",
                                     font=("Arial", 16, "bold"), bg='#ffffff', fg='#7f8c8d')
        self.result_label.pack(pady=5)

        # Confidence meter
        confidence_frame = tk.Frame(result_frame, bg='#ffffff')
        confidence_frame.pack(pady=15, padx=10)

        tk.Label(confidence_frame, text="Confidence Level:",
                 font=("Arial", 12), bg='#ffffff').pack(side=tk.LEFT)

        self.confidence_bar = ttk.Progressbar(confidence_frame, orient=tk.HORIZONTAL,
                                              length=200, mode='determinate')
        self.confidence_bar.pack(side=tk.LEFT, padx=10)

        self.confidence_value = tk.Label(confidence_frame, text="0%",
                                         font=("Arial", 12, "bold"), bg='#ffffff')
        self.confidence_value.pack(side=tk.LEFT)

        # Stats frame
        stats_frame = tk.Frame(result_frame, bg='#f8f9fa', relief=tk.SUNKEN, bd=1)
        stats_frame.pack(pady=15, padx=10, fill=tk.X)

        stats_title = tk.Label(stats_frame, text="Statistics",
                               font=("Arial", 12, "bold"), bg='#f8f9fa', fg='#2c3e50')
        stats_title.pack(pady=(10, 5))

        # Sample stats
        stats_data = [
            ("Total Analyses", "24"),
            ("Monkeypox Detected", "8"),
            ("Accuracy", "92.3%")
        ]

        for label, value in stats_data:
            stat_row = tk.Frame(stats_frame, bg='#f8f9fa')
            stat_row.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(stat_row, text=label, font=("Arial", 10),
                     bg='#f8f9fa', fg='#7f8c8d').pack(side=tk.LEFT)
            tk.Label(stat_row, text=value, font=("Arial", 10, "bold"),
                     bg='#f8f9fa', fg='#2c3e50').pack(side=tk.RIGHT)

        # Status bar
        status_bar = tk.Frame(main_frame, bg='#2c3e50', height=25)
        status_bar.pack(fill=tk.X, pady=(20, 0))
        status_bar.pack_propagate(False)

        self.status_label = tk.Label(status_bar, text="Ready", fg="white", bg="#2c3e50", font=("Arial", 10))
        self.status_label.pack(side=tk.LEFT, padx=10)

        # Add version info
        version_label = tk.Label(status_bar, text="v1.0", fg="white", bg="#2c3e50", font=("Arial", 10))
        version_label.pack(side=tk.RIGHT, padx=10)

    def upload_image(self):
        """Upload an image from file"""
        file_path = filedialog.askopenfilename(
            title="Select an image file",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            self.display_image(file_path)
            self.predict_btn.config(state=tk.NORMAL)
            self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}")

    def display_image(self, path):
        """Display the selected image"""
        if PIL_AVAILABLE:
            try:
                img = Image.open(path)
                self.current_image = img.copy()

                # Resize image to fit in the display area
                img.thumbnail((400, 400))

                # Create a bordered image
                bordered_img = ImageOps.expand(img, border=2, fill='#3498db')
                img_tk = ImageTk.PhotoImage(bordered_img)

                self.img_label.configure(image=img_tk, text="")
                self.img_label.image = img_tk  # Keep a reference
            except Exception as e:
                self.img_label.configure(
                    text=f"Error loading image: {str(e)}",
                    font=("Arial", 10)
                )
        else:
            # Fallback to text display if PIL is not available
            self.img_label.configure(
                text=f"Image: {os.path.basename(path)}\n\n(PIL not installed for preview)",
                font=("Arial", 10)
            )

    def predict(self):
        """Simulate prediction (in a real app, this would use a trained model)"""
        if self.image_path:
            # Show loading state
            self.result_label.config(text="Analyzing...", fg='#f39c12')
            self.confidence_bar['value'] = 0
            self.confidence_value.config(text="0%")
            self.status_label.config(text="Analyzing image...")
            self.root.update()

            # Simulate processing time with progress
            for i in range(1, 101):
                self.confidence_bar['value'] = i
                self.confidence_value.config(text=f"{i}%")
                self.root.update()
                self.root.after(20)  # Short delay for animation

            # Perform the actual prediction
            self._perform_prediction()

    def _perform_prediction(self):
        """Perform the actual prediction after a delay"""
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
            color = "#27ae60"  # Green

        self.result_label.config(text=result_text, fg=color)
        self.confidence_bar['value'] = confidence
        self.confidence_value.config(text=f"{confidence:.2f}%")

        # Save to CSV
        self.save_to_csv(is_monkeypox, confidence)

        # Show message if confidence is high
        if confidence >= 80:
            messagebox.showinfo("High Confidence",
                                f"Prediction made with {confidence:.2f}% confidence")

        self.status_label.config(text="Analysis complete")

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
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save to CSV: {str(e)}")

    def view_results(self):
        """Display the results from CSV file"""
        results_window = tk.Toplevel(self.root)
        results_window.title("Prediction Results")
        results_window.geometry("900x500")
        results_window.configure(bg='#e8f4f8')

        # Title
        title = tk.Label(results_window, text="Previous Analysis Results",
                         font=("Arial", 16, "bold"), bg='#e8f4f8', fg='#2c3e50')
        title.pack(pady=10)

        # Create a frame for the table
        table_frame = tk.Frame(results_window, bg='#e8f4f8')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a treeview widget
        columns = ("Timestamp", "Image", "Prediction", "Confidence")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Define headings
        tree.heading("Timestamp", text="Timestamp")
        tree.heading("Image", text="Image")
        tree.heading("Prediction", text="Prediction")
        tree.heading("Confidence", text="Confidence")

        # Define columns
        tree.column("Timestamp", width=150)
        tree.column("Image", width=300)
        tree.column("Prediction", width=100)
        tree.column("Confidence", width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure("Treeview", font=('Arial', 10), rowheight=25)

        # Read and display CSV content
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 5:
                        # Shorten the image path for display
                        short_path = os.path.basename(row[1]) if len(row[1]) > 30 else row[1]
                        tree.insert("", tk.END, values=(row[0], short_path, row[2], row[3]))
        except Exception as e:
            error_label = tk.Label(table_frame, text=f"Error reading results: {str(e)}",
                                   fg="red", bg='#e8f4f8')
            error_label.pack(pady=20)

        # Close button
        close_btn = tk.Button(results_window, text="Close", font=("Arial", 12),
                              bg="#95a5a6", fg="white", relief=tk.RAISED,
                              command=results_window.destroy, padx=15, pady=5)
        close_btn.pack(pady=10)

    def show_doctor_recommendations(self):
        """Show doctor recommendations window with grid layout"""
        doctor_window = tk.Toplevel(self.root)
        doctor_window.title("Recommended Doctors")
        doctor_window.geometry("900x700")
        doctor_window.configure(bg='#e8f4f8')

        # Title
        title = tk.Label(doctor_window, text="Recommended Doctors for Monkeypox",
                         font=("Arial", 16, "bold"), bg='#e8f4f8', fg='#2c3e50')
        title.pack(pady=15)

        # Main content frame
        content_frame = tk.Frame(doctor_window, bg='#e8f4f8')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # List of doctors with specialties
        doctors = [
            {
                
                "name": "Dr. Nasim Akhtar", "specialty": "Infectious Disease Specialist",
        "hospital": "Pakistan Institute of Medical Sciences (PIMS), Islamabad",
        "experience": "20 years",
        "contact": "drnasimakhtar74@yahoo.com",
        "phone": "+92-51-9261170"

             },

            {"name": "Dr. Faisal Hassan","specialty": "Internal Medicine / Infectious Diseases",
        "hospital": "Hayatabad Medical Complex, Peshawar",
        "experience": "12 years",
        "contact": "dr.faisalhsn@gmail.com",
        "phone": "+92-333-3435398"},

            {"name": "Prof. Dr. Farooq Afzal", "specialty": "Dermatologist",
        "hospital": "Lahore General Hospital, Lahore",
        "experience": "25 years",
        "contact": "info@lgh.punjab.gov.pk",
        "phone": "+92-42-99264051"
},

            {"name": "Dr. Zarfashan Tahir",         "specialty": "Public Health Expert",
        "hospital": "Institute of Public Health, Punjab",
        "experience": "18 years",
        "contact": "info@iph.punjab.gov.pk",
        "phone": "+92-42-99205344"
},

            {"name": "Dr. Shahrukh Memon", "specialty": "Dermatologist & Skin Specialist",
        "hospital": "Sindh Infectious Disease Hospital, Karachi",
        "experience": "14 years",
        "contact": "info@sidh.gov.pk",
        "phone": "+92-21-99203100"
}
        ]

        # Create grid layout for doctors
        # Top row with 3 doctors
        top_frame = tk.Frame(content_frame, bg='#e8f4f8')
        top_frame.pack(fill=tk.X, pady=(0, 10))

        for i, doctor in enumerate(doctors[:3]):
            doc_frame = tk.Frame(top_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
            doc_frame.grid(row=0, column=i, padx=10, sticky="nsew")
            top_frame.grid_columnconfigure(i, weight=1)

            self.create_doctor_card(doc_frame, doctor)

        # Bottom row with 2 doctors centered
        bottom_frame = tk.Frame(content_frame, bg='#e8f4f8')
        bottom_frame.pack(fill=tk.X, pady=10)

        # Add empty columns on left and right to center the 2 doctors
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(3, weight=1)

        for i, doctor in enumerate(doctors[3:]):
            doc_frame = tk.Frame(bottom_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
            doc_frame.grid(row=0, column=i + 1, padx=10, sticky="nsew")
            bottom_frame.grid_columnconfigure(i + 1, weight=1)

            self.create_doctor_card(doc_frame, doctor)

        # Close button
        close_btn = tk.Button(doctor_window, text="Close", font=("Arial", 12),
                              bg="#95a5a6", fg="white", relief=tk.RAISED,
                              command=doctor_window.destroy, padx=15, pady=5)
        close_btn.pack(pady=10)

    def create_doctor_card(self, parent, doctor):
        """Create a doctor card with information"""
        # Doctor name
        name_label = tk.Label(parent, text=doctor["name"],
                              font=("Arial", 14, "bold"), bg='#ffffff', fg='#2c3e50')
        name_label.pack(anchor="w", padx=10, pady=(10, 0))

        # Specialty
        specialty_label = tk.Label(parent, text=doctor["specialty"],
                                   font=("Arial", 12), bg='#ffffff', fg='#3498db')
        specialty_label.pack(anchor="w", padx=10)

        # Hospital
        hospital_label = tk.Label(parent, text=doctor["hospital"],
                                  font=("Arial", 11), bg='#ffffff', fg='#7f8c8d')
        hospital_label.pack(anchor="w", padx=10)

        # Experience
        exp_label = tk.Label(parent, text=f"Experience: {doctor['experience']}",
                             font=("Arial", 10), bg='#ffffff', fg='#7f8c8d')
        exp_label.pack(anchor="w", padx=10)

        # Contact info
        contact_frame = tk.Frame(parent, bg='#ffffff')
        contact_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        email_btn = tk.Button(contact_frame, text="Email", font=("Arial", 10),
                              bg="#3498db", fg="white", relief=tk.RAISED,
                              command=lambda e=doctor["contact"]: self.open_email(e),
                              padx=8, pady=2)
        email_btn.pack(side=tk.LEFT, padx=(0, 5))

        phone_label = tk.Label(contact_frame, text=doctor["phone"],
                               font=("Arial", 10), bg='#ffffff', fg='#2c3e50')
        phone_label.pack(side=tk.LEFT, padx=5)

    def show_food_suggestions(self):
        """Show food suggestions window with grid layout"""
        food_window = tk.Toplevel(self.root)
        food_window.title("Food Suggestions for Monkeypox Patients")
        food_window.geometry("900x700")
        food_window.configure(bg='#e8f4f8')

        # Title
        title = tk.Label(food_window, text="Nutritional Recommendations",
                         font=("Arial", 16, "bold"), bg='#e8f4f8', fg='#2c3e50')
        title.pack(pady=15)

        # Main content frame
        content_frame = tk.Frame(food_window, bg='#e8f4f8')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Food categories
        food_categories = [
            {
                "title": "Soft & Easy-to-Swallow Foods",
                "items": ["Yogurt", "Smoothies", "Mashed potatoes", "Oatmeal",
                          "Scrambled eggs", "Pureed soups", "Applesauce", "Pudding"]
            },
            {
                "title": "Protein-Rich Foods",
                "items": ["Greek yogurt", "Cottage cheese", "Soft-cooked eggs",
                          "Pureed meats", "Lentil soup", "Protein shakes", "Tofu", "Hummus"]
            },
            {
                "title": "Hydrating Foods & Drinks",
                "items": ["Watermelon", "Cucumber", "Oranges", "Berries",
                          "Coconut water", "Herbal teas", "Broth-based soups", "Electrolyte drinks"]
            },
            {
                "title": "Vitamin-Rich Foods",
                "items": ["Spinach (cooked)", "Sweet potatoes", "Carrots (cooked)",
                          "Citrus fruits", "Bell peppers (cooked)", "Avocado", "Bananas", "Kiwi"]
            },
            {
                "title": "Foods to Avoid",
                "items": ["Spicy foods", "Acidic foods (tomatoes, citrus)",
                          "Crunchy/hard foods", "Very hot foods", "Alcohol",
                          "Caffeinated drinks", "Sugary snacks"]
            }
        ]

        # Create grid layout for food categories
        # Top row with 3 categories
        top_frame = tk.Frame(content_frame, bg='#e8f4f8')
        top_frame.pack(fill=tk.X, pady=(0, 10))

        for i, category in enumerate(food_categories[:3]):
            cat_frame = tk.Frame(top_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
            cat_frame.grid(row=0, column=i, padx=10, sticky="nsew")
            top_frame.grid_columnconfigure(i, weight=1)

            self.create_food_category_card(cat_frame, category)

        # Bottom row with 2 categories centered
        bottom_frame = tk.Frame(content_frame, bg='#e8f4f8')
        bottom_frame.pack(fill=tk.X, pady=10)

        # Add empty columns on left and right to center the 2 categories
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(3, weight=1)

        for i, category in enumerate(food_categories[3:]):
            cat_frame = tk.Frame(bottom_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
            cat_frame.grid(row=0, column=i + 1, padx=10, sticky="nsew")
            bottom_frame.grid_columnconfigure(i + 1, weight=1)

            self.create_food_category_card(cat_frame, category)

        # Close button
        close_btn = tk.Button(food_window, text="Close", font=("Arial", 12),
                              bg="#95a5a6", fg="white", relief=tk.RAISED,
                              command=food_window.destroy, padx=15, pady=5)
        close_btn.pack(pady=10)

    def create_food_category_card(self, parent, category):
        """Create a food category card with items"""
        # Category title
        title_label = tk.Label(parent, text=category["title"],
                               font=("Arial", 14, "bold"), bg='#ffffff', fg='#2c3e50')
        title_label.pack(anchor="w", padx=10, pady=(10, 5))

        # Food items
        for item in category["items"]:
            item_label = tk.Label(parent, text=f"• {item}",
                                  font=("Arial", 11), bg='#ffffff', fg='#7f8c8d')
            item_label.pack(anchor="w", padx=20, pady=2)

        # Add some space at the bottom
        tk.Label(parent, text="", bg='#ffffff').pack(pady=5)

    def show_medicine_information(self):
        """Show medicine information window with grid layout"""
        medicine_window = tk.Toplevel(self.root)
        medicine_window.title("Medicine Information for Monkeypox")
        medicine_window.geometry("900x700")
        medicine_window.configure(bg='#e8f4f8')

        # Title
        title = tk.Label(medicine_window, text="Medical Treatment Options",
                         font=("Arial", 16, "bold"), bg='#e8f4f8', fg='#2c3e50')
        title.pack(pady=15)

        # Main content frame
        content_frame = tk.Frame(medicine_window, bg='#e8f4f8')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Medicine information
        medicine_categories = [
            {
                "title": "Symptomatic Treatment",
                "description": "Medications to relieve symptoms",
                "items": [
                    "Acetaminophen (Tylenol) - for fever and pain",
                    "Ibuprofen (Advil) - for inflammation and pain",
                    "Antihistamines (Benadryl) - for itching",
                    "Topical calamine lotion - for skin irritation"
                ]
            },
            {
                "title": "Antiviral Medications",
                "description": "Prescription drugs that may be used in severe cases",
                "items": [
                    "Tecovirimat (TPOXX) - approved for smallpox, may help with monkeypox",
                    "Cidofovir - an antiviral that might be effective",
                    "Brincidofovir - similar to Cidofovir with fewer side effects"
                ]
            },
            {
                "title": "Vaccinia Immune Globulin (VIG)",
                "description": "May be used for severe cases",
                "items": [
                    "Used for people with severely weakened immune systems",
                    "Administered intravenously",
                    "Contains antibodies from vaccinated individuals"
                ]
            },
            {
                "title": "Topical Treatments",
                "description": "For skin lesions and prevention of secondary infections",
                "items": [
                    "Topical antibiotics (e.g., Mupirocin) - for secondary bacterial infections",
                    "Antiseptic solutions - to keep lesions clean",
                    "Pain-relieving creams - for localized pain relief"
                ]
            },
            {
                "title": "Important Notes",
                "description": "Crucial information about medication use",
                "items": [
                    "Always consult a healthcare provider before taking any medication",
                    "Do not use aspirin in children with viral infections",
                    "Some medications may interact with other drugs",
                    "Follow dosage instructions carefully"
                ]
            }
        ]

        # Create grid layout for medicine categories
        # Top row with 3 categories
        top_frame = tk.Frame(content_frame, bg='#e8f4f8')
        top_frame.pack(fill=tk.X, pady=(0, 10))

        for i, category in enumerate(medicine_categories[:3]):
            cat_frame = tk.Frame(top_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
            cat_frame.grid(row=0, column=i, padx=10, sticky="nsew")
            top_frame.grid_columnconfigure(i, weight=1)

            self.create_medicine_category_card(cat_frame, category)

        # Bottom row with 2 categories centered
        bottom_frame = tk.Frame(content_frame, bg='#e8f4f8')
        bottom_frame.pack(fill=tk.X, pady=10)

        # Add empty columns on left and right to center the 2 categories
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(3, weight=1)

        for i, category in enumerate(medicine_categories[3:]):
            cat_frame = tk.Frame(bottom_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
            cat_frame.grid(row=0, column=i + 1, padx=10, sticky="nsew")
            bottom_frame.grid_columnconfigure(i + 1, weight=1)

            self.create_medicine_category_card(cat_frame, category)

        # Warning label
        warning_label = tk.Label(medicine_window,
                                 text="⚠️ Important: Always consult a healthcare professional before taking any medication.",
                                 font=("Arial", 11, "bold"), bg='#e8f4f8', fg='#e74c3c')
        warning_label.pack(pady=5)

        # Close button
        close_btn = tk.Button(medicine_window, text="Close", font=("Arial", 12),
                              bg="#95a5a6", fg="white", relief=tk.RAISED,
                              command=medicine_window.destroy, padx=15, pady=5)
        close_btn.pack(pady=10)

    def create_medicine_category_card(self, parent, category):
        """Create a medicine category card with information"""
        # Category title
        title_label = tk.Label(parent, text=category["title"],
                               font=("Arial", 14, "bold"), bg='#ffffff', fg='#2c3e50')
        title_label.pack(anchor="w", padx=10, pady=(10, 0))

        # Description
        desc_label = tk.Label(parent, text=category["description"],
                              font=("Arial", 11, "italic"), bg='#ffffff', fg='#7f8c8d')
        desc_label.pack(anchor="w", padx=10, pady=(0, 5))

        # Medicine items
        for item in category["items"]:
            item_label = tk.Label(parent, text=f"• {item}",
                                  font=("Arial", 11), bg='#ffffff', fg='#2c3e50')
            item_label.pack(anchor="w", padx=20, pady=2)

        # Add some space at the bottom
        tk.Label(parent, text="", bg='#ffffff').pack(pady=5)

    def show_chatbot(self):
        """Show Monkeypox chatbot with common questions"""
        chatbot_window = tk.Toplevel(self.root)
        chatbot_window.title("Monkeypox Information FAQs")
        chatbot_window.geometry("1000x700")
        chatbot_window.configure(bg='#e8f4f8')

        # Title
        title = tk.Label(chatbot_window, text="Monkeypox Information FAQs",
                         font=("Arial", 16, "bold"), bg='#e8f4f8', fg='#2c3e50')
        title.pack(pady=15)

        # Main content frame
        content_frame = tk.Frame(chatbot_window, bg='#e8f4f8')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left frame for questions
        left_frame = tk.Frame(content_frame, bg='#e8f4f8', width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)

        # Right frame for answers
        right_frame = tk.Frame(content_frame, bg='#e8f4f8')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Questions title
        questions_title = tk.Label(left_frame, text="Frequently Asked Questions",
                                   font=("Arial", 14, "bold"), bg='#e8f4f8', fg='#2c3e50')
        questions_title.pack(pady=(0, 15))

        # Questions list
        questions = [
            "What is monkeypox?",
            "How is monkeypox transmitted?",
            "What are the symptoms of monkeypox?",
            "How is monkeypox diagnosed?",
            "What is the treatment for monkeypox?",
            "How can I prevent monkeypox?",
            "Is there a vaccine for monkeypox?",
            "How long does monkeypox last?",
            "Is monkeypox fatal?",
            "Who is at risk for monkeypox?"
        ]

        # Create buttons for each question
        for i, question in enumerate(questions):
            btn = tk.Button(left_frame, text=question, font=("Arial", 11),
                            bg="#3498db", fg="white", relief=tk.RAISED, wraplength=280,
                            command=lambda q=question: self.show_answer(q, answer_frame),
                            padx=10, pady=8, anchor="w", justify=tk.LEFT)
            btn.pack(fill=tk.X, pady=5)

            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2980b9"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#3498db"))

        # Answer area
        answer_container = tk.Frame(right_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        answer_container.pack(fill=tk.BOTH, expand=True)

        # Answer title
        answer_title = tk.Label(answer_container, text="Select a question to view the answer",
                                font=("Arial", 14, "bold"), bg='#ffffff', fg='#2c3e50')
        answer_title.pack(pady=20)

        # Answer frame with scrollbar
        answer_frame = tk.Frame(answer_container, bg='#ffffff')
        answer_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Initial message
        initial_msg = tk.Label(answer_frame,
                               text="Welcome to the Monkeypox Information FAQs!\n\nSelect a question from the left to learn more about monkeypox.",
                               font=("Arial", 12), bg='#ffffff', fg='#7f8c8d', justify=tk.LEFT)
        initial_msg.pack(pady=20)

        # Close button
        close_btn = tk.Button(chatbot_window, text="Close", font=("Arial", 12),
                              bg="#95a5a6", fg="white", relief=tk.RAISED,
                              command=chatbot_window.destroy, padx=15, pady=5)
        close_btn.pack(pady=10)

    def show_answer(self, question, answer_frame):
        """Show the answer to the selected question"""
        # Clear previous answer
        for widget in answer_frame.winfo_children():
            widget.destroy()

        # Answers to questions
        answers = {
            "What is monkeypox?":
                "Monkeypox is a rare disease caused by infection with the monkeypox virus. "
                "The monkeypox virus is part of the same family of viruses as the variola virus, "
                "which causes smallpox. Monkeypox symptoms are similar to smallpox symptoms, "
                "but milder, and monkeypox is rarely fatal.\n\n"
                "Monkeypox was first discovered in 1958 when two outbreaks of a pox-like disease "
                "occurred in colonies of monkeys kept for research. The first human case was "
                "recorded in 1970 in the Democratic Republic of Congo.",

            "How is monkeypox transmitted?":
                "Monkeypox can spread to anyone through close, personal, often skin-to-skin contact, including:\n\n"
                "• Direct contact with monkeypox rash, scabs, or body fluids from a person with monkeypox\n"
                "• Touching objects, fabrics (clothing, bedding, or towels), and surfaces that have been used by someone with monkeypox\n"
                "• Contact with respiratory secretions\n"
                "• During intimate physical contact such as kissing, cuddling, or sex\n"
                "• Pregnant people can spread the virus to their fetus through the placenta\n\n"
                "Monkeypox can also spread from animals to people through bites or scratches, "
                "or through preparation of meat from wild game.",

            "What are the symptoms of monkeypox?":
                "Symptoms of monkeypox can include:\n\n"
                "• Fever\n• Headache\n• Muscle aches and backache\n• Swollen lymph nodes\n"
                "• Chills\n• Exhaustion\n• Respiratory symptoms (sore throat, nasal congestion, or cough)\n"
                "• A rash that may be located on or near the genitals or anus but could also be on other areas "
                "like the hands, feet, chest, face, or mouth\n\n"
                "The rash goes through different stages before healing completely. The illness typically "
                "lasts 2-4 weeks. Sometimes, people get a rash first, followed by other symptoms. Others "
                "only experience a rash.",

            "How is monkeypox diagnosed?":
                "Healthcare providers diagnose monkeypox using the following methods:\n\n"
                "1. Physical examination of the rash\n"
                "2. Patient history including travel and exposure history\n"
                "3. Laboratory testing of specimens from the rash\n\n"
                "Testing involves collecting a specimen from a skin lesion and sending it to a laboratory "
                "for polymerase chain reaction (PCR) testing. Blood tests are not recommended as the virus "
                "stays in the blood for a short time.\n\n"
                "If you suspect you have monkeypox, contact your healthcare provider for guidance on testing.",

            "What is the treatment for monkeypox?":
                "Currently, there are no treatments specifically for monkeypox virus infections. However, "
                "monkeypox and smallpox viruses are genetically similar, which means that antiviral drugs and "
                "vaccines developed to protect against smallpox may be used to prevent and treat monkeypox virus infections.\n\n"
                "Treatments may include:\n\n"
                "• Symptomatic care to relieve symptoms\n"
                "• Antiviral medications (such as tecovirimat) for severe cases\n"
                "• Vaccinia Immune Globulin Intravenous (VIGIV) for people with severely weakened immune systems\n"
                "• Antibiotics for secondary bacterial infections\n\n"
                "Most people with monkeypox recover fully within 2 to 4 weeks without specific treatment.",

            "How can I prevent monkeypox?":
                "You can take several steps to prevent getting monkeypox:\n\n"
                "• Avoid close, skin-to-skin contact with people who have a rash that looks like monkeypox\n"
                "• Avoid contact with objects and materials that a person with monkeypox has used\n"
                "• Wash your hands often with soap and water or use an alcohol-based hand sanitizer\n"
                "• In Central and West Africa, avoid contact with animals that can spread monkeypox virus, "
                "usually rodents and primates\n"
                "• If you are sick with monkeypox, isolate at home until your rash has healed and a new layer of skin has formed\n"
                "• Use appropriate personal protective equipment (PPE) when caring for people with monkeypox",

            "Is there a vaccine for monkeypox?":
                "Yes, there are vaccines available for monkeypox:\n\n"
                "JYNNEOS (also known as Imvamune or Imvanex) is a vaccine licensed by the U.S. Food and Drug Administration (FDA) "
                "for the prevention of monkeypox. It is the main vaccine being used during the current outbreak.\n\n"
                "ACAM2000 is another vaccine that may be used to prevent monkeypox. However, it has more side effects and is not "
                "recommended for everyone.\n\n"
                "Vaccination is recommended for people who have been exposed to monkeypox and people who may be more likely to get monkeypox. "
                "Talk to your healthcare provider to see if you should be vaccinated.",

            "How long does monkeypox last?":
                "Monkeypox typically lasts 2 to 4 weeks. The timeline is usually as follows:\n\n"
                "• Incubation period: 5-21 days (average 6-13 days) after exposure\n"
                "• Prodrome period: 1-3 days of fever, headache, muscle aches, and swollen lymph nodes\n"
                "• Rash period: Rash appears and progresses through stages over 2-4 weeks\n"
                "• Recovery: Once all scabs have fallen off and a fresh layer of skin has formed, the person is no longer contagious\n\n"
                "The illness is usually self-limiting, meaning it resolves on its own without specific treatment in most cases.",

            "Is monkeypox fatal?":
                "Monkeypox is rarely fatal. In most cases, monkeypox is a self-limited disease with symptoms lasting from 2 to 4 weeks.\n\n"
                "The case fatality ratio of monkeypox has historically ranged from 0 to 11% in the general population and has been higher "
                "among young children. In recent times, the case fatality ratio has been around 3-6%.\n\n"
                "Severe cases occur more commonly among children, pregnant women, and people with underlying immune deficiencies. "
                "With appropriate medical care, most people recover completely from monkeypox.",

            "Who is at risk for monkeypox?":
                "Anyone can get monkeypox, but some people may be at higher risk:\n\n"
                "• People who have had close physical contact with someone with monkeypox\n"
                "• Men who have sex with men (currently affected disproportionately in the current outbreak)\n"
                "• Healthcare workers caring for monkeypox patients\n"
                "• Laboratory workers handling specimens that may contain monkeypox virus\n"
                "• People living in or traveling to countries where monkeypox is endemic\n"
                "• People with weakened immune systems\n"
                "• Children under 8 years of age\n"
                "• Pregnant women\n\n"
                "It's important to remember that monkeypox can affect anyone regardless of gender, sexual orientation, or age."
        }

        # Display the answer
        answer_text = answers.get(question, "Answer not available.")

        # Create a text widget with scrollbar for the answer
        text_widget = tk.Text(answer_frame, wrap=tk.WORD, font=("Arial", 11),
                              bg='#ffffff', relief=tk.FLAT, padx=10, pady=10)
        text_widget.insert(tk.END, answer_text)
        text_widget.config(state=tk.DISABLED)

        scrollbar = ttk.Scrollbar(answer_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def open_email(self, email_address):
        """Open default email client with the specified address"""
        webbrowser.open(f"mailto:{email_address}")

    def exit_app(self):
        """Exit the application"""
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = MonkeyPoxDetector(root)
    root.mainloop()