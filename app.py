import json
import tkinter as tk
from tkinter import filedialog
import person_data

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Isikuandmete vaataja")

        self.load_button = tk.Button(root, text="Laadi andmefail", command=self.load_data_file, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.load_button.pack(pady=20)

        self.result_text = tk.Text(root, wrap=tk.WORD, width=80, height=20)
        self.result_text.pack(pady=20)

    def load_data_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON failid", "*.json")])
        if not file_path:
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.person_data = person_data.PersonData(data)
        self.display_results()

    def display_results(self):
        self.result_text.delete(1.0, tk.END)

        results_data = self.person_data.get_results()

        results = [
            "1. Isikute arv kokku: {}".format(results_data["total_count"]),
            "2. Kõige pikem nimi ja tähemärkide arv: {} ({} tähemärki)".format(
                results_data["longest_name"].name,
                len(results_data["longest_name"].name)
            ),
            "3. Kõige vanem elav inimene: {}, {} aastat vana ({})".format(
                results_data["oldest_living_person"].name,
                results_data["oldest_living_person"].age(),
                results_data["oldest_living_person"].birth_date_estonian()
            ),
            "4. Kõige vanem surnud inimene: {}, {} aastat vana ({} - {})".format(
                results_data["oldest_deceased_person"].name,
                results_data["oldest_deceased_person"].age(),
                results_data["oldest_deceased_person"].birth_date_estonian(),
                results_data["oldest_deceased_person"].death_date_estonian()
            ),
            "5. Näitlejate koguarv: {}".format(results_data["actor_count"]),
            "6. Sündinud 1997. aastal: {}".format(results_data["count_born_in_1997"]),
            "7. Erinevate elukutsete arv: {}".format(results_data["unique_occupations"]),
            "8. Nimi sisaldab rohkem kui kaks nime: {}".format(results_data["multi_name_count"]),
            "9. Sünniaeg ja surmaaeg on sama, välja arvatud aasta: {}".format(results_data["same_birth_death_month_day"]),
            "10. Elavaid isikuid: {}, Surnud isikuid: {}".format(
                results_data["living_count"], results_data["deceased_count"]
            )
        ]

        for result in results:
            self.result_text.insert(tk.END, result + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
