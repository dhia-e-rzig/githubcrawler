import csv
import pickle

import pandas
from efficient_apriori import apriori
# "CSV Files/commit-types-files-12-08-20-05-37-34-tool.csv"
# "CSV Files/commit-types-files-12-09-20-09-41-56-tool.csv"
# CSV Files/commit-types-files-12-09-20-21-54-39-applied.csv
# CSV Files/commit-types-files-12-11-20-08-02-01-no-ai-ml.csv

import multiprocessing as mp

import os

with open("..\\Excel Files\ConfigFiles_all.xlsx", "rb") as configFile:
    special_files_dataframe = pandas.read_excel(configFile)
# text_ext = ['.csv', '.md', '.txt','.ini','.map','.markdown','.pem','.xaml','.onnx','.resx','.tdb','.log','.pbtxt',".xaml",'.tsv','.h',".xml"]
source_ext = ['.py', '.java', '.c', '.cpp', '.cs', '.ts', '.go', '.js', '.s', 'ipynb', '.sh', '.csproj', '.sln', '.p',
              '.h', '.pyc', '.rjs', '.rb']
ignored_ext = ['.gitignore', 'README.md', 'LICENSE', "AUTHORS", "CONTRIBUTORS", "PATENTS", "OWNERS",
               "SECURITY_CONTACTS", "NOTICE", "Readme", ".DS_Store", ".gitattributes", "CODEOWNERS", ".gitkeep",
               ".gitmodules", "GOLANG_CONTRIBUTORS"]
Directories = special_files_dataframe["Directory"].tolist()
FileNamesAndExtensions = special_files_dataframe["Files"].tolist()
FileNamesAndExtensionsAndDirectories = list(zip(FileNamesAndExtensions, Directories))


def info():
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def classify_file(dirpath, filename, level):
    filename = str(filename).strip()
    # count_dict["total"] += 1

    if ".git" in dirpath:
        return "ignore"
    if ".idea" in dirpath:
        return "ignore"
    if ".vscode" in dirpath:
        return "ignore"
    for iext in ignored_ext:
        if filename == iext:
            return "ignore"

    for i in range(0, len(FileNamesAndExtensionsAndDirectories)):
        (ext, dir) = FileNamesAndExtensionsAndDirectories[i]
        if isinstance(dir, str):
            if dir != 'NA' and dir not in dirpath:
                continue
        if filename.lower().endswith(ext.lower()):
            category = str(
                special_files_dataframe.loc[special_files_dataframe['Files'] == ext]['Category'].values).replace('[',
                                                                                                                 '').replace(
                ']', '').replace('\'', '')
            tool = str(special_files_dataframe.loc[special_files_dataframe['Files'] == ext]['Tool'].values).replace('[',
                                                                                                                    '').replace(
                ']', '').replace('\'', '')
            if level == "Coarse":
                return "DevOps"
            elif level == "Medium":
                return category
            elif level == "Fine":
                return tool
            else:
                return "DevOps"

        if "test" in filename.lower():
            # count_dict[gext] += 1
            return "Test"

    for gext in source_ext:
        if filename.lower().endswith(gext):
            # count_dict[gext] += 1
            return "Source"
    return "ignore"




#
# def gen_coarse_rules(min_s, min_c):
#     info()
#     print("Generating coarse")
#     # transactions = []
#     # for index, row in df_all.iterrows():
#     #     files = str(row["CommitFiles"]).split("==")
#     #     elements = []
#     #     for file in files:
#     #         name = file.split("//")[-1]
#     #         dir = file[:len(file) - len(name)]
#     #         classification = classify_file(dir, file, "Coarse")
#     #         if classification != "ignore":
#     #             elements.append(classification)
#     #     transactions.append(tuple(elements))
#     binary_file = open('coarse_transactions.bin', mode='rb')
#     transactions=pickle.load(binary_file)
#     binary_file.close()
#     print(transactions)
#     itemsets, rules = apriori(transactions, min_support=min_s, min_confidence=min_c)
#     apriori_coarse_rules_file = open(
#         "../CSV Files/apriori-coarserules-supp-" + str(min_s) + "-conf-" + str(min_c) + ".csv", "w+", encoding="utf-8")
#     apriori_coarse_rules_file.write("RuleLHS;RuleRHS;Conf;Supp;Lift;Conv\n")
#     for rule in rules:
#         print(rule)
#         apriori_coarse_rules_file.write(
#             str(rule.lhs) + ";" + str(rule.rhs) + ";" + str(rule.confidence) + ";" + str(rule.support) + ';' + str(
#                 rule.lift) + ";" + str(rule.conviction) + "\n")
#     return "Coarse"



