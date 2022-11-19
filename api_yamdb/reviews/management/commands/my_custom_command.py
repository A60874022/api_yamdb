import csv
from django.core.management.base import BaseCommand
from reviews.models import Categories, Genres, Titles, GenresTitles


files = {
    Categories: 'static/data/category.csv',
    Genres: 'static/data/genre.csv',
    Titles: 'static/data/titles.csv',
    GenresTitles: 'static/data/genre_title.csv',

}

class Command(BaseCommand):
    help = 'load people from csv'

    def handle(self, *args, **options):
        for key, f in files.items():
            with open(f, encoding="utf8") as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    try:
                        key.objects.bulk_create(**row)
                        
                    except Exception as error:
                        print(error, f'{key}')
