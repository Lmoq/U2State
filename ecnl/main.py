from U2.Bots.msbot import MSBot
from U2.states import Handler
from U2.debug import Logger, printLog
from U2.process import start_adb_shell_pipes, system_type

from U2.notif import NotifLog
from U2.adb_tools import switch_keyboard
try:
    from .states import states_list
    from .context import CTX
except:
    from states import states_list
    from context import CTX
    
ctx = CTX()

# New class instance memebers
# ==========================
ctx.tab_instance_number = 1
ctx.retries = 0
ctx.failed_cycle = False
ctx.debug_snip = False
# ==========================

ctx.restart_time = 1800
ctx.expected_time_avg = 33

Bot = Handler( context = ctx )

Bot.chain_states( states_list, loop = True )
Bot.set_state( states_list[0], states_list[-1] )

def main():
    import uiautomator2 as u2

    Logger.init()
    if system_type == "Windows":
        import logging
        Logger.disable_levels( [logging.INFO] )

    start_adb_shell_pipes( system_type )
    switch_keyboard( "off" )

    ctx.init_device_session( device = u2.connect(), package_name = "com.facebook.orca" )

    Bot.state_loop()
    switch_keyboard( "on" )

if __name__=="__main__":
    main()
