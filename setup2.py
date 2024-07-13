import subprocess

# Define the command to be executed
adb_command = "adb shell \"mount -o rw,remount /system && cd /mnt/media_rw/40F465C7F465C030/Akiba_new_setup/ && sh 2_Kandel_setup.sh\""

# Run the command
process = subprocess.Popen(adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for the command to complete
stdout, stderr = process.communicate()

# Check if the command was executed successfully
if process.returncode == 0:
    print("Command executed successfully.")
    print(stdout.decode())
else:
    print("An error occurred.")
    print(stderr.decode())