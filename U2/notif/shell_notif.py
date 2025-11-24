import subprocess, sys, pathlib

Path = pathlib.Path
sys.path.append( str( Path(__file__).parent.parent.parent ) )

from U2.process import system_type


class NotifLog():

    lines: list[str] = []
    capacity = 4

    titles: list[tuple[ str,str ]] = []
    title_str = ""

    @staticmethod
    def add_line( line ):

        lines = NotifLog.lines
        lines.append( line )

        if len( lines ) > NotifLog.capacity:
            del lines[0]


    @staticmethod
    def set_title( titles: list[tuple[ str, str ]] = [] ):
        # Set title where tuple[0] is Displayed name and tuple[1] is the attribute reference
        NotifLog.titles = titles

        for nick, attr in titles:
            setattr( NotifLog, attr, "0" )


    @staticmethod
    def arrange_title():
        tmp = []
        for nick, title in NotifLog.titles:
            tmp.append(f'{ nick.upper() } : { getattr(NotifLog, title) }' )
        NotifLog.title_str = 'U2 ' + ' | '.join(tmp)


    @staticmethod
    def update_title( render = True ):
        NotifLog.arrange_title()
        if render:
            NotifLog.post_notif()
        pass


    @staticmethod
    def post_notif():
        #cm = f'''echo 'cmd notification post -S inbox {notiflog} -t "{NotifLog.title}" notif logs &> /dev/null' > ~/pipes/adbpipe'''
        lines = NotifLog.get_shell_notif_line_args()
        NotifLog.update_title( render = False )

        cm = f"cmd notification post -S inbox { lines } -t { repr(NotifLog.title_str) } notif logs"
        _exec(cm)


    @staticmethod
    def notif( log ):
        # Display log to shell notification
        NotifLog.add_line( log )

        NotifLog.update_title( render = False )
        NotifLog.post_notif()


    @staticmethod
    def get_shell_notif_line_args() -> str:
        # Wrapped in quotes to work with shell notif post
        return ' '.join([f'--line "{ _line }"' for _line in NotifLog.lines ])

        
def _set_process_caller( system_type ):
    # Set process caller based on system type
    def bash_preset( args ):
        subprocess.run( f"echo {args} > ~/pipes/adbpipe &", shell=True )

    def cmd_preset( args ):
        subprocess.run( f"adb shell {args}".split(), stdout=subprocess.DEVNULL )

    match system_type:
        case "Windows":
            print(f"Notif using windows preset for [{system_type}]")
            return cmd_preset
        case "Linux":
            print(f"Notif using linux preset for [{system_type}]")
            return bash_preset

_exec = _set_process_caller( system_type )
