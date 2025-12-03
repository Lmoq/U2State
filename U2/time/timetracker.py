import time


class Time:


    def __init__( self ):
        self.str = "00:00"
        self.seconds = 0


    def set_seconds( self, n : int ):
        if not isinstance( n, int ):
            self.str = "Error"
            return
        self.seconds = n

        # Convert int to time string
        hour = ( n // 3600 ) % 24
        mins = ( n // 60 ) % 60
        secs = ( n % 60 )

        _str = ""
        _str += f"{hour:02d}:" if hour else ""
        _str += f"{mins:02d}:{secs:02d}"
        self.str = _str


    def set_string( self, s : str ):
        if not isinstance( s, str ):
            self.seconds = 0
            self.str = "Error"
            return
        self.str = s

        # Convert time string to seconds
        _split = s.split( ':' )

        hour = int( _split[0] ) * 3600 if len( _split ) > 2 else 0
        mins = int( _split[-2] ) * 60
        secs = int( _split[-1] )

        self.seconds = hour + mins + secs


    def __repr__( self ):
        if self.str == "00:00" and self.seconds:
            self.set_seconds( self.seconds )
        return self.str


    def __lt__( self, n ):
        if isinstance( n, int ):
            return self.seconds < n
        elif isinstance( n, Time ):
            return self.seconds < n.seconds

        raise NotImplementedError


    def __gt__( self, n ):
        if isinstance( n, int ):
            return self.seconds > n
        elif isinstance( n, Time ):
            return self.seconds > n.seconds

        raise NotImplementedError


    def __le__( self, n ):
        if isinstance( n, int ):
            return self.seconds <= n
        elif isinstance( n, Time ):
            return self.seconds <= n.seconds

        raise NotImplementedError


    def __ge__( self, n ):
        if isinstance( n, int ):
            return self.seconds >= n
        elif isinstance( n, Time ):
            return self.seconds >= n.seconds

        raise NotImplementedError


class TimeTracker( Time ):


    def __init__( self, min_interval = 0 ):
        # Buffer list for calculation of time intervals
        self.interval_buffer = []

        # Tracks of intervals
        self.interval_list = []
        self.sum_of_intervals = 0
        self.track_calls = 0

        # Minimum interval required to track interval for calculating average
        self.min_interval = min_interval
        self.avg_of_n = 0
        self.average = Time()


    def track_interval( self ):
        # Used for tracking short interval of one or more series of process
        buffer = self.interval_buffer
        buffer.append( time.time() )

        if len( buffer ) > 1:
            interval = int( buffer[1] - buffer[0] )

            # Verify, track and calculate average of interval 
            # while using a minimum threshold to filter out faulty ones
            threshold = self.min_interval

            if interval > threshold:
                self.track_calls += 1

                self.sum_of_intervals += interval
                self.interval_list.append( interval )

                avg = self.get_avg_of_n( self.avg_of_n ) or self.get_total_avg()
                self.average.set_seconds( avg )

            self.set_seconds( interval )
            del buffer[0]


    def get_total_avg( self ) -> int:
        # Calculate total average and keeps the record or list piled up until reset
        if self.track_calls:
            self.average.set_seconds( self.sum_of_intervals // self.track_calls )


    def get_avg_of_n( self, aoN, cap: bool = True ) -> int:
        # Calculate average of N
        # Set cap to false if keeping the interval list after calling this function 
        # to get total interval average is still desired
        if aoN and self.track_calls >= aoN:
            avg = sum( self.interval_list[-aoN:] ) // aoN
            if cap: 
                del self.interval_list[0]
            self.average.set_seconds( avg )


    def reset( self ):
        # Reset interval
        self.interval_buffer.clear()
        self.interval_list.clear()

        self.sum_of_intervals = 0
        self.track_calls = 0
        
        self.average.set_seconds( 0 )


    def __lt__( self, n ):
        if self.track_calls:
            return super().__lt__( n )
        return False


    def __gt__( self, n ):
        if self.track_calls:
            return super().__gt__( n )
        return False


    def __le__( self, n ):
        if self.track_calls:
            return super().__le__( n )
        return False


    def __ge__( self, n ):
        if self.track_calls:
            return super().__ge__( n )
        return False
