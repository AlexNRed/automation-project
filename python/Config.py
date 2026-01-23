import serial
import time
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass
import json


# ============================================================================
# CONFIGURATION SECTION
# ============================================================================

@dataclass #A decorator - a moidifer or enchancer for this class
class Config:
    """
    Configuration class that uses a dataclass decorator
    makes it easier to manage all the settings in 1 place.
    """
    
    # Serial port settings
    arduino_port: str = 'COM3' # type hints improve readility
    baud_rate: int = 9600
    serial_timeout: int = 1

    # the Temperature thresholds
    temp_hot_threshold: float = 78.0
    temp_cold_threshold: float = 60.0

    # the Humidity thresholds
    humidity_high_threshold: float = 60.0
    humidity_low_threshold: float = 30.0

    # Data validation ranges
    temp_min: float = -40.0
    temp_max: float = 140.0
    hum_min: float = 0.0
    hum_max: float = 100.0

    # logging and data files
    log_file: str = 'temperature_log.csv' #stores the temperature and humidity readings
    app_log_file: str = 'app.log' #stores what the program is actually doing 

    # timing
    reading_interval: float = 5.0 # the seconds between readings

    @classmethod #uses cls (class) instead of self (instance)
    def load_from_json(cls, filepath: str) -> 'Config':
        """Load configuration from a JSON file."""
        try:
            with open(filepath, 'r') as logFile: #opens the file called logFile in read mode and closes it
                data = json.load(logFile) #load the json data into a dictionary and read JSON FROM file 
                return cls(**data) #creates a config object using the dictionary unpacking (kwargs)
        except FileNotFoundError:
            logging.warning(f"Config file {filepath} not found. Using defaults.") #shows the massage about the state of the program (like will show you when the program crashes an why)
            return cls()
        except json.JSONDecodeError:  # ← Add this!
            logging.error(f"Invalid JSON in {filepath}. Using defaults.")
            return cls()
        
    def save_to_json(self, filepath: str) -> None:
        """opens the file and calls it logFIle, Gets the object's data,  converts the object's data to 
        JSON format through the json.dump method, and writes it into the file logFile."""
        with open(filepath, 'w') as logFile:
            json.dump(self.__dict__, logFile, indent=4)

# ============================================================================
# LOGGING SETUP
# ============================================================================

    def setup_logging(log_file: str = 'app.log') -> None:
        """ the method is to set up the logging system to print out the data onto a file and also the terminal?"""
        logging.basicConfig(level = logging.INFO, 
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file), logging.StreamHandler()] ) #sets the logging level to INFO (5 Levels: DEBUG, INFO, WARNING, ERORR, CRITICAL) -> Saying: "Show me INFO messages and everything MORE important than INFO" , logging provides all the values automatically
        """Logging.basicConfig sets up the logging system with the settings you specify. 
        You only call this once at the start of your program. """

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class SensorReading:
    temperature: float
    humidity: float
    timestamp: datetime = None

    def __post_init__(self):
        """Automatically sets the timestamp if not provided"""
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def is_valid(self, config: Config) -> bool:
        """Checks if the readings are within the valid ranges"""
        return(
            config.temp_min <= self.temperature <= config.temp_max and 
            config.humidity_min <= self.humidity <= config.hum_max
        )
    
    def to_dict(self) -> dict:
        """Converts the reading to a dictionary format so it's easier to log/save"""
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

# ============================================================================
# ARDUINO COMMUNICATION CLASS
# ============================================================================

class ArudinoController:
    """tm"""

    def __init__(self, config: Config):
        self.config = config #stores the config object passed to the constructor
        self.serial_connection: Optional[serial.Serial] = None #initially no serial connection but later will be assigned a serial.Serial object
        self.logger  = logging.getLogger(__name__) #creates a logger object for this module

    def connect(self) -> bool:
        """Establishes a serial connection to the Arduino."""
        try: 
            self.serial_connection = serial.Serial( #establishes the serial connection that was before, None
                self.config.arduino_port, 
                self.config.baud_rate, 
                timeout=self.config.serial_timeout
            )
            time.sleep(2)  # wait for the connection to establish
            self.logger.info(f"Connected to Arduino on port {self.config.arduino_port}")
            return True
        except serial.SerialException as e:
            self.logger.error(f"Failed to connect to Arduino: {e}")
            return False

    def disconnect(self) -> None:
        """method used to close the serial connection"""
        if self.serial_connection and self.serial_connection.is_open:
            self.send_command('LED_OFF')  # Turn off LED before disconnecting
            time.sleep(0.5)
            self.serial_connection.close()
            self.logger.info("Disconnected from Arduino")
            """"If there's an open connection, turn off the LED, wait a moment, close the connection cleanly, and log that we disconnected."""

    def send_command(self, command: str) -> None:
        """Method is intended to send a command to the arduino through the serial connection through bytes."""
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.write(f'{command}\n'.encode()) #write method uses bytes and the encode method converts the string to bytes
                self.logger.debug(f"Sent command: {command}")
            except serial.SerialException as e:
                self.logger.error(f"Failed to send command '{command}': {e}")
    
    def readLine(self) -> Optional[str]: #Either none or a String 
        """
        Read a line from the serial port.
        Returns None if no data available or on error.
        """
        try:
            if self.serial_connection.in_waiting > 0: #checks if there is data available to read (data = 1)
                line = self.serial_connection.readline().decode('utf-8', errors='ignore').strip() # readline Method reads byte from the serial port until \n, decode method converts bytes into strings (if any bug just skip it), and strip method removes any extra whitespace from the beginning and end
                return line if line else None #if line has data return it, else return None, short end for if line else none,
        except serial.SerialException as e:
                self.logger.error(f"Failed to read from serial port: {e}")

        return None
    
# ============================================================================
# DATA PARSER
# ============================================================================

class SensorDataParser:
    pass
