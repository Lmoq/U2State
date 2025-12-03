import time


class Stime:
    # A time string class that can be represented as string or int, 
    # Scope : 7 days / 1 Week
    # Bounds
    beginning = "Mon 00:00:00"
    end = "Sun 23:59:59"

    # Seconds in a week
    max_seconds = 604800

    week_map_string = {
        "Mon" : 0,
        "Tue" : 1,
        "Wed" : 2,
        "Thu" : 3,
        "Fri" : 4,
        "Sat" : 5,
        "Sun" : 6
    }
    week_map_int = {
        0 : "Mon",
        1 : "Tue",
        2 : "Wed",
        3 : "Thu",
        4 : "Fri",
        5 : "Sat",
        6 : "Sun"
    }

    # init : str = "<Abreviated dayname> <24hour>:<minutes>:<seconds>"
    def __init__( self, init_data: str | int = None, default = True ):
        #self.str = timenow() if (default and not time_str) else time_str
        self.str = ""
        self.seconds = 0

        if init_data != None:
            match init_data:
                case str():
                    self.to_seconds( init_data )
                    self.str = init_data

                case int():
                    self.to_str( init_data )
                    self.seconds = init_data


    def to_seconds( self, string ):
        # Convert time string to seconds
        _str = string.split(' ')

        day = self.week_map_string.get( _str[0] )
        hour, mins, secs = _str[1].split(':')

        self.seconds = ( day * ( 3600 * 24 ) ) + \
               ( int(hour) * 3600 ) + \
               ( int(mins) * 60 ) + \
               ( int(secs) )


    def now( self ):
        # Update value to current time
        self.str = timenow()
        self.to_seconds( self.str )


    def to_str( self, _int ):
        # Convert seconds to time string
        day = (_int // ( 3600 * 24 )) % 7
        hour = (_int // 3600 ) % 24
        mins = (_int // 60 ) % 60
        secs = _int % 60

        day = self.week_map_int.get( day )
        self.str = f"{day} {hour:02d}:{mins:02d}:{secs:02d}"


    def __add__( self, _int ):
        if not isinstance( _int, int ):
            return None
        return Stime( (self.seconds + _int) % Stime.max_seconds )


    def __iadd__( self, _int ):
        if not isinstance( _int, int ):
            return None

        self.seconds = ( self.seconds + _int ) % Stime.max_seconds
        self.to_str( self.seconds )
        
        return self


    def __sub__( self, _int ):
        if not isinstance( _int, int ):
            return None
        return Stime( (self.seconds - _int) % Stime.max_seconds )

    
    def __isub__( self, _int ):
        if not isinstance( _int, int ):
            return None

        self.seconds = ( self.seconds - _int ) % Stime.max_seconds
        self.to_str( self.seconds )
        
        return self


    def __lt__( self, stime ):
        if isinstance( stime, Stime ):
            return self.seconds < stime.seconds

        elif isinstance( stime, str ):
            return self.seconds < Stime( stime ).seconds 

    
    def __gt__( self, stime ):
        if isinstance( stime, Stime ):
            return self.seconds > stime.seconds

        elif isinstance( stime, str ):
            return self.seconds > Stime( stime ).seconds

 
    def __le__( self, stime ):
        if isinstance( stime, Stime ):
            return self.seconds <= stime.seconds

        elif isinstance( stime, str ):
            return self.seconds <= Stime( stime ).seconds

    def __ge__( self, stime ):
        if isinstance( stime, Stime ):
            return self.seconds >= stime.seconds

        elif isinstance( stime, str ):
            return self.seconds >= Stime( stime ).seconds


    def __eq__( self, stime ):
        if isinstance( stime, Stime ):
            return self.seconds == stime.seconds

        elif isinstance( stime, str ):
            return self.seconds == Stime( stime ).seconds
    

    def __repr__( self ):
        if not self.str:
            self.to_str( self.seconds )
        return self.str


    def in_range( self, start, end ):
        # Verify object type
        if not isinstance( start, Stime ) and isinstance( start, str ):
            start = Stime( start )

        if not isinstance( end, Stime ) and isinstance( start, str ):
            end = Stime( end )


        if self >= start and self <= end:
            # Bounds doesn't wrap around
            return True

        elif start > end:
            # Comparison when end time wrapped around week limit
            if self >= start or self <= end:
                return True
        return False


def timenow() -> str:
    return time.strftime("%a %H:%M:%S")

def getHour() -> str:
    return time.strftime("%H:%M")

def getHourSec() -> str:
    return time.strftime("%H:%M:%S")

if __name__=='__main__':
    pass
