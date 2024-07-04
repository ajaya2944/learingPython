import subprocess
import time

sh_script_path = "C:\platform-tools\Akiba_new_setup"


# Function to push files to the Android device
def push_files_to_device(local_path, device_path):
    adb_push_command = ["adb", "push", local_path, device_path]
    try:
        subprocess.run(adb_push_command, check=True)
        # Set executable permission if needed (example)
        # subprocess.run(["adb", "shell", "chmod", "+x", f"{device_path}/{local_path.split('/')[-1]}"])
    except subprocess.CalledProcessError as e:
        if e.stderr:
            print(f"Error pushing {local_path} to {device_path}:")
            print(e.stderr.decode())
        else:
            print(f"Error pushing {local_path} to {device_path}: No error message provided.")

# Function to execute the shell script on the Android device
def execute_shell_script_on_android(script_path):
    # Push required files to the device
    push_files_to_device(r"C:\platform-tools\Akiba_new_setup\dev900.ovpn", "/sdcard/")
    push_files_to_device(r"C:\platform-tools\Akiba_new_setup\debian_stretch_rootfs_release_20200309.tgz", "/sdcard/")

    # Wait for a few seconds to ensure files are transferred
    time.sleep(5)

    # Push the shell script to the device
    push_files_to_device(script_path, "/sdcard/")

    # Get the filename of the script from the path
    script_filename = script_path.split('\\')[-1]

    # Construct the ADB command to execute the shell script
    run_command = ["adb", "shell", "sh", f"/sdcard/{script_filename}"]

    try:
        # Execute the shell script on the device
        result = subprocess.run(run_command, check=True, capture_output=True, text=True)
        print("Shell script executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing shell script:")
        if e.stderr:
            print(e.stderr)
        else:
            print("No error message provided.")

# Example usage: Replace with the actual path to your shell script on your local machine
sh_script_path = r"C:\platform-tools\Akiba_new_setup\1_Kandel_setup.sh"
execute_shell_script_on_android(sh_script_path)



