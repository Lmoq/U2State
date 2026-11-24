import cv2 as cv
from U2.Bots.msbot import MSBot
from U2.states import Task_State
from U2.process import system_type
from U2.time import Stime
from U2.debug import infoLog, debugLog, printLog
try:
    from .states import Question
except:
    from states import Question


class CTX( MSBot ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )
        self.name = "🌜ECNL🌜"

        self.tab_instance_number = 1
        self.points_increment = 1

        self.cycle_timer.avg_of_n = 0
        self.restart_time = 1800
        self.expected_time_avg = 33

        self.failed_cycle = False
        self.debug_snip = False
        self.snip_send = True

        self.retries = 0

        self.restricted_ui = { "textContains" : "Couldn't send" }
        self.question_ui = ""

        self.start_time_restriction = Stime("Wed 10:26:30")
        self.end_time_restriction = Stime("Wed 10:27:45")

    
    def get_current_state_wait_time( self, state: Task_State = None ) -> int:
        match state:
            case Question():
                #print("type:Question")
                return 33


    def saveData( self ):
        infoLog( f"[{self}] Attempting snip data save[snip_send:{'True' if self.snip_send else 'False'}] [snip_data:{'Exists' if self.snip_data is not None else 'None'}]")
        if system_type in ["Linux","Android"] and self.snip_send and self.snip_data is not None:
            dst, image = self.snip_data
            cv.imwrite( dst, image )
            infoLog( f"[{self}] Saved previous buffer to : {dst}" )

        
