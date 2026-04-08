import cv2 as cv, time
from U2.Bots.msbot import MSCheck
from U2.states import Handler, Click, Wait, Write, Swipe, Check
from U2.task import Task_Info

from U2.debug import printLog, infoLog, debugLog, snip_screen
from U2.adb_tools import adbSwipeUi, vibrate
from U2.notif import NotifLog

from U2.process import system_type
from U2.enums import Wtype, Direction
from U2.time import Stime, timenow

try:
    from .alg import get_answer_regex, get_points
except:
    from alg import get_answer_regex, get_points


class Question( Wait ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def run( self, ctx ):
        tfo = self.task_info
        ctx.restart_timer.track_interval( delete_buffer_pos = 1 )

        # Scheduled restart so app ram usage reset
        if ctx.restart_timer > ctx.restart_time:
            ctx.restartTarget( ctx.tab_instance_number )

            ctx.restart_timer.reset()
            # printLog( f"Scheduled restart {Stime()}" )

        ctx.setPointsData( ctx.points )

        timeout = 3
        timeout = tfo.match_selector_timeout if ctx.retries < 1 else 3
        time_wait = ctx.next_time_wait

        if time_wait:
            current_time = time.time()
            timeout = ( ctx.next_time_wait - current_time ) if time_wait > current_time else 3

        # print( f"[{ctx}] Searching Question timeout : {timeout}" )

        # Main selector search
        uinfo = ctx.search_sibling_element( tfo.emoji_button, tfo.match_selector, timeout )
        if uinfo is None:
            infoLog( f"[{ctx}]    <<Question not found>>" )

            ctx.retries += 1
            printLog( f"[{ctx}] Retries : { ctx.retries }" )

            if ctx.retries > 2:
                sign = ctx.search_element( ctx.restricted_ui, 3 )
                if sign is None:
                    return self
                else:
                    Handler.sig_term = True
                    log = f"[{ctx}] Restriction ui found"
                    
                    infoLog( log )
                    debugLog( log )

            elif ctx.retries > 1:
                ctx.restartTarget( ctx.tab_instance_number )
            else:
                in_target_app = ctx.device.wait_activity( ctx.launch_activity.split('/')[1], timeout=1 )

                if in_target_app:
                    adbSwipeUi( ctx.screen_dimension, Direction.up, 500 )
                    print( f"[{ctx}] Swiping retries:{ctx.retries}" )

            ctx.failed_cycle = True
            return self

        ctx.cycle_timer.track_interval()
        ctx.task_timer.track_interval()

        if ( not ctx.failed_cycle and ctx.cycle_timer.track_calls > 0 and ctx.cycle_timer < 25 ) or uinfo['text'] == ctx.question_ui:
            # Handle sudden reappearance of target ui to prevent spam
            snip_screen( name = "sudden", unique = True )
            log = f"[{ctx}] Reappearance of target ui {timenow()}"

            infoLog( log )
            debugLog( log )
            printLog( log )

            NotifLog.snip_sudden += 1

            # Save previous check image data
            ctx.saveData()

            ctx.restartTarget( ctx.tab_instance_number )
            ctx.cycle_timer.reset()

            ctx.debug_snip = True
            ctx.question_ui = "N/A"
            return self

        ctx.uinfo = uinfo
        infoLog( f"[{ctx}] Question : {ctx.uinfo['text']}" )
        answered = self.callback( ctx )


        # Check if local db is synced with latest info
        p_uinfo = ctx.search_element( {"textContains" : f"Bot Income:"}, tfo.ps_timeout )
        if p_uinfo is None:
            log = f"[{ctx}]    <<Pinfo not found>> {Stime()}"

            printLog( log )
            infoLog( log )

            snip_screen( name = "pinfo", unique = True )
            vibrate( 2, 1 )
        else:
            prev_points = int( get_points( p_uinfo["text"] ) )

            log = f"[{ctx}] Local : {ctx.points} Pinfo : {prev_points}"
            infoLog( log )

            if prev_points != ctx.points:
                vibrate( 0.5, 2 )

                recent = Stime()
                log = f"[{ctx}] Db[{ctx.points}] P[{prev_points}] {recent}"

                printLog( log )
                infoLog( log )
                debugLog( log )

                ctx.points = prev_points

        return self.next( ctx ) if answered else self


    def callback( self, ctx ):
        question = ctx.uinfo["text"]
        answer = get_answer_regex( question )

        if not answer:
            debugLog( f"    <<Failed to get answer>>" )
            ctx.failed_cycle = True
            return False

        ctx.write_text = answer
        ctx.failed_cycle = False

        ctx.question_ui = question
        ctx.retries = 0

        return True


class ClickEdit( Click ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def next( self, ctx ):
        check = ECCheck( desc = f"Check task for {self}" )

        check.current_state = self
        check.next_state = self.next_state
        check.root_state = self.root_state

        return check


class Write( Write ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )

        self.task_info = Task_Info()
        self.desc = "Write Text"


    def callback( self, ctx ):
        super().callback( ctx )
        self.task_info.check_selector = { "text" : ctx.write_text, "className" : Wtype.editText.value }


    def next( self, ctx ):
        check = ECCheck( desc = f"Check task for {self}" )

        check.current_state = self
        check.next_state = self.next_state
        check.root_state = self.root_state

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
        check = ECCheck( desc = f"Check task for {self}" )

        check.current_state = self
        check.next_state = self.next_state
        check.root_state = self.root_state

        return check


class ECCheck( MSCheck ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def callback( self, ctx ):
        # Temporary snip debugging
        if ctx.debug_snip:
            printLog( f"Follow up snip : {ctx.debug_snip} desc : {self.desc} {Stime()}" )

            if self.desc == "Check task for Write Text":
                snip_screen( name = "write_sudden", unique = True )

            if self.desc == "Check task for Click Send Button":
                snip_screen( name = "send_sudden", unique = True )
                ctx.debug_snip = False

        if system_type == "Linux" and ctx.snip_send and self.desc == "Check task for Click Send Button":
            uinfo = ctx.getInfo( ctx.uiObject )

            ctx.snip_data = snip_screen( 
                uinfo['bounds'], 
                name = "snip_proof", 
                
                unique = True, 
                write = False, 
                image_data = True 
            )


states_list = [
    Question(
        task_info = Task_Info(
            match_selector = { 'textContains' : '\nIdentify the color of' },
            emoji_button = { 'description' : 'Add custom reaction', 'className' : Wtype.button.value },
            match_selector_timeout = 35,

            points_selector = { "textContains" : "Bot Income" },
            ps_timeout = 15,
        ),
        desc = "Wait Question"
    ),
    ClickEdit( task_info = Task_Info
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

# Manual redirection of checkpoint states
states_list[3].root_state = states_list[1]
states_list[2].root_state = states_list[1]
