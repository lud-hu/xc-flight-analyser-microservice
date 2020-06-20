import os
import sys
from datetime import datetime
from xcsoar import Flight
from pprint import pprint

def analyse(file):
    # Create Flight object
    flight = Flight(file)

    # Prepare start and end dates
    # Since XCSoar is not recognizing take offs for
    # paragliding flights properly, use a wide date
    # range in order to analyse the whole log file.
    start_date = datetime(1970, 1, 1)
    end_date = datetime(2100, 1, 1)

    # Analyse flight
    result = flight.analyse(
        start_date, start_date,
        end_date, end_date
    )

    # Return analysed data
    return result