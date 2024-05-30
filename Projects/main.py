# main.py
import pandas as pd

class Main:
    df = pd.read_csv("Projects/netflix_titles.csv", encoding='latin-1')
    df['director'] = df['director'].fillna(0)
    df['cast'] = df['cast'].fillna(0)
    df['country'] = df['country'].fillna(0)
    df['date_added'] = df["date_added"].fillna(0)
    Unnamed = ['Unnamed: 12', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15',
               'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18', 'Unnamed: 19',
               'Unnamed: 20', 'Unnamed: 21', 'Unnamed: 22', 'Unnamed: 23',
               'Unnamed: 24', 'Unnamed: 25']
    df = df.drop(columns=Unnamed, axis=1)

    country_list = pd.read_excel("Projects/Country.xlsx")
    genres_list = pd.read_excel("Projects/Genres.xlsx")
    filters_list = []

    def __init__(self):
        self.filters_list = []  # Ensure filters_list is reset for each instance
        self.recommendations = None

    def create_recommendations(self):
        self.recommendations = Recommendations.call_database(self.filters_list)
        if self.recommendations['results'].empty:
            return False
        return True

    def base(self, type_value):
        if type_value == 'movie':
            self.filters_list.append(('type', 'Movie'))
        elif type_value == 'series':
            self.filters_list.append(('type', 'TV Show'))
        else:
            print('Please choose either "movie" or "series". Let\'s try again.')

    def genres_filters(self, genres_value):
        if genres_value != '':
            if genres_value in self.genres_list.values:
                self.filters_list.append(('genres', genres_value))
                print('Thanks for the clue.')
            else:
                print("Please select a valid genre.")
        else:
            print("Please provide some clue.")

    def country_filters(self, country_value):
        if country_value != '':
            if country_value in self.country_list.values:
                self.filters_list.append(('country', country_value))
            else:
                print("Sorry, but we don't have that country... Can you give us another country, please?")
        else:
            print("Please provide a country.")


class Recommendations(Main):

    @staticmethod
    def call_database(filters_list):
        df = Main.df.copy()

        for filter_type, filter_value in filters_list:
            if filter_type == 'type':
                df = df[df['type'].str.contains(filter_value, case=False, na=False)]
            elif filter_type == 'genres':
                df = df[df['listed_in'].str.contains(filter_value, case=False, na=False)]
            elif filter_type == 'country':
                df = df[df['country'].str.contains(filter_value, case=False, na=False)]

        return {'results': df}
