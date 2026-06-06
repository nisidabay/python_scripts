#!/usr/bin/env bash
#
# setup_environments.sh
# This script sets up the new environments for the project, installs the
# requirements, and makes the script executable

set -euo pipefail # Exit on error, treat unset variables as an error, and fail on pipe errors

trap 'echo "Error on line $LINENO"' ERR
PROJECT_ROOT=$(pwd)
LOG_FILE="$PROJECT_ROOT/setup.log"

# Function to check if a command exists
command_exists() {
	command -v "$1" >/dev/null 2>&1
}

# Ensure required commands are available
for cmd in python3 pip sed; do
	if ! command_exists "$cmd"; then
		echo "Error: $cmd is not installed." >&2
		exit 1
	fi
done

# Function to setup a specific component
create_venv() {
	local component=$1
	local requirements=$2
	echo "Setting up $component..." | tee -a "$LOG_FILE"
	
	# Create new venv
	python3 -m venv "$component"
	
	# Upgrade pip first to avoid the notice
	echo "Upgrading pip..." | tee -a "$LOG_FILE"
	"$component/bin/python3" -m pip install --upgrade pip
	
	# Install requirements
	echo "Installing requirements..." | tee -a "$LOG_FILE"
	if ! "$component/bin/pip" install -r "$PROJECT_ROOT/requirements/$requirements"; then
		echo "Error installing requirements for $component, but continuing..." | tee -a "$LOG_FILE"
	fi
	
	# Env shebang
	local env_shebang
	env_shebang="$PROJECT_ROOT/$component/bin/python3"
	
	# Update or add shebang in python files
	echo "Updating shebangs..." | tee -a "$LOG_FILE"
	if [[ "$OSTYPE" == "darwin"* ]]; then
		# macOS version (BSD sed)
		# First check if shebang exists and replace it
		find "$component" -name "*.py" -type f -exec sed -i '' '1s|^#!.*$|#!'"$env_shebang"'|' {} \;
		# Then add shebang to files that don't have one
		find "$component" -name "*.py" -type f -exec sh -c 'if [ "$(head -1 "$1" | grep -c "^#!")" -eq 0 ]; then sed -i "" "1i\\
#!'"$env_shebang"'" "$1"; fi' sh {} \;
	else
		# Linux version (GNU sed)
		# First check if shebang exists and replace it
		find "$component" -name "*.py" -type f -exec sed -i '1s|^#!.*$|#!'"$env_shebang"'|' {} \;
		# Then add shebang to files that don't have one
		find "$component" -name "*.py" -type f -exec sh -c 'if [ "$(head -1 "$1" | grep -c "^#!")" -eq 0 ]; then sed -i "1i#!'"$env_shebang"'" "$1"; fi' sh {} \;
	fi
	echo "Shebang added or modified to: $env_shebang" | tee -a "$LOG_FILE"
}

# Main execution
echo "Starting setup process" | tee -a "$LOG_FILE"

# Setup component
create_venv "env" "requirements.txt" || {
	echo "Error in setup_component, but continuing..." | tee -a "$LOG_FILE"
}

# Make all Python files executable
echo "Making Python files executable..." | tee -a "$LOG_FILE"
find . -name "*.py" -type f -exec chmod +x {} \;
echo "Setup process complete!" | tee -a "$LOG_FILE"
exit 0
