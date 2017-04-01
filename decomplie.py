# coding=utf-8
import subprocess
from os import path
import glob

apkPath = "kongzhongjr.apk"
apkOutput = "output"
decompiler = ""

# use apkTools
subprocess.call(("java -jar ./lib/apktool.jar d " + apkPath + " -s " + "-o " + apkOutput).split(" "))

dexFiles = glob.glob1(apkOutput, '*.dex')
jarFilePaths = []
for dexFile in dexFiles:
    # use dex2jar
    jarFilePath = path.join(apkOutput, path.splitext(path.basename(dexFile))[0] + '.jar')
    jarFilePaths.append(jarFilePath)
    subprocess.call(("lib/dex2jar-2.0/d2j-dex2jar.sh " + path.join(apkOutput, dexFile)
                     + " -o " + jarFilePath).split(" "))

# todo add more decompiler
# use java decompiler


#   JDCore (very fast)
#   CFR (very good and well-supported decompiler for Java 8)
#   Jadx, fast and with Android support
#   Procyon
#   Fernflower
#   JAD (very fast, but outdated)
def cfr(jar_file_path, output_path):
    subprocess.call(("java -jar lib/cfr.jar " + jar_file_path + " --outputdir " + output_path).split(" "))


# 效率慢，出错多，还会卡死，最好每个class分别编译，就不会死
def fernflower(jar_file_path, output_path):
    subprocess.call(("java -jar lib/fernflower.jar " + jar_file_path + " " + output_path).split(" "))


for jarFilePath in jarFilePaths:
    cfr(jarFilePath, path.join(apkOutput, 'java'))

