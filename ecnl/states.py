from U2.Bots.msbot import MSCheck
from U2.states import Click, Wait, Write, Swipe, Check
from U2.task import Task_Info

from U2.debug import printLog, infoLog, debugLog, snip_screen
from U2.adb_tools import adbSwipeUi, vibrate
from U2.notif import NotifLog

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


        # Main selector search
        uinfo = ctx.search_sibling_element( tfo.emoji_button, tfo.match_selector, tfo.match_selector_timeout )
        if uinfo is None:
            infoLog( f"    <<Question not found>>" )

            printLog( f"Retries : { ctx.retries }" )
            ctx.retries += 1

            if ctx.retries > 1:
                ctx.restartTarget( ctx.tab_instance_number )

            else:
                in_target_app = ctx.device.wait_activity( ctx.launch_activity.split('/')[1], timeout=1 )

                if in_target_app:
                    adbSwipeUi( ctx.screen_dimension, Direction.up, 500 )

            ctx.failed_cycle = True
            return self

        ctx.cycle_timer.track_interval()


        if not ctx.failed_cycle and ctx.cycle_timer.track_calls > 0 and ctx.cycle_timer < 25:
            # Handle sudden reappearance of target ui to prevent spam
            snip_screen( name = "sudden", unique = True )
            log = f"Sudden reappearance of target ui {timenow()}"

            infoLog( log )
            debugLog( log )
            printLog( log )

            ctx.restartTarget( ctx.tab_instance_number )
            ctx.cycle_timer.reset()

            ctx.debug_snip = True
            printLog( f"Toggled snip : {ctx.debug_snip} {Stime()}" )
            return self

        ctx.uinfo = uinfo
        ctx.retries = 0

        infoLog( f"Question : {ctx.uinfo['text']}" )
        answered = self.callback( ctx )


        # Check if local db is synced with latest info
        p_uinfo = ctx.search_element( {"textContains" : f"Bot Income:"}, tfo.ps_timeout )
        if p_uinfo is None:
            log = f"    <<Pinfo not found>> {Stime()}"

            printLog( log )
            infoLog( log )

            vibrate( 2, 1 )
        else:
            text = get_points( p_uinfo["text"] )

            log = f"Local : {ctx.points} Pinfo : {text}"
            infoLog( log )

            NotifLog.db_points = ctx.points
            NotifLog.live_points = text

            if int( text ) != ctx.points:
                vibrate( 2, 1 )

                recent = Stime()
                NotifLog.recent_desync = recent

                log = f"Db[{ctx.points}] P[{text}] {recent}"

                printLog( log )
                infoLog( log )
                debugLog( log )

                ctx.points = int( text )

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
        check = ECCheck( desc = f"Check task for {self}" )

        check.current_state = self
        check.next_state = self.next_state

        return check


class ECCheck( MSCheck ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def callback( self, ctx ):
        # Increment points
        ctx.points += 1

        # Temporary snip debugging
        if ctx.debug_snip:
            printLog( f"Follow up snip : {ctx.debug_snip} {Stime()}" )

            if self.desc == "Check task for Write Text":
                snip_screen( name = "write_sudden", unique = True )

            if self.desc == "Check task for Click Send Button":
                snip_screen( name = "send_sudden", unique = True )
                ctx.debug_snip = False
                printLog( f"Toggled off {ctx.debug_snip} {Stime()}" )


states_list = [
    Question(
        task_info = Task_Info(
            match_selector = { 'textContains' : '\nIdentify the color of' },
            emoji_button = { 'description' : 'Add custom reaction', 'className' : Wtype.button.value },

            points_selector = { "textContains" : "Correct Answer" },
            ps_timeout = 20,
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
