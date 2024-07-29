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
        os.system("sudo apt install debootstrap")
    elif is_command_available('dnf'):
        os.system("sudo dnf install debootstrap")
    elif is_command_available('yum'):
        print("Please upgrade your Fedora/RHEL/Nobara/etc version.")
        sys.exit()
    elif is_command_available('pacman'):
        os.system("sudo pacman -S debootstrap")
    elif is_command_available('zypper'):
        os.system("sudo zypper in debootstrap")

def install_debian():
    install_script()
    os.mkdir("/etc/nspawnbox/debian")

    print("Bootstrapping Debian...")
    os.system("sudo debootstrap --include=dbus-broker,systemd-container --components=main stable /etc/nspawnbox/debian http://deb.debian.org/debian/")
    print("Setting up nspawn container...")
    os.system("echo 'DISPLAY=:0' > /etc/nspawnbox/debian/etc/environment")
    print("Please set your password")
    os.system("sudo systemd-nspawn -D /etc/nspawnbox/debian /bin/passwd")



