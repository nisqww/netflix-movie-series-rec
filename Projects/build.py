# build.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from main import Main, Recommendations

class NetflixRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Netflix Recommender")
        self.root.geometry("800x600")
        self.style = ttk.Style()
        
        # Set the theme to clam (built-in theme in ttk)
        self.style.theme_use("clam")

        # Configure styles
        self.style.configure("TLabel", font=("Helvetica", 12), background="#ffebcd")
        self.style.configure("TButton", font=("Helvetica", 12), background="#4CAF50", foreground="#ffffff")
        self.style.map("TButton", background=[("active", "#45a049")])
        self.style.configure("TCombobox", font=("Helvetica", 12))
        self.style.configure("TRadiobutton", font=("Helvetica", 12), background="#ffebcd")

        self.main_frame = tk.Frame(self.root, bg="#ffebcd")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.main = Main()
        self.create_widgets()

    def create_widgets(self):
        # Header
        self.header_label = tk.Label(self.main_frame, text="Netflix Recommender", font=("Helvetica", 16, "bold"), bg="#ffebcd")
        self.header_label.pack(pady=10)

        # Movie or Series
        self.type_label = ttk.Label(self.main_frame, text="Do you want recommendations for movies or series?")
        self.type_label.pack(pady=5)
        self.type_var = tk.StringVar(value="movie")
        self.movie_radio = ttk.Radiobutton(self.main_frame, text="Movie", variable=self.type_var, value="movie")
        self.series_radio = ttk.Radiobutton(self.main_frame, text="Series", variable=self.type_var, value="series")
        self.movie_radio.pack(pady=2)
        self.series_radio.pack(pady=2)

        # Genres
        self.genres_label = ttk.Label(self.main_frame, text="Select a genre (or leave blank for no preference):")
        self.genres_label.pack(pady=5)
        self.genres_combo = ttk.Combobox(self.main_frame, values=[''] + list(Main.genres_list.iloc[:, 0].values))
        self.genres_combo.pack(pady=5)

        # Country
        self.country_label = ttk.Label(self.main_frame, text="Select a country (or leave blank for no preference):")
        self.country_label.pack(pady=5)
        self.country_combo = ttk.Combobox(self.main_frame, values=[''] + list(Main.country_list.iloc[:, 0].unique()))
        self.country_combo.pack(pady=5)

        # Submit button
        self.submit_button = ttk.Button(self.main_frame, text="Get Recommendations", command=self.get_recommendations)
        self.submit_button.pack(pady=20)

        # Treeview for displaying recommendations
        self.tree_frame = tk.Frame(self.main_frame, bg="#ffebcd")
        self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.tree = ttk.Treeview(self.tree_frame, columns=("title", "type", "country", "release_year", "rating", "duration", "listed_in"), show='headings')
        self.tree.heading("title", text="Title")
        self.tree.heading("type", text="Type")
        self.tree.heading("country", text="Country")
        self.tree.heading("release_year", text="Release Year")
        self.tree.heading("rating", text="Rating")
        self.tree.heading("duration", text="Duration")
        self.tree.heading("listed_in", text="Genres")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def get_recommendations(self):
        type_value = self.type_var.get()
        genres_value = self.genres_combo.get()
        country_value = self.country_combo.get()

        # Clear existing recommendations
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Set filters for recommendations
        self.main.base(type_value)
        self.main.genres_filters(genres_value)
        self.main.country_filters(country_value)

        # Generate recommendations
        if not self.main.create_recommendations():
            messagebox.showinfo("No Results")
            self.main.filters_list = []  # Reset filters
            self.show_restart_prompt()
        else:
            # Display recommendations in Treeview
            for key, df in self.main.recommendations.items():
                for index, row in df.iterrows():
                    self.tree.insert("", "end", values=(row['title'], row['type'], row['country'], row['release_year'], row['rating'], row['duration'], row['listed_in']))

    def show_restart_prompt(self):
        response = messagebox.askyesno("Restart", "Would you like to try again?")
        if response:
            self.reset_ui()

    def reset_ui(self):
        self.type_var.set("movie")
        self.genres_combo.set('')
        self.country_combo.set('')


if __name__ == "__main__":
    root = tk.Tk()
    app = NetflixRecommenderApp(root)
    root.mainloop()
