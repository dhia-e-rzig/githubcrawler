# #independent sample t-test
# import random
# random.seed(20) #for results to be recreated
#
# N = 50 #number of samples to take from each population
# a = [random.gauss(55,20) for x in range(N)] #take N samples from population A
# b = [random.gauss(50,15) for x in range(N)] #take N samples from population B
# import pandas as pd
from scipy import stats
import pandas

tool=pandas.read_csv("../CSV Files/Tool_avg_churn.csv", sep=',', encoding="utf-8",
                     error_bad_lines="ignore")

applied=pandas.read_csv("../CSV Files/Applied_avg_churn.csv", sep=',', encoding="utf-8",
                        error_bad_lines="ignore")


# aiml= tool["Avg_NBReviewCount"].tolist() + applied["Avg_NBReviewCount"].tolist()




noaiml=pandas.read_csv("../CSV Files/NoAIML_avg_churn.csv", sep=',', encoding="utf-8",
                       error_bad_lines="ignore")

fvalue, pvalue = stats.f_oneway(applied['SourceCodeChurn'], tool['SourceCodeChurn'], noaiml['SourceCodeChurn'])
print("F-Value:{0} P-Value:{1}".format(fvalue,pvalue))

fvalue, pvalue = stats.f_oneway(applied['DevOpsCodeChurn'], tool['DevOpsCodeChurn'], noaiml['DevOpsCodeChurn'])
print("F-Value:{0} P-Value:{1}".format(fvalue,pvalue))

# import seaborn as sns
# import matplotlib.pyplot as plt
# sns.kdeplot(tool["Avg_NBReviewCount"], shade=True)
# sns.kdeplot(applied["Avg_NBReviewCount"], shade=True)
# plt.title("Independent Sample T-Test")
# plt.show()



# tStat, pValue = stats.ttest_ind(tool["Avg_NBReviewCount"],applied["Avg_NBReviewCount"], equal_var = False) #run independent sample T-Test
# print("tool and applied")
# print("P-Value:{0} T-Statistic:{1}".format(pValue,tStat)) #print the P-Value and the T-Statistic
###P-Value:0.017485741540118758 T-Statistic:2.421942924642376

# The stats ttest_ind function runs the independent sample T-Test and outputs a P-Value and the Test-Statistic.
# In this example, there is enough evidence to reject the Null Hypothesis as the P-Value is low (typically ≤ 0.05).

# df_applied = pd.read_csv('../CSV Files/devopsfiles-mergingcommits-04-04-21-09-32-11-no-ai-ml.csv',sep=';')
# df_tool = pd.read_csv('../CSV Files/devopsfiles-mergingcommits-04-03-21-09-33-20-tool.csv',sep=';')
# df_nonaiml = pd.read_csv('../CSV Files/devopsfiles-mergingcommits-04-04-21-09-32-11-no-ai-ml.csv',sep=';')

df_applied_issues1 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-07-21-45-applied.csv', sep=";",
                                 error_bad_lines=False)
df_applied_issues2 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-10-32-55-applied.csv', sep=";",
                                 error_bad_lines=False)
df_applied_issues3 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-12-04-44-applied.csv', sep=";",
                                 error_bad_lines=False)
df_applied_issues4 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-12-52-03-applied.csv', sep=";",
                                 error_bad_lines=False)
df_applied_issues5 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-10-47-42-applied.csv', sep=";",
                                 error_bad_lines=False)
df_applied_issues6 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-10-54-12-applied.csv', sep=";",
                                 error_bad_lines=False)
df_applied_issues7 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-11-26-41-applied.csv', sep=";",
                                 error_bad_lines=False)

df_applied_issues = (((((df_applied_issues1.append(df_applied_issues2)).append(df_applied_issues3)).append(
    df_applied_issues4)).append(df_applied_issues5)).append(df_applied_issues6)).append(df_applied_issues7)

# df_applied['BeforeOrAfterDevOps']=np.where(df_applied['DateOpened'] < df_applied['CreationDate'],'Before','After')

# df_applied_before=df_applied[df_applied['BeforeOrAfterDevOps']=='Before']

