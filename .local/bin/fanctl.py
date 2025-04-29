#!/home/gsm/miniconda3/bin/python
import sys
import subprocess
from pathlib import Path
from loguru import logger

# Configure loguru
# logger.remove()
# logger.add(sys.stderr, format="{level} | {message}")

# Global path constants
ASUS_DEBUG_PATH = "/sys/kernel/debug/asus-nb-wmi"
ASUS_DEV_ID_PATH = f"{ASUS_DEBUG_PATH}/dev_id"
ASUS_CTRL_PARAM_PATH = f"{ASUS_DEBUG_PATH}/ctrl_param"
ASUS_DEVS_PATH = f"{ASUS_DEBUG_PATH}/devs"
ASUS_PLATFORM_PATH = "/sys/devices/platform/asus-nb-wmi"

# Function to find hwmon paths
def find_hwmon_paths():
    hwmon_base = Path(ASUS_PLATFORM_PATH)
    hwmon_dirs = list(hwmon_base.glob("hwmon/hwmon*"))
    if not hwmon_dirs:
        return None, None, None
    
    hwmon_dir = hwmon_dirs[0]
    pwm_path = hwmon_dir / "pwm1_enable"
    fan_rpm_path = hwmon_dir / "fan1_input"
    
    return hwmon_dir, pwm_path, fan_rpm_path

# Initialize global hwmon paths
HWMON_DIR, PWM_ENABLE_PATH, FAN_INPUT_PATH = find_hwmon_paths()


def set_fan_state(state):
    state_value = None
    
    if state in ["0", "standard"]:
        state_value = 0
    elif state in ["1", "quiet"]:
        state_value = 1
    elif state in ["2", "high"]:
        state_value = 2
    elif state in ["3", "full"]:
        state_value = 3
    else:
        logger.error("Invalid fan state. Use 0-3 or standard/quiet/high/full.")
        sys.exit(1)
    
    logger.info(f"Setting fan state to {state_value}")
    try:
        # Direct file operations
        with open(ASUS_DEV_ID_PATH, "w") as f:
            f.write("0x110019")
        
        with open(ASUS_CTRL_PARAM_PATH, "w") as f:
            f.write(str(state_value))
            
        # Optionally read back the state from devs for confirmation
        with open(ASUS_DEVS_PATH, "r") as f:
            result = f.read().strip()
            logger.debug(f"Result: {result}")
    except Exception as e:
        logger.error(f"Error setting fan state: {e}")
        sys.exit(1)

def get_fan_state():
    try:
        # Create a list to collect all the messages
        info_messages = []
        
        # Direct file operations without sudo
        with open(ASUS_DEV_ID_PATH, "w") as f:
            f.write("0x110019")
        
        with open(ASUS_CTRL_PARAM_PATH, "r") as f:
            state = f.read().strip()

        info_messages.append(f"{HWMON_DIR.name}")
        
        # Get fan mode
        if state == "0x00000000":
            info_messages.append("state: Standard (0)")
        elif state == "0x00000001":
            info_messages.append("state: Quiet (1)")
        elif state == "0x00000002":
            info_messages.append("state: High-Performance (2)")
        elif state == "0x00000003":
            info_messages.append("state: Full-Performance (3)")
        else:
            info_messages.append(f"state: Unknown ({state})")
        
        # Use the global hwmon paths
        if HWMON_DIR:
            # Get pwm1_enable
            if PWM_ENABLE_PATH and PWM_ENABLE_PATH.exists():
                pwm_enable = PWM_ENABLE_PATH.read_text().strip()
                pwm_status = "AUTO (0)" if pwm_enable == "0" else "MANUAL (1)" if pwm_enable == "1" else "OFF (2)" if pwm_enable == "2" else f"UNKNOWN ({pwm_enable})"
                info_messages.append(f"mode: {pwm_status}")
            
            # Get fan1_input (RPM)
            if FAN_INPUT_PATH and FAN_INPUT_PATH.exists():
                fan_rpm = FAN_INPUT_PATH.read_text().strip()
                info_messages.append(f"{fan_rpm} RPM")
        
        # Display all information in a single log message
        logger.info("\n".join(info_messages))
        # write message to stdout
        print("|\n".join(info_messages))
        
    except Exception as e:
        logger.error(f"Error reading fan state: {e}")
        sys.exit(1)

def set_fan_power(state):
    if state.lower() in ["on", "1"]:
        value = 0
        state_str = "ON"
    elif state.lower() in ["off", "0"]:
        value = 2
        state_str = "OFF"
    else:
        logger.error("Invalid power state. Use 'on'/'off' or '1'/'0'.")
        sys.exit(1)
    
    # Use the global PWM_ENABLE_PATH
    if not PWM_ENABLE_PATH or not PWM_ENABLE_PATH.exists():
        logger.error("Fan power control not available - no hwmon directory found with pwm1_enable.")
        sys.exit(1)
    
    try:
        hwmon_number = HWMON_DIR.name if HWMON_DIR else "unknown"
        logger.info(f"Setting fan power to {state_str} @ {hwmon_number}")
        PWM_ENABLE_PATH.write_text(str(value))
    except Exception as e:
        logger.error(f"Error setting fan power: {e}")
        sys.exit(1)

def print_usage():
    logger.info("Usage: fanctl [set <0-3|standard|quiet|high|full>|get|power <on|off>]")

def main():
    if len(sys.argv) == 1:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "set":
        if len(sys.argv) != 3:
            logger.error("'set' command requires an argument (0-3 or standard/quiet/high/full).")
            sys.exit(1)
        set_fan_state(sys.argv[2])
    elif command == "get":
        get_fan_state()
    elif command == "power":
        if len(sys.argv) != 3:
            logger.error("'power' command requires an argument (on/off).")
            sys.exit(1)
        set_fan_power(sys.argv[2])
    else:
        logger.error("Invalid command. Use 'set <0-3|standard|quiet|high|full>', 'get', or 'power <on|off>'.")
        sys.exit(1)

if __name__ == "__main__":
    main()