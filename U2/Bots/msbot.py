import time
from pathlib import Path

from U2.states import Session, Check, Handler, Task_State
from U2.time import TimeTracker, Stime

from U2.process import system_type
from U2.adb_tools import adbClick, exec_

from U2.debug import get_elements, infoLog, debugLog, printLog, snip_screen
from U2.enums import Wtype



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
        self.points_increment = 0
        self.restart_time = 1800

        self.snip_data: tuple[ Path:"image data" ] = None


    def intervalExceed( self ) -> bool:
        limit = self.expected_time_avg
        if limit and self.cycle_timer.average > limit:
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


    def restartPackage( self ):
        # Restart target package
        stop_cm = f"am force-stop {self.target_package}"
        start_cm = f"am start -n {self.launch_activity}"

        linux_pipe = False if system_type == "Linux" else None

        exec_( stop_cm, pipe = linux_pipe )
        time.sleep( 0.3 )
        exec_( start_cm, pipe = linux_pipe )


    def restartTarget( self, tab_instance_number:int = 0, include_click = True ):
        assert tab_instance_number > 0, "Instance number should be provided"

        self.restartPackage()
        self.device.wait_activity( self.launch_activity.split('/')[1] )

        if not include_click:
            return

        elements = get_elements( self, 10 , Wtype.button, capture_output = True, timeout = 4 )

        if not elements:
            Handler.sig_term = True
            log = f"Failed to restart"

            infoLog( log )
            debugLog( log )
            printLog( log )
            return

        bounds = self.get_msg_tab( tab_instance_number, elements )
        adbClick( bounds )


    def get_current_state_wait_time( self, state: Task_State = None  ) -> int:
        raise NotImplementedError



class MSCheck( Check ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def run( self, ctx ):
        tfo = self.current_state.task_info
        ui = ctx.waitElement( tfo.check_selector, tfo.check_selector_timeout )

        if ui is None:
            infoLog( f"    <<Check selector>> not found reverting to <<{self.current_state}>>" )
            snip_screen( name = self.desc, unique = True )

            # state_type = f""
            # desc = f""
            
            # if self.root_state:
                # state_type = "Root State"

                # desc = str( self.root_state )
                # log = f"Reverting to : {state_type} | desc : {desc}"

                # printLog( f"{log}" )
            # else:
                # state_type = "Current State"
                # desc = str( self.current_state )

                # log = f"Reverting to : {state_type} | desc : {desc}"
                # printLog( f"{log}" )

            return self.root_state or self.current_state

        elif ui == "FAILED":
            infoLog( f"Check error" )
            return self

        infoLog( f"Check selector found" )
        ctx.uiObject = ui

        # Additional calls in middle of run()
        self.callback( ctx )

        if self.current_state == ctx.end_state:
            ctx.points += ctx.points_increment

            if Handler.multi_bot:
                ctx.active = False
                return self.next_state

            if ctx.intervalExceed():
                log = f"ET exceeded:{ ctx.cycle_timer } ET:{ctx.expected_time_avg} trackcalls:{ctx.cycle_timer.track_calls}"

                infoLog( log )
                debugLog( log )

                ctx.restartTarget( ctx.tab_instance_number )
                ctx.cycle_timer.reset()

        return self.next_state