def pickle_medium_transactions_tool():
    df1_tool = pandas.read_csv("../CSV Files/commit-types-files-12-08-20-05-37-34-tool.csv", sep=';', encoding="utf-8",
                               error_bad_lines="ignore",
                               usecols=["ProjectName", "CommitOID", "CommitDateAndTime", "CommitFiles", "IsBuildFix",
                                        "IsBugFix",
                                        "IsCodeImprovement"])
    df2_tool = pandas.read_csv("../CSV Files/commit-types-files-12-09-20-09-41-56-tool.csv", sep=';', encoding="utf-8",
                               error_bad_lines="ignore",
                               usecols=["ProjectName", "CommitOID", "CommitDateAndTime", "CommitFiles", "IsBuildFix",
                                        "IsBugFix",
                                        "IsCodeImprovement"])

    df3_tool = pandas.read_csv("../CSV Files/commit-types-files-12-31-20-11-01-36-tool.csv", sep=';', encoding="utf-8",
                               error_bad_lines="ignore",
                               usecols=["ProjectName", "CommitOID", "CommitDateAndTime", "CommitFiles", "IsBuildFix",
                                        "IsBugFix",
                                        "IsCodeImprovement"])
    df_all_tool = df1_tool.append(df2_tool).append(df3_tool)
    info()
    print("Pickling Medium Tool")
    transactions = []
    for index, row in df_all_tool.iterrows():
        files = str(row["CommitFiles"]).split("==")
        elements = []
        for file in files:
            name = file.split("//")[-1]
            dir = file[:len(file) - len(name)]
            classification = classify_file(dir, file, "Coarse")
            if classification != "ignore":
                elements.append(classification)
        transactions.append(tuple(elements))
    # print(transactions)
    binary_file = open('medium_transactions_tool2.bin', mode='wb')
    pickle.dump(transactions, binary_file)
    binary_file.close()
    return "trans"

def pickle_medium_transactions_applied():
    df1 = pandas.read_csv("../CSV Files/commit-types-files-12-09-20-21-54-39-applied.csv", sep=';', encoding="utf-8",
                               error_bad_lines="ignore",
                               usecols=["ProjectName", "CommitOID", "CommitDateAndTime", "CommitFiles", "IsBuildFix",
                                        "IsBugFix",
                                        "IsCodeImprovement"])
    df2 = pandas.read_csv("../CSV Files/commit-types-files-12-31-20-11-01-20-applied.csv", sep=';', encoding="utf-8",
                               error_bad_lines="ignore",
                               usecols=["ProjectName", "CommitOID", "CommitDateAndTime", "CommitFiles", "IsBuildFix",
                                        "IsBugFix",
                                        "IsCodeImprovement"])

    df_all = df1.append(df2)
    info()
    print("Pickling Medium Applied")
    transactions = []
    for index, row in df_all.iterrows():
        files = str(row["CommitFiles"]).split("==")
        elements = []
        for file in files:
            name = file.split("//")[-1]
            dir = file[:len(file) - len(name)]
            classification = classify_file(dir, file, "Coarse")
            if classification != "ignore":
                elements.append(classification)
        transactions.append(tuple(elements))
    # print(transactions)
    binary_file = open('medium_transactions_applied2.bin', mode='wb')
    pickle.dump(transactions, binary_file)
    binary_file.close()
    return "trans"

def pickle_medium_transactions_noaiml():
    df1 = pandas.read_csv("../CSV Files/commit-types-files-12-11-20-08-02-01-no-ai-ml.csv", sep=';', encoding="utf-8",
                          error_bad_lines="ignore",
                          usecols=["ProjectName", "CommitOID", "CommitDateAndTime", "CommitFiles", "IsBuildFix",
                                   "IsBugFix",
                                   "IsCodeImprovement"])
    df2 = pandas.read_csv("../CSV Files/commit-types-files-12-31-20-11-31-37-no-ai-ml.csv", sep=';', encoding="utf-8",
                          error_bad_lines="ignore",
                          usecols=["ProjectName", "CommitOID", "CommitDateAndTime", "CommitFiles", "IsBuildFix",
                                   "IsBugFix",
                                   "IsCodeImprovement"])

    df_all = df1.append(df2)
    info()
    print("Pickling Medium NOAIML")
    transactions = []
    for index, row in df_all.iterrows():
        files = str(row["CommitFiles"]).split("==")
        elements = []
        for file in files:
            name = file.split("//")[-1]
            dir = file[:len(file) - len(name)]
            classification = classify_file(dir, file, "Coarse")
            if classification != "ignore":
                elements.append(classification)
        transactions.append(tuple(elements))
    # print(transactions)
    binary_file = open('medium_transactions_noaiml2.bin', mode='wb')
    pickle.dump(transactions, binary_file)
    binary_file.close()
    return "trans"

def gen_medium_rules_tool(min_s, min_c):
    info()
    print("generating tool rules")
    binary_file = open('medium_transactions_tool2.bin', mode='rb')
    transactions = pickle.load(binary_file)
    binary_file.close()
    itemsets, rules = apriori(transactions, min_support=min_s, min_confidence=min_c)
    apriori_coarse_rules_file = open(
        "../CSV Files/apriori-mediumrules-supp-" + str(min_s) + "-conf-" + str(min_c) + "-tool.csv", "w+", encoding="utf-8")
    apriori_coarse_rules_file.write("RuleLHS;RuleRHS;Conf;Supp;Lift;Conv\n")
    for rule in rules:
        print(rule)
        apriori_coarse_rules_file.write(
            str(rule.lhs) + ";" + str(rule.rhs) + ";" + str(rule.confidence) + ";" + str(rule.support) + ';' + str(
                rule.lift) + ";" + str(rule.conviction) + "\n")
    return "Medium"


