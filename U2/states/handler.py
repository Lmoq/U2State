from U2.states.states import Task_State_U2
from U2.states.context import Session
from U2.states.state import Task_State
from U2.debug import debugLog, infoLog, printLog, Logger
from U2.time import Stime


class Handler:

    sig_term = False
    multi_bot = False

    def __init__( self, context: Session = None ):
        assert context is not None, "Required setting context inside init method first"

        self.ctx = context
        # This will be toggled off occasionally if multi_bot flag is True
        self.active = True

        self.current_state: Task_State = None
        self.previous_state: Task_State = None

        self.end_state: Task_State = None
        self.states_list: list = None


    @staticmethod
    def chain_states( states_list: list[Task_State] = None, loop:bool = False ):
        last_index = len( states_list ) - 1
        assert last_index > -1, "States_list should not be empty"

        for i in range( last_index ):
            states_list[ i ].next_state = states_list[ i + 1 ]

        states_list[ last_index ].next_state = states_list[0] if loop else None


    def set_state( self, start: Task_State, end:list[Task_State], states_list ):
        print( f"Setting {self.ctx} states type : {type(end)}" ) 
        self.current_state = start
        self.end_states = end

        self.ctx.end_states = end
        self.states_list = states_list


    def switch_state( self, next_state: Task_State ):
        if self.current_state is None:
            debugLog( f"Switch state : <<Current State>> is None" )

        self.previous_state = self.current_state
        self.current_state = next_state

        if not isinstance( self.current_state, Task_State ):
            debugLog( f"Current State is not Task_State: <<{str(type(self.current_state))}>> | Previous State : <<{self.previous_state}>>" )

        self.previous_state.exit( self.ctx )
        self.current_state.enter( self.ctx )

        if isinstance( self.current_state, Task_State_U2 ):
            self.ctx.state_index = self.states_list.index( self.current_state )
            # print( f"Current State Index : [{self.ctx.state_index}]" )


    def state_loop( self ):
        assert Logger._init is not False, "Logger class should be initialized before running state loop"
        assert self.current_state != None, "State Handler current state should be set first"

        self.current_state.enter( self.ctx )
        while self.ctx.active and not type( self ).sig_term:
            try:
                next_state = self.current_state.run( self.ctx )

                if next_state is None:
                    break
                elif next_state != self.current_state:
                    self.switch_state( next_state )

            except KeyboardInterrupt:
                type( self ).sig_term = True
                break

        #printLog( f"<<Exiting state loop>> {Stime()}" )
        self.current_state.exit( self.ctx )

        if type( self ).sig_term:
            print( f"[{self.ctx}] snip_send[{self.ctx.snip_send}] snip_data[{'True' if self.ctx.snip_data else 'False'}]" )
            self.ctx.saveData()
