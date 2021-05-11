import pandas as pd

df_tool = pd.read_csv('../CSV Inputs/devsonly_reclassified_commit-types-files-01-05-21-20-40-30-tool.csv',sep=';')
df_applied = pd.read_csv('../CSV Inputs/devsonly_reclassified_commit-types-files-01-05-21-20-42-19-applied.csv',sep=';')
df_noaiml = pd.read_csv('../CSV Inputs/devsonly_reclassified_commit-types-files-01-05-21-20-44-09-no-ai-ml.csv',sep=';')

df_tool_classification = pd.read_csv('../CSV Files/ToolProjects_classification.csv')
df_applied_classification = pd.read_csv('../CSV Files/AppliedProjects_classification.csv')
df_noaiml_classification = pd.read_csv('../CSV Files/NoAIMLProjects_classification.csv')

df_tool_bci=df_tool_classification.loc[(df_tool_classification['Build']==1) & (df_tool_classification['CI']==1)]
df_tool_bciprojects=list(df_tool_bci['ProjectName'])


df_applied_bci=df_applied_classification.loc[(df_applied_classification['Build']==1) & (df_applied_classification['CI']==1)]
df_applied_bciprojects=list(df_applied_bci['ProjectName'])

df_noaiml_bci=df_noaiml_classification.loc[(df_noaiml_classification['Build']==1) & (df_noaiml_classification['CI']==1)]
df_noaiml_bciprojects=list(df_noaiml_bci['ProjectName'])


df_tool= df_tool.loc[df_tool['ProjectName'].isin(df_tool_bciprojects)]
df_applied= df_applied.loc[df_applied['ProjectName'].isin(df_applied_bciprojects)]
df_noaiml= df_noaiml.loc[df_noaiml['ProjectName'].isin(df_noaiml_bciprojects)]

df_tool.to_csv('commits_tool_B_CI_ONLY.csv',index=False)
df_applied.to_csv('commits_applied_B_CI_ONLY.csv',index=False)
df_noaiml.to_csv('commits_noaiml_B_CI_ONLY.csv',index=False)

