import sys
import platform
import datetime

def get_system_info():
    """Gathers system information and returns it as a dictionary."""
    return {
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "python_version": sys.version.split()[0],
        "os_name": platform.system(),
        "os_release": platform.release(),
        "machine_arch": platform.machine()
    }

def print_report(info_dict):
    """Handles all console I/O to display the system report."""
    print("=" * 40)
    print("🚀 System Check Initiated")
    print("=" * 40)
    print(f"🕒 Current Time: {info_dict['time']}")
    print(f"🐍 Python Version: {info_dict['python_version']}")
    print(f"💻 Operating System: {info_dict['os_name']} {info_dict['os_release']}")
    print(f"⚙️  Architecture: {info_dict['machine_arch']}")
    print("-" * 40)
    print("✅ If you can read this, your Python environment is working properly!")
    print("=" * 40)

def main():
    system_data = get_system_info()
    print_report(system_data)

if __name__ == "__main__":
    main()
