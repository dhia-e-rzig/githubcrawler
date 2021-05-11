import json

import pandas
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
from xml.dom import minidom

# def analyzeMavenProject2( file_path):
#     # doc = minidom.parse(file_name)
#     with open(file_path,"r") as file:
#         soup = bs(file,"xml")
#     deps=""
#     depsFound=False
#     print(soup.attrs)
#     # for child in soup.children:
#     #     print(child)
#     #     print("-------")
#         # if "dependencies" in str(child):
#         #     deps=child
#         #     depsFound=True
#     if(not depsFound):
#         return
#     # for dep in deps.children:
#     #     print(dep)
#     #     print("____________")
#         # for item in list(dep):
#         #     if "artifactId" in str(item):
#         #         for conf in reference_list:
#         #             if conf == "Maven":
#         #                 continue
#         #             if str(conf).lower().strip() in str(item.text).lower().strip():
#         #                 out.write(str(project_name) +";" + str(file_path) + ";" + str(conf) + ";" + str(item.text)+"\n")
#     return


def analyzeMavenProject(project_name, file_path, reference_list, out):
    # doc = minidom.parse(file_name)
    try:
        tree = ET.parse(file_path)
        root=tree.getroot()
        deps=""
        depsFound=True
        for child in list(root):
            if "dependencies" in str(child):
                deps=child
                depsFound=True
        if(not depsFound):
            return
        for dep in list(deps):
            for item in list(dep):
                if "artifactId" in str(item):
                    for conf in reference_list:
                        if conf == "Maven":
                            continue
                        if str(conf).lower().strip() in str(item.text).lower().strip():
                            out.write(str(project_name) +";" + str(file_path) + ";" + str(conf) + ";" + str(item.text)+"\n")
        return
    except:
        with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
            dependencies_zone = False
            comment_zone = False
            for line in file:
                line=line.lower()
                if line.startswith("<!--"):
                    comment_zone = True
                if line.endswith("-->"):
                    comment_zone = False
                if comment_zone:
                    continue
                if line.startswith("<!--"):
                    continue
                if line.startswith("<!-- "):
                    continue
                if "dependencies" in line:
                    dependencies_zone = True
                if dependencies_zone:
                    for conf in reference_list:
                        if conf == "Maven":
                            continue
                        if str(conf).lower().strip() in str(line).lower().strip():
                            out.write(
                                str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
                if "/dependencies" in line:
                    dependencies_zone = False

def analyzeGradleProject(project_name,file_path, reference_list, out):
    with open(file_path,"r+",encoding="utf-8",errors="ignore") as file:
        dependencies_zone=False
        comment_zone=False
        for line in file:
            line=line.lower()
            if line.startswith("*/"):
                comment_zone=False
            if line.startswith("/*"):
                comment_zone=True
            if comment_zone:
                continue
            if line.startswith("//"):
                continue
            if line.startswith("// "):
                continue
            if "dependencies" in line:
                dependencies_zone=True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "Gradle":
                        continue
                    if str(conf).lower().strip() in str(line).lower().strip():
                        out.write(str(project_name) +";" + str(file_path) + ";" + str(conf) + ";" + line.strip()+"\n")
            if "}" in line:
                dependencies_zone=False



def analyzeRakeProject(project_name,file_path, reference_list, out):
    with open(file_path,"r+",encoding="utf-8",errors="ignore") as file:
        dependencies_zone=False
        # comment_zone=False
        for line in file:
            line=line.lower()
            # if line.startswith("*/"):
            #     comment_zone=False
            # if line.startswith("/*"):
            #     comment_zone=True
            # if comment_zone:
            #     continue
            if line.startswith("#"):
                continue
            if line.startswith("# "):
                continue
            if "dependencies" in line:
                dependencies_zone=True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "Rake":
                        continue
                    if str(conf).lower().strip() in str(line).lower().strip():
                        out.write(str(project_name) +";" + str(file_path) + ";" + str(conf) + ";" + line.strip()+"\n")
            if "end" in line:
                dependencies_zone=False

# path="D:\\PhD Work\\repos\\no-ai-ml\\javaee\\glassfish\\appserver\\tests\\embedded\\maven-plugin\\pom.xml"
# analyzeMavenProject2(path)

def analyzeAntProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        for line in file:
            line=line.lower()
            if line.startswith("<!--"):
                comment_zone = True
            if line.endswith("-->"):
                comment_zone = False
            if comment_zone:
                continue
            if line.startswith("<!--"):
                continue
            if line.startswith("<!-- "):
                continue
            if "dependency" in line:
                dependencies_zone = True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "Ant":
                        continue
                    arr=str(line).lower().strip().split("name")
                    if (len(arr) <= 1):
                        continue
                    name=arr[1].split(" ")[0]
                    if str(conf).lower().strip() in name:
                        out.write(
                            str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
            if "/>" in line:
                dependencies_zone = False


def analyzeBazelProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        for line in file:
            line=line.lower()
            # if line.startswith("<!--"):
            #     comment_zone = True
            # if line.endswith("-->"):
            #     comment_zone = False
            # if comment_zone:
            #     continue
            if line.startswith("#"):
                continue
            if line.startswith("# "):
                continue
            if "(" in line:
                dependencies_zone = True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "Bazel":
                        continue
                    arr=str(line).lower().strip().split("name")
                    if(len(arr) <=1):
                        continue
                    name=arr[1].split(" ")[0]
                    if str(conf).lower().strip() in name:
                        out.write(
                            str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
            if ")" in line:
                dependencies_zone = False


def analyzeBuckProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        for line in file:
            line=line.lower()
            # if line.startswith("<!--"):
            #     comment_zone = True
            # if line.endswith("-->"):
            #     comment_zone = False
            # if comment_zone:
            #     continue
            if line.startswith("#"):
                continue
            if line.startswith("# "):
                continue
            if "deps" in line:
                dependencies_zone = True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "Buck":
                        continue
                    s=str(line).lower().strip()
                    if str(conf).lower().strip() in s:
                        out.write(
                            str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
            if "]" in line:
                dependencies_zone = False


def analyzeCMakeProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        for line in file:
            line=line.lower()
            # if line.startswith("<!--"):
            #     comment_zone = True
            # if line.endswith("-->"):
            #     comment_zone = False
            # if comment_zone:
            #     continue
            if line.startswith("#"):
                continue
            if line.startswith("# "):
                continue
            if "find_package" or "add_executable" or "target_link_libraries" in line:
                dependencies_zone = True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "CMake":
                        continue
                    s=line.strip()
                    if str(conf).lower().strip() in s:
                        out.write(
                            str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
            if ")" in line:
                dependencies_zone = False


def analyzeIvyProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        for line in file:
            line=line.lower()
            if line.startswith("<!--"):
                comment_zone = True
            if line.endswith("-->"):
                comment_zone = False
            if comment_zone:
                continue
            if line.startswith("<!--"):
                continue
            if line.startswith("<!-- "):
                continue
            if "dependencies" in line:
                dependencies_zone = True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "Ivy":
                        continue
                    arr=str(line).lower().strip().split("name")
                    if (len(arr) <= 1):
                        continue
                    name=arr[1].split(" ")[0]
                    if str(conf).lower().strip() in name:
                        out.write(
                            str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
            if "/dependencies" in line:
                dependencies_zone = False

def analyzeJamProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        try:
            for line in file:
                line=line.lower()
                # if line.startswith("<!--"):
                #     comment_zone = True
                # if line.endswith("-->"):
                #     comment_zone = False
                # if comment_zone:
                #     continue
                if line.startswith("#"):
                    continue
                if line.startswith("# "):
                    continue
                if "import"  in line:
                    dependencies_zone = True
                if dependencies_zone:
                    for conf in reference_list:
                        if conf == "Jam":
                            continue
                        s=line.strip()
                        if str(conf).lower().strip() in s:
                            out.write(
                                str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
                if ";" in line:
                    dependencies_zone = False
        except:
            return
def analyzeMakeProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        for line in file:
            line=line.lower()
            # if line.startswith("<!--"):
            #     comment_zone = True
            # if line.endswith("-->"):
            #     comment_zone = False
            # if comment_zone:
            #     continue
            if line.startswith("#"):
                continue
            if line.startswith("# "):
                continue
            if "-l"  in line:
                dependencies_zone = True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "MakeFile":
                        continue
                    arr=line.strip().split("-l")
                    if str(conf).lower().strip() in arr[1]:
                        out.write(
                            str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
            if line.endswith("\n"):
                dependencies_zone = False


def analyzeQMakeProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        for line in file:
            line=line.lower()
            # if line.startswith("<!--"):
            #     comment_zone = True
            # if line.endswith("-->"):
            #     comment_zone = False
            # if comment_zone:
            #     continue
            if line.startswith("#"):
                continue
            if line.startswith("# "):
                continue
            if "libs"  in line:
                dependencies_zone = True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "QMake":
                        continue
                    s=line.strip()
                    if str(conf).lower().strip() in s:
                        out.write(
                            str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
            if line.endswith("\\n"):
                continue
            if line.endswith("\n"):
                dependencies_zone = False


def analyzeNinjaProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        for line in file:
            line=line.lower()
            # if line.startswith("<!--"):
            #     comment_zone = True
            # if line.endswith("-->"):
            #     comment_zone = False
            # if comment_zone:
            #     continue
            if line.startswith("#"):
                continue
            if line.startswith("# "):
                continue
            if "deps"  in line:
                dependencies_zone = True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "Ninja":
                        continue
                    s=line.strip()
                    if str(conf).lower().strip() in s:
                        out.write(
                            str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
            if line.endswith("\\n"):
                continue
            if line.endswith("\n"):
                dependencies_zone = False


def analyzeSoongProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        for line in file:
            line=line.lower()
            if line.startswith("/*"):
                comment_zone = True
            if line.endswith("*/"):
                comment_zone = False
            if comment_zone:
                continue
            if line.startswith("//"):
                continue
            if line.startswith("// "):
                continue
            if "{"  in line:
                dependencies_zone = True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "Soong":
                        continue
                    s=line.strip()
                    if "name" in line:
                        arr=s.split(":")
                        if(len(arr)>1):
                            if str(conf).lower().strip() in arr[1]:
                                out.write(
                                    str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
            if line.endswith("}"):
                dependencies_zone = False


def analyzeMesonProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        for line in file:
            line=line.lower()
            # if line.startswith("/*"):
            #     comment_zone = True
            # if line.endswith("*/"):
            #     comment_zone = False
            # if comment_zone:
            #     continue
            if line.startswith("#"):
                continue
            if line.startswith("# "):
                continue
            if "dependency"  in line:
                dependencies_zone = True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "Meson":
                        continue
                    s=line.strip()
                    if str(conf).lower().strip() in s:
                        out.write(
                            str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
            if line.endswith(")") or line.endswith("]")  :
                dependencies_zone = False


def analyzeSetupProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        for line in file:
            line=line.lower()
            # if line.startswith("/*"):
            #     comment_zone = True
            # if line.endswith("*/"):
            #     comment_zone = False
            # if comment_zone:
            #     continue
            if line.startswith("#"):
                continue
            if line.startswith("# "):
                continue
            if not(line.startswith("    ") or line.startswith("\t")):
                dependencies_zone=False
            if "requires"  in line:
                dependencies_zone = True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "setuptools":
                        continue
                    s=line.strip()
                    if str(conf).lower().strip() in s:
                        out.write(
                            str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
            if line.endswith(")") or line.endswith("]")  :
                dependencies_zone = False


def analyzeBowerProject(project_name,file_path, reference_list, out):
    with open(file_path, "r+", encoding="utf-8",errors="ignore") as file:
        dependencies_zone = False
        comment_zone = False
        for line in file:
            line=line.lower()
            # if line.startswith("/*"):
            #     comment_zone = True
            # if line.endswith("*/"):
            #     comment_zone = False
            # if comment_zone:
            #     continue
            if line.startswith("#"):
                continue
            if line.startswith("# "):
                continue
            if "dependencies"  in line:
                dependencies_zone = True
            if dependencies_zone:
                for conf in reference_list:
                    if conf == "Bower":
                        continue
                    s=line.strip()
                    if str(conf).lower().strip() in s:
                        out.write(
                            str(project_name) + ";" + str(file_path) + ";" + str(conf) + ";" + line.strip() + "\n")
            if line.endswith("}")  :
                dependencies_zone = False
