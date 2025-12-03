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


    # To change default path, set_path() must be called first before this
    @classmethod
    def init( cls ):
        cls.create_log_path()
        cls.init_loggers()


    @classmethod
    def create_log_path( cls ):
        cls.debug_path.mkdir( exist_ok = True )
        print(f"Created log directory {cls.debug_path}")


    # Must preceed calling init()
    @classmethod
    def set_path( cls, new ):
        cls.debug_path = Path( new )


    @classmethod
    def init_loggers( cls ):
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
        
        infLHandler.propagate = False
        dbgLHandler.propagate = False

        infLHandler.setLevel( logging.INFO )
        dbgLHandler.setLevel( logging.DEBUG )

        formatter = logging.Formatter( fmt = "%(asctime)s : %(message)s", datefmt = "%Y-%m-%d %a %H:%M:%S" )

        infLHandler.setFormatter( formatter )
        dbgLHandler.setFormatter( formatter )

        info_Logger.addHandler( infLHandler )
        debug_Logger.addHandler( dbgLHandler )

        cls.info_Logger = info_Logger
        cls.debug_Logger = debug_Logger


def infoLog( message ):
    Logger.info_Logger.info( message )
    if Logger.stdout or Logger.info_stdout:
        print( message )


def debugLog( message ):
    Logger.debug_Logger.debug( message )
    if Logger.stdout or Logger.debug_stdout:
        print( message )




