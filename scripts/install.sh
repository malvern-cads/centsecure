DESTINATION="/opt/centsecure"
ZIP_FILE="centsecure.zip"

echo "CentSecure Installer"

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Install dependencies
echo "Installing dependencies (1/2)..."
apt install software-properties-common apt-transport-https -y
add-apt-repository ppa:deadsnakes/ppa
apt update
apt install unzip python3.8 python3.8-dev python3.8-distutils curl -y

# Unzip file to destination
echo "Extracting files..."
mkdir -p ${DESTINATION}
unzip ${ZIP_FILE} -d ${DESTINATION}
cp requirements.txt ${DESTINATION}

cd /opt/centsecure
echo "Installing dependencies (2/2)..."
python3.8 -m pip install -r requirements.txt

echo "CentSecure has been installed. To run, change directory to '${DESTINATION}' and run the command 'python3.8 centsecure.py'. Good luck!"