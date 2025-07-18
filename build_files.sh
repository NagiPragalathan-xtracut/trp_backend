# Check the installed Python version and adjust the command accordingly
PYTHON_VERSION=$(python3 --version)
if [[ $PYTHON_VERSION == *"3.12"* ]]; then
    PYTHON_COMMAND="python3.12"
elif [[ $PYTHON_VERSION == *"3.11"* ]]; then
    PYTHON_COMMAND="python3.11"
elif [[ $PYTHON_VERSION == *"3.9"* ]]; then
    PYTHON_COMMAND="python3.9"
else
    PYTHON_COMMAND="python3"  # Fallback to default Python 3 version
fi

  
# Replace `python3.11.5` with `$PYTHON_COMMAND`
$PYTHON_COMMAND manage.py collectstatic --noinput

$PYTHON_COMMAND -m pip install -r requirements.txt
# Create the output directory if it doesn't exist
mkdir -p staticfiles_build

# Move the static files into the output directory
mv media staticfiles_build
