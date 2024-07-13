import subprocess

# Define the commands to be executed step-by-step
commands = [
    "adb shell mount -o rw,remount /system",
    "adb shell ls -l /mnt/media_rw/40F465C7F465C030/Akiba_new_setup/",  # List directory contents to verify the script exists
    "adb shell ls -l /mnt/media_rw/40F465C7F465C030/Akiba_new_setup/dev900.ovpn",  # Check existence and permissions of dev900.ovpn
    "adb shell ls -l /mnt/media_rw/40F465C7F465C030/Akiba_new_setup/debian_stretch_rootfs_release_20200309.tgz",  # Check existence and permissions of debian_stretch_rootfs_release_20200309.tgz
    "adb shell sh /mnt/media_rw/40F465C7F465C030/Akiba_new_setup/1_Kandel_setup.sh"  # Use full path to the script
]

# Function to run a command and capture its output
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()

# Execute each command and print the results
for command in commands:
    print(f"Running command: {command}")
    returncode, stdout, stderr = run_command(command)
    
    if returncode == 0:
        print(f"Command executed successfully:\n{stdout}")
    else:
        print(f"An error occurred while running command: {command}\n{stderr}")
        break  # Stop executing further commands if an error occurs

# Check if all commands executed successfully
if returncode == 0:
    print("All commands executed successfully.")
else:
    print("One or more commands failed.")
