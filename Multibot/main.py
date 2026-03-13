import time, sys 
from pathlib import Path

# Resolve paths
root = Path(__file__).resolve().parent
bots_dir = str( root.parent )
sys.path.extend( [ bots_dir ] )

from U2.time import Stime
from U2.Bots.msbot import MSBot
from U2.states import Handler

from U2.debug import Logger, infoLog
from U2.process import system_type, start_adb_shell_pipes
from U2.adb_tools import switch_keyboard

from U2.notif import notif, NotifLog

from bot_handler import Bot_Handler
from config import extractJsonData, loadJson, saveJson
import config
from utils import rs_main, toggle_keyboard, switchFocus, updateShellNotif

from ecnl.main import Bot as ECNL
from ecnl.states import Question
#from decoy.main import Bot as DECOY

from pprint import pp
import logging


def exec():
    import uiautomator2 as u2
    Logger.init()

    # Load bot handlers with Handlers
    B1 = Bot_Handler( ECNL )

    B1.name = "🌜ECNL🌜"
    B1.key_name = "ECNL"
    # --------------------
    
    #B2 = Bot_Handler( DECOY )

    #B2.name = "🌜DECOY🌜"
    #B2.key_name = "DECOY"
    # --------------------
    
    tmp = [ B1 ]

    # Set tab instance number based on list order
    for i in range( len(tmp) ):
        tmp[i].bot.ctx.tab_instance_number = i + 1

    # Load config from data base
    savePath = "./data/data.json"
    loadJson( tmp, config.DataJson, path = savePath )

    # Filter restricted bots
    for bot in tmp:

        # Allow bots to have change to lift restrictions
        bot.bot.ctx.restricted = bot.bot.ctx.timeRestricted() or bot.bot.ctx.pointsReachedLimit()
        
        if bot.bot.ctx.restricted:
            # Append to discarded list
            config.BotDis.append( bot )
            continue

        # Add to botlist if not time restricted
        config.BotList.append( bot )

    Bot: Bot_Handler = None

    if config.BotList: Bot = config.BotList[0]
    del tmp

    # Initialize class level device, toggle multi_bot flag for all Handlers
    MSBot.init_device_session( u2.connect(), "com.facebook.orca" )
    Handler.multi_bot = True

    if system_type == "Windows":
        Logger.disable_levels( [logging.INFO] )

    infoLog( "Session Start" )

    while config.BotList and not Handler.sig_term:
        try:
            # Update shell notification
            updateShellNotif( config.BotList )

            Bot.bot.ctx.active = True
            Bot.bot.state_loop()

            Bot.next_time_wait = Bot.bot.ctx.get_current_state_wait_time( Bot.bot.current_state )
            #print( f"wait time : {Bot.next_time_wait}" )

            if Handler.sig_term:
                print( "Sigterm..")
                continue

            # Choose the quickest wait time if all Bots have complete a cycle
            if all( b.next_time_wait for b in config.BotList ):

                config.BotList = sorted( config.BotList, key=lambda b : b.next_time_wait )
                next_bot = config.BotList[0]

                ctx = Bot.bot.ctx
                next_ctx = next_bot.bot.ctx

                # Check if restriction flag flipped from checking time and points limit
                if next_ctx.restricted:

                    # Move bot from discarded list
                    config.BotDis.append( config.BotList.pop( 0 ) )

                    if not config.BotList: 
                        break 

                    next_bot = config.BotList[0]

                restarted = False

                # Check duration of cycles, if it has slowed down restart target app
                if not ctx.restricted and ctx.intervalExceed():

                    # Restart target with or without clicking tab UI, then disable press_back incase switchFocus will be called
                    ctx.restartTarget( 
                        ctx.tab_instance_number, 
                        include_click = False if Bot != next_bot else True )

                    restarted = True
                    ctx.cycle_timer.reset()
                    
                # Switch focus
                if Bot != next_bot:
                    Bot = next_bot
                    switchFocus( Bot.bot.ctx, press_back = False if restarted else True )

                continue

            for bot in config.BotList:
                if not bot.next_time_wait:
                    Bot = bot
                    switchFocus( Bot.bot.ctx )
                    pass

        except KeyboardInterrupt:
            print("Mainloop sigint")
            Handler.sig_term = True
            break

    # Save attribute changes to data base
    config.BotList.extend( config.BotDis )
    saveJson( config.BotList, config.DataJson, savePath )


def main():
    # Run main
    start_adb_shell_pipes( system_type )

    NotifLog.set_title({
        "DB" : "db_points",
        "LV" : "live_points",
        "RC" : "recent_desync"
    })

    if system_type == "Linux":
        notif(
            title = "Maccazudon",
            b1 = "Jdon", b1_action = toggle_keyboard,
            b2 = "Our Soul", b2_action = rs_main,
            prio = "low"
        )

    switch_keyboard( "off" ) 
    exec()
    switch_keyboard( "on" ) 


main()
