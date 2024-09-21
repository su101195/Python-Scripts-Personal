from datetime import datetime, timedelta
def gpsWeek_seconds_to_datetime(gpsweek, seconds):
    gpsweek = int(gpsweek)
    seconds = float(seconds)
    # Number of seconds that have passed since the start of the GPS epoch
    gps_epoch = datetime(1980, 1, 6, 0, 0, 0)
    elapsed_seconds = gpsweek * 7 * 24 * 60 * 60 + seconds
    # Convert to timedelta
    elapsed_seconds -= 18
    delta = timedelta(seconds=elapsed_seconds)
    # Add timedelta to the start of the GPS epoch
    return str(gps_epoch + delta)