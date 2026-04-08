import time, sys 
from pathlib import Path

# Resolve paths
root = Path(__file__).resolve().parent
bots_dir = str( root.parent )
sys.path.extend( [ bots_dir ] )

from U2.time import Stime
from U2.Bots.msbot import MSBot
from U2.states import Handler

from U2.process import system_type, start_adb_shell_pipes
from U2.adb_tools import switch_keyboard

from U2.debug import Logger, infoLog, printLog
from U2.notif import notif, NotifLog

from bot_handler import Bot_Handler
from config import extractJsonData, loadJson, saveJson
from utils import rs_main, toggle_keyboard, switchFocus, updateShellNotif

from ecnl.main import Bot as ECNL
from lecb.main import Bot as LECB
from pprint import pp

import logging
import config


def exec():
    import uiautomator2 as u2
    Logger.init()

    # Load bot handlers with Handlers
    B1 = Bot_Handler( ECNL )

    B1.name = ECNL.ctx.name
    B1.key_name = "ECNL"
    # --------------------
    
    B2 = Bot_Handler( LECB )

    B2.name = LECB.ctx.name
    B2.key_name = "LECB"
    # --------------------
    
    tmp = [ B1, B2 ]

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
            print( f"[{bot}] is currently restricted" )
            config.BotDis.append( bot )
            continue

        bot.bot.current_state = bot.bot.states_list[ bot.bot.ctx.state_index ]
        bot.next_time_wait = bot.bot.ctx.next_time_wait
        time_stamp = time.strftime( "%H:%M:%S", time.localtime( bot.next_time_wait ) )

        print( f"[{bot}] Current state : {bot.bot.current_state} time_wait : {time_stamp}" )
        print( f"[{bot}] restriction start : {bot.bot.ctx.start_time_restriction} end : {bot.bot.ctx.end_time_restriction}")

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

            time_wait = Bot.bot.ctx.get_current_state_wait_time( Bot.bot.current_state )

            Bot.next_time_wait = time.time() + time_wait
            Bot.bot.ctx.next_time_wait = Bot.next_time_wait

            if not Bot.next_time_wait:
                print( f"!!![{Bot}] current_state : {Bot.bot.current_state} next_wait_time : {time_wait}!!!" )
                Handler.sig_term = True
                break

            if Handler.sig_term:
                print( "Sigterm..")
                continue

            # Allow lifting restriction of suspended bots
            for bot in config.BotDis:

                ctx = bot.bot.ctx
                ctx.restricted = ctx.timeRestricted() or ctx.pointsReachedLimit()

                if not ctx.restricted:
                    print( f"Restriction lifted for {bot}" )
                    config.BuffList.append( bot )

            if config.BuffList:
                # Transfer items from BotDis to BotList
                [ config.BotList.append( config.BotDis.pop( config.BotDis.index( Bot ) ) ) for Bot in config.BuffList ]
                config.BuffList.clear()

            # Choose the quickest wait time if all Bots have completed a cycle
            if all( b.next_time_wait for b in config.BotList ):

                config.BotList = sorted( config.BotList, key=lambda b : b.next_time_wait )
                next_bot = config.BotList[0]

                ctx = Bot.bot.ctx
                next_ctx = next_bot.bot.ctx

                # Check if restriction flag was toggled from checking time and points limit
                if next_ctx.restricted:

                    # Move bot from discarded list
                    config.BotDis.append( config.BotList.pop( 0 ) )

                    if not config.BotList: 
                        break 
                    next_bot = config.BotList[0]

                restarted = False

                # Check duration of cycles, if it has slowed down restart target app
                if not ctx.restricted and ctx.intervalExceed():

                    # Restart target with or without clicking tab UI, then disable press_back for switchFocus incase it will be called
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
        "SS" : "snip_sudden",
        "GI" : "g_info",
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
