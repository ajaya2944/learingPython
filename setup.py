import subprocess

# Define the path to the adb executable and the shell script
adb_path = 'C:\Users\owner\Desktop\picosetup'  # Replace with the actual path to your adb executable
shell_script_path = 'C:\\Users\\owner\\Desktop\\picosetup\\1_Kandel_setup.sh'
android_script_path = '/data/local/tmp/1_Kandel_setup.sh'  # Temporary path on Android device

# Push the shell script to the Android device
subprocess.run([adb_path, 'push', shell_script_path, android_script_path])

# Change the permissions of the shell script to make it executable
subprocess.run([adb_path, 'shell', 'chmod', '755', android_script_path])

# Execute the shell script on the Android device
subprocess.run([adb_path, 'shell', 'sh', android_script_path])