import time, sys 
from pathlib import Path

# Resolve paths
root = Path(__file__).resolve().parent
bots_dir = str( root.parent )
sys.path.extend( [ bots_dir ] )

from U2.time import Stime
from U2.Bots.msbot import MSBot
from U2.states import Handler

from U2.debug import Logger
from U2.process import system_type, start_adb_shell_pipes
from U2.adb_tools import switch_keyboard

from U2.notif import notif, NotifLog

from bot_handler import Bot_Handler
from config import DataJson, BotList, BotDis, extractJsonData, loadJson, saveJson
from utils import switchFocus, rs_main, toggle_keyboard

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
    loadJson( tmp, DataJson, path = savePath )

    # Filter restricted bots
    for bot in tmp:
        # Allow bots to have change to lift restrictions
        bot.bot.ctx.restricted = bot.bot.ctx.timeRestricted() or bot.bot.ctx.pointsReachedLimit()
        
        if bot.bot.ctx.restricted:
            # Append to discarded list
            BotDis.append( bot )
            continue

        # Add to botlist if not time restricted
        BotList.append( bot )

    Bot: Bot_Handler = None
    if BotList: Bot = BotList[0]
    del tmp

    # Initialize class level device, toggle multi_bot flag for all Handlers
    MSBot.init_device_session( u2.connect(), "com.facebook.orca" )
    Handler.multi_bot = True

    if system_type == "Windows":
        Logger.disable_levels( [logging.INFO] )

    while BotList and not Handler.sig_term:
        try:
            # Update shell notification
            NotifLog("")

            Bot.bot.ctx.active = True
            Bot.bot.state_loop()

            Bot.next_time_wait = Bot.bot.ctx.get_current_state_wait_time( Bot.bot.current_state )
            #print( f"wait time : {Bot.next_time_wait}" )

            if Handler.sig_term:
                print( "Sigterm..")
                continue

            # Choose the quickest wait time if all Bot have done task and time wait
            if all( b.next_time_wait for b in BotList ):
                continue

            for b in BotList:
                if not b.next_time_wait:
                    pass

        except KeyboardInterrupt:
            print("Mainloop sigint")
            Handler.sig_term = True
            break

    # Save attribute changes to data base
    BotList.extend( BotDis )
    saveJson( BotList, DataJson, savePath )


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
