import cv2 as cv
from U2.Bots.msbot import MSBot
from U2.states import Task_State
from U2.process import system_type
from U2.debug import infoLog, debugLog, printLog
try:
    from .states import ClickAnswer, ClickNext, VerifyAnswer, Question
except:
    from states import ClickAnswer, ClickNext, VerifyAnswer, Question


class CTX( MSBot ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )
        self.name = "🌟LECB🌟"

        self.tab_instance_number = 2
        self.points_increment = 2

        self.cycle_timer.avg_of_n = 0
        self.restart_time = 1800
        self.expected_time_avg = ( 15 * 60 ) * 2 

        self.failed_cycle = False
        self.debug_snip = False
        self.snip_send = True

        self.retries = 0

        self.failed_cycle = False
        self.debug_snip = False

        self.snip_send = False
        self.restricted_ui = { "textContains" : "Couldn't send" }
        self.question_ui = ""


    def get_current_state_wait_time( self, state: Task_State = None ) -> int:
        match state:
            case Question():
                return ( 12 * 60 ) + 25
            case VerifyAnswer():
                return ( 12 * 60 ) + 31


    def saveData( self ):
        if system_type == "Linux" and self.snip_send and self.snip_data is not None:
            dst, image = self.snip_data
            cv.imwrite( dst, image )
            print( f"Saved previous buffer to : {dst}" )
