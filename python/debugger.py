def parse_sensor_data(line):
    try:
        parts = line.split(',')
        temp_part = parts[0].split(':')[1].strip()
        temp = float(temp_part.replace('°F', '').strip())
        humidity_part = parts[1].split(':')[1].strip()
        humidity = float(humidity_part.replace('%', '').strip())
        return temp, humidity
    except Exception as e:
        return None, None
    

print("Test 1: Normal data")
temp, humidity = parse_sensor_data("Temperature: 72.5°F, Humidity: 45.0%")
print(f"  Temp: {temp}, Humidity: {humidity}")
print()