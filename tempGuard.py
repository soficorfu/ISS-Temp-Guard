from sense_hat import SenseHat
from time import sleep
from datetime import datetime
import csv

sense = SenseHat()

GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CSV_FILE = "temperature_log.csv"

def read_temperature():
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    temp = (t1 + t2) / 2
    return round(temp, 1)

def check_status(temp):
    if 18 <= temp <= 27:
        return "OK"
    elif (16 <= temp < 18) or (27 < temp <= 29):
        return "WARNING"
    else:
        return "ALARM"

def display_status(temp, status):
    if status == "OK":
        sense.clear(GREEN)
        sense.show_message(
            f"{temp}C OK",
            text_colour=WHITE,
            back_colour=GREEN,
            scroll_speed=0.20
        )

    elif status == "WARNING":
        sense.clear(YELLOW)
        sense.show_message(
            f"{temp}C WARN",
            text_colour=BLACK,
            back_colour=YELLOW,
            scroll_speed=0.20
        )

    else:
        sense.clear(RED)
        sense.show_message(
            f"{temp}C ALARM",
            text_colour=WHITE,
            back_colour=RED,
            scroll_speed=0.20
        )

def save_log(temp, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([now, temp, status])

def setup_file():
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["datetime", "temperature", "status"])

def main():
    setup_file()
    sense.show_message(
        "ISS TEMP",
        text_colour=WHITE,
        back_colour=BLACK,
        scroll_speed=0.05
    )

    while True:
        temp = read_temperature()
        status = check_status(temp)

        print("Temperature:", temp, "Status:", status)

        display_status(temp, status)
        save_log(temp, status)

        sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sense.clear()
        print("Το πρόγραμμα τερματίστηκε.")