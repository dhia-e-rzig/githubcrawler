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
        with open(file_path, "r+", encoding="utf-8") as file:
            dependencies_zone = False
            comment_zone = False
            for line in file:
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
                if "}" in line:
                    dependencies_zone = False

def analyzeGradleProject(project_name,file_path, reference_list, out):
    with open(file_path,"r+",encoding="utf-8") as file:
        dependencies_zone=False
        comment_zone=False
        for line in file:
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
            if "/dependencies" in line:
                dependencies_zone=False



def analyzeRakeProject(project_name,file_path, reference_list, out):
    with open(file_path,"r+",encoding="utf-8") as file:
        dependencies_zone=False
        # comment_zone=False
        for line in file:
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