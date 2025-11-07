
import sys, time#, traceback
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent) )

from U2.base import U2_Device
#from U2.enums import TaskType, Wtype
#from U2.states import Task_State
#from U2.debug import debugLog
#from U2.process import start_adb_shell_pipes


class Task_State:


    def __init__( self, ctx: U2_Device = None, **kwargs ):
        self.ctx = ctx

        for k,v in kwargs.items():
            setattr( self, k, v )

    def enter( self ):
        print( f"{self} state enter" )
        pass

    def run( self ):
        print( f"{self} state run" )
        pass

    def exit( self ):
        print( f"{self} state exit" )
        pass

    def __repr__( self ):
        return str( self.__class__ ).split(".")[-1][:-2]


class Task_Handler:


    def __init__( self ):
        self.states_stack : list = []

        self.current_state: Task_State = None
        self.previous_state: Task_State = None

        self.check_selector = {}
        pass


    def set_state( self, state: Task_State ):
        self.current_state = state


    def switch_state( self, next_state: Task_State ):
        log = f"Transitioning to [{next_state}]"
        print(log)

        # Terminate current running state
        self.current_state.exit()
        
        # Transition to next state
        next_state.enter()

        # Update handler
        self.previous_state = self.current_state
        self.current_state = next_state


    def run_current_state( self ):
        # Get current task state
        self.current_state.run()
        pass
