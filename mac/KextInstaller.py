import os
import os.path
from os import path
import platform

def warn ():
	print("OS => ", platform.system())
	print("Version => ", platform.mac_ver()[0])
	print("Installing dependencies...")
	print("Needing Superuser Permissions... only once")

def detect():
	# return  && os.system("")
	return path.exists("/Library/Extensions/Soundflower.kext") and not bool(os.system("kextstat | grep Soundflower"))
	# return bool(os.system("kextstat | grep smbfs"))

def install():
	os.system("sudo cp -R ./Soundflower.kext /Library/Extensions")
	os.system("sudo chown -R root:wheel /Library/Extensions/Soundflower.kext")
	os.system("sudo kextload /Library/Extensions/Soundflower.kext")

def delete():
	# os.system("osacript ./delete.scpt")
	os.system("sudo kextunload /Library/Extensions/Soundflower.kext")
	os.system("sudo rm -rf /Library/Extensions/Soundflower.kext")

def upgrade():
	delete()
	if not detect():
		install()

def main():
	warn()
	install()

	print("Done...")

if __name__ == '__main__':
	main()