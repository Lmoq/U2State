import platform


def get_system_info():
    global system_type

    system_type = platform.system()
    print(f"\nOperating System: {system_type}")

    machine_type = platform.machine()
    print(f"Machine Type: {machine_type}")

    processor_type = platform.processor()
    print(f"Processor Type: {processor_type}")

    platform_info = platform.platform()
    print(f"Platform Information: {platform_info}")

    os_release = platform.release()
    print(f"OS Release: {os_release}")

    os_version = platform.version()
    print(f"OS Version: {os_version}\n")

system_type = None
get_system_info()

if __name__=="__main__":
    pass
