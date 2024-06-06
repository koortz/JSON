import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


class PersonData:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_total_count(self):
        return len(self.data)

    def get_longest_name(self):
        longest_name = max((person for person in self.data if 'nimi' in person), key=lambda person: len(person['nimi']))
        return longest_name['nimi'], len(longest_name['nimi'])

    def get_oldest_person(self, alive=True):
        today = datetime.today()
        persons = [p for p in self.data if
                   'sundinud' in p and (p['surnud'] == '0000-00-00' if alive else p['surnud'] != '0000-00-00')]
        oldest = min(persons,
                     key=lambda p: today.year - int(p['sundinud'][:4]) if alive else int(p['surnud'][:4]) - int(
                         p['sundinud'][:4]))
        birth_year = int(oldest['sundinud'][:4])
        if alive:
            age = today.year - birth_year
        else:
            death_year = int(oldest['surnud'][:4])
            age = death_year - birth_year
        return oldest['nimi'], age

    def get_actor_count(self):
        return sum('amet' in person and 'näitleja' in person['amet'].lower() for person in self.data)

    def born_in_year(self, year):
        return sum('sundinud' in person and person['sundinud'].startswith(str(year)) for person in self.data)

    def get_unique_occupations_count(self):
        occupations = {occupation for person in self.data if 'amet' in person for occupation in
                       person['amet'].split(', ')}
        return len(occupations)

    def names_with_more_than_two_parts(self):
        return sum('nimi' in person and len(person['nimi'].split()) > 2 for person in self.data)

    def same_birth_death_except_year(self):
        return sum(
            'sundinud' in person and 'surnud' in person and person['sundinud'][5:] == person['surnud'][5:] and person[
                'surnud'] != '0000-00-00' for person in self.data)

    def get_living_and_deceased_counts(self):
        living = sum('surnud' in person and person['surnud'] == '0000-00-00' for person in self.data)
        deceased = len(self.data) - living
        return living, deceased


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Isikuandmete analüüs")
        self.filename = "2018-09-18_tuntud_eesti.json"

        # Frame for the buttons
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        # Laadi nupp
        self.load_button = tk.Button(self.frame, text="Laadi andmed", command=self.load_data, font=("Arial", 14),
                                     bg="#4CAF50", fg="white")
        self.load_button.pack(pady=10)

        # Tulemuste kuvamine
        self.results = tk.Text(self.root, width=100, height=25, font=("Arial", 12), padx=20, pady=20)
        self.results.pack(pady=10)

    def load_data(self):
        try:
            data = PersonData(self.filename)

            # Tulemuste kuvamine
            results_text = (
                f"Isikute arv kokku: {data.get_total_count()}\n"
                f"Kõige pikem nimi ja tähemärkide arv: {data.get_longest_name()}\n"
                f"Kõige vanem elav inimene: {data.get_oldest_person(alive=True)}\n"
                f"Kõige vanem surnud inimene: {data.get_oldest_person(alive=False)}\n"
                f"Näitlejate koguarv: {data.get_actor_count()}\n"
                f"Sündinud 1997 aastal: {data.born_in_year(1997)}\n"
                f"Erinevaid elukutseid: {data.get_unique_occupations_count()}\n"
                f"Nimi sisaldab rohkem kui kaks nime: {data.names_with_more_than_two_parts()}\n"
                f"Sünniaeg ja surmaaeg sama v.a. aasta: {data.same_birth_death_except_year()}\n"
                f"Elavad ja surnud isikud: {data.get_living_and_deceased_counts()}\n"
            )

            self.results.delete(1.0, tk.END)
            self.results.insert(tk.END, results_text)

        except Exception as e:
            messagebox.showerror("Viga", f"Andmete laadimine ebaõnnestus: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
