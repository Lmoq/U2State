from U2.base import U2_Device
from U2.enums import Wtype

from U2.states.state import Task_State, Task_Handler
from U2.states.functions import default_match, click, swipe, write


class CheckUI( Task_State ):


    def __init__( self, **kwargs ):
        self.current_state = None
        self.next_state = None

        self.check_selector = {}
        super().__init__( **kwargs )


    def run( self, ctx ):
        super().run( ctx )

        tfo = self.current_state.task_info
        selector = self.check_selector

        u2 = ctx.u2_session
        print(f"[{self}] Checking uinfo : { selector }")

        ui = u2.waitElement( self.check_selector, tfo.check_selector_timeout )
        
        if ui == None:
            print(f"[{self}] : element not found..reverting to [{self.current_state}]")
            return self.current_state
        elif ui == "FAILED":
            return self

        if Task_Handler.multi_bot:
            Task_Handler.sig_term = True
            
        return self.next_state 


class Task_State_U2( Task_State ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def callback( self, ctx ):
        pass


    def run( self, ctx ):
        super().run( ctx )
        tfo = self.task_info

        uinfo = default_match( self, ctx.u2_session, tfo.match_selector, tfo.match_selector_timeout )
        
        if not uinfo:
            print(f"[{self}] : element not found, rerunning...")
            return self

        print(f"[{self}] parsing uinfo : { uinfo['text'] or uinfo['contentDescription'] }")

        ctx.uinfo = uinfo
        self.callback( ctx )

        return self.next( ctx )


    def next( self, ctx ):
        check_state = CheckUI()

        check_state.current_state = self
        check_state.next_state = self.next_state

        tfo = self.task_info
        check_state.check_selector = tfo.check_selector
        print( f"Check state for {self}" )
        return check_state


class ClickUI( Task_State_U2 ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


class SwipeUI( Task_State_U2 ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


class WaitUI( Task_State_U2 ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )

    def next( self, ctx ):
        return self.next_state


class WriteUI( Task_State_U2 ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )

    def run( self, ctx ):
        self.callback( ctx )
        return self.next( ctx )


ClickUI.callback = click
SwipeUI.callback = swipe
WriteUI.callback = write
