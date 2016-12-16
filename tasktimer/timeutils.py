from datetime import datetime, timedelta

def timedelta2hourmin_string(td): 
    return ("{}:{:02d}".format(
            24 * td.days + td.seconds // 3600, 
            (td.seconds % 3600 ) // 60)
            )
    
def timedelta2hour_float(td):
    return (24.0 * td.days + td.seconds / 3600.0)

def hour_string2time_delta(hour_string): 
    hour_int = float(hour_string)
    td = timedelta(hours = hour_int)
    return td


