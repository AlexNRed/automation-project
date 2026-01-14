import serial 
import time

arduino_port = 'COM3' # match with your arudino port
baud_rate = 9600

def parse_sensor_data(line):

    try:

        parts = line.split(',') # this is only to split the line by ',' into a list

        # extract the temp
        temp_parts = parts[0].split(':')[1].strip() # splits the parts list into a new list by ':'
        temp = float(temp_parts.replace('°f', '').strip()) # removes the '°f' and converts to float

        # extract the humidity
        humidity_parts = parts[1].split(':')[1].strip() # splits the parts list into a new list by ':'
        humidity = float(humidity_parts.replace('%', '').strip()) # removes the '%' and converts to float

        return temp, humidity
    except Exception as e:
        return None, None
    

