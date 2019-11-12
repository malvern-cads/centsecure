echo "CentSecure Installer"

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Install dependencies
echo "Installing python and dependencies..."
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install python3-pip python3.7 -y

# The python modules that we require
python3.7 -m pip install colorama

echo "CentSecure has been installed. Make sure you're in the main CentSecure folder and run the command 'python3.7 centsecure.py'. Good luck!"