def gen_medium_rules_applied(min_s, min_c):
    info()
    print("generating applied rules")
    binary_file = open('medium_transactions_applied2.bin', mode='rb')
    transactions = pickle.load(binary_file)
    binary_file.close()
    itemsets, rules = apriori(transactions, min_support=min_s, min_confidence=min_c)
    apriori_coarse_rules_file = open(
        "../CSV Files/apriori-mediumrules-supp-" + str(min_s) + "-conf-" + str(min_c) + "-applied.csv", "w+", encoding="utf-8")
    apriori_coarse_rules_file.write("RuleLHS;RuleRHS;Conf;Supp;Lift;Conv\n")
    for rule in rules:
        print(rule)
        apriori_coarse_rules_file.write(
            str(rule.lhs) + ";" + str(rule.rhs) + ";" + str(rule.confidence) + ";" + str(rule.support) + ';' + str(
                rule.lift) + ";" + str(rule.conviction) + "\n")
    return "Medium"

def gen_medium_rules_noaiml(min_s, min_c):
    info()
    print("generating noaiml rules")
    binary_file = open('medium_transactions_noaiml2.bin', mode='rb')
    transactions = pickle.load(binary_file)
    binary_file.close()
    itemsets, rules = apriori(transactions, min_support=min_s, min_confidence=min_c)
    apriori_coarse_rules_file = open(
        "../CSV Files/apriori-mediumrules-supp-" + str(min_s) + "-conf-" + str(min_c) + "-noaiml.csv", "w+", encoding="utf-8")
    apriori_coarse_rules_file.write("RuleLHS;RuleRHS;Conf;Supp;Lift;Conv\n")
    for rule in rules:
        print(rule)
        apriori_coarse_rules_file.write(
            str(rule.lhs) + ";" + str(rule.rhs) + ";" + str(rule.confidence) + ";" + str(rule.support) + ';' + str(
                rule.lift) + ";" + str(rule.conviction) + "\n")
    return "Medium"

#
#
# def gen_fine_rules(min_s, min_c):
#     info()
#     print("Generating Fine")
#     transactions = []
#     # for index, row in df_all.iterrows():
#     #     files = str(row["CommitFiles"]).split("==")
#     #     elements = []
#     #     for file in files:
#     #         name = file.split("//")[-1]
#     #         dir = file[:len(file) - len(name)]
#     #         classification = classify_file(dir, file, "Fine")
#     #         if classification != "ignore":
#     #             elements.append(classification)
#     #     transactions.append(tuple(elements))
#     binary_file = open('fine_transactions.bin', mode='rb')
#     # pickle.dump(transactions, binary_file)
#     transactions = pickle.load(binary_file)
#     binary_file.close()
#     itemsets, rules = apriori(transactions, min_support=min_s, min_confidence=min_c)
#     apriori_coarse_rules_file = open(
#         "../CSV Files/apriori-finerules-supp-" + str(min_s) + "-conf-" + str(min_c) + ".csv", "w+", encoding="utf-8")
#     apriori_coarse_rules_file.write("RuleLHS;RuleRHS;Conf;Supp;Lift;Conv\n")
#     for rule in rules:
#         print(rule)
#         apriori_coarse_rules_file.write(
#             str(rule.lhs) + ";" + str(rule.rhs) + ";" + str(rule.confidence) + ";" + str(rule.support) + ';' + str(
#                 rule.lift) + ";" + str(rule.conviction) + "\n")
#     return "Fine"
def export_transactions_as_csv():
    base1_path="medium_transactions_applied2.bin"
    base2_path="medium_transactions_tool2.bin"
    base3_path="medium_transactions_noaiml2.bin"
    binary_file = open(base1_path, mode='rb')
    base1 = pickle.load(binary_file)
    binary_file.close()
    binary_file = open(base2_path, mode='rb')
    base2 = pickle.load(binary_file)
    binary_file.close()
    binary_file = open(base3_path, mode='rb')
    base3 = pickle.load(binary_file)
    binary_file.close()
    with open('applied_transactions.csv', 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(base1)
    with open('tool_transactions.csv', 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(base2)
    with open('noaiml_transactions.csv', 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(base3)


if __name__ == '__main__':
    # min_supp = 0
    # min_conf = 0
    # info()
    # with mp.Pool(processes=4) as pool:
    #     # results1 = pool.apply_async(pickle_medium_transactions_applied, ())
    #     # results2 = pool.apply_async(pickle_medium_transactions_tool, ())
    #     # results3 = pool.apply_async(pickle_medium_transactions_noaiml, ())
    #     results1 = pool.apply_async(gen_medium_rules_tool, (min_supp,min_conf))
    #     results2 = pool.apply_async(gen_medium_rules_applied, (min_supp,min_conf))
    #     results3 = pool.apply_async(gen_medium_rules_noaiml, (min_supp,min_conf))
    #
    #
    #     results1.wait()
    #     results2.wait()
    #     results3.wait()
    export_transactions_as_csv()


