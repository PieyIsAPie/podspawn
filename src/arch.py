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
        os.system("apt install arch-install-scripts")
    elif is_command_available('dnf'):
        os.system("dnf install arch-install-scripts")
    elif is_command_available('yum'):
        print("Please upgrade your Fedora/RHEL/Nobara/etc version.")
        sys.exit()
    elif is_command_available('pacman'):
        os.system("pacman -S arch-install-scripts")
    elif is_command_available('zypper'):
        os.system("zypper in arch-install-scripts")

def install_arch():
    install_script()
    os.mkdir("/etc/nspawnbox/arch")

    print("Arch not installed, installing...")
    print("Bootstrapping Arch...")
    os.system("pacstrap -K /etc/nspawnbox/arch base-devel base git")
    print("Setting up nspawn container...")
    os.system("echo 'DISPLAY=:0' > /etc/nspawnbox/arch/etc/environment")
    os.system("systemd-nspawn -D /etc/nspawnbox/arch /bin/passwd")




