import subprocess
import re
import os

def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip()

def check_latest_version(provider_namespace, resource_type, api_version):
    command = f"az provider show --namespace {provider_namespace} --query \"resourceTypes[?resourceType=='{resource_type}'].apiVersions\" -o tsv"
    all_versions = run_command(command)

    if not all_versions:
        all_versions_list = []
        latest_supported_version = "N/A"
    else:
        all_versions_list = all_versions.split()
        non_preview_versions = [v for v in all_versions_list if "preview" not in v]
        latest_supported_version = non_preview_versions[0] if non_preview_versions else all_versions_list[0]

    if "preview" in api_version:
        color = "\033[0;31m"
        status = "Preview"
    elif api_version not in all_versions_list:
        color = "\033[0;33m"
        status = "Deprecated"
    elif latest_supported_version != "N/A" and latest_supported_version != api_version:
        color = "\033[0;33m"
        status = "Not Latest"
    else:
        color = "\033[0;32m"
        status = "Latest"

    print(f"{color}API: {provider_namespace}/{resource_type}")
    print(f"Current Version: {api_version}")
    print(f"Latest Supported Version: {latest_supported_version} ({status})\033[0m")
    print("----------------------------------------")

def find_and_check_bicep_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".bicep"):
                bicep_file = os.path.join(root, file)
                print(f"Ejecutando script para el archivo: {bicep_file}")
                print(f"Checking {bicep_file} for API versions...")
                with open(bicep_file, 'r') as f:
                    content = f.read()
                    api_versions = re.findall(r"Microsoft\.\w+/\w+@[^ ]+", content)
                for line in sorted(set(api_versions)):
                    provider_namespace = re.split('[@/]', line)[0]
                    resource_type = re.split('[@/]', line)[1]
                    api_version = re.split('[@/]', line)[2].strip("'")
                    check_latest_version(provider_namespace, resource_type, api_version)

find_and_check_bicep_files(".")

