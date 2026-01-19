import serial
import time
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass
import json

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

    def setup_logging(log_file: str = 'app.log') -> None:
        """ the method is to set up the logging system to print out the data onto a file and also the terminal?"""
        logging.basicConfig(level = logging.INFO, 
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file), logging.StreamHandler()] ) #sets the logging level to INFO (5 Levels: DEBUG, INFO, WARNING, ERORR, CRITICAL) -> Saying: "Show me INFO messages and everything MORE important than INFO" , logging provides all the values automatically
        """Logging.basicConfig sets up the logging system with the settings you specify. 
        You only call this once at the start of your program. """
        
@dataclass
class SensorReading:
    pass

