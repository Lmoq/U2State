import subprocess, os
from pathlib import Path


def check_fifo_pipe( pipe_name ):
    pipe_dir = Path.home() / "pipes"
    pipe = pipe_dir / pipe_name

    if not pipe.exists():
        print(f"Pipe doesn't exist.. {str(pipe)}")
        if not pipe_dir.exists():
            pipe_dir.mkdir( exist_ok = True )
            print(f"Pipe dir doesn't exist {str(pipe_dir)}.. creating diretory..")
        subprocess.run( f"mkfifo {str(pipe)}", shell = True )
    else:
        print("Fifo pipes exists")


def start_adb_shell_pipes( system_type: str = None ):
    assert system_type != None, "Providing operating system type is required"

    if system_type != "Linux":
        print(f"System[{system_type}] is not Linux, pipes won't be used")
        return

    # Start adb shell for pipe communication
    # and adb for uiautomator2 session
    os.system("adb devices")

    cm = ["pgrep", "-fa", "adb shell|tail -f"]
    result = subprocess.run( cm, stdout=subprocess.PIPE ).stdout.decode()

    print( "Checking pipes..\n" )
    print(result if result else "N/A")

    pipe_name = "adbpipe"
    check_fifo_pipe( pipe_name )

    if "adb shell" not in result and "tail -f" not in result:  
        print("Pipes not found")
        print("Starting pipes\n")

        subprocess.Popen(
            f"tail -f /dev/null > ~/pipes/{pipe_name}",
            shell=True,
            start_new_session=True
        )

        subprocess.Popen(
            f"adb shell < ~/pipes/{pipe_name}",
            shell=True,
            start_new_session=True
        )
        result = subprocess.run( cm, stdout=subprocess.PIPE ).stdout.decode()
        print(result)
    else:
        print("Pipes found\n")


