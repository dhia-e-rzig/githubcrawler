import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
# from pandas.tests.tools.test_to_numeric import errors

sns.set_theme(style="whitegrid")
#

def codechurn():
    df=pd.read_excel('../Excel Files/Code Churn-V2.xlsx',sheet_name=0)
    df.columns =df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    # df=df[(df.SourceCodeChurn !=0) | (df.DevOpsCodeChurn !=0) ]

    df_devopschurn=df.drop(['SourceCodeChurn'],axis=1)

    df_devopschurn.rename(columns={'DevOpsCodeChurn':'Churn'},inplace=True)
    df_devopschurn=df_devopschurn.groupby(['ProjectName']).mean()
    df_devopschurn['Type']='DevOps Churn'
    Q1 = df_devopschurn['Churn'].quantile(0.25)
    Q3 = df_devopschurn['Churn'].quantile(0.75)
    IQR = Q3 - Q1
    df_devopschurn = df_devopschurn[~((df_devopschurn['Churn'] < (Q1 - 1.5 * IQR)) | (df_devopschurn['Churn'] > (Q3 + 1.5 * IQR)))]
    print("DevOps applied Quantiles")
    print(df_devopschurn.Churn.quantile([0.25,0.5,0.75]))

    df_sourcechurn=df.drop(['DevOpsCodeChurn'],axis=1)

    print(df_sourcechurn.rename(columns={'SourceCodeChurn':'Churn'},inplace=True))

    df_sourcechurn=df_sourcechurn.groupby(['ProjectName']).mean()
    df_sourcechurn['Type'] = 'Source Churn'
    Q1 = df_sourcechurn['Churn'].quantile(0.25)
    Q3 = df_sourcechurn['Churn'].quantile(0.75)
    IQR = Q3 - Q1
    df_sourcechurn = df_sourcechurn[~((df_sourcechurn['Churn'] < (Q1 - 1.5 * IQR)) | (
                df_sourcechurn['Churn'] > (Q3 + 1.5 * IQR)))]

    print("Source applied Quantiles")
    print(df_sourcechurn.Churn.quantile([0.25,0.5,0.75]))


    df_applied=df_devopschurn.append(df_sourcechurn)

    df_applied['Project Type']='AI/ML Applied'


    df=pd.read_excel('../Excel Files/Codechurn.xlsx',sheet_name=1)
    df.columns =df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    print(df.columns)

    # df=df[(df.SourceCodeChurn !=0) | (df.DevOpsCodeChurn !=0) ]

    df_devopschurn=df.drop(['SourceCodeChurn'],axis=1)

    df_devopschurn.rename(columns={'DevOpsCodeChurn':'Churn'},inplace=True)
    df_devopschurn = df_devopschurn.groupby(['ProjectName']).mean()
    df_devopschurn['Type']='DevOps Churn'
    Q1 = df_devopschurn['Churn'].quantile(0.25)
    Q3 = df_devopschurn['Churn'].quantile(0.75)
    IQR = Q3 - Q1
    df_devopschurn = df_devopschurn[~((df_devopschurn['Churn'] < (Q1 - 1.5 * IQR)) | (
            df_devopschurn['Churn'] > (Q3 + 1.5 * IQR)))]

    print("DevOps tool Quantiles")
    print(df_devopschurn.Churn.quantile([0.25,0.5,0.75]))


    df_sourcechurn=df.drop(['DevOpsCodeChurn'],axis=1)

    df_sourcechurn.rename(columns={'SourceCodeChurn':'Churn'},inplace=True)
    df_sourcechurn = df_sourcechurn.groupby(['ProjectName']).mean()
    df_sourcechurn['Type'] = 'Source Churn'
    Q1 = df_sourcechurn['Churn'].quantile(0.25)
    Q3 = df_sourcechurn['Churn'].quantile(0.75)
    IQR = Q3 - Q1
    df_sourcechurn = df_sourcechurn[~((df_sourcechurn['Churn'] < (Q1 - 1.5 * IQR)) | (
            df_sourcechurn['Churn'] > (Q3 + 1.5 * IQR)))]

    print("Source Tool Quantiles")
    print(df_sourcechurn.Churn.quantile([0.25,0.5,0.75]))

    df_tool=df_devopschurn.append(df_sourcechurn)

    df_tool['Project Type']='AI/ML Tool'


    df=pd.read_excel('../Excel Files/Codechurn.xlsx',sheet_name=2)
    df.columns =df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    print(df.columns)

    df=df[(df.SourceCodeChurn !=0) | (df.DevOpsCodeChurn !=0) ]

    df_devopschurn=df.drop(['SourceCodeChurn'],axis=1)

    df_devopschurn.rename(columns={'DevOpsCodeChurn':'Churn'},inplace=True)
    df_devopschurn = df_devopschurn.groupby(['ProjectName']).mean()
    df_devopschurn['Type'] = 'DevOps Churn'
    Q1 = df_devopschurn['Churn'].quantile(0.25)
    Q3 = df_devopschurn['Churn'].quantile(0.75)
    IQR = Q3 - Q1
    df_devopschurn = df_devopschurn[~((df_devopschurn['Churn'] < (Q1 - 1.5 * IQR)) | (
            df_devopschurn['Churn'] > (Q3 + 1.5 * IQR)))]


    print("DevOps NonAIML Quantiles")
    print(df_devopschurn.Churn.quantile([0.25,0.5,0.75]))

    df_sourcechurn=df.drop(['DevOpsCodeChurn'],axis=1)

    df_sourcechurn.rename(columns={'SourceCodeChurn':'Churn'},inplace=True)

    Q1 = df_sourcechurn['Churn'].quantile(0.25)
    Q3 = df_sourcechurn['Churn'].quantile(0.75)
    IQR = Q3 - Q1
    df_sourcechurn = df_sourcechurn[~((df_sourcechurn['Churn'] < (Q1 - 1.5 * IQR)) | (
            df_sourcechurn['Churn'] > (Q3 + 1.5 * IQR)))]
    df_sourcechurn = df_sourcechurn.groupby(['ProjectName']).mean()
    df_sourcechurn['Type'] = 'Source Churn'
    print("Source NonAIML Quantiles")
    print(df_sourcechurn.Churn.quantile([0.25,0.5,0.75]))

    df_non=df_devopschurn.append(df_sourcechurn)
    df_non['Project Type']='Non-AI/ML'



    df_all=(df_applied.append(df_tool)).append(df_non)

    df_all.to_csv('codechurn_avg_all.csv')

    figure(figsize=(5,6), dpi=80)

    df_all.fillna(0)
    print(df_all.columns)

    # Build,CI,Deployment Automation,Monitoring and Logging,Analyzer,Test

    ax = sns.violinplot(cut=0,palette='gist_gray', x=df_all['Project Type'], y=df_all['Churn'],
                        hue=df_all['Type'], split=True, legend=False, inner="quartile")
    ax.set(ylabel='Normalized Code Churn', xlabel='Project Category')
    L = plt.legend(bbox_to_anchor=(0.5, -0.35), borderaxespad=0, loc='lower center')
    L.get_texts()[0].set_text('DevOps Code Churn')
    L.get_texts()[1].set_text('Source Code Churn')
    plt.setp(ax.get_legend().get_texts(), fontsize='10')
    # for legend title
    plt.setp(ax.get_legend().get_title(), fontsize='10')

    plt.tight_layout()

    plt.savefig('RQ2-CodeChurn.eps', format='eps')
    plt.savefig('RQ2-CodeChurn.jpg', format='jpg')
    plt.show()

