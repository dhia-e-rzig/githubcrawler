import json
from datetime import datetime

import pandas
import re

type_c_code_ext = ['.c', '.cpp', '.c++', '.cc', '.h', '.hpp', '.hh', '.h']
cs_code_ext = ['.cs']
java_code_ext = ['.java']
python_code_ext = ['.py', '.pyi', '.pyw', '.pyx', '.pxd']
r_code_ext = ['.r', '.rd', '.profile']
ruby_code_ext = ['.ru', '.rb']
ignored_ext=['.gitignore', 'README.md', 'LICENSE', "AUTHORS", "CONTRIBUTORS", "PATENTS", "OWNERS", "SECURITY_CONTACTS", "NOTICE", "Readme", ".DS_Store", ".gitattributes", "CODEOWNERS", ".gitkeep", ".gitmodules", "GOLANG_CONTRIBUTORS"]

ctypetool_found = False
csharptool_found = False
javatool_found = False
pythontool_found = False
rtool_found = False
rubytool_found = False


def analyze_type_c_file(dirpath):
    # print('c-analysis')
    # print(dirpath)
    toolList=set()
    with open("..\\Excel Files\\TestTools.csv", "r") as configFile:
        test_exts = pandas.read_csv(configFile)
    try:
        f = open(dirpath, "r",encoding='utf-8', errors='ignore')
        l = f.readline()
        statements = test_exts.loc[test_exts['Language'].isin(['C','C++','Obj-C'])]['Statement']
        while ("{" not in l) and (l!=''):
            for  statement in statements:
                p = re.compile(statement, re.IGNORECASE)
                m=p.match(l)
                l = f.readline()
                if m:
                    tool=''
                    templ=test_exts.loc[test_exts['Statement']==statement]['Tool'].values
                    if (isinstance(templ, list)):
                        tool = str(templ[0]).replace('[', '').replace(']', '')
                    else:
                        tool = str(templ).replace('[', '').replace(']', '')
                    # f.close()
                    toolList.add(tool)
        f.close()
        if(len(toolList)>=0):
            return (True,toolList)
        else:
            return (False,toolList)
    except Exception  as e :
        print(e)
    return (False, toolList)

def analyze_csharp_file(dirpath):
    # print('cs-analysis')
    # print(dirpath)
    toolList=set()
    with open("..\\Excel Files\\TestTools.csv", "r") as configFile:
        test_exts = pandas.read_csv(configFile)
    try:
        f = open(dirpath, "r",encoding='utf-8', errors='ignore')
        l = f.readline()
        statements = test_exts.loc[test_exts['Language'].isin(['C#'])]['Statement']
        while "{" not in l and (l!=''):
            for statement in statements:
                p = re.compile(statement, re.IGNORECASE)
                m = p.match(l)
                l = f.readline()
                if m:
                    tool = ''
                    templ = test_exts.loc[test_exts['Statement']==statement]['Tool'].values
                    if (isinstance(templ, list)):
                        tool = str(templ[0]).replace('[', '').replace(']', '')
                    else:
                        tool = str(templ).replace('[', '').replace(']', '')
                    toolList.add(tool)
        f.close()
        if (len(toolList) >= 0):
            return (True, toolList)
        else:
            return (False, toolList)
    except Exception  as e :
        print(e)
    return (False, toolList)


def analyze_java_file(dirpath):
    # print('cs-analysis')
    # print(dirpath)
    toolList=set()
    with open("..\\Excel Files\\TestTools.csv", "r") as configFile:
        test_exts = pandas.read_csv(configFile)
    try:
        f = open(dirpath, "r",encoding='utf-8', errors='ignore')
        l = f.readline()
        statements = test_exts.loc[test_exts['Language'].isin(['Java'])]['Statement']
        while "{" not in l and (l!=''):
            for statement in statements:
                p = re.compile(statement, re.IGNORECASE)
                m = p.match(l)
                l = f.readline()
                if m:
                    tool=''
                    templ = test_exts.loc[test_exts['Statement']==statement]['Tool'].values
                    if (isinstance(templ, list)):
                        tool = str(templ[0]).replace('[', '').replace(']', '')
                    else:
                        tool = str(templ).replace('[', '').replace(']', '')
                    toolList.add(tool)
        f.close()
        if (len(toolList) >= 0):
            return (True, toolList)
        else:
            return (False, toolList)
    except Exception  as e :
        print(e)
    return (False, toolList)


