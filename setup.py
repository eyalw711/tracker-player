"""
Tracker-Player Installation:

Operating System: Windows 10

Run in administrator mode.

- Adds context menu entry by editing registry.
- Program Files folder + copy script files
"""

import winreg
import os, errno
import sys
import win32com.shell.shell as shell
from shutil import copyfile

def DllRegisterServer(prog_files_dir):
    executable_path = os.path.sep.join([os.path.dirname(sys.executable), "pythonw.exe"])

    folder_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT,
                                  "Directory\\Background\\shell\\tracker_player")
    winreg.SetValue(winreg.HKEY_CLASSES_ROOT,
                    "Directory\\Background\\shell\\tracker_player",
                    winreg.REG_SZ,
                    "Tracker Player")
    folder_subkey = winreg.CreateKey(folder_key, "command")

    winreg.SetValue(folder_key, "command", winreg.REG_SZ,
                    r'"{}" "{}\TrackerPlayer.pyw"'.format(executable_path, prog_files_dir))

def install_in_program_files():
    # make a ProgramFiles folder
    directory = os.path.sep.join([os.environ["ProgramFiles"], "TrackerPlayer"])
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    print("Created directory in program files...")

    # copy relevant files to ProgramFiles folder
    cwd = os.getcwd()
    filepaths = [(os.path.sep.join([cwd, filename]), os.path.sep.join([directory, filename])) for filename in
                 ["TrackerPlayer.pyw",
                  "PlayerGui.py",
                  "TrackBoard.py"]]
    for src, dst in filepaths:
        copyfile(src, dst)
    print("Copied all source files to directory...")
    return directory

if __name__ == "__main__":
    ASADMIN = 'asadmin'
    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        sys.exit(0)

    print("Installing Tracker-Player!")
    prog_files_dir = install_in_program_files()
    DllRegisterServer(prog_files_dir)
    input("Press any key to quit")