# sns.color_palette("")


def avg_merging_commits_graphs():
    df_nonaiml_projects=pd.read_csv('../CSV Files/devopsfiles-mergingcommits-04-04-21-09-32-11-no-ai-ml.csv',sep=";")
    df_applied_projects=pd.read_csv('../CSV Files/devopsfiles-mergingcommits-04-01-21-08-19-42-applied.csv',sep=";")
    df_tool_projects=pd.read_csv('../CSV Files/devopsfiles-mergingcommits-04-03-21-09-33-20-tool.csv',sep=";")

    df_tool_classification=pd.read_csv('../CSV Files/ToolProjects_classification.csv')
    df_applied_classification=pd.read_csv('../CSV Files/AppliedProjects_classification.csv')
    df_noaiml_classification=pd.read_csv('../CSV Files/NoAIMLProjects_classification.csv')



    df_applied=pd.merge(df_applied_projects,df_applied_classification,how="outer",on="ProjectName")
    Q1=df_applied['MonthlyDevOpsCommitAvg'].quantile(0.25)
    Q3=df_applied['MonthlyDevOpsCommitAvg'].quantile(0.75)
    IQR=Q3-Q1
    df_applied = df_applied[~((df_applied['MonthlyDevOpsCommitAvg'] < (Q1 - 1.5 * IQR)) |(df_applied['MonthlyDevOpsCommitAvg'] > (Q3 + 1.5 * IQR)))]
    # print(df_applied.MonthlyAllCommitAvg.quantile([0.25, 0.5, 0.75]))


    df_tool=pd.merge(df_tool_projects,df_tool_classification,how="outer",on="ProjectName")


    Q1=df_tool['MonthlyDevOpsCommitAvg'].quantile(0.25)
    Q3=df_tool['MonthlyDevOpsCommitAvg'].quantile(0.75)
    IQR=Q3-Q1
    df_tool = df_tool[~((df_tool['MonthlyDevOpsCommitAvg'] < (Q1 - 1.5 * IQR)) |(df_tool['MonthlyDevOpsCommitAvg'] > (Q3 + 1.5 * IQR)))]
    # print(df_tool.MonthlyAllCommitAvg.quantile([0.25, 0.5, 0.75]))


    df_noaiml=pd.merge(df_nonaiml_projects,df_noaiml_classification,how="outer",on="ProjectName")


    Q1=df_noaiml['MonthlyDevOpsCommitAvg'].quantile(0.25)
    Q3=df_noaiml['MonthlyDevOpsCommitAvg'].quantile(0.75)
    IQR=Q3-Q1
    df_noaiml = df_noaiml[~((df_noaiml['MonthlyDevOpsCommitAvg'] < (Q1 - 1.5 * IQR)) |(df_noaiml['MonthlyDevOpsCommitAvg'] > (Q3 + 1.5 * IQR)))]
    # print(df_noaiml.MonthlyAllCommitAvg.quantile([0.25, 0.5, 0.75]))

    df_noaiml['Project Category']= "Non-AI/ML"
    df_applied['Project Category']= "AI/ML Applied"
    df_tool['Project Category']= "AI/ML Tool"

    df_all=df_tool.append(df_applied).append(df_noaiml)

    ax = sns.violinplot(cut=0,palette='gist_gray', x=df_all['Project Category'], y=df_all['MonthlyDevOpsCommitAvg'], hue=df_all['Deployment Automation'],
                        split=True, legend=False, inner="quartile")
    ax.set(ylabel='Avg. Monthly DevOps Commits (Commits)', xlabel='Project Category')
    L = plt.legend(bbox_to_anchor=(0.5, -0.35), borderaxespad=0, loc='lower center')
    L.get_texts()[0].set_text('Project that do not have Deployment Automation tool(s)')
    L.get_texts()[1].set_text('Project that have Deployment Automation tool(s)')

    plt.tight_layout()

    plt.savefig('RQ3-MergingCommits_DA.eps', format='eps')
    plt.savefig('RQ3-MergingCommits_DA.jpg', format='jpg')
    plt.show()