def analyze_python_file(dirpath):
    # print('py-analysis')
    # print(dirpath)
    toolList=set()
    with open("..\\Excel Files\\TestTools.csv", "r") as configFile:
        test_exts = pandas.read_csv(configFile)

    try:

        f = open(dirpath, "r",encoding='utf-8', errors='ignore')
        l = f.readline()
        statements = test_exts.loc[test_exts['Language'].isin(['Python'])]['Statement']
        while ("import" in l) or ("from" in l) or (l == "\n") or (l.isspace()) or(l.startswith('#')):
            for statement in statements:
                tool=''
                p = re.compile(statement, re.IGNORECASE)
                m = p.match(l)
                l = f.readline()
                if m:
                    templ = test_exts.loc[test_exts['Statement'] == statement]['Tool'].values
                    if (isinstance(templ, list)):
                        tool = str(templ[0]).replace('[', '').replace(']', '')
                    else:
                        tool = str(templ).replace('[', '').replace(']', '')
                    toolList.add(tool)
        f.close()
        if (len(toolList) >= 0):
            return (True, toolList)
        else:
            return (False, toolList)
    except Exception  as e :
        print(e)
    return (False, toolList)

def analyze_r_file(dirpath):
    # print('r-analysis')
    # print(dirpath)
    toolList=set()
    with open("..\\Excel Files\\TestTools.csv", "r") as configFile:
        test_exts = pandas.read_csv(configFile)
    try:
        f = open(dirpath, "r",encoding='utf-8', errors='ignore')
        l = f.readline()
        statements = test_exts.loc[test_exts['Language'].isin(['R'])]['Statement']
        while l != '':
            for statement in statements:
                tool=''
                p = re.compile(statement, re.IGNORECASE)
                m = p.match(l)
                l = f.readline()
                if m:
                    # templ = test_exts.loc[test_exts['Statement'] == statement]['Tool'].values
                    tool = 'testthat'
                    toolList.add(tool)
        f.close()
        if (len(toolList) >= 0):
            return (True, toolList)
        else:
            return (False, toolList)
    except Exception  as e :
        print(e)
    return (False, toolList)


def analyze_ruby_tool(dirpath):
    # print('ru-analysis')
    # print(dirpath)
    toolList=set()
    with open("..\\Excel Files\\TestTools.csv", "r") as configFile:
        test_exts = pandas.read_csv(configFile)
    try:
        f = open(dirpath, "r",encoding='utf-8', errors='ignore')
        l = f.readline()
        statements = test_exts.loc[test_exts['Language'].isin(['Ruby'])]['Statement']
        while ("require" in l) or (l == "\n") or (l.isspace()) or(l.startswith('#')):
            for statement in statements:
                p = re.compile(statement, re.IGNORECASE)
                m = p.match(l)
                l = f.readline()
                if m:
                    tool=''
                    templ = test_exts.loc[test_exts['Statement'] == statement]['Tool'].values
                    if (isinstance(templ, list)):
                        tool = str(templ[0]).replace('[', '').replace(']', '')
                    else:
                        tool = str(templ).replace('[', '').replace(']', '')
                    toolList.add(tool)
        f.close()
        if (len(toolList) >= 0):
            return (True, toolList)
        else:
            return (False, toolList)
    except Exception  as e :
        print(e)
    return (False, toolList)


