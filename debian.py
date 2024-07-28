import os, sys

import subprocess

def is_command_available(command):
    """Check if a command is available on the system."""
    try:
        subprocess.run([command, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def install_script():
    if is_command_available('apt') or is_command_available('apt-get'):
        os.system("apt install debootstrap")
    elif is_command_available('dnf'):
        os.system("dnf install debootstrap")
    elif is_command_available('yum'):
        print("Please upgrade your Fedora/RHEL/Nobara/etc version.")
        sys.exit()
    elif is_command_available('pacman'):
        os.system("pacman -S debootstrap")
    elif is_command_available('zypper'):
        os.system("zypper in debootstrap")

install_script()
if not os.path.exists("/etc/podspawn"):
    os.mkdir("/etc/podspawn")
if not os.path.exists("/etc/podspawn/debian"):
    os.mkdir("/etc/podspawn/debian")
elif os.path.exists("/etc/podspawn/debian"):
    print("Podspawn/Debian is already installed.")
    sys.exit()

print("Bootstrapping Debian...")
os.system("debootstrap --include=dbus-broker,systemd-container --components=main stable /etc/podspawn/debian http://deb.debian.org/debian/")
print("Setting up nspawn container...")
print("Please set your password")
os.system("systemd-nspawn -D /etc/podspawn/debian /bin/passwd")

print("Making command...")
with open("/usr/bin/podspawn.debian", "w+") as f:
    f.writelines("""#!/bin/bash
sudo systemd-nspawn -b -D /etc/podspawn/debian
""")

os.system("sudo chmod +x /usr/bin/podspawn.debian")

print("Podspawn/Debian installed.")
print("Run 'podspawn.debian' to load Podspawn/Debian")