def commits_frequency_graphs():


    df_nonaiml_projects=pd.read_csv('../CSV Files/devopsfiles-mergingcommits-04-04-21-09-32-11-no-ai-ml.csv',sep=";")
    df_applied_projects=pd.read_csv('../CSV Files/devopsfiles-mergingcommits-04-01-21-08-19-42-applied.csv', sep=";")
    df_tool_projects=pd.read_csv('../CSV Files/devopsfiles-mergingcommits-04-03-21-09-33-20-tool.csv',sep=";")

    # df_tool_classification=pd.read_csv('../ToolProjects_classification.csv')
    # df_applied_classification=pd.read_csv('../AppliedProjects_classification.csv')
    # df_noaiml_classification=pd.read_csv('../NoAIMLProjects_classification.csv')

    df_applied_devops_date = pd.read_csv('../CSV Files/Applied-DevOps-adoption-Date.csv', sep=",")
    df_applied=pd.merge(df_applied_projects,df_applied_devops_date,how="left",on="ProjectName")

    df_tool_devops_date = pd.read_csv('../CSV Files/Tool-DevOps-adoption-Date.csv', sep=",")
    df_tool = pd.merge(df_tool_projects, df_tool_devops_date, how="left", on="ProjectName")

    df_noaiml_devops_date = pd.read_csv('../CSV Files/NoAIML-DevOps-adoption-Date.csv', sep=",")
    df_noaiml = pd.merge(df_nonaiml_projects, df_noaiml_devops_date, how="left", on="ProjectName")

    # df_applied=pd.merge(df_applied_projects,df_applied_classification,how="outer",on="ProjectName")
    print(df_applied.columns)
    Q1=df_applied['MonthlyDevOpsCommitAvg'].quantile(0.25)
    Q3=df_applied['MonthlyDevOpsCommitAvg'].quantile(0.75)
    IQR=Q3-Q1
    df_applied = df_applied[~((df_applied['MonthlyDevOpsCommitAvg'] < (Q1 - 1.5 * IQR)) |(df_applied['MonthlyDevOpsCommitAvg'] > (Q3 + 1.5 * IQR)))]

    Q1 = df_applied['MonthlySourceCommitAvg'].quantile(0.25)
    Q3 = df_applied['MonthlySourceCommitAvg'].quantile(0.75)
    IQR = Q3 - Q1
    df_applied = df_applied[~((df_applied['MonthlySourceCommitAvg'] < (Q1 - 1.5 * IQR)) | (
                df_applied['MonthlySourceCommitAvg'] > (Q3 + 1.5 * IQR)))]

    # print(df_applied.MonthlyAllCommitAvg.quantile([0.25, 0.5, 0.75]))


    Q1=df_tool['MonthlyDevOpsCommitAvg'].quantile(0.25)
    Q3=df_tool['MonthlyDevOpsCommitAvg'].quantile(0.75)
    IQR=Q3-Q1
    df_tool = df_tool[~((df_tool['MonthlyDevOpsCommitAvg'] < (Q1 - 1.5 * IQR)) |(df_tool['MonthlyDevOpsCommitAvg'] > (Q3 + 1.5 * IQR)))]

    Q1=df_tool['MonthlySourceCommitAvg'].quantile(0.25)
    Q3=df_tool['MonthlySourceCommitAvg'].quantile(0.75)
    IQR=Q3-Q1
    df_tool = df_tool[~((df_tool['MonthlySourceCommitAvg'] < (Q1 - 1.5 * IQR)) |(df_tool['MonthlySourceCommitAvg'] > (Q3 + 1.5 * IQR)))]
    # print(df_tool.MonthlyAllCommitAvg.quantile([0.25, 0.5, 0.75]))


    Q1=df_noaiml['MonthlyDevOpsCommitAvg'].quantile(0.25)
    Q3=df_noaiml['MonthlyDevOpsCommitAvg'].quantile(0.75)
    IQR=Q3-Q1
    df_noaiml = df_noaiml[~((df_noaiml['MonthlyDevOpsCommitAvg'] < (Q1 - 1.5 * IQR)) |(df_noaiml['MonthlyDevOpsCommitAvg'] > (Q3 + 1.5 * IQR)))]
    # print(df_noaiml.MonthlyAllCommitAvg.quantile([0.25, 0.5, 0.75]))

    Q1=df_noaiml['MonthlySourceCommitAvg'].quantile(0.25)
    Q3=df_noaiml['MonthlySourceCommitAvg'].quantile(0.75)
    IQR=Q3-Q1
    df_noaiml = df_noaiml[~((df_noaiml['MonthlySourceCommitAvg'] < (Q1 - 1.5 * IQR)) |(df_noaiml['MonthlySourceCommitAvg'] > (Q3 + 1.5 * IQR)))]

    df_tool_source=df_tool.drop(columns={'MonthlyDevOpsCommitAvg'},axis=1)
    df_tool_source.rename(columns={'MonthlySourceCommitAvg':'CommitAvg'},inplace=True)
    df_tool_source['CommitType']='Source Commit'
    df_tool_devops=df_tool.drop(columns={'MonthlySourceCommitAvg'},axis=1)
    df_tool_devops.rename(columns={'MonthlyDevOpsCommitAvg': 'CommitAvg'},inplace=True)
    df_tool_devops['CommitType'] ='DevOps Commit'

    df_tool=df_tool_source.append(df_tool_devops)

    df_applied_source = df_applied.drop(columns={'MonthlyDevOpsCommitAvg'}, axis=1)
    df_applied_source.rename(columns={'MonthlySourceCommitAvg': 'CommitAvg'},inplace=True)
    df_applied_source['CommitType'] = 'Source Commit'
    df_applied_devops = df_applied.drop(columns={'MonthlySourceCommitAvg'}, axis=1)
    df_applied_devops.rename(columns={'MonthlyDevOpsCommitAvg': 'CommitAvg'},inplace=True)
    df_applied_devops['CommitType'] = 'DevOps Commit'

    df_applied = df_applied_source.append(df_applied_devops)



    df_noaiml_source = df_noaiml.drop(columns={'MonthlyDevOpsCommitAvg'}, axis=1)
    df_noaiml_source.rename(columns={'MonthlySourceCommitAvg': 'CommitAvg'},inplace=True)
    df_noaiml_source['CommitType'] = 'Source Commit'
    df_noaiml_devops = df_noaiml.drop(columns={'MonthlySourceCommitAvg'}, axis=1)
    df_noaiml_devops.rename(columns={'MonthlyDevOpsCommitAvg': 'CommitAvg'},inplace=True)
    df_noaiml_devops['CommitType'] = 'DevOps Commit'

    df_noaiml = df_noaiml_source.append(df_noaiml_devops)




    df_noaiml['Project Category']= "Non-AI/ML"
    df_applied['Project Category']= "AI/ML Applied"
    df_tool['Project Category']= "AI/ML Tool"

    df_all=df_tool.append(df_applied).append(df_noaiml)

    ax = sns.violinplot(cut=0,palette='gist_gray', x=df_all['Project Category'], y=df_all['CommitAvg'], hue=df_all['CommitType'],
                        split=True, legend=False, inner="quartile")
    # ax.set(ylabel='Avg. Monthly DevOps Commits (Commits)', xlabel='Project Category')
    # L = plt.legend(bbox_to_anchor=(0.5, -0.35), borderaxespad=0, loc='lower center')
    # L.get_texts()[0].set_text('Project that do not have Deployment Automation tool(s)')
    # L.get_texts()[1].set_text('Project that have Deployment Automation tool(s)')

    plt.tight_layout()

    # plt.savefig('RQ3-MergingCommits_DA.eps', format='eps')
    # plt.savefig('RQ3-MergingCommits_DA.jpg', format='jpg')
    plt.show()


