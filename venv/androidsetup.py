import subprocess

# Full paths to the APK files and their package names
apk_info = [
    {"path": r"C:\platform-tools\OpenVPN.apk", "package": "net.openvpn.openvpn"},
    {"path": r"C:\platform-tools\tukpy_rev_26974.apk", "package": "az.osmdroidprop"}
]

# Function to uninstall and then install an APK
def reinstall_apk(apk_path, package_name):
    # Uninstall the existing APK
    uninstall_command = ["adb", "uninstall", package_name]
    uninstall_process = subprocess.Popen(uninstall_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    uninstall_stdout, uninstall_stderr = uninstall_process.communicate()

    if uninstall_process.returncode == 0:
        print(f"Uninstalled the existing app with package name {package_name}")
    else:
        # If uninstallation fails, print the error message and continue
        print(f"Failed to uninstall app with package name {package_name}:")
        print(uninstall_stderr.decode())

    # Install the new APK
    install_command = ["adb", "install", apk_path]
    install_process = subprocess.Popen(install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    install_stdout, install_stderr = install_process.communicate()

    if install_process.returncode == 0:
        print(f"Installed {apk_path} with package name {package_name}")
    else:
        # If installation fails, print the error message
        print(f"Error installing {apk_path}:")
        print(install_stderr.decode())

# Reinstall each APK by iterating over the apk_info list
for apk in apk_info:
    reinstall_apk(apk["path"], apk["package"])
