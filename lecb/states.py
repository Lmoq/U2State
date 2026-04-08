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
    from .alg import get_answer, get_points
except:
    from alg import get_answer, get_points



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

        # Main selector search
        # print( f"[{ctx}] Searching Question timeout : {timeout}" )
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
                    print(f"[{ctx}] Swiping retries:{ctx.retries}")

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


        return self.next( ctx ) if answered else self


    def callback( self, ctx ):
        question = ctx.uinfo["text"]
        answer = get_answer( question )

        if not answer:
            debugLog( f"[{ctx}]    <<Failed to get answer>>" )
            ctx.failed_cycle = True
            return False

        ctx.click_text = answer
        ctx.failed_cycle = False

        ctx.question_ui = question
        ctx.retries = 0

        return True



class ClickAnswer( Click ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def run( self, ctx ):
        self.task_info.match_selector |= { "text" : ctx.click_text }
        self.task_info.check_selector = { "text" : ctx.click_text, "className" : Wtype.text.value }

        return super().run( ctx )


    def next( self, ctx ):
        check = MSCheck( desc = f"Check task for {self}" )

        check.current_state = self
        check.next_state = self.next_state
        check.root_state = self.root_state

        return check


class VerifyAnswer( Wait ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def run( self, ctx ):
        tfo = self.task_info

        timeout = 3
        timeout = tfo.match_selector_timeout if ctx.retries < 1 else 3
        time_wait = ctx.next_time_wait

        if time_wait:
            current_time = time.time()
            timeout = ( ctx.next_time_wait - current_time ) if time_wait > current_time else 3

        # print( f"[{ctx}] Verifying Answer timeout : {timeout}" )
        uinfo = ctx.search_sibling_element( tfo.emoji_button, tfo.match_selector, timeout = timeout )

        if uinfo is None:
            infoLog( f"[{ctx}]    <<Verify ui not found>>" )

            ctx.retries += 1
            printLog( f"Retries : { ctx.retries }" )

            if ctx.retries > 2:
                sign = ctx.search_element( ctx.restricted_ui, 1 )
                if sign is None:

                    ctx.retries = 0
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

            ctx.failed_cycle = True
            return self

        ctx.task_timer.track_interval()
        ctx.uinfo = uinfo

        points = int( get_points( uinfo['text'] ) )
        log = f"[{ctx}] Local : {ctx.points} Points : {points}"
        infoLog( log )

        if points != ctx.points:
            vibrate( 0.5, 2 )

            recent = Stime()
            log = f"[{ctx}] Db[{ctx.points}] P[{points}]"

            printLog( log )
            infoLog( log )
            debugLog( log )

            ctx.points = points

        if ctx.pointsReachedLimit():
            self.active = False
            self.restricted = False
            return None

        return self.next_state


class ClickNext( Click ):


    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def next( self, ctx ):
        check = MSCheck( desc = f"Check task for {self}" )

        check.current_state = self
        check.next_state = self.next_state
        check.root_state = self.root_state

        return check


states_list = [
    Question(
        task_info = Task_Info(
            match_selector = { 'textContains' : '𝐀.' },
            emoji_button = { 'description' : 'Add custom reaction', 'className' : Wtype.button.value },
            match_selector_timeout = 12 * 60,

            points_selector = { "textContains" : "UiObject String Content" },
            ps_timeout = 15,
        ),
        desc = "Wait Question"
    ),
    ClickAnswer(
        task_info = Task_Info( match_selector = { "text" : "UiObject" } ),
        desc = "Click Answer"
    ),
    VerifyAnswer(
        task_info = Task_Info( 
            match_selector = { "textContains" : "𝐂𝐎𝐑𝐑𝐄𝐂𝐓 𝐀𝐍𝐒𝐖𝐄𝐑", "className" : Wtype.text.value },
            emoji_button = { 'description' : 'Add custom reaction', 'className' : Wtype.button.value },
            match_selector_timeout = 12 * 60
        ),
        desc = "Verify Answer"
    ),
    ClickNext(
        task_info = Task_Info(
            match_selector = { 'text' : '💫 𝐍𝐄𝐗𝐓 💫', "className" : Wtype.clickable.value },
            match_selector_timeout = 4,

            check_selector = { 'text' : '💫 𝐍𝐄𝐗𝐓 💫', "className" : Wtype.text.value }
        ),
        desc = "Click Next"
    )
]