def avg_issue_duration_before_and_after_devops():
    df_applied_issues1 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-07-21-45-applied.csv',sep=";",error_bad_lines=False)
    df_applied_issues2 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-10-32-55-applied.csv',sep=";",error_bad_lines=False)
    df_applied_issues3 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-12-04-44-applied.csv',sep=";",error_bad_lines=False)
    df_applied_issues4 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-12-52-03-applied.csv',sep=";",error_bad_lines=False)
    df_applied_issues5 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-10-47-42-applied.csv',sep=";",error_bad_lines=False)
    df_applied_issues6 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-10-54-12-applied.csv',sep=";",error_bad_lines=False)
    df_applied_issues7 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-11-26-41-applied.csv',sep=";",error_bad_lines=False)

    df_applied_issues=(((((df_applied_issues1.append(df_applied_issues2)).append(df_applied_issues3)).append(df_applied_issues4)).append(df_applied_issues5)).append(df_applied_issues6)).append(df_applied_issues7)
    df_applied_devops_date = pd.read_csv('../CSV Files/Applied-DevOps-adoption-Date.csv', sep=",")
    df_applied=pd.merge(df_applied_issues,df_applied_devops_date,how="inner",on="ProjectName")

    df_applied['BeforeOrAfterDevOps']=np.where(df_applied['DateOpened'] < df_applied['CreationDate'],'Before','After')

    df_applied_before=df_applied[df_applied['BeforeOrAfterDevOps']=='Before']
    df_applied_avg_duration_before=df_applied_before.drop(['IssueNumber','IssueTitle','DateOpened','DateClose','FilePath','CommitComment','Total','Percentage'],axis=1)
    df_applied_avg_duration_before=df_applied_avg_duration_before.groupby(['ProjectName']).mean()
    df_applied_avg_duration_before['IssueTypes']='Before DevOps'
    df_applied_avg_duration_before['Project Category']='AI/ML Applied'



    df_applied_after=df_applied[df_applied['BeforeOrAfterDevOps']=='After']
    df_applied_avg_duration_after=df_applied_after.drop(['IssueNumber','IssueTitle','DateOpened','DateClose','FilePath','CommitComment','Total','Percentage'],axis=1)
    df_applied_avg_duration_after=df_applied_avg_duration_after.groupby(['ProjectName']).mean()
    df_applied_avg_duration_after['IssueTypes']='After DevOps'
    df_applied_avg_duration_after['Project Category']='AI/ML Applied'

    df_applied_avg_duration=df_applied_avg_duration_before.append(df_applied_avg_duration_after)
    Q1=df_applied_avg_duration['Duration'].quantile(0.25)
    Q3=df_applied_avg_duration['Duration'].quantile(0.75)
    IQR=Q3-Q1
    df_applied_avg_duration = df_applied_avg_duration[~((df_applied_avg_duration['Duration'] < (Q1 - 1.5 * IQR)) |(df_applied_avg_duration['Duration'] > (Q3 + 1.5 * IQR)))]




    df_tool_issues1 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-05-20-11-tool.csv',sep=";",error_bad_lines=False)
    df_tool_issues2 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-11-59-32-tool.csv',sep=";",error_bad_lines=False)

    df_tool_issues=df_tool_issues1.append(df_tool_issues2)
    df_tool_devops_date = pd.read_csv('../CSV Files/Tool-DevOps-adoption-Date.csv', sep=",")
    df_tool=pd.merge(df_tool_issues,df_tool_devops_date,how="inner",on="ProjectName")
    df_tool['BeforeOrAfterDevOps']=np.where(df_tool['DateOpened'] < df_tool['CreationDate'],'Before','After')


    df_tool_before=df_tool[df_tool['BeforeOrAfterDevOps']=='Before']
    df_tool_avg_duration_before=df_tool_before.drop(['IssueNumber','IssueTitle','DateOpened','DateClose','FilePath','CommitComment','Total','Percentage'],axis=1)
    df_tool_avg_duration_before=df_tool_avg_duration_before.groupby(['ProjectName']).mean()
    df_tool_avg_duration_before['IssueTypes']='Before DevOps'
    df_tool_avg_duration_before['Project Category']='AI/ML Tool'

    df_tool_after=df_tool[df_tool['BeforeOrAfterDevOps']=='After']
    df_tool_avg_duration_after=df_tool_after.drop(['IssueNumber','IssueTitle','DateOpened','DateClose','FilePath','CommitComment','Total','Percentage'],axis=1)
    df_tool_avg_duration_after=df_tool_avg_duration_after.groupby(['ProjectName']).mean()
    df_tool_avg_duration_after['IssueTypes']='After DevOps'
    df_tool_avg_duration_after['Project Category']='AI/ML Tool'


    df_tool_avg_duration=df_tool_avg_duration_before.append(df_tool_avg_duration_after)
    Q1=df_tool_avg_duration['Duration'].quantile(0.25)
    Q3=df_tool_avg_duration['Duration'].quantile(0.75)
    IQR=Q3-Q1
    df_tool_avg_duration = df_tool_avg_duration[~((df_tool_avg_duration['Duration'] < (Q1 - 1.5 * IQR)) |(df_tool_avg_duration['Duration'] > (Q3 + 1.5 * IQR)))]


    df_noaiml_issues1 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-05-47-15-no-ai-ml.csv',sep=";",error_bad_lines=False)
    df_noaiml_issues2 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-07-43-26-no-ai-ml.csv',sep=";",error_bad_lines=False)
    df_noaiml_issues3 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-09-44-29-no-ai-ml.csv',sep=";",error_bad_lines=False)
    df_noaiml_issues4 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-12-21-50-no-ai-ml.csv',sep=";",error_bad_lines=False)

    df_noaiml_issues=((df_noaiml_issues1.append(df_noaiml_issues2)).append(df_noaiml_issues3)).append(df_noaiml_issues4)
    df_noaiml_devops_date = pd.read_csv('../CSV Files/NoAIML-DevOps-adoption-Date.csv', sep=",")

    df_noaiml=pd.merge(df_noaiml_issues,df_noaiml_devops_date,how="inner",on="ProjectName")
    df_noaiml['BeforeOrAfterDevOps']=np.where(df_noaiml['DateOpened'] < df_noaiml['CreationDate'],'Before','After')


    df_noaiml_before=df_noaiml[df_noaiml['BeforeOrAfterDevOps']=='Before']
    df_noaiml_avg_duration_before=df_noaiml_before.drop(['IssueNumber','IssueTitle','DateOpened','DateClose','FilePath','CommitComment','Total','Percentage'],axis=1)
    df_noaiml_avg_duration_before=df_noaiml_avg_duration_before.groupby(['ProjectName']).mean()
    df_noaiml_avg_duration_before['IssueTypes']='Before DevOps'
    df_noaiml_avg_duration_before['Project Category']='Non-AI/ML'



    df_noaiml_after=df_noaiml[df_noaiml['BeforeOrAfterDevOps']=='After']
    df_noaiml_avg_duration_after=df_noaiml_after.drop(['IssueNumber','IssueTitle','DateOpened','DateClose','FilePath','CommitComment','Total','Percentage'],axis=1)
    df_noaiml_avg_duration_after=df_noaiml_avg_duration_after.groupby(['ProjectName']).mean()
    df_noaiml_avg_duration_after['IssueTypes']='After DevOps'
    df_noaiml_avg_duration_after['Project Category']='Non-AI/ML'


    df_noaiml_avg_duration=df_noaiml_avg_duration_before.append(df_noaiml_avg_duration_after)
    Q1=df_noaiml_avg_duration['Duration'].quantile(0.25)
    Q3=df_noaiml_avg_duration['Duration'].quantile(0.75)
    IQR=Q3-Q1
    df_noaiml_avg_duration = df_noaiml_avg_duration[~((df_noaiml_avg_duration['Duration'] < (Q1 - 1.5 * IQR)) |(df_noaiml_avg_duration['Duration'] > (Q3 + 1.5 * IQR)))]



    df_all=df_applied_avg_duration.append(df_tool_avg_duration).append(df_noaiml_avg_duration)




    df_all.fillna(0)
    print(df_all.columns)

    # Build,CI,Deployment Automation,Monitoring and Logging,Analyzer,Test

    ax=sns.violinplot(cut=0,palette='gist_gray',x=df_all['Project Category'],y= df_all['Duration'], hue= df_all['IssueTypes'], split= True, legend= False, inner= "quartile")
    ax.set(ylabel='Avg Issue Duration', xlabel='Project Category')
    L=plt.legend(bbox_to_anchor=(0.5, -0.35) ,borderaxespad=0,loc='lower center')
    L.get_texts()[0].set_text('Before adopting DevOps')
    L.get_texts()[1].set_text('After adopting DevOps')

    plt.tight_layout()

    plt.savefig('RQ3-IssueReport.eps', format='eps')
    plt.show()