df_applied_issues = df_applied_issues.drop(['IssueNumber', 'IssueTitle', 'DateOpened', 'DateClose'], axis=1)
df_applied_issues = df_applied_issues.groupby(['ProjectName']).mean()
df_applied = df_applied_issues
Q1 = df_applied['Duration'].quantile(0.25)
Q3 = df_applied['Duration'].quantile(0.75)
IQR = Q3 - Q1
df_applied = df_applied[~((df_applied['Duration'] < (Q1 - 1.5 * IQR)) | (df_applied['Duration'] > (Q3 + 1.5 * IQR)))]
# df_applied['Project Category'] = 'AI/ML Applied'

df_tool_issues1 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-05-20-11-tool.csv', sep=";",
                              error_bad_lines=False)
df_tool_issues2 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-11-59-32-tool.csv', sep=";",
                              error_bad_lines=False)

df_tool_issues = df_tool_issues1.append(df_tool_issues2)
# df_tool_devops_date = pd.read_csv('../Tool-DevOps-adoption-Date.csv',sep=",")
df_tool = df_tool_issues

df_tool = df_tool.drop(
    ['IssueNumber', 'IssueTitle', 'DateOpened', 'DateClose'],
    axis=1)
df_tool = df_tool.groupby(['ProjectName']).mean()
Q1 = df_tool['Duration'].quantile(0.25)
Q3 = df_tool['Duration'].quantile(0.75)
IQR = Q3 - Q1
df_tool = df_tool[
    ~((df_tool['Duration'] < (Q1 - 1.5 * IQR)) | (df_tool['Duration'] > (Q3 + 1.5 * IQR)))]

# df_tool['Project Category'] = 'AI/ML Tool'

df_noaiml_issues1 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-05-47-15-no-ai-ml.csv', sep=";",
                                error_bad_lines=False)
df_noaiml_issues2 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-07-43-26-no-ai-ml.csv', sep=";",
                                error_bad_lines=False)
df_noaiml_issues3 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-09-44-29-no-ai-ml.csv', sep=";",
                                error_bad_lines=False)
df_noaiml_issues4 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-12-21-50-no-ai-ml.csv', sep=";",
                                error_bad_lines=False)

df_noaiml_issues = ((df_noaiml_issues1.append(df_noaiml_issues2)).append(df_noaiml_issues3)).append(df_noaiml_issues4)
# df_noaiml_devops_date = pd.read_csv('../NoAIML-DevOps-adoption-Date.csv',sep=",")

df_noaiml = df_noaiml_issues
df_noaiml = df_noaiml.groupby(['ProjectName']).mean()

Q1 = df_noaiml['Duration'].quantile(0.25)
Q3 = df_noaiml['Duration'].quantile(0.75)
IQR = Q3 - Q1
df_noaiml = df_noaiml[
    ~((df_noaiml['Duration'] < (Q1 - 1.5 * IQR)) | (df_noaiml['Duration'] > (Q3 + 1.5 * IQR)))]

# df_noaiml['Project Category'] = 'Non-AI/Ml'

# df_all = df_tool.append(df_applied).append(df_noaiml)

df_applied.fillna(0,inplace=True)
df_tool.fillna(0,inplace=True)
df_noaiml.fillna(0,inplace=True)
print(df_applied)
print(df_tool)
print(df_noaiml)

# # Build,CI,Deployment Automation,Monitoring and Logging,Analyzer,Test
#
# ax = sns.violinplot(cut=0, palette='gist_gray', x=df_all['Project Category'], y=df_all['Duration'], hue=df_all['Test'],
#                     split=True, legend=False, inner="quartile")



# print(df_tool.columns)
fvalue, pvalue = stats.f_oneway(df_applied['Duration'], df_tool['Duration'], df_noaiml['Duration'])
print("F-Value:{0} P-Value:{1}".format(fvalue,pvalue))


# fvalue, pvalue = stats.f_oneway(df_applied['DevOpsCodeChurn'], df_tool['DevOpsCodeChurn'], df_nonaiml['DevOpsCodeChurn'])
# print("F-Value:{0} P-Value:{1}".format(fvalue,pvalue))
