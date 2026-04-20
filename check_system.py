import sys
import platform
import datetime

def run_system_check():
    print("=" * 40)
    print("🚀 System Check Initiated")
    print("=" * 40)
    
    # Check Current Date and Time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🕒 Current Time: {current_time}")
    
    # Check Python Version
    # sys.version contains a lot of info, we just grab the main version number here
    python_version = sys.version.split()[0]
    print(f"🐍 Python Version: {python_version}")
    
    # Check Operating System Info
    os_name = platform.system()
    os_release = platform.release()
    machine_arch = platform.machine()
    print(f"💻 Operating System: {os_name} {os_release}")
    print(f"⚙️  Architecture: {machine_arch}")
    
    print("-" * 40)
    print("✅ If you can read this, your Python environment is working properly!")
    print("=" * 40)

if __name__ == "__main__":
    run_system_check()
