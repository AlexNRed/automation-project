import serial
import time

arduino_port = 'COM3'
baud_rate = 9600

def parse_sensor_data(line):

    try:

        parts = line.split(',') # this is only to split the line by ',' into a list

        # extract the temp
        temp_parts = parts[0].split(':')[1].strip() # splits the parts list into a new list by ':'
        temp = float(temp_parts.replace('°F', '').strip()) # removes the '°f' and converts to float

        # extract the humidity
        humidity_parts = parts[1].split(':')[1].strip() # splits the parts list into a new list by ':'
        humidity = float(humidity_parts.replace('%', '').strip()) # removes the '%' and converts to float

        return temp, humidity
    except Exception as e:
        return None, None
    
def main():
    
    print("=" * 50)
    print("Temperature Monitor -- Python Edition")
    print("=" * 50)
    print(f"Connecting to Arudino port {arduino_port}...")

    try:
        arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
        time.sleep(2)

        while True:

            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8', errors = 'ignore').strip()

                if not line:
                    continue
                
                print(f"DEBUG: Received: '{line}'")
                
                if line.startswith("Temperature:"):

                    temp, humidity = parse_sensor_data(line)

                    if temp is not None and humidity is not None:
                        
                        
                        print(f"🌡️  Temperature: {temp}°F")
                        
                        print(f"💧 Humidity: {humidity}%")

                        if temp > 78:
                            print("   → 🔥 It's HOT! Fan should be ON")
                            arduino.write(b'LED_RED\n') # Turn on red LED and represents the hottness
                        elif temp < 68:
                            print("   → ❄️  It's COLD! Heater should be ON")
                            arduino.write(b'LED_BLUE\n') # Turn on blue LED and represents the coldness
                        else:
                            print("   → ✓ Temperature is comfortable")
                            arduino.write(b'LED_GREEN\n') # Turn on green LED and represents when the temp is just right. 

                        if humidity > 60:
                            print("   → 💦 High humidity - consider dehumidifier")
                        elif humidity < 30:
                            print("   → 🏜️  Low humidity - consider humidifier")
                        
                        print("-" * 50)
                        print()

                        time.sleep(5)  # wait before next read

                else:
                    print(f'[line]')    

    except serial.SerialException as e:
        print()
        print("❌ ERROR: Could not connect to Arduino")
        print(f"Port: {arduino_port}")
        
    
    except KeyboardInterrupt:
        print()
        print()
        print("=" * 50)
        print("Stopping monitor...")

        arduino.write(b'LED_OFF\n') 
        time.sleep(0.5) 

        arduino.close()
        print("✓ Disconnected from Arduino")
        print("=" * 50)
    
    except Exception as e:
        print(f"Unexpected error: {e}")

    ## To see what to put within the excepts, you would first run your code without try and except and see the erorrs that you can get.

if __name__ == "__main__":
    main()
