import subprocess, os
from pathlib import Path


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

    if "adb shell" not in result and "tail -f" not in result:  
        print("Pipes not found")

        print("Starting pipes\n")

        subprocess.Popen(
            "tail -f /dev/null > ~/pipes/adbpipe",
            shell=True,
            start_new_session=True
        )

        subprocess.Popen(
            "adb shell < ~/pipes/adbpipe",
            shell=True,
            start_new_session=True
        )
        result = subprocess.run( cm, stdout=subprocess.PIPE ).stdout.decode()
        print(result)
    else:
        print("Pipes found\n")


