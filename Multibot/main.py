import time, sys 
from pathlib import Path

# Resolve paths
root = Path(__file__).resolve().parent
bots_dir = str( root.parent )
sys.path.extend( [ bots_dir ] )

from ecnl__.main import Bot as ECNL
from ecnl__.states import Question
from decoy.main import Bot as DECOY

from bot_handler import Bot_Handler
from config import DataJson, BotList, BotDis, extractJsonData, loadJson, saveJson

from U2.time import Stime
from U2.states import Handler
from pprint import pp



def main():

    # Load bot handlers with Handlers
    B1 = Bot_Handler( ECNL )

    B1.name = "🌜ECNL🌜"
    B1.key_name = "ECNL"
    # --------------------
    
    B2 = Bot_Handler( DECOY )

    B2.name = "🌜DECOY🌜"
    B2.key_name = "DECOY"
    # --------------------
    
    tmp = [ B1, B2 ]

    # Set tab instance number based on list order
    for i in range( len(tmp) ):
        tmp[i].bot.ctx.tab_instance_number = i + 1

    # Load config from data base
    savePath = "./data/data.json"
    loadJson( tmp, DataJson, path = savePath )

    # Toggle multi_bot flag for all Handlers
    Handler.multi_bot = True

    # Filter restricted bots
    for bot in tmp:
        # Allow bots to lift restrictions
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

    print( BotList[0].bot.current_state )

    # Save attribute changes to data base
    BotList.extend( BotDis )
    saveJson( BotList, DataJson, savePath )



main()
