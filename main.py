#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def find_row_with_value(csv_file, column_index, search_value):
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the headers
        for row in reader:
            if row[column_index] == search_value:
                return row
    return None


reader = SimpleMFRC522()

try:
        id, text = reader.read()
        print(id)
        
        print(text)
        csv_file = 'perm.csv'  # Replace with your CSV file path
        column_to_search = 0  # Index of the column (0-based) where you want to search
        value_to_find = '3'  # The value you want to find in the specified column
        result_column = 1
        row = find_row_with_value(csv_file, column_to_search, value_to_find)

        if row:
        #print(f"Found '{value_to_find}' in the CSV file:")
        #print(f"Entire row: {row}")
        # Example: Print a specific column value from the found row
                perm_bool=row[result_column]
                print(perm_bool)
        else:
                perm_bool='n'
                print(f"No results found for '{value_to_find}'.")
finally:
        GPIO.cleanup()

