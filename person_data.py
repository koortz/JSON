from datetime import datetime

class Person:
    def __init__(self, data):
        self.name = data["nimi"]
        self.birth_date = data["sundinud"]
        self.occupation = data["amet"]
        self.death_date = data["surnud"]

    def age(self):
        birth_date = datetime.strptime(self.birth_date, "%Y-%m-%d")
        if self.death_date != "0000-00-00":
            death_date = datetime.strptime(self.death_date, "%Y-%m-%d")
            return death_date.year - birth_date.year - ((death_date.month, death_date.day) < (birth_date.month, birth_date.day))
        else:
            today = datetime.today()
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    def birth_year(self):
        return self.birth_date.split("-")[0]

    def death_year(self):
        return self.death_date.split("-")[0]

    def birth_date_estonian(self):
        return datetime.strptime(self.birth_date, "%Y-%m-%d").strftime("%d.%m.%Y")

    def death_date_estonian(self):
        if self.death_date != "0000-00-00":
            return datetime.strptime(self.death_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        return None

class PersonData:
    def __init__(self, data):
        self.people = [Person(person) for person in data]

        self.total_count = len(self.people)
        self.longest_name = max(self.people, key=lambda person: len(person.name))
        self.oldest_living_person = None
        self.oldest_deceased_person = None
        self.actor_count = 0
        self.count_born_in_1997 = 0
        self.unique_occupations = set()
        self.multi_name_count = 0
        self.same_birth_death_month_day = 0
        self.living_count = 0
        self.deceased_count = 0

        self.analyze_data()

    def analyze_data(self):
        for person in self.people:
            if "näitleja" in person.occupation:
                self.actor_count += 1

            if person.birth_date.startswith("1997"):
                self.count_born_in_1997 += 1

            self.unique_occupations.add(person.occupation)

            if len(person.name.split()) > 2:
                self.multi_name_count += 1

            if person.death_date != "0000-00-00" and person.birth_date[5:] == person.death_date[5:]:
                self.same_birth_death_month_day += 1

            if person.death_date == "0000-00-00":
                self.living_count += 1
                if self.oldest_living_person is None or person.age() > self.oldest_living_person.age():
                    self.oldest_living_person = person
            else:
                self.deceased_count += 1
                if self.oldest_deceased_person is None or person.age() > self.oldest_deceased_person.age():
                    self.oldest_deceased_person = person

    def get_results(self):
        return {
            "total_count": self.total_count,
            "longest_name": self.longest_name,
            "oldest_living_person": self.oldest_living_person,
            "oldest_deceased_person": self.oldest_deceased_person,
            "actor_count": self.actor_count,
            "count_born_in_1997": self.count_born_in_1997,
            "unique_occupations": len(self.unique_occupations),
            "multi_name_count": self.multi_name_count,
            "same_birth_death_month_day": self.same_birth_death_month_day,
            "living_count": self.living_count,
            "deceased_count": self.deceased_count,
        }