# def avg_issue_duration_devops_vs_non_devops():
#     df_applied_issues1 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-07-21-45-applied.csv',sep=";",error_bad_lines=False)
#     df_applied_issues2 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-10-32-55-applied.csv',sep=";",error_bad_lines=False)
#     df_applied_issues3 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-12-04-44-applied.csv',sep=";",error_bad_lines=False)
#     df_applied_issues4 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-12-52-03-applied.csv',sep=";",error_bad_lines=False)
#     df_applied_issues5 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-10-47-42-applied.csv',sep=";",error_bad_lines=False)
#     df_applied_issues6 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-10-54-12-applied.csv',sep=";",error_bad_lines=False)
#     df_applied_issues7 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-11-26-41-applied.csv',sep=";",error_bad_lines=False)
#
#     df_applied_issues=(((((df_applied_issues1.append(df_applied_issues2)).append(df_applied_issues3)).append(df_applied_issues4)).append(df_applied_issues5)).append(df_applied_issues6)).append(df_applied_issues7)
#     df_applied_devops_date = pd.read_csv('../CSV Files/Applied-DevOps-adoption-Date.csv', sep=",")
#     df_applied_devops=pd.merge(df_applied_issues,df_applied_devops_date,how="inner",on="ProjectName")
#
#     devops_projects=list(df_applied_devops['ProjectName'])
#     df_applied_no_devops=df_applied_issues[~df_applied_issues['ProjectName'].isin(devops_projects)]
#
#
#     # df_applied['BeforeOrAfterDevOps']=np.where(df_applied['DateOpened'] < df_applied['CreationDate'],'Before','After')
#
#     # df_applied_before=df_applied[df_applied['BeforeOrAfterDevOps']=='Before']
#
#     df_applied_devops=df_applied_devops.drop(['IssueNumber','IssueTitle','DateOpened','DateClose','FilePath','CommitComment','Total','Percentage'],axis=1)
#     df_applied_devops=df_applied_devops.groupby(['ProjectName']).mean()
#     df_applied_no_devops=df_applied_no_devops.drop(['IssueNumber','IssueTitle','DateOpened','DateClose'],axis=1)
#     df_applied_no_devops=df_applied_no_devops.groupby(['ProjectName']).mean()
#     df_applied_no_devops['HasDevOps']=0
#     df_applied_devops['HasDevOps'] = 1
#     df_applied=df_applied_devops.append(df_applied_no_devops)
#
#
#     Q1=df_applied['Duration'].quantile(0.25)
#     Q3=df_applied['Duration'].quantile(0.75)
#     IQR=Q3-Q1
#     df_applied = df_applied[~((df_applied['Duration'] < (Q1 - 1.5 * IQR)) |(df_applied['Duration'] > (Q3 + 1.5 * IQR)))]
#     df_applied['Project Category']='AI/ML Applied'
#
#     df_tool_issues1 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-05-20-11-tool.csv',sep=";",error_bad_lines=False)
#     df_tool_issues2 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-11-59-32-tool.csv',sep=";",error_bad_lines=False)
#
#     df_tool_issues=df_tool_issues1.append(df_tool_issues2)
#     df_tool_devops_date = pd.read_csv('../CSV Files/Tool-DevOps-adoption-Date.csv', sep=",")
#     df_tool_devops=pd.merge(df_tool_issues,df_tool_devops_date,how="inner",on="ProjectName")
#
#     devops_projects = list(df_tool_devops['ProjectName'])
#     df_tool_no_devops = df_tool_issues[
#         ~df_tool_issues['ProjectName'].isin(devops_projects)]
#
#
#     # df_applied['BeforeOrAfterDevOps']=np.where(df_applied['DateOpened'] < df_applied['CreationDate'],'Before','After')
#
#     # df_applied_before=df_applied[df_applied['BeforeOrAfterDevOps']=='Before']
#
#     df_tool_devops = df_tool_devops.drop(
#         ['IssueNumber', 'IssueTitle', 'DateOpened', 'DateClose', 'FilePath', 'CommitComment', 'Total', 'Percentage'],
#         axis=1)
#     df_tool_devops = df_tool_devops.groupby(['ProjectName']).mean()
#     df_tool_no_devops = df_tool_no_devops.drop(
#         ['IssueNumber', 'IssueTitle', 'DateOpened', 'DateClose'],
#         axis=1)
#     df_tool_no_devops = df_tool_no_devops.groupby(['ProjectName']).mean()
#
#     df_tool_devops['HasDevOps'] = 1
#     df_tool_no_devops['HasDevOps'] = 0
#
#     df_tool = df_tool_devops.append(df_tool_no_devops)
#
#
#     Q1 = df_tool['Duration'].quantile(0.25)
#     Q3 = df_tool['Duration'].quantile(0.75)
#     IQR = Q3 - Q1
#     df_tool = df_tool[
#         ~((df_tool['Duration'] < (Q1 - 1.5 * IQR)) | (df_tool['Duration'] > (Q3 + 1.5 * IQR)))]
#
#     df_tool['Project Category']='AI/ML Tool'
#
#     df_noaiml_issues1 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-05-47-15-no-ai-ml.csv',sep=";",error_bad_lines=False)
#     df_noaiml_issues2 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-07-43-26-no-ai-ml.csv',sep=";",error_bad_lines=False)
#     df_noaiml_issues3 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-09-44-29-no-ai-ml.csv',sep=";",error_bad_lines=False)
#     df_noaiml_issues4 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-12-21-50-no-ai-ml.csv',sep=";",error_bad_lines=False)
#
#     df_noaiml_issues=((df_noaiml_issues1.append(df_noaiml_issues2)).append(df_noaiml_issues3)).append(df_noaiml_issues4)
#     df_noaiml_devops_date = pd.read_csv('../CSV Files/NoAIML-DevOps-adoption-Date.csv', sep=",")
#
#     df_noaiml_devops=pd.merge(df_noaiml_issues,df_noaiml_devops_date,how="inner",on="ProjectName")
#
#     devops_projects = list(df_noaiml_devops['ProjectName'])
#     df_noaiml_no_devops = df_noaiml_issues[
#         ~df_noaiml_issues['ProjectName'].isin(devops_projects)]
#
#
#     # df_applied['BeforeOrAfterDevOps']=np.where(df_applied['DateOpened'] < df_applied['CreationDate'],'Before','After')
#
#     # df_applied_before=df_applied[df_applied['BeforeOrAfterDevOps']=='Before']
#
#     df_noaiml_devops = df_noaiml_devops.drop(
#         ['IssueNumber', 'IssueTitle', 'DateOpened', 'DateClose', 'FilePath', 'CommitComment', 'Total', 'Percentage'],
#         axis=1)
#     df_noaiml_devops = df_noaiml_devops.groupby(['ProjectName']).mean()
#     df_noaiml_no_devops = df_noaiml_no_devops.drop(
#         ['IssueNumber', 'IssueTitle', 'DateOpened', 'DateClose'],
#         axis=1)
#     df_noaiml_no_devops = df_noaiml_no_devops.groupby(['ProjectName']).mean()
#
#
#
#     df_noaiml_devops['HasDevOps'] = 1
#     df_noaiml_no_devops['HasDevOps'] = 0
#     df_noaiml = df_noaiml_devops.append(df_noaiml_no_devops)
#
#
#     Q1 = df_noaiml['Duration'].quantile(0.25)
#     Q3 = df_noaiml['Duration'].quantile(0.75)
#     IQR = Q3 - Q1
#     df_noaiml = df_noaiml[
#         ~((df_noaiml['Duration'] < (Q1 - 1.5 * IQR)) | (df_noaiml['Duration'] > (Q3 + 1.5 * IQR)))]
#
#     df_noaiml['Project Category']='Non-AI/Ml'
#
#     df_all=df_tool.append(df_applied).append(df_noaiml)
#
#
#
#
#     df_all.fillna(0)
#     print(df_all.columns)
#
#     # Build,CI,Deployment Automation,Monitoring and Logging,Analyzer,Test
#
#     ax=sns.violinplot(cut=0,palette='gist_gray',x=df_all['Project Category'],y= df_all['Duration'], hue= df_all['HasDevOps'], split= True, legend= False, inner= "quartile")
#     ax.set(ylabel='Avg Issue Duration', xlabel='Project Category')
#     L=plt.legend(bbox_to_anchor=(0.5, -0.35) ,borderaxespad=0,loc='lower center')
#     L.get_texts()[0].set_text('Project that do not have DevOps')
#     L.get_texts()[1].set_text('Project that have DevOps')
#
#     plt.tight_layout()
#
#     plt.savefig('RQ3-IssueReport_DevOpsvsNoDevOps.eps', format='eps')
#     plt.savefig('RQ3-IssueReport_DevOpsvsNoDevOps.jpg', format='jpg')
#     plt.show()

