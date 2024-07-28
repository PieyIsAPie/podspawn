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

install_script()
if not os.path.exists("/etc/podspawn"):
    os.mkdir("/etc/podspawn")
if not os.path.exists("/etc/podspawn/arch"):
    os.mkdir("/etc/podspawn/arch")
elif os.path.exists("/etc/podspawn/fedora"):
    print("Podspawn/Fedora is already installed.")
    sys.exit()

print("Bootstrapping Arch...")
os.system("pacstrap -K /etc/podspawn/arch base-devel base git")
print("Setting up nspawn container...")
print("Please set your password")
os.system("systemd-nspawn -D /etc/podspawn/arch /bin/passwd")

print("Making command...")
with open("/usr/bin/podspawn.arch", "w+") as f:
    f.writelines("""#!/bin/bash
sudo systemd-nspawn -b -D /etc/podspawn/arch
""")
    
os.system("sudo chmod +x /usr/bin/podspawn.arch")

print("Podspawn/Arch installed.")
print("Run 'podspawn.arch' to load Podspawn/Arch")



