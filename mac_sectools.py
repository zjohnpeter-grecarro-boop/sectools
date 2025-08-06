# This script is created by Gab for the benefit of ESS. The aim is to get basic info such as hostname,
# username, OS version, PC hardware make and installed AV and other applications as part of the attestation process. The output can be verified by the user 
# prior to submission to MISG. Use freely but ErnstGV will take no responsibility from any undesired effect. Thank you.



import datetime
import os
import hashlib
import getpass # Import the getpass module for a more robust way to get the username

def serialnumberfunc():
    """Gets the Mac's serial number."""
    try:
        serialnumberstream = os.popen('system_profiler SPHardwareDataType | grep "Serial Number"')
        serialnumber = serialnumberstream.read().strip()
        serialnumberstream.close()
        return serialnumber
    except Exception as e:
        return f"Error getting serial number: {e}"

def systemversionfunc():
    """Gets the macOS system version."""
    try:
        systemversion_stream = os.popen('system_profiler SPSoftwareDataType | grep "System Version"')
        systemversion = systemversion_stream.read().strip()
        systemversion_stream.close()
        return systemversion
    except Exception as e:
        return f"Error getting system version: {e}"

def applistfunc():
    """Gets a list of applications in the /Applications directory."""
    try:
        appliststream = os.popen("system_profiler SPApplicationsDataType | grep 'Location: /Applications' | sed 's/Location://g' | sed -e 's/^[ \t]*//'")
        applist = appliststream.read().strip()
        appliststream.close()
        return applist
    except Exception as e:
        return f"Error getting application list: {e}"

def md5checksum(fname):
    """Calculates the MD5 hash of a file."""
    md5hash = hashlib.md5()
    try:
        with open(fname, "rb") as filetohash:
            for byte_block in iter(lambda: filetohash.read(4096), b""):
                md5hash.update(byte_block)
        return md5hash.hexdigest()
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error calculating MD5: {e}"

def startfunc():
    """Main function to gather system info, save it to a file, and generate a checksum."""
    timestampnow = datetime.datetime.today().strftime("%m%d%Y%H%M%s")
    myhostname = os.uname()[1]
    
    # --- CHANGE START ---
    # Replaced os.getlogin() with getpass.getuser() for better reliability.
    try:
        myusername = getpass.getuser()
    except Exception:
        myusername = "UnknownUser"
    # --- CHANGE END ---

    myfilename = f"{myhostname}_{timestampnow}.txt"

    systemversionout = systemversionfunc()
    serialnumberout = serialnumberfunc()
    myapplist = applistfunc()

    outfile = open(myfilename, "w")
    outfile.writelines(f"Timestamp: {timestampnow}\n\n")
    outfile.writelines(f"Hostname: {myhostname}\n\n")
    outfile.writelines(f"Username: {myusername}\n\n")
    outfile.writelines(f"{systemversionout}\n")
    outfile.writelines(f"{serialnumberout}\n")
    outfile.writelines("\n")
    outfile.writelines("List of Applications \n\n")
    outfile.writelines(f"{myapplist}\n\n")
    outfile.close()

    outputfilepath = os.path.abspath(myfilename)

    submission_step = f''' 
                        #####  SUBMISSION INSTRUCTIONS  ####
                        
                        To OTS: Please take a screenshot of the hash output below between
                        BEGIN and END marker then send to SecAdmin via Email or TG group 
                        chat with the name of the user.

                        To EndUser: Please fillup the form that will be provided by SecAdmin.
                        In that same form, upload the generated output file from -> {outputfilepath}
                        That is usually the same directory where the script has executed.
                        Do not modify the content of {myfilename}. The hash will be counterchecked by SecAdmin.
    '''

    print(submission_step + "\n")

    md5result = md5checksum(myfilename)

    print("------------------------------------------ BEGIN ----------------------------------------------------\n")
    print(f"               {myfilename} : {md5result}\n")
    print("------------------------------------------- END -----------------------------------------------------")
    print("\n\n\n")

if __name__ == "__main__":
    startfunc()
