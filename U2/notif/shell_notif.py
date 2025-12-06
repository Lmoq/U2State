import subprocess 
from U2.process import system_type


class Meta( type ):

    def __call__( cls, *args ):
        cls.notif( *args )


class NotifLog( metaclass = Meta ):

    lines: list[str] = []
    capacity = 4

    titles: list[tuple[ str,str ]] = []
    title_str = ""

    @classmethod
    def add_line( cls, line ):
        # Fifo queue for adding text lines capped with NotifLog capacity
        lines = cls.lines
        lines.append( line )

        if len( lines ) > cls.capacity:
            del lines[0]


    @classmethod
    def set_title( cls, titles: list[tuple[ str, str ]] = [] ):
        # Set title where tuple[0] is displayed name and tuple[1] is the attribute reference as value
        cls.titles = titles

        for nick, attr in titles:
            setattr( cls, attr, 0 )


    @classmethod
    def arrange_title( cls ):
        # Displayed values can be changed by modifying the attribute name reference through this class
        tmp = []
        for nick, title in cls.titles:
            tmp.append(f'{ nick.upper() } : { getattr(cls, title) }' )
        cls.title_str = 'U2 ' + ' | ' +  ' | '.join(tmp)


    @classmethod
    def update_title( cls, render = True ):
        cls.arrange_title()
        if render:
            cls.post_notif()
        pass


    @classmethod
    def post_notif( cls ):
        # Render shell notification
        # cm = f'''cmd notification post -S inbox {notiflog} -t "{NotifLog.title}" notif logs &> /dev/null'''
        lines = cls.get_shell_notif_line_args()

        render_ = False
        assert render_ == False, "Setting render to True inside post_notif() will cause infinite recursion"
        cls.update_title( render = render_ )

        cm = f"cmd notification post -S inbox { lines } -t { repr(cls.title_str) } notif logs"
        _exec(cm)


    @classmethod
    def notif( cls, log ):
        # Display log to shell notification
        cls.add_line( log )

        cls.update_title( render = False )
        cls.post_notif()


    @classmethod
    def get_shell_notif_line_args( cls ) -> str:
        # Wrapped in quotes to work with shell notif post
        return ' '.join([f'--line "{ _line }"' for _line in cls.lines ])

        
def _set_process_caller( system_type ):
    # Set process caller based on system type
    def bash_preset( args ):
        subprocess.run( f'echo "{args}" > ~/pipes/adbpipe &', shell=True )

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
