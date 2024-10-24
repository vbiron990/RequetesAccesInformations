import csv
import os

from core.db import Events
from core.db import CarModel


if __name__ == '__main__':

    """
    CASE 1: Ingest data in DB
    CASE 2: Delete all data from DB  !!!! WARNING !!!!
    CASE 3: Print data from event and car_model table
    CASE 4: Show how many entries are in the tables.
    """

    CASE = 3

    if CASE == 1:
        path = "data.csv"

        with open(os.path.abspath(path), newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in list(spamreader)[1:]:
                event_data = row[0].split(",")
                if len(event_data) < 9:
                    while len(event_data) < 9:
                        event_data.append("")

                car = CarModel.add_entry(
                    sequential_number=event_data[0],
                    car_type=event_data[3],
                    brand=event_data[4],
                    model=event_data[5],
                    cylindrical=event_data[6],
                    year=event_data[7],
                )
        CarModel.commit()

        with open(os.path.abspath(path), newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in list(spamreader)[1:]:
                event_data = row[0].split(",")
                event = Events()
                event.sequential_number = event_data[0]
                event.gravity = event_data[1]
                event.user_type = event_data[2]
                car_model = CarModel.get_one(CarModel.sequential_number == event.sequential_number)
                event.car_model_id = car_model.id
                event.add()

        Events.commit()
        CarModel.commit()

    elif CASE == 2:
        for event in Events.get():
            print(event.id)
            # event.delete(auto_commit=False)
        for car in CarModel.get():
            print(car.id)
            # car.delete(auto_commit=False)
    elif CASE == 3:
        events = Events.get()
        for event in events:
            print(event)
            print(event.car_model)
    elif CASE == 4:
        events = Events.get()
        print(f"{events.count()} events.")
        cars = CarModel.get()
        print(f"{cars.count()} cars.")

