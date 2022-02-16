import os
import sys
import hashlib
import platform
import subprocess

BASE_GETTER_CONST = "github.com/armosec/kubescape/cautils/getter"
BE_SERVER_CONST   = BASE_GETTER_CONST + ".ArmoBEURL"
ER_SERVER_CONST   = BASE_GETTER_CONST + ".ArmoERURL"
WEBSITE_CONST     = BASE_GETTER_CONST + ".ArmoFEURL"
AUTH_SERVER_CONST = BASE_GETTER_CONST + ".armoAUTHURL"

def checkStatus(status, msg):
    if status != 0:
        sys.stderr.write(msg)
        exit(status)


def getBuildDir():
    currentPlatform = platform.system()
    buildDir = "build/"

    if currentPlatform == "Windows": buildDir += "windows-latest"
    elif currentPlatform == "Linux": buildDir += "ubuntu-latest"
    elif currentPlatform == "Darwin": buildDir += "macos-latest"
    else: raise OSError("Platform %s is not supported!" % (currentPlatform))

    return buildDir

def getPackageName():
    packageName = "kubescape"
    # if platform.system() == "Windows": packageName += ".exe"

    return packageName


def main():
    print("Building Kubescape")

    # print environment variables
    # print(os.environ)

    # Set some variables
    packageName = getPackageName()
    buildUrl = "github.com/armosec/kubescape/cautils.BuildNumber"
    releaseVersion = os.getenv("RELEASE")
    ArmoBEServer = os.getenv("ArmoBEServer")
    ArmoERServer = os.getenv("ArmoERServer")
    ArmoWebsite = os.getenv("ArmoWebsite")
    ArmoAuthServer = os.getenv("ArmoAuthServer")

    ks_file = os.path.join(buildDir, packageName)
    hash_file = os.path.join(buildDir, packageName + ".sha256")

    # Create build directory
    buildDir = getBuildDir()

    if not os.path.isdir(buildDir):
        os.makedirs(buildDir)

    # Build kubescape
    ldflags = "-w -s -X %s=%s -X %s=%s -X %s=%s -X %s=%s -X %s=%s" \
        % (buildUrl, releaseVersion, BE_SERVER_CONST, ArmoBEServer,
           ER_SERVER_CONST, ArmoERServer, WEBSITE_CONST, ArmoWebsite,
           AUTH_SERVER_CONST, ArmoAuthServer)

    print("Building kubescape and saving here: {}".format(ks_file))
    status = subprocess.call(["go", "build", "-o", ks_file, "-ldflags" ,ldflags])
    checkStatus(status, "Failed to build kubescape")
    
    sha256 = hashlib.sha256()
    with open(ks_file, "rb") as kube:
        sha256.update(kube.read())
        with open(hash_file, "w") as kube_sha:
            hash = sha256.hexdigest()
            print("kubescape hash: {}, file: {}".format(hash, hash_file))
            kube_sha.write(sha256.hexdigest())

    print("Build Done")
 
 
if __name__ == "__main__":
    main()
