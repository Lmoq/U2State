import sys
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent.parent) )

from U2.base import U2_Device
from U2.enums import Wtype
from U2.states.state import Task_State
from U2.states.functions import default_match, click


class CheckUI( Task_State ):

    def __init__( self, **kwargs ):
        self.current_state = None
        self.next_state = None

        self.check_selector = {}
        super().__init__( **kwargs )


    def run( self, ctx ):
        super().run( ctx )

        tfo = self.current_state.task_info
        selector = tfo.check_selector

        u2 = ctx.u2_session
        print(f"[{self}] Checking uinfo : { selector }")

        ui = u2.waitElement( tfo.check_selector, tfo.check_selector_timeout )
        
        if ui == None:
            print(f"[{self}] : element not found..reverting to [{self.current_state}]")
            return self.current_state
        elif ui == "FAILED":
            return self

        print(f"Check succeed : {tfo.check_selector}" )
        return self.next_state 


class Task_State_U2( Task_State ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def enter( self, ctx ):
        super().enter( ctx )


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
        check_state.check_selector = tfo.check_selector or { "text" : tfo.match_selector['text'], "className" : Wtype.text.value }
        print( f"Check state for {self}" )
        return check_state


    def exit( self, ctx ):
        super().exit( ctx )



class ClickUI( Task_State_U2 ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


class SwipeUI( Task_State_U2 ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


# Set default callbacks
ClickUI.callback = click


