from U2.states import Session
from U2.time import TimeTracker, Stime
from U2.process import system_type

from U2.adb_tools import adbClick, exec_
from U2.debug import get_elements
from U2.enums import Wtype

import time


class MSBot( Session ):


    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.tab_instance_number = 0

        self.restart_timer = TimeTracker()
        self.task_timer = TimeTracker()

        self.cycle_timer = TimeTracker( min_interval = 0 )
        self.cycle_timer.avg_of_n = 5

        self.expected_time_avg = 0

        self.points_limit = 0
        self.points = 0

        self.restart_time = 1800


    def intervalTimeExceed( self, elapsed:int, limit:int ):
        if elapsed > limit:
            return True
        return False


    def pointsReachedLimit( self ):
        if self.points_limit and self.points > self.points_limit:
            return True
        return False


    def get_msg_tab( self, instance: int, elements: dict ) -> dict:
        msg_tabs = []

        width_min = 718
        height_min = 142

        for v in elements.values():
            width = v['right'] - v['left']
            height = v['bottom'] - v['top']

            if width >= width_min and height >= height_min:
                msg_tabs.append( v )

        return msg_tabs[ instance - 1 ] if msg_tabs else None


    def timeRestricted( self ):
        # Checks if runs at valid time
        if ( not self.start_time_restriction or not self.end_time_restriction ):
            return False
        stime = Stime()

        return stime.in_range( self.start_time_restriction, self.end_time_restriction )


    def restartTarget( self, tab_instance_number:int = 0 ):
        assert tab_instance_number > 0, "Instance number should be provided"

        # Restart target package
        stop_cm = f"am force-stop {self.target_package}"
        start_cm = f"am start -n {self.launch_activity}"

        if system_type == "Windows":
            exec_( stop_cm )
            time.sleep( 0.3 )
            exec_( start_cm )

            print( f"Restarting with Windows" )

        elif system_type == "Linux":
            exec_( f"adb shell { stop_cm }", pipe = False )
            time.sleep( 0.3 )
            exec_( f"adb shell { start_cm }", pipe = False )

            print( f"Restarting with Linux" )

        self.device.wait_activity( self.launch_activity.split('/')[1] )
        elements = get_elements( self, 10 , Wtype.button, capture_output = True )

        bounds = self.get_msg_tab( tab_instance_number, elements )
        adbClick( bounds )