def avg_merg_devopstool_vs_non_devopstool(var):

    df_tool_classification = pd.read_csv('../CSV Files/Tool-classification.csv')
    df_applied_classification = pd.read_csv('../CSV Files/Applied-classification.csv')
    df_noaiml_classification = pd.read_csv('../CSV Files/NonML-classification.csv')


    df_applied_codefrequ_df=pd.read_csv('../CSV Files/Commit-Merging-Frequency-Applied-All.csv',sep=",",error_bad_lines=False)

    # df_applied['BeforeOrAfterDevOps']=np.where(df_applied['DateOpened'] < df_applied['CreationDate'],'Before','After')

    # df_applied_before=df_applied[df_applied['BeforeOrAfterDevOps']=='Before']

    df_applied=pd.merge(df_applied_codefrequ_df,df_applied_classification,how="left",on="ProjectName")
    # df_applied.fillna(0,inplace=True)
    Q1=df_applied['MonthlyMergingCommitsAvg'].quantile(0.25)
    Q3=df_applied['MonthlyMergingCommitsAvg'].quantile(0.75)
    IQR=Q3-Q1
    df_applied = df_applied[~((df_applied['MonthlyMergingCommitsAvg'] < (Q1 - 1.5 * IQR)) |(df_applied['MonthlyMergingCommitsAvg'] > (Q3 + 1.5 * IQR)))]
    df_applied['Project Category']='AI/ML Applied'

    df_tool_codefrequ_df=pd.read_csv('../CSV Files/Commit-Merging-Frequency-Tool-All.csv',sep=",",error_bad_lines=False)
    # df_tool_devops_date = pd.read_csv('../Tool-DevOps-adoption-Date.csv',sep=",")
    df_tool=pd.merge(df_tool_codefrequ_df,df_tool_classification,how="left",on="ProjectName")
    # df_tool.fillna(0,inplace=True)
    # df_tool = df_tool.drop(
    #     ['IssueNumber', 'IssueTitle', 'DateOpened', 'DateClose'],
    #     axis=1)

    Q1 = df_tool['MonthlyMergingCommitsAvg'].quantile(0.25)
    Q3 = df_tool['MonthlyMergingCommitsAvg'].quantile(0.75)
    IQR = Q3 - Q1
    df_tool = df_tool[
        ~((df_tool['MonthlyMergingCommitsAvg'] < (Q1 - 1.5 * IQR)) | (df_tool['MonthlyMergingCommitsAvg'] > (Q3 + 1.5 * IQR)))]
    df_tool['Project Category']='AI/ML Tool'


    df_noaiml_codefrequ_df=pd.read_csv('../CSV Files/Commit-Merging-Frequency-NonAIML-All.csv',sep=",",error_bad_lines=False)

    df_noaiml=pd.merge(df_noaiml_codefrequ_df,df_noaiml_classification,how="left",on="ProjectName")

    Q1 = df_noaiml['MonthlyMergingCommitsAvg'].quantile(0.25)
    Q3 = df_noaiml['MonthlyMergingCommitsAvg'].quantile(0.75)
    IQR = Q3 - Q1
    df_noaiml = df_noaiml[
        ~((df_noaiml['MonthlyMergingCommitsAvg'] < (Q1 - 1.5 * IQR)) | (df_noaiml['MonthlyMergingCommitsAvg'] > (Q3 + 1.5 * IQR)))]

    df_noaiml['Project Category']='Non-AI/Ml'

    df_all = df_applied.append(df_tool).append(df_noaiml)


    # df_all.fillna(0)

    ax=sns.violinplot(cut=0,palette='gist_gray',x=df_all['Project Category'],y= df_all['MonthlyMergingCommitsAvg'], hue= df_all[var],
                      split= True, legend= False, inner= "quartile")
    ax.set(ylabel='Avg. Monthly Merging Commits (Commits)', xlabel='Project Category')
    L=plt.legend(bbox_to_anchor=(0.5, -0.35) ,borderaxespad=0,loc='lower center')
    L.get_texts()[0].set_text('Project that do not have '+var+' tool(s)')
    L.get_texts()[1].set_text('Project that have '+var+' tool(s)')

    plt.tight_layout()

    plt.savefig('RQ3-MergeFreq_'+var+'.eps', format='eps')
    plt.savefig('RQ3-MergeFreq_'+var+'.jpg', format='jpg')
    plt.show()

def avg_commit_devopstool_vs_non_devopstool(var):

    df_tool_classification = pd.read_csv('../CSV Files/Tool-classification.csv')
    df_applied_classification = pd.read_csv('../CSV Files/Applied-classification.csv')
    df_noaiml_classification = pd.read_csv('../CSV Files/NonML-classification.csv')


    df_applied_codefrequ_df=pd.read_csv('../CSV Files/Commit-Merging-Frequency-Applied-All.csv',sep=",",error_bad_lines=False)

    # df_applied['BeforeOrAfterDevOps']=np.where(df_applied['DateOpened'] < df_applied['CreationDate'],'Before','After')

    # df_applied_before=df_applied[df_applied['BeforeOrAfterDevOps']=='Before']

    df_applied=pd.merge(df_applied_codefrequ_df,df_applied_classification,how="left",on="ProjectName")
    # df_applied.fillna(0,inplace=True)
    Q1=df_applied['MonthlyAllCommitAvg'].quantile(0.25)
    Q3=df_applied['MonthlyAllCommitAvg'].quantile(0.75)
    IQR=Q3-Q1
    df_applied = df_applied[~((df_applied['MonthlyAllCommitAvg'] < (Q1 - 1.5 * IQR)) |(df_applied['MonthlyAllCommitAvg'] > (Q3 + 1.5 * IQR)))]
    df_applied['Project Category']='AI/ML Applied'

    df_tool_codefrequ_df=pd.read_csv('../CSV Files/Commit-Merging-Frequency-Tool-All.csv',sep=",",error_bad_lines=False)
    # df_tool_devops_date = pd.read_csv('../Tool-DevOps-adoption-Date.csv',sep=",")
    df_tool=pd.merge(df_tool_codefrequ_df,df_tool_classification,how="left",on="ProjectName")
    # df_tool.fillna(0,inplace=True)
    # df_tool = df_tool.drop(
    #     ['IssueNumber', 'IssueTitle', 'DateOpened', 'DateClose'],
    #     axis=1)

    Q1 = df_tool['MonthlyAllCommitAvg'].quantile(0.25)
    Q3 = df_tool['MonthlyAllCommitAvg'].quantile(0.75)
    IQR = Q3 - Q1
    df_tool = df_tool[
        ~((df_tool['MonthlyAllCommitAvg'] < (Q1 - 1.5 * IQR)) | (df_tool['MonthlyAllCommitAvg'] > (Q3 + 1.5 * IQR)))]
    df_tool['Project Category']='AI/ML Tool'


    df_noaiml_codefrequ_df=pd.read_csv('../CSV Files/Commit-Merging-Frequency-NonAIML-All.csv',sep=",",error_bad_lines=False)

    df_noaiml=pd.merge(df_noaiml_codefrequ_df,df_noaiml_classification,how="left",on="ProjectName")

    Q1 = df_noaiml['MonthlyAllCommitAvg'].quantile(0.25)
    Q3 = df_noaiml['MonthlyAllCommitAvg'].quantile(0.75)
    IQR = Q3 - Q1
    df_noaiml = df_noaiml[
        ~((df_noaiml['MonthlyAllCommitAvg'] < (Q1 - 1.5 * IQR)) | (df_noaiml['MonthlyAllCommitAvg'] > (Q3 + 1.5 * IQR)))]

    df_noaiml['Project Category']='Non-AI/Ml'

    df_all=df_applied.append(df_tool).append(df_noaiml)


    # df_all.fillna(0)

    ax=sns.violinplot(cut=0,palette='gist_gray',x=df_all['Project Category'],y= df_all['MonthlyAllCommitAvg'], hue= df_all[var],
                      split= True, legend= False, inner= "quartile")
    ax.set(ylabel='Avg. Monthly Commits (Commits)', xlabel='Project Category')
    L=plt.legend(bbox_to_anchor=(0.5, -0.35) ,borderaxespad=0,loc='lower center')
    L.get_texts()[0].set_text('Project that do not have '+var+' tool(s)')
    L.get_texts()[1].set_text('Project that have '+var+' tool(s)')

    plt.tight_layout()

    plt.savefig('RQ3-CommitFreq_'+var+'.eps', format='eps')
    plt.savefig('RQ3-CommitFreq_'+var+'.jpg', format='jpg')
    plt.show()

