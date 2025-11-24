import shutil, logging
from pathlib import Path


class Logger:
    # A static logger class that logs info and debug logging levels
    debug_path = Path("logs")

    info_Logger: logging.Logger = None
    debug_Logger: logging.Logger = None

    # If set to True logs will also be displayed on standard output
    stdout: bool = False

    info_stdout = False
    debug_stdout = False


    @staticmethod
    def create_log_path():
        Logger.debug_path.mkdir( exist_ok = True )
        print(f"Created log directory {Logger.debug_path}")


    @staticmethod
    def set_path( new ):
        Logger.debug_path = Path( new )


    @staticmethod
    def init():
        Logger.create_log_path()
        Logger.init_loggers()


    @staticmethod
    def init_loggers():
        # Setup loggers
        info_Logger = logging.getLogger("infoLog")
        debug_Logger = logging.getLogger("debugLog")


        info_Logger.setLevel( logging.INFO )
        debug_Logger.setLevel( logging.DEBUG )
        
        info_Logger.propagate = False
        debug_Logger.propagate = False

        # Add Handlers
        infLHandler = logging.FileHandler( Path( Logger.debug_path / "info.log") )
        dbgLHandler = logging.FileHandler( Path( Logger.debug_path / "debug.log") )

        infLHandler.setLevel( logging.INFO )
        dbgLHandler.setLevel( logging.DEBUG )

        formatter = logging.Formatter( fmt = "%(asctime)s : %(message)s", datefmt = "%Y-%m-%d %a %H:%M:%S" )

        infLHandler.setFormatter( formatter )
        dbgLHandler.setFormatter( formatter )

        info_Logger.addHandler( infLHandler )
        debug_Logger.addHandler( dbgLHandler )

        Logger.info_Logger = info_Logger
        Logger.debug_Logger = debug_Logger


def infoLog( message ):
    Logger.info_Logger.info( message )
    if Logger.stdout or Logger.info_stdout:
        print( message )


def debugLog( message ):
    Logger.debug_Logger.debug( message )
    if Logger.stdout or Logger.debug_stdout:
        print( message )