def detect_test_tools(dirpath, filename, projectname, output_file):
    global ctypetool_found, csharptool_found, pythontool_found, rtool_found, rubytool_found, javatool_found
    filename = str(filename).strip()

    # if ".git" in dirpath:
    #     return
    # if ".idea" in dirpath:
    #     return
    # if ".vscode" in dirpath:
    #     return
    for iext in ignored_ext:
        if filename == iext:
            return

    if("ansible.cfg"==filename):
        string = projectname + ";" + dirpath + ";" + 'Ansible' + "\n"
        output_file.write(str(string))
        return
    for cext in type_c_code_ext:
        if ('test' in dirpath.lower() or 'spec' in dirpath.lower()) and filename.lower().endswith(cext):
            if (ctypetool_found == False)or True:
                (ctypetool_found, tools) = analyze_type_c_file(dirpath)
                if (ctypetool_found):
                    for tool in tools:
                        string = str(projectname) + ";" + str(dirpath) + ";" + tool + "\n"
                        print(string)
                        output_file.write(str(string))
                        output_file.flush()
                        return
            return


    for csext in cs_code_ext:
        if ('test' in dirpath.lower() or 'spec' in dirpath.lower()) and filename.lower().endswith(csext):
            if (csharptool_found == False)or True:
                (csharptool_found, tools) = analyze_csharp_file(dirpath)
                if (csharptool_found):
                    for tool in tools:
                        string = str(projectname) + ";" + str(dirpath) + ";" + tool + "\n"
                        print(string)
                        output_file.write(str(string))
                        output_file.flush()
                        return
            return
    for pyext in python_code_ext:
        if ('test' in dirpath.lower() or 'spec' in dirpath.lower()) and filename.lower().endswith(pyext):
            if (pythontool_found == False) or True:
                (pythontool_found, tools) = analyze_python_file(dirpath)
                if (pythontool_found):
                    for tool in tools:
                        string = str(projectname) + ";" + str(dirpath) + ";" + tool  + "\n"
                        print(string)
                        output_file.write(str(string))
                        output_file.flush()
                        return
            return
    for jext in java_code_ext:
        if ('test' in dirpath.lower() or 'spec' in dirpath.lower()) and filename.lower().endswith(jext):
            if (javatool_found == False) or True:
                (javatool_found, tools) = analyze_java_file(dirpath)
                if (javatool_found):
                    for tool in tools:
                        string = str(projectname) + ";" + str(dirpath) + ";" + tool  + "\n"
                        print(string)
                        output_file.write(str(string))
                        output_file.flush()
                        return
            return

    for rext in r_code_ext:
        if ('test' in dirpath.lower() or 'spec' in dirpath.lower()) and filename.lower().endswith(rext):
            if (rtool_found == False) or True:
                (rtool_found, tools) = analyze_r_file(dirpath)
                if (rtool_found):
                    for tool in tools:
                        string = str(projectname) + ";" + str(dirpath) + ";" + tool + "\n"
                        print(string)
                        output_file.write(str(string))
                        output_file.flush()
                        return
            return


    for rubyext in ruby_code_ext:
        if ('test' in dirpath.lower() or 'spec' in dirpath.lower()) and filename.lower().endswith(rubyext):
            if (rubytool_found == False) or True:
                (rubytool_found, tools) = analyze_ruby_tool(dirpath)
                if (rubytool_found):
                    for tool in tools:
                        string = str(projectname) + ";" + str(dirpath) + ";" + tool + "\n"
                        print(string)
                        output_file.write(str(string))
                        output_file.flush()
                        return
            return
    return




#Main
i=2
listOfTypes=["applied","tool","no-ai-ml"]
type=listOfTypes[i]
# type1='Top1000AIML'
# type2='Top1000NoAIML'
x = datetime.now()
time = x.strftime("%x-%X").replace(":", "-").replace("/", "-")
outfile1= open("../CSV Files/TestTools"+type+'-'+time+'.csv','w+')
outfile1.write("ProjectName;FilePath;TestTool\n")
outfile1.flush()
# outfile2= open("../CSV Files/TestTools"+type2+'-'+time+'.csv','w+')
# outfile2.write("ProjectName;FilePath;TestTool;\n")
# outfile2.flush()
with open("../JSON Files/lastOutputForType" + str(i) + ".json", 'r+') as infile:
    lastfilename = json.load(infile)
fs_df = pandas.read_csv(lastfilename, usecols=["ProjectName", "FilePath", "FileName", "Extension"],sep=",")

# fs_df = pandas.read_csv('../CSV Files/ReposLabeller/Top1000AIMLProjectsFiles.csv', usecols=["ProjectName", "FilePath", "FileName", "Extension"])
# fs_df2 = pandas.read_csv('../CSV Files/ReposLabeller/Top1000NoAIMLProjectsFiles.csv', usecols=["ProjectName", "FilePath", "FileName", "Extension"])

old_project=""
for index, row in fs_df.iterrows():
    if(old_project!=row['ProjectName']):
        ctypetool_found = False
        csharptool_found = False
        javatool_found = False
        pythontool_found = False
        rtool_found = False
        rubytool_found = False
        old_project=row['ProjectName']
    # path=row['FilePath']
    # arr = path.split("\\")
    # filename = arr[-1]
    detect_test_tools(row['FilePath'],row["FileName"], row['ProjectName'], outfile1)


# for index, row in fs_df2.iterrows():
#     if (old_project != row['ProjectName']):
#         ctypetool_found = False
#         csharptool_found = False
#         javatool_found = False
#         pythontool_found = False
#         rtool_found = False
#         rubytool_found = False
#         old_project = row['ProjectName']
#     detect_test_tools(row['FilePath'], row['FileName'], row['ProjectName'], outfile2)


