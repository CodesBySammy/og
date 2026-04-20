import sys
import platform
import datetime
import logging

# Configure enterprise-standard logging instead of raw print()
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

class SystemMonitor:
    """Encapsulates system information retrieval to ensure strict modularity."""

    def __init__(self) -> None:
        self.timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.python_version: str = sys.version.split()[0]
        self.os_name: str = platform.system()
        self.os_release: str = platform.release()
        self.architecture: str = platform.machine()

    def generate_report_string(self) -> str:
        """Constructs the report string mathematically without performing any direct I/O."""
        report = [
            "=" * 40,
            "🚀 System Check Initiated",
            "=" * 40,
            f"🕒 Current Time: {self.timestamp}",
            f"🐍 Python Version: {self.python_version}",
            f"💻 Operating System: {self.os_name} {self.os_release}",
            f"⚙️  Architecture: {self.architecture}",
            "-" * 40,
            "✅ If you can read this, your Python environment is working properly!",
            "=" * 40
        ]
        return "\n".join(report)

def main() -> None:
    """Main execution entry point coordinating logic and presentation."""
    monitor = SystemMonitor()
    report_output = monitor.generate_report_string()
    
    # Pure I/O execution via logger
    logger.info(report_output)

if __name__ == "__main__":
    main()
