from U2.states import Click, Wait, Write, Swipe, Check
from U2.debug import printLog, infoLog, debugLog, snip_screen
from U2.task import Task_Info
from U2.enums import Wtype, Direction
from U2.time import Stime, timenow
from U2.adb_tools import adbSwipeUi
from alg import get_answer_regex
import time


screen = {
    'top' : 0,
    'left' : 0,
    'bottom' : 1612,
    'right' : 720
}

class Question( Wait ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def run( self, ctx ):
        tfo = self.task_info
        ctx.restart_timer.track_interval( delete_buffer_pos = 1 )

        # Scheduled restart so app ram usage reset
        if ctx.restart_timer > ctx.restart_time:
            snip_screen( name = "restart", unique = True )
            ctx.restartTarget( ctx.tab_instance_number )

            ctx.restart_timer.reset()
            log = f"Scheduled restart {Stime()}"
            printLog( log )
            infoLog( log )

        uinfo = ctx.search_sibling_element( tfo.emoji_button, tfo.match_selector, tfo.match_selector_timeout )
        if uinfo is None:
            infoLog( f"    <<Question not found>>" )

            printLog( f"Retries : { ctx.retries }" )
            ctx.retries += 1

            if ctx.retries > 1:
                ctx.restartTarget( ctx.tab_instance_number )
                log = f"Exceeded number of retries, restarting .. {Stime()}"

                infoLog( log )
                debugLog( log  )
                printLog( log )
                # ctx.retries = 0
            else:
                in_target_app = ctx.device.wait_activity( ctx.launch_activity.split('/')[1], timeout=1 )

                if in_target_app:
                    adbSwipeUi( screen, Direction.up, 500 )

            ctx.failed_cycle = True
            return self

        ctx.cycle_timer.track_interval()

        if not ctx.failed_cycle and ctx.cycle_timer.track_calls > 0 and ctx.cycle_timer < 25:
            # Handle sudden reappearance of target ui to prevent spam
            log = f"Sudden reappearance of target ui {timenow()}"
           
            infoLog( log )
            debugLog( log )
            printLog( log )

            snip_screen( name = "sudden", unique = True )

            ctx.restartTarget( ctx.tab_instance_number )
            ctx.cycle_timer.reset()

            ctx.debug_snip = True
            return self

        ctx.uinfo = uinfo
        ctx.retries = 0

        infoLog( f"Question : {ctx.uinfo['text']}" )
        answer = self.callback( ctx )

        return self.next( ctx ) if answer else self


    def callback( self, ctx ):
        question = ctx.uinfo["text"]
        answer = get_answer_regex( question )

        if not answer:
            log = f"    <<Failed to get answer>>"
            debugLog( log )
            infoLog( log )

            ctx.failed_cycle = True
            return False

        ctx.write_text = answer
        ctx.failed_cycle = False

        return True



class Write( Write ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )

        self.task_info = Task_Info()
        self.desc = "Write Text"


    def callback( self, ctx ):
        super().callback( ctx )
        self.task_info.check_selector = { "text" : ctx.write_text, "className" : Wtype.editText.value }


    def next( self, ctx ):
        check = MSCheck( desc = f"Check task for {self}" )

        check.current_state = self
        check.next_state = self.next_state

        return check


class ClickSend( Click ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )

        self.task_info = Task_Info( match_selector = { "description" : "Send" } )
        self.desc = "Click Send Button"


    def callback( self, ctx ):
        super().callback( ctx )
        self.task_info.check_selector = { "text" : ctx.write_text, "className" : Wtype.text.value }

        
    def next( self, ctx ):
        check = MSCheck( desc = f"Check task for {self}" )

        check.current_state = self
        check.next_state = self.next_state

        return check


class MSCheck( Check ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def run( self, ctx ):
        tfo = self.current_state.task_info
        ui = ctx.waitElement( tfo.check_selector, tfo.check_selector_timeout )
        
        if ui is None:
            infoLog( f"    <<Check selector>> not found reverting to <<{self.current_state}>>" )
            snip_screen( name = self.desc, unique = True )
            return self.current_state

        elif ui == "FAILED":
            infoLog( f"Check error" )
            return self

        # Temporary snip debugging
        if ctx.debug_snip:
            if self.desc == "Check task for Write Text":
                snip_screen( name = "write_sudden", unique = True )

            if self.desc == "Check task for Click Send Button":
                snip_screen( name = "send_sudden", unique = True )
                ctx.debug_snip = False


        if self.current_state == ctx.end_state and ctx.cycle_timer.average > ctx.expected_time_avg:
            log = f"Interval exceeded { ctx.cycle_timer.average } expected_time {ctx.expected_time_avg} track_calls { ctx.cycle_timer.track_calls }"

            infoLog( log )
            debugLog( log )

            ctx.restartTarget( ctx.tab_instance_number )
            ctx.cycle_timer.reset()
            
        infoLog( f"Check selector found" )
        return self.next_state


states_list = [
    Question(
        task_info = Task_Info(
            match_selector = { 'textContains' : '\nIdentify the color of' },
            emoji_button = { 'description' : 'Add custom reaction', 'className' : Wtype.button.value },
            match_selector_timeout = 35
        ),
        desc = "Wait Question"
    ),
    Click( task_info = Task_Info
        (
        match_selector = { "textContains" : "essage" },
        match_alt_selector = { "className" : Wtype.editText.value },
        
        match_selector_timeout = 1,
        class_name_delimiter = [ Wtype.editText.value, Wtype.button.value ],
        check_selector = { "className" : Wtype.editText.value }
        ),
        desc = "Click Edit Text"
    ),
    Write(
        task_info = Task_Info(),
        desc = "Write Text"
    ),
    ClickSend(
        task_info = Task_Info( match_selector = { "description" : "Send" } ),
        desc = "Click Send Button"
    )
]

