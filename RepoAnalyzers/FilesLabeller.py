import pandas
import subprocess

# TODO: run this on AI and non-AI
def processfiles():

    with open("..\\CSV Files\\ReposLabeller\\Top1000AIMLProjectsFiles.csv","rb") as configFile:
        files_dataframe=pandas.read_csv(configFile,usecols=["ID","ProjectName","FilePath","FileName","Extension"],error_bad_lines=False, encoding="utf-8")

    output_files_list = open("../CSV Files/" + str("AIFilesLabelled") + ".csv", "w+", newline='', encoding="utf-8")
    output_files_list.write("ID,ProjectName,FilePath,FileName,FileType,FileLanguage\n")

    for index,row in files_dataframe.iterrows():
        ID=row["ID"]
        Project_Name=row["ProjectName"]
        File_Path=row["FilePath"]
        File_Name=row["FileName"]
        command = "github-linguist  \""+str(File_Path)+"\" " # command to be executed
        res = subprocess.check_output(command,shell=True)  # system command
        output = res.decode("utf-8")
        # print(output)
        arr1 = output.split("\n")
        # type
        arrType = arr1[1].split(":")
        type=arrType[1].strip()
        # language
        arrLang = arr1[3].split(":")
        language=arrLang[1].strip()
        if(language.strip() == ""):
            language="Unknown"
        output_files_list.write(str(ID)+","+str(Project_Name)+","+str(File_Path)+","+str(File_Name)+","+str(type)+","+str(language)+"\n")
        print(str(ID)+","+str(Project_Name)+","+str(File_Path)+","+str(File_Name)+","+str(type)+","+str(language))
        output_files_list.flush()

def processfiles2():

    with open("..\\CSV Files\\ReposLabeller\\Top1000NoAIMLProjectsFiles.csv","rb") as configFile:
        files_dataframe=pandas.read_csv(configFile,usecols=["ID","ProjectName","FilePath","FileName","Extension"],error_bad_lines=False, encoding="utf-8")

    output_files_list = open("../CSV Files/" + str("NoAIFilesLabelled") + ".csv", "w+", newline='', encoding="utf-8")
    output_files_list.write("ID,ProjectName,FilePath,FileName,FileType,FileLanguage\n")

    for index,row in files_dataframe.iterrows():
        ID=row["ID"]
        Project_Name=row["ProjectName"]
        File_Path=row["FilePath"]
        File_Name=row["FileName"]
        command = "github-linguist  \""+str(File_Path)+"\" " # command to be executed
        res = subprocess.check_output(command,shell=True)  # system command
        output = res.decode("utf-8")
        # print(output)
        arr1 = output.split("\n")
        # type
        arrType = arr1[1].split(":")
        type=arrType[1].strip()
        # language
        arrLang = arr1[3].split(":")
        language=arrLang[1].strip()
        if(language.strip() == ""):
            language="Unknown"
        output_files_list.write(str(ID)+","+str(Project_Name)+","+str(File_Path)+","+str(File_Name)+","+str(type)+","+str(language)+"\n")
        print(str(ID)+","+str(Project_Name)+","+str(File_Path)+","+str(File_Name)+","+str(type)+","+str(language))
        output_files_list.flush()
#
# filepath="E:\\PhD Work\\repos\\tool\\oracle\\Skater\\examples\\image_interpretability\\self_driving_toy_example\\drive_trial_2\\steer\\003369.txt"
# command = "github-linguist \""+str(filepath)+"\""  # command to be executed
# try:
#     res = subprocess.check_output(command, shell=True,stderr=subprocess.STDOUT)  # system command
# except subprocess.CalledProcessError as e:
#     raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

# print("Return type: ", type(res))  # type of the value returned
# print("Decoded string: ", res.decode("utf-8"))# decoded resul
# output=res.decode("utf-8")
# arr1=output.split("\n")
# # type
# arrType=arr1[1].split(":")
# print(arrType[1].strip())
# # language
# arrLang=arr1[3].split(":")
# print(arrLang[1].strip())
processfiles()
processfiles2()