def avg_issue_devopstool_vs_non_devopstool(var):
    df_tool_classification = pd.read_csv('../CSV Files/Tool-classification.csv')
    df_applied_classification = pd.read_csv('../CSV Files/Applied-classification.csv')
    df_noaiml_classification = pd.read_csv('../CSV Files/NonML-classification.csv')


    # df_applied_issues1 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-07-21-45-applied.csv',sep=";",error_bad_lines=False)
    # df_applied_issues2 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-10-32-55-applied.csv',sep=";",error_bad_lines=False)
    # df_applied_issues3 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-12-04-44-applied.csv',sep=";",error_bad_lines=False)
    # df_applied_issues4 = pd.read_csv('../CSV Files/projects-issuereports-03-31-21-12-52-03-applied.csv',sep=";",error_bad_lines=False)
    # df_applied_issues5 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-10-47-42-applied.csv',sep=";",error_bad_lines=False)
    # df_applied_issues6 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-10-54-12-applied.csv',sep=";",error_bad_lines=False)
    # df_applied_issues7 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-11-26-41-applied.csv',sep=";",error_bad_lines=False)

    df_applied_issues=pd.read_csv('../CSV Files/projects-issuereports-10-19-21-09-41-18-applied.csv',sep=";",error_bad_lines=False)

    # df_applied['BeforeOrAfterDevOps']=np.where(df_applied['DateOpened'] < df_applied['CreationDate'],'Before','After')

    # df_applied_before=df_applied[df_applied['BeforeOrAfterDevOps']=='Before']

    df_applied_issues = df_applied_issues.drop(['IssueNumber', 'IssueTitle', 'DateOpened', 'DateClose'], axis=1)
    df_applied_issues=df_applied_issues.groupby(['ProjectName']).mean()


    Q1=df_applied_issues['Duration'].quantile(0.25)
    Q3=df_applied_issues['Duration'].quantile(0.75)
    IQR=Q3-Q1
    df_applied_issues = df_applied_issues[~((df_applied_issues['Duration'] < (Q1 - 1.5 * IQR)) |(df_applied_issues['Duration'] > (Q3 + 1.5 * IQR)))]
    df_applied_issues['Project Category']='AI/ML Applied'

    df_applied = pd.merge(df_applied_issues, df_applied_classification, how="left", on="ProjectName")

    print(df_applied_issues)
    # df_tool_issues1 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-05-20-11-tool.csv',sep=";",error_bad_lines=False)
    # df_tool_issues2 = pd.read_csv('../CSV Files/projects-issuereports-04-01-21-11-59-32-tool.csv',sep=";",error_bad_lines=False)

    df_tool_issues=pd.read_csv('../CSV Files/projects-issuereports-10-19-21-12-10-09-tool.csv',sep=";",error_bad_lines=False)
    # df_tool_devops_date = pd.read_csv('../Tool-DevOps-adoption-Date.csv',sep=",")
    df_tool_issues = df_tool_issues.drop(
        ['IssueNumber', 'IssueTitle', 'DateOpened', 'DateClose'],
        axis=1)
    df_tool_issues = df_tool_issues.groupby(['ProjectName']).mean()

    # df_tool = df_tool.groupby(['ProjectName']).mean()
    #
    # df_tool.to_csv('tool_mean_churn')

    Q1 = df_tool_issues['Duration'].quantile(0.25)
    Q3 = df_tool_issues['Duration'].quantile(0.75)
    IQR = Q3 - Q1
    df_tool_issues = df_tool_issues[
        ~((df_tool_issues['Duration'] < (Q1 - 1.5 * IQR)) | (df_tool_issues['Duration'] > (Q3 + 1.5 * IQR)))]
    df_tool=pd.merge(df_tool_issues,df_tool_classification,how="left",on="ProjectName")

    df_tool['Project Category']='AI/ML Tool'
    print(df_tool)
    # df_noaiml_issues1 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-05-47-15-no-ai-ml.csv',sep=";",error_bad_lines=False)
    # df_noaiml_issues2 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-07-43-26-no-ai-ml.csv',sep=";",error_bad_lines=False)
    # df_noaiml_issues3 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-09-44-29-no-ai-ml.csv',sep=";",error_bad_lines=False)
    # df_noaiml_issues4 = pd.read_csv('../CSV Files/projects-issuereports-04-02-21-12-21-50-no-ai-ml.csv',sep=";",error_bad_lines=False)

    df_noaiml_issues=pd.read_csv('../CSV Files/projects-issuereports-10-19-21-17-05-47-no-ai-ml.csv',sep=";",error_bad_lines=False)
    # df_noaiml_devops_date = pd.read_csv('../NoAIML-DevOps-adoption-Date.csv',sep=",")
    df_noaiml_issues = df_noaiml_issues.drop(
        ['IssueNumber', 'IssueTitle', 'DateOpened', 'DateClose'],
        axis=1)
    df_noaiml_issues = df_noaiml_issues.groupby(['ProjectName']).mean()

    # df_noaiml = df_noaiml.groupby(['ProjectName']).mean()
    # df_noaiml.to_csv('noaiml_mean_churn.csv')

    Q1 = df_noaiml_issues['Duration'].quantile(0.25)
    Q3 = df_noaiml_issues['Duration'].quantile(0.75)
    IQR = Q3 - Q1
    df_noaiml_issues = df_noaiml_issues[
        ~((df_noaiml_issues['Duration'] < (Q1 - 1.5 * IQR)) | (df_noaiml_issues['Duration'] > (Q3 + 1.5 * IQR)))]

    df_noaiml_issues['Project Category']='Non-AI/Ml'
    df_noaiml = pd.merge(df_noaiml_issues, df_noaiml_classification, how="left", on="ProjectName")

    print(df_noaiml)


    df_all = df_applied.append(df_tool).append(df_noaiml)




    df_all.fillna(0)
    # print(df_all.columns)
    print()
    # Build,CI,Deployment,Monitoring,Analyzer,Test

    ax=sns.violinplot(cut=0,palette='gist_gray',x=df_all['Project Category'],y= df_all['Duration'], hue= df_all[var],
                      split= True, legend= False, inner= "quartile")
    ax.set(ylabel='Avg. Issue Duration (Days)', xlabel='Project Category')
    L=plt.legend(bbox_to_anchor=(0.5, -0.35) ,borderaxespad=0,loc='lower center')
    L.get_texts()[0].set_text('Project that do not have '+var+' tool(s)')
    L.get_texts()[1].set_text('Project that have '+var+' tool(s)')

    plt.tight_layout()

    plt.savefig('RQ3-IssueReport_'+var+'.eps', format='eps')
    plt.savefig('RQ3-IssueReport_'+var+'.jpg', format='jpg')
    plt.show()

