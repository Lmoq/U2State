
import sys, time#, traceback
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent.parent) )

from U2.base import U2_Device
from U2.task import Task_Info
#from U2.enums import TaskType, Wtype
#from U2.states import Task_State
#from U2.debug import debugLog
#from U2.process import start_adb_shell_pipes


class Task_Context:

    def __init__( self ):
        self.u2_session: U2_Device = None
        self.uinfo: dict = None

        self.current_task_state: str = None
        self.restricted = False

        self.start_time_restriction: str = None
        self.end_time_restriction: str = None


class Task_State:


    def __init__( self, **kwargs ):
        self.next_state: Task_State
        self.task_info: Task_Info

        for k,v in kwargs.items():
            setattr( self, k, v )
        
        assert self.task_info != None

    def enter( self, ctx ):
        print( f"{self} state enter" )
        pass

    def run( self, ctx ):
        print( f"{self} state run" )
        pass

    def next( self, ctx ):
        print( f"{self} state next" )
        pass

    def exit( self, ctx ):
        print( f"{self} state exit" )
        pass

    def __repr__( self ):
        return str( self.__class__ ).split(".")[-1][:-2]


class Task_Handler:

    sig_term = False
    multi_bot = False

    def __init__( self ):
        self.ctx = None
        self.active = True

        self.current_state: Task_State = None
        self.previous_state: Task_State = None

        self.end_state: Task_State = None

        self.check_selector = {}
        pass


    def set_state( self, start: Task_State, end: Task_State ):
        self.current_state = start
        self.end_state = end


    @staticmethod
    def chain_states( states_list: list[Task_State] = None, loop:bool = False ):
        last_index = len( states_list ) - 1
        
        for i in range( last_index ):
            states_list[ i ].next_state = states_list[ i + 1 ]

        states_list[ last_index ].next_state = states_list[0] if loop else None


    def switch_state( self, next_state: Task_State ):
        log = f"\nTrasitioning to [{next_state}]\n"
        print(log)

        # Terminate current running state
        self.current_state.exit( self.ctx )
        
        # Transition to next state
        next_state.enter( self.ctx )

        # Update handler
        self.previous_state = self.current_state
        self.current_state = next_state

    
    def state_loop( self ):
        assert self.current_state != None, "State Handler current state should be set first"

        while self.active:
            try:
                next_state = self.current_state.run( self.ctx )

                if next_state == None:
                    break
                if next_state != self.current_state:
                    self.switch_state( next_state )
            except KeyboardInterrupt:
                Task_Handler.sig_term = True
                break



