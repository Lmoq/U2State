from U2.states.state import Task_State
from U2.states.context import Session
from U2.debug import infoLog, debugLog, printLog


class Task_State_U2( Task_State ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def run( self, ctx ) -> Task_State:
        tfo = self.task_info
        uinfo = ctx.search_element( tfo.match_selector, tfo.match_selector_timeout )
        
        if uinfo is None and tfo.match_alt_selector:
            infoLog( f"    <<{self}>> element not found .. using alt selector instead .." )
            
            uinfo = ctx.search_element( tfo.match_alt_selector, tfo.match_selector_timeout )
            if uinfo is None: infoLog( "    <<{self}>> alt selector not found .." )

        if uinfo is None:
            infoLog( f"    <<{self}>> element not found rerunning .." )
            return self

        if not not tfo.class_name_delimiter:
            uinfo = ctx.search_qualified_class_names( uinfo, tfo )
            
            if not uinfo:
                infoLog( f"    <<{self}>> specified className not found" )
                return self

        infoLog( f"Ui found ({ repr(uinfo['text'] or uinfo['contentDescription']) })" )

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
        ui = ctx.waitElement( tfo.check_selector, tfo.check_selector_timeout )
        
        if ui is None:
            infoLog( f"    <<Check selector>> not found reverting to <<{self.current_state}>>" )
            return self.current_state

        elif ui == "FAILED":
            infoLog( f"Check error" )
            return self

        infoLog( f"Check selector found" )
        return self.next_state


class Click( Task_State_U2 ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )

    def callback( self, ctx ):
        ctx.clickUI()
        

class PressKey( Task_State_U2 ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )

    def run( self, ctx ):
        self.callback( ctx )
        return self.next( ctx )

    def callback( self, ctx ):
        ctx.pressKey( self.task_info.key )


class Wait( Task_State_U2 ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )

    def next( self, ctx ):
        return self.next_state


class Swipe( Task_State_U2 ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )

    def callback( self, ctx ):
        tfo = self.task_info
        ctx.swipeUI( tfo.swipe_direction, tfo.swipe_points, tfo.swipe_duration )
        

class Write( Task_State_U2 ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )

    def run( self, ctx ):
        self.callback( ctx )
        return self.next( ctx )

    def callback( self, ctx ):
        ctx.writeText()



