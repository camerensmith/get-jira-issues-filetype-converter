import easygui
import pathlib
import string
import pandas
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os
import boto3
from tkinter import Tk, filedialog
import pickle

global Dir
global awsvalue
global OutputFile

# Code that runs all the main functions
def PickFile():
    easygui.msgbox("Enter what you want to convert")
    global InputFile
    global InputFileType
    InputFile = easygui.fileopenbox(filetypes = ["*.csv", "*.json", "*.xlsx"])
    InputFileType = pathlib.Path(InputFile).suffix
    os.rename(InputFile, InputFile.translate(str.maketrans('', '', string.whitespace)))
    InputFile = InputFile.translate(str.maketrans('', '', string.whitespace))
    PossibleConversions = [".json", ".csv", ".xlsx"]
    PossibleConversions.remove(InputFileType)
    if InputFileType == ".json" or InputFileType == ".csv" or InputFileType == ".xlsx":
        ConvertChoice = easygui.buttonbox(msg="What would you like to convert to?" + " Input file:" + str(InputFile), choices=(PossibleConversions[0], PossibleConversions[1]))
        return ConvertChoice
    else:
        # This *should* be impossible to call
        easygui.msgbox("ERROR: Unexpected File Format Entered")
        PickFile()

def aws():

    if awsvalue == True:
        s3 = boto3.client("s3")
        with open(OutputFile, "rb") as f:
            # My Bucket for testing was called "thereismore" replace it with your one.
            s3.upload_fileobj(f, "thereismore", "/")



def GoogleDrive():
    # This is all pretty rough, but it should work
    # I wasn't able to configure it to work with my account as it isn't set up correctly
    # The code is set up to upload an entire folder, one file at a time to a users drive.
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    path = Folder
    for x in os.listdir(path):
        f = drive.CreateFile({'title': x})
        f.SetContentFile(os.path.join(path, x))
        f.Upload()
        f = None

# This does work
def csvtojson():
    global OutputFile
    csv = pandas.read_csv(InputFile)
    csv.to_json(str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".json")
    OutputFile = (str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".json")
    aws()

def csvtoxlsx():
    global OutputFile
    csv = pandas.read_csv(InputFile)
    csv.to_excel(str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".xlsx")
    OutputFile = (str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".xlsx")
    aws()
def jsontoxlsx():
    global OutputFile
    json = pandas.read_json(InputFile, lines=True, orient="records")
    json.to_excel(str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".xlsx")
    OutputFile = (str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".xlsx")
    aws()
def xlsxtocsv():
    global OutputFile
    xlsx = pandas.read_excel(InputFile)
    xlsx.to_csv(str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".csv")
    OutputFile = (str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".csv")
    aws()
def xlsxtojson():
    global OutputFile
    xlsx = pandas.read_excel(InputFile)
    xlsx.to_json(str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".json")
    OutputFile = (str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".json")
    aws()

# I removed the package that this needs to work, but I thought I may as well leave it just in case.
def xlsxtoxls():
    xlsx = pandas.read_excel(InputFile)
    xlsx.to_xls(str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".xls")
    aws()

# This *might* work
def jsontocsv():
    global OutputFile
    with open(InputFile, encoding='utf-8') as inputfile:
        df = pandas.read_json(inputfile)

    df.to_csv(str(Dir) + "/" + (pathlib.Path(InputFile).stem) + ".csv", encoding='utf-8', index=False)
    OutputFile = (str(Dir) + "/" + (pathlib.Path(InputFile).stem) + ".csv")
    aws()

