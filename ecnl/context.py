from U2.Bots.msbot import MSBot
from U2.states import Task_State
try:
    from .states import Question
except:
    from states import Question


class CTX( MSBot ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )

    
    def get_current_state_wait_time( self, state: Task_State = None ) -> int:
        match state:
            case Question():
                print("type:Question")
                return 33
        
