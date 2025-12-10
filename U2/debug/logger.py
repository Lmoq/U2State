import sys, shutil, logging
from pathlib import Path


class Logger:
    # A logger class that logs into file or stdout
    debug_path = Path("logs")

    info_Logger: logging.Logger = None
    debug_Logger: logging.Logger = None
    stream_Logger: logging.Logger = None

    # If set to True logs will also be displayed on standard output
    stdout: bool = False

    info_stdout = False
    debug_stdout = False


    """To change default path, set_path() must be called first before this"""
    @classmethod
    def init( cls ):
        cls.create_log_dir()
        cls.init_loggers()


    @classmethod
    def create_log_dir( cls ):
        cls.debug_path.mkdir( exist_ok = True )
        print(f"Created log directory at {cls.debug_path.resolve()}")


    # Must preceed calling init()
    @classmethod
    def set_path( cls, new ):
        cls.debug_path = Path( new )


    @classmethod
    def init_loggers( cls ):
        msg_format = "%(asctime)s : %(message)s"
        date_format = "%Y-%m-%d %a %H:%M:%S"

        info_logger = logging.getLogger( "infoLogger" )
        debug_logger = logging.getLogger( "debugLogger" )
        stream_logger = logging.getLogger( "streamLogger" )

        # Custom level
        stream_level = 5

        cls.addFileHandler( info_logger, logging.INFO, "info.log", msg_format, date_format, False )
        cls.addFileHandler( debug_logger, logging.DEBUG, "debug.log", msg_format, date_format, False )
        cls.addStreamHandler( stream_logger, stream_level, sys.stdout, False )

        cls.info_Logger = info_logger
        cls.debug_Logger = debug_logger
        cls.stream_Logger = stream_logger


    @classmethod
    def addFileHandler( cls, logger, level, file_name, msg_format, date_format, propagate = False ):
        # Set properties
        logger.setLevel( level )
        logger.propagate = propagate

        # Setup FileHandler
        file_handler = logging.FileHandler( cls.debug_path / file_name )
        file_handler.setLevel( level )
        file_handler.propagate = propagate

        # Set Formatter
        formatter = logging.Formatter( fmt = msg_format, datefmt = date_format )
        file_handler.setFormatter( formatter )

        # Add Handler
        logger.addHandler( file_handler )


    @classmethod
    def addStreamHandler( cls, logger, level_number, stream_arg, propagate = False ):
        # Add stream level for stream logger
        streamLevel = level_number
        logging.addLevelName( streamLevel, "STREAM" )

        # Add method for stream level
        def stream( self, message, *args, **kwargs ):
            if self.isEnabledFor( streamLevel ):
                self._log( streamLevel, message, args, **kwargs )

        logging.Logger.stream = stream

        logger.setLevel( streamLevel )
        logger.propagate = propagate

        stream_handler = logging.StreamHandler( stream_arg )
        stream_handler.setLevel( streamLevel )
        stream_handler.propagate = propagate

        logger.addHandler( stream_handler )


def infoLog( message ):
    Logger.info_Logger.info( message )
    if Logger.stdout or Logger.info_stdout:
        printLog( message )


def debugLog( message ):
    Logger.debug_Logger.debug( message )
    if Logger.stdout or Logger.debug_stdout:
        printLog( message )


def printLog( message ):
    Logger.stream_Logger.stream( message )