def avg_count_gen():
    df = pd.read_csv('csv_out_applied.csv',sep=';')
    old_project='empty'
    csv_out=open('applied_commitgoal_percentages.csv','w+')
    nb_both=0
    nb_build=0
    nb_bug=0
    nb_cimprov=0
    nb_all=0
    for index,row in df.iterrows():
        project_name=row['ProjectName']
        IsBuildANDBugFix=row['IsBuildANDBugFix']
        IsOnlyBuildFix=row['IsOnlyBuildFix']
        IsOnlyBugFix=row['IsOnlyBugFix']
        IsCodeImprovement=row['IsCodeImprovement']
        if old_project == 'empty':
            old_project=project_name
        if old_project != project_name:
            percent_both="%.5f" % ((nb_both/nb_all))
            percent_build="%.5f" % ((nb_build/nb_all))
            percent_bug="%.5f" % ((nb_bug/nb_all))
            percent_cimprov="%.5f" % ((nb_cimprov/nb_all))
            csv_out.write(old_project+','+percent_both+','+percent_build+','+percent_bug+','+percent_cimprov+'\n')
            nb_both = 0
            nb_build = 0
            nb_bug = 0
            nb_cimprov = 0
            nb_all = 0
            old_project=project_name
        nb_all+=1
        if(IsBuildANDBugFix):
            nb_both+=1
        elif(IsOnlyBuildFix):
            nb_build+=1
        elif(IsOnlyBugFix):
            nb_bug+=1
        elif(IsCodeImprovement):
            nb_cimprov+=1
        else:
            nb_cimprov += 1
    percent_both = "%.5f" % ((nb_both / nb_all))
    percent_build = "%.5f" % ((nb_build / nb_all))
    percent_bug = "%.5f" % ((nb_bug / nb_all))
    percent_cimprov = "%.5f" % ((nb_cimprov / nb_all))
    csv_out.write(
        old_project + ',' + percent_both + ',' + percent_build + ',' + percent_bug + ',' + percent_cimprov + '\n')


    df = pd.read_csv('csv_out_tool.csv', sep=';')
    old_project = 'empty'
    csv_out = open('tool_commitgoal_percentages.csv','w+')
    nb_both = 0
    nb_build = 0
    nb_bug = 0
    nb_cimprov = 0
    nb_all = 0

    for index, row in df.iterrows():
        project_name = row['ProjectName']
        IsBuildANDBugFix = row['IsBuildANDBugFix']
        IsOnlyBuildFix = row['IsOnlyBuildFix']
        IsOnlyBugFix = row['IsOnlyBugFix']
        IsCodeImprovement = row['IsCodeImprovement']
        if old_project == 'empty':
            old_project = project_name
        if old_project != project_name:
            percent_both = "%.5f" % ((nb_both / nb_all))
            percent_build = "%.5f" % ((nb_build / nb_all))
            percent_bug = "%.5f" % ((nb_bug / nb_all))
            percent_cimprov = "%.5f" % ((nb_cimprov / nb_all))
            csv_out.write(
                old_project + ',' + percent_both + ',' + percent_build + ',' + percent_bug + ',' + percent_cimprov + '\n')
            nb_both = 0
            nb_build = 0
            nb_bug = 0
            nb_cimprov = 0
            nb_all = 0
            old_project = project_name
            # count += 1
        nb_all += 1
        if (IsBuildANDBugFix):
            nb_both += 1
        elif (IsOnlyBuildFix):
            nb_build += 1
        elif (IsOnlyBugFix):
            nb_bug += 1
        elif (IsCodeImprovement):
            nb_cimprov += 1
        else:
            nb_cimprov += 1
    percent_both = "%.5f" % ((nb_both / nb_all) )
    percent_build = "%.5f" % ((nb_build / nb_all) )
    percent_bug = "%.5f" % ((nb_bug / nb_all) )
    percent_cimprov = "%.5f" % ((nb_cimprov / nb_all) )
    csv_out.write(
        old_project + ',' + percent_both + ',' + percent_build + ',' + percent_bug + ',' + percent_cimprov + '\n')


    df = pd.read_csv('csv_out_nonaiml.csv', sep=';')
    old_project = 'empty'
    csv_out = open('noml_commitgoal_percentages.csv','w+')
    nb_both = 0
    nb_build = 0
    nb_bug = 0
    nb_cimprov = 0
    nb_all = 0

    for index, row in df.iterrows():
        project_name = row['ProjectName']
        IsBuildANDBugFix = row['IsBuildANDBugFix']
        IsOnlyBuildFix = row['IsOnlyBuildFix']
        IsOnlyBugFix = row['IsOnlyBugFix']
        IsCodeImprovement = row['IsCodeImprovement']
        if old_project == 'empty':
            old_project = project_name

        if old_project != project_name:
            percent_both = "%.5f" % ((nb_both / nb_all))
            percent_build = "%.5f" % ((nb_build / nb_all))
            percent_bug = "%.5f" % ((nb_bug / nb_all))
            percent_cimprov = "%.5f" % ((nb_cimprov / nb_all))
            csv_out.write(
                old_project + ',' + percent_both + ',' + percent_build + ',' + percent_bug + ',' + percent_cimprov + '\n')
            nb_both = 0
            nb_build = 0
            nb_bug = 0
            nb_cimprov = 0
            nb_all = 0
            old_project = project_name
            # count += 1
        nb_all += 1
        if (IsBuildANDBugFix):
            nb_both += 1
        elif (IsOnlyBuildFix):
            nb_build += 1
        elif (IsOnlyBugFix):
            nb_bug += 1
        elif (IsCodeImprovement):
            nb_cimprov += 1
        else:
            nb_cimprov += 1
    percent_both = "%.5f" % ((nb_both / nb_all) )
    percent_build = "%.5f" % ((nb_build / nb_all) )
    percent_bug = "%.5f" % ((nb_bug / nb_all) )
    percent_cimprov = "%.5f" % ((nb_cimprov / nb_all) )
    csv_out.write(
        old_project + ',' + percent_both + ',' + percent_build + ',' + percent_bug + ',' + percent_cimprov + '\n')





def avg_gen():
    df = pd.read_csv('devopsfiles-churn-10-20-21-11-11-40-applied.csv',sep=';')
    # df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    # print(df)
    df = df.groupby(['ProjectName']).mean()
    df.to_csv('Applied_avg_churn.csv')


    df = pd.read_csv('devopsfiles-churn-11-18-21-10-32-33-tool.csv',sep=';')
    # df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    df = df.groupby(['ProjectName']).mean()
    df.to_csv('Tool_avg_churn.csv')

    df = pd.read_csv('devopsfiles-churn-10-20-21-16-33-58-no-ai-ml.csv',sep=';')
    # df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    df = df.groupby(['ProjectName']).mean()
    df.to_csv('NoAIML_avg_churn.csv')

# avg_gen()

if __name__ == "__main__":
    list_l=['Build','CI','Deployment','Monitoring','Analyzer','Test']
    for var in list_l:
    #     avg_commit_devopstool_vs_non_devopstool(var)
    #     avg_merg_devopstool_vs_non_devopstool(var)
        avg_issue_devopstool_vs_non_devopstool(var)
    # # avg_count_gen()
    # # codechurn()
    # avg_count_gen()
    # avg_issue_devopstool_vs_non_devopstool('Build')