def difficultconversion():
    ConvertChoice = PickFile()
    print(ConvertChoice)
    global OutputFile

    if ConvertChoice == ".json" and InputFileType == ".csv":
        csvtojson()
        easygui.msgbox("File Converted at" + str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".json")

    elif ConvertChoice == ".csv" and InputFileType == ".json":
        easygui.msgbox("This feature is still in development, so it might not work!")
        jsontocsv()
        csvtojson() # This is complete nonsense but makes the code run, it needs to be fixed though.
        easygui.msgbox("File Converted at" + str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".csv")

    elif ConvertChoice == ".json" and InputFileType == ".xlsx":
        xlsxtojson()
        easygui.msgbox("File Converted at" + str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".json")

    elif ConvertChoice == ".csv" and InputFileType == ".xlsx":
        xlsxtocsv()
        easygui.msgbox("File Converted at" + str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".csv")

    elif ConvertChoice == ".xlsx" and InputFileType == ".csv":
        csvtoxlsx()
        easygui.msgbox("File Converted at" + str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".xlsx")

    elif ConvertChoice == ".xlsx" and InputFileType == ".json":
        jsontoxlsx()
        easygui.msgbox("File Converted at" + str(Dir) + "/" + str(pathlib.Path(InputFile).stem) + ".xlsx")


    output = InputFile
    print((str(pathlib.Path(InputFile).parent) + "/" + str(pathlib.Path(InputFile).stem) + ".csv"))

def settings():
    global Dir
    global awsvalue
    f = open('store.pckl', 'wb')
    pickle.dump(Dir, f)
    pickle.dump(awsvalue, f)
    f.close()
    Choice = easygui.buttonbox(choices=("Set Output Path", "Enable/Disable AWS", "First Time Setup", "Back"))
    if Choice == "Back":
        MainMenu()
    elif Choice == "Set Output Path":
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        Dir = filedialog.askdirectory()
        settings()
    elif Choice == "Enable/Disable AWS":
        if awsvalue != True:
            Choice = easygui.buttonbox(choices=("Enable", "Back"))
            if Choice == "Enable":
                awsvalue = True
                f2 = open('store2.pckl', 'wb')
                pickle.dump(awsvalue, f2)
                f2.close()
                settings()
            else:
                settings()
        else:
            Choice = easygui.buttonbox(choices=("Disable", "Back"))
            if Choice == "Disable":
                awsvalue = False
                f2 = open('store2.pckl', 'wb')
                pickle.dump(awsvalue, f2)
                f2.close()
                settings()
            else:
                settings()
    elif Choice == "First Time Setup":
        Dir = "/"
        awsvalue = False
        f = open('store.pckl', 'wb')
        pickle.dump(Dir, f)
        pickle.dump(awsvalue, f)
        f.close()
        f2 = open('store2.pckl', 'wb')
        pickle.dump(awsvalue, f2)
        f2.close()
        settings()

def MainMenu():
    Choice = easygui.buttonbox(Dir, choices=("Convert", "Settings"))
    if Choice == "Convert":
        difficultconversion()
    elif Choice == "Settings":
        settings()
    else:
        quit()


def OnStart():
    global OutputFile
    global Dir
    global awsvalue
    if os.path.exists("store.pckl"):
        f = open('store.pckl', 'rb')
        Dir = pickle.load(f)
        f.close()
        MainMenu()
    else:
        Dir = "/"
        awsvalue = False
        f = open('store.pckl', 'wb')
        pickle.dump(Dir, f)
        pickle.dump(awsvalue, f)
        f.close()
        MainMenu()

    if os.path.exists("store2.pckl"):
        f2 = open('store2.pckl', 'rb')
        awsvalue = pickle.load(f2)
        f2.close()
        MainMenu()
    else:
        awsvalue = False
        f2 = open('store2.pckl', 'wb')
        pickle.dump(awsvalue, f2)
        f2.close()
        MainMenu()

if os.path.exists("store2.pckl"):
    f2 = open('store2.pckl', 'rb')
    awsvalue = pickle.load(f2)
    f2.close()
else:
    awsvalue = False
    f2 = open('store2.pckl', 'wb')
    pickle.dump(awsvalue, f2)
    f2.close()

OnStart()
