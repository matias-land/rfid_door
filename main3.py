#!/usr/bin/env python
#source env/bin/activate
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import csv


GPIO.setmode(GPIO.BCM)
master_card = 1076492271060
csv_file = 'perm.csv'
result_column = 1
search_column = 0
relay_pin = 3
limit_switch_pin = 5
led_pin = 7
buzzer_pin = 11
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, GPIO.LOW)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def find_empty_column(filename):
    # Function to find the first empty column in the CSV file
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        max_columns = len(header)
        for row in reader:
            for idx in range(max_columns):
                if idx >= len(row) or not row[idx]:  # Check if column is empty
                    return idx
        return max_columns  # If all columns are filled, return the next column index

def write_to_empty_column(filename, data_list):
    empty_column_idx = find_empty_column(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Pad the row with empty strings until the empty column index
        if empty_column_idx > 0:
            writer.writerow([''] * empty_column_idx)
        writer.writerow(data_list)

def find_row_with_value(csv_file, colum_index, search_value):
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            if row[colum_index] == search_value:
                return row
    return None

def close_door():
    GPIO.output(relay_pin, GPIO.HIGH)

def open_door():
    GPIO.output(relay_pin, GPIO.LOW)

def open_door_sequence():
    open_door()
    time.sleep(5)
    if GPIO.input(limit_switch_pin)== HIGH:
        for i in range(20):
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(0.5)  
        GPIO.output(led_pin, GPIO.LOW)  
        time.sleep(0.5)
        print("test3")
    while GPIO.input(limit_switch_pin)== HIGH:
        GPIO.output(led_pin, GPIO.HIGH)
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(0.5)  
        GPIO.output(led_pin, GPIO.LOW)
        GPIO.output(buzzer_pin, GPIO.LOW)  
        time.sleep(0.5)
        print("test4")

reader = SimpleMFRC522()
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=toggle_relay, bouncetime=200)

try:
    id, text = reader.read()
    print(id)
    if __name__ =='__main__':
        value_to_find=f'{id}'
        row = find_row_with_value(csv_file, search_column, value_to_find)
        if id == master_card:
            print("place new card")
            time.sleep(3)
            id, text = reader.read()
            print(id)
            new_member_id =f'{id}'
            new_member=[new_member_id, 'y']
            write_to_empty_column(csv_file, new_member)
            print("test2")
        elif row:
            print(row[result_column])
            if row[result_column] == 'y':
                open_door_sequence()
        else:
            print("not found")
finally:
        GPIO.cleanup()