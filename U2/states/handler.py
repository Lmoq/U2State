from U2.states.context import Session
from U2.states.state import Task_State
from U2.debug import debugLog, infoLog, printLog


class Handler:

    sig_term = False
    multi_bot = False

    def __init__( self, context: Session = None ):
        self.ctx = context
        # This will be toggled off when multi_bot flag is True
        self.active = True

        self.current_state: Task_State = None
        self.previous_state: Task_State = None

        self.end_state: Task_State = None


    @staticmethod
    def chain_states( states_list: list[Task_State] = None, loop:bool = False ):
        last_index = len( states_list ) - 1
        assert last_index > -1, "States_list should not be empty"

        for i in range( last_index ):
            states_list[ i ].next_state = states_list[ i + 1 ]

        states_list[ last_index ].next_state = states_list[0] if loop else None


    def set_state( self, start: Task_State, end: Task_State ):
        self.current_state = start
        self.end_state = end


    def switch_state( self, next_state: Task_State ):
        if self.current_state is None:
            debugLog( f"Switch state : <<Current State>> is None" )

        self.previous_state = self.current_state
        self.current_state = next_state

        if not isinstance( self.current_state, Task_State ):
            debugLog( f"Current State is not Task_State: <<{str(type(self.current_state))}>> | Previous State : <<{self.previous_state}>>" )

        self.previous_state.exit( self.ctx )
        self.current_state.enter( self.ctx )


    def state_loop( self ):
        assert self.current_state != None, "State Handler current state should be set first"

        self.current_state.enter( self.ctx )
        while self.active:
            try:
                printLog(f"Running current state <<{self.current_state}>>")
                next_state = self.current_state.run( self.ctx )

                if next_state is None:
                    break
                elif next_state != self.current_state:
                    self.switch_state( next_state )

            except KeyboardInterrupt:
                type( self ).sig_term = True
                break
        printLog( "<<Exiting state loop>>" )
        self.current_state.exit( self.ctx )
        
