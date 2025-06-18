import os
import time
import shutil
import sys

SCANNER_TEMPLATE = '''import socket
import sys

def scan_ip_range(base_ip, third_octet, port, output_file):
    found_servers = []
    total_ips = 256
    checked = 0
    for last_octet in range(0, 256):
        ip = f"{{base_ip}}.{{third_octet}}.{{last_octet}}"
        checked += 1
        print(f"Scanned: {{ip}}:{{port}} ({{checked}}/{{total_ips}})")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"Server found: {{ip}}:{{port}}")
                found_servers.append(f"{{ip}}:{{port}}")
            sock.close()
        except Exception as e:
            print(f"Error scanning {{ip}}: {{e}}")

    with open(output_file, "w") as f:
        for server in found_servers:
            f.write(server + "\\n")

    print("\\nScanning complete. Results saved to {{output_file}}")
    sys.exit(0)

if __name__ == "__main__":
    base_ip = "{base_ip}"
    third_octet = {third_octet}
    port = {port}
    output_file = "servers_{third_octet}.txt"
    scan_ip_range(base_ip, third_octet, port, output_file)
'''

def show_warning_and_get_agreement():
    warning_text = """
 Users who are inexperienced or uncertain about system behavior under high load are strongly advised not to run more than 10-20 scanners at once. Do not run All at once unless you know what you are doing.
"""
    print("|"*90)
    print(warning_text)
    print("_|_"*30)
    print("\nYou must type 'I Understand' (case-sensitive) to continue.")
    user_agree = input("Type here: ").strip()
    if user_agree != "I Understand":
        print("You did not agree to the warning. Exiting.")
        sys.exit(1)

def validate_octet_range(input_str):
    input_str = input_str.strip()
    if not input_str:
        raise ValueError("You must provide a value for the third octet (either a single number like 123 or a range like 120-130).")
    if '-' in input_str:
        parts = input_str.split('-')
        if len(parts) != 2:
            raise ValueError("Malformed range. Use format: start-end (e.g., 10-20)")
        try:
            start = int(parts[0])
            end = int(parts[1])
        except ValueError:
            raise ValueError("Range must contain only numbers (e.g., 10-20)")
        if not (0 <= start <= 255 and 0 <= end <= 255 and start <= end):
            raise ValueError("Range must be within 0-255 and start <= end.")
        return start, end
    else:
        try:
            val = int(input_str)
        except ValueError:
            raise ValueError("Third octet must be a number between 0 and 255, or a range like 5-10.")
        if not (0 <= val <= 255):
            raise ValueError("Octet value must be within 0-255.")
        return val, val

def main():
    print("=== Minecraft IP-Range Sweeper ===")
    show_warning_and_get_agreement()
    try:
        # User input for base IP
        base_ip = input("Enter base IP (first two octets, e.g. 89.244): ").strip()
        if len(base_ip.split('.')) != 2 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in base_ip.split('.')):
            print("Invalid base IP format! Please enter like 89.244")
            return

        # User input for port
        port = input("Enter port (default 25565): ").strip()
        if not port:
            port = 25565
        else:
            try:
                port = int(port)
                if not (1 <= port <= 65535):
                    raise ValueError()
            except ValueError:
                print("Invalid port! Must be an integer between 1 and 65535.")
                return

        # User input for third octet range with strong validation
        range_input = input("Enter third-octet (e.g. 0-10 for 89.244.0.0–89.244.10.255 or just 255): ").strip()
        try:
            range_start, range_end = validate_octet_range(range_input)
        except ValueError as ve:
            print(f"Input error: {ve}")
            return

        print(f"Preparing to generate scanner(s) for {base_ip}.{range_start}-{range_end}.0-255 ...")

        # Prepare folders and scanner scripts
        scanner_configs = []
        for yyy in range(range_start, range_end + 1):
            folder = f"scanner_{yyy}"
            try:
                if os.path.exists(folder):
                    print(f"Removing existing folder: {repr(folder)}")
                    shutil.rmtree(folder)
                os.makedirs(folder, exist_ok=True)
                scan_py_path = os.path.join(folder, "scan.py")
                print(f"Writing scanner script: {repr(scan_py_path)}")
                with open(scan_py_path, "w") as f:
                    f.write(SCANNER_TEMPLATE.format(
                        base_ip=base_ip, third_octet=yyy, port=port
                    ))
                if not os.path.exists(scan_py_path):
                    print(f"Failed to create scanner script: {repr(scan_py_path)}")
                scanner_configs.append((folder, scan_py_path))
                print(f"Created: {scan_py_path}")
            except Exception as e:
                print(f"Error creating folder or file for {yyy}: {e}")

        if not scanner_configs:
            print("No scanners created. Exiting.")
            return

        # Execution prompt
        run = input(f"\nRun scanners now? (y/n): ").strip().lower()
        if run != 'y':
            print("Scanners generated. Run them manually from their folders.")
            return

        max_at_once = input(f"How many scanners to run at once? (Enter number or 'all'): ").strip()
        python_cmd = sys.executable  # Use the running Python

        if max_at_once.lower() == 'all':
            print("Launching ALL scanners in new windows...")
            for folder, scan_py in scanner_configs:
                try:
                    abs_folder = os.path.abspath(folder)
                    abs_script = os.path.abspath(scan_py)
                    if sys.platform == "win32":
                        cmd = f'start "" cmd /C "cd /d {abs_folder} && {python_cmd} scan.py"'
                        print(f"Launching with command: {repr(cmd)}")
                        os.system(cmd)
                    else:
                        cmd = f'gnome-terminal -- bash -c "cd {abs_folder} && {python_cmd} scan.py"'
                        print(f"Launching with command: {repr(cmd)}")
                        os.system(cmd)
                except Exception as e:
                    print(f"Error launching {scan_py}: {e}")
            print("All scanners launched.")
        else:
            try:
                max_at_once = int(max_at_once)
                if max_at_once < 1:
                    print("You must run at least one scanner at once.")
                    return
            except ValueError:
                print("Invalid number!")
                return

            delay = 350  # 5 minutes 50 seconds
            total_scanners = len(scanner_configs)
            idx = 0

            while idx < total_scanners:
                # Launch up to max_at_once scanners at once
                batch = scanner_configs[idx:idx+max_at_once]
                for folder, scan_py in batch:
                    print(f"Launching {scan_py} in new window")
                    try:
                        abs_folder = os.path.abspath(folder)
                        abs_script = os.path.abspath(scan_py)
                        if sys.platform == "win32":
                            cmd = f'start "" cmd /C "cd /d {abs_folder} && {python_cmd} scan.py"'
                            print(f"Launching with command: {repr(cmd)}")
                            os.system(cmd)
                        else:
                            cmd = f'gnome-terminal -- bash -c "cd {abs_folder} && {python_cmd} scan.py"'
                            print(f"Launching with command: {repr(cmd)}")
                            os.system(cmd)
                    except Exception as e:
                        print(f"Error launching {scan_py}: {e}")
                idx += max_at_once
                if idx < total_scanners:
                    print(f"Waiting {delay} seconds before launching the next batch of scanners...")
                    time.sleep(delay)
            print("All scanners launched.")

    except Exception as e:
        print(f"FATAL ERROR: {e}")

if __name__ == "__main__":
    main()
