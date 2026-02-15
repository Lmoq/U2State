import uiautomator2 as u2, sys, pathlib, time

root = pathlib.Path(__file__).parent
sys.path.extend( [str(root) ,str( root.parent / "U2" )] )

from U2.bot import Bot
from U2.enums import TaskType, ActionType, Wtype, Direction
from U2.task import Task

from U2.actions import switch_keyboard
from U2.debug import debugLog, infoLog, notif_
from U2.notif import notif
from U2.process import start_adb_shell_pipes


class Conv( Bot ):

    def __init__( self, **kwargs ):
        super().__init__( **kwargs )


    def swipe_function( self, ui_info ):
        super().swipe_function( ui_info )
        return True



def main():
    conv = Conv()
    conv.init_device_session( u2.connect() )

    # ======================= Check callback ==================================
    task = Task()
    task.number = TaskType.check
    task.callback = conv.doCheck

    task.bHandle_callback = False
    conv.add_task( task )


    # Setup task
    # ======================= Task 1 ==================================
    task = Task()
    task.number = 1
    
    task.match_selector = { "description" : "Menu", "className" : Wtype.image }
    task.match_selector_timeout = 40

    task.action_type = ActionType.click


    # Embed function
    task.bHandle_callback = True
    task.callback = conv.click_function


    # Post callback
    task.check_selector = { "text" : "Send a message…" }
    task.prev_task_number = task.number
    task.next_task_number = 2

    conv.add_task( task )
    # =================================================================


    # ======================= Task 2 ==================================
    task = Task()
    task.number = 2

    task.match_selector = { "text" : "Send a message…" }
    task.action_type = ActionType.swipe

    task.swipe_direction = Direction.up
    task.swipe_points = 200
    task.delay = 0


    # Embed function
    task.bHandle_callback = True
    task.callback = conv.swipe_function
    task.check_selector = { "text" : "Bot Settings", "className" : Wtype.text }

    task.prev_task_number = task.number
    task.next_task_number = 3

    conv.add_task( task )
    # =================================================================


    # ======================= Task 4 ==================================
    task = Task()
    task.number = 3

    task.match_selector = { "text" : "Bot Settings", "className" : Wtype.text }
    task.action_type = ActionType.click


    # Embed function
    task.bHandle_callback = True
    task.callback = conv.click_function
    task.check_selector = { "text" : "Bot Settings", "className" : Wtype.text }

    task.prev_task_number = task.number
    task.next_task_number = 4

    conv.add_task( task )
    # =================================================================


    # ======================= Task 5 ==================================
    task = Task()
    task.number = 4

    task.match_selector = { "text" : "Transfer Points 💸", "className" : Wtype.button }
    task.action_type = ActionType.click


    # Embed function
    task.bHandle_callback = True
    task.callback = conv.click_function
    task.check_selector = { "text" : "Transfer Points 💸", "className" : Wtype.text }

    task.prev_task_number = task.number
    task.next_task_number = 5

    conv.add_task( task )
    # =================================================================


    # ======================= Task 6 ==================================
    task = Task()
    task.number = 5

    task.match_selector = { "text" : "Proceed 🚀", "className" : Wtype.clickable }
    task.action_type = ActionType.click


    # Embed function
    task.bHandle_callback = True
    task.callback = conv.click_function
    task.check_selector = { "text" : "Proceed 🚀", "className" : Wtype.text }

    task.prev_task_number = task.number
    task.next_task_number = 6

    conv.add_task( task )
    # ==============================================================================


    # ======================= Task 7 ===============================================
    task = Task()
    task.number = 6

    task.match_selector = { "text" : "Transfer Now 💸", "className" : Wtype.clickable }
    task.action_type = ActionType.click


    # Embed function
    task.bHandle_callback = True
    task.callback = conv.click_function
    task.check_selector = { "text" : "Transfer Now 💸", "className" : Wtype.text }

    task.prev_task_number = task.number
    task.next_task_number = 7

    conv.add_task( task )
    # ==============================================================================


    # ======================= Task 8 ===============================================
    task = Task()
    task.number = 7

    task.match_selector = { "text" : "Enter 200 ⤵️", "className" : Wtype.text }
    task.action_type = ActionType.wait

    # Embed function
    task.bHandle_callback = True
    task.callback = conv.doWait
    task.check_selector = task.match_selector

    task.prev_task_number = task.number
    task.next_task_number = 8

    conv.add_task( task )
    # ==============================================================================


    # ======================= Task 9 ===============================================
    task = Task()
    task.number = 8
    task.prev_task_number = task.number
    task.next_task_number = 9

    task.match_selector = { 'textContains' : 'essage' }
    task.match_class_inclusion_list = [ Wtype.editText, Wtype.button ]
    task.check_selector = task.match_selector

    task.bHandle_callback = True
    task.callback = conv.click_function

    conv.add_task( task )
    # ==============================================================================

    
    # ======================= Task 10 ===============================================
    task = Task()
    task.number = 9
    task.prev_task_number = task.number
    task.next_task_number = 10

    task.bHandle_callback = True
    task.callback = conv.write_function
    task.write_text = "200"

    task.check_selector = {'text' : task.write_text, 'className' : Wtype.editText}
    conv.add_task( task )
    # ==============================================================================


    # ======================= Task 11 ===============================================
    task = Task()
    task.number = 10
    task.prev_task_number = task.number
    task.next_task_number = 1

    task.match_selector = {'description' : 'Send'}
    task.match_selector_timeout = 0.5
    task.check_selector_timeout = 70
    task.check_selector = {'textContains' : 'Dashboard', 'className' : Wtype.button}

    task.bHandle_callback = True
    task.callback = conv.click_function

    conv.add_task( task )
    # ==============================================================================


    # ======================= Bot main simulation ==================================
    conv.current_task_number = TaskType.t1

    start_adb_shell_pipes()
    notif( content = "Switch Keyboard", b1 = "Switch", b1_action = "~/share/bash/disable_keyboard.sh")

    switch_keyboard('off')
    conv.mainloop()
    #switch_keyboard('on')


if __name__=='__main__':
    main()
