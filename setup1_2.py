import subprocess

# Define the commands to be executed step-by-step

commands = [
    "mount -o rw,remount /system",
    "adb shell d /mnt/media_rw/40F465C7F465C030/Akiba_new_setup/ h 1_Kandel_setup.sh"
    
]

# Function to run a command and capture its output
def run_command(command):
    process = subprocess.Popen(f"adb shell \"{command}\"", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
