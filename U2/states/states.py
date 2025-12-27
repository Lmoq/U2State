from U2.states.state import Task_State
from U2.states.context import Session
from U2.debug import infoLog, debugLog, printLog


class Task_State_U2( Task_State ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def run( self, ctx ) -> Task_State:
        tfo = self.task_info

        uinfo = ctx.search_element( tfo.match_selector, tfo.match_selector_timeout )

        if uinfo is None:
            printLog( f"<<{self} element not found>> rerunning .." )

        printLog( f"Ui found { uinfo['text'] or uinfo['contentDescription'] }" )

        ctx.uinfo = uinfo
        self.callback( ctx )
        
        return self.next( ctx )


    def next( self, ctx ) -> Task_State:
        check = Check( desc = f"Check task for {self}" )

        check.current_state = self
        check.next_state = self.next_state

        return check


class Check( Task_State ):


    def __init__( self, desc = None ):
        self.desc: str = desc

        self.current_state: Task_State = None
        self.next_state: Task_State = None


    def run( self, ctx ) -> Task_State:
        tfo = self.current_state.task_info

        ui = ctx.search_element( tfo.check_selector, tfo.check_selector_timeout )
        
        if ui is None:
            infoLog( f"Check selector not found reverting to <<{self.current_state}>>" )
            return self.current_state

        elif ui == "FAILED":
            infoLog( f"Check error" )
            return self

        return self.next_state


class Click( Task_State_U2 ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )

    def callback( self, ctx ):
        ctx.clickUI()
        




