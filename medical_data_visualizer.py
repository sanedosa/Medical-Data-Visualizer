import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
bmi=df["weight"]/(df["height"]/100)**2
overweight=bmi>25
df['overweight'] = overweight.astype(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df.loc[df.cholesterol ==1, 'cholesterol'] = 0
df.loc[df.cholesterol >1, 'cholesterol'] = 1
df.loc[df.gluc ==1, 'gluc'] = 0
df.loc[df.gluc >1, 'gluc'] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df.melt(value_vars=["active", "alco", "cholesterol", "gluc", "overweight", "smoke"])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    # df_cat.loc[(df_cat.variable=="active")&(df_cat.value==1),"total"]=df_cat[(df_cat.variable=="active")&(df_cat.value==1)].index.size
    # df_cat.loc[(df_cat.variable=="active")&(df_cat.value==0),"total"]=df_cat[(df_cat.variable=="active")&(df_cat.value==0)].index.size
    # df_cat.loc[(df_cat.variable=="alco")&(df_cat.value==1),"total"]=df_cat[(df_cat.variable=="alco")&(df_cat.value==1)].index.size
    # df_cat.loc[(df_cat.variable=="alco")&(df_cat.value==0),"total"]=df_cat[(df_cat.variable=="alco")&(df_cat.value==0)].index.size
    # df_cat.loc[(df_cat.variable=="cholesterol")&(df_cat.value==1),"total"]=df_cat[(df_cat.variable=="cholesterol")&(df_cat.value==1)].index.size
    # df_cat.loc[(df_cat.variable=="cholesterol")&(df_cat.value==0),"total"]=df_cat[(df_cat.variable=="cholesterol")&(df_cat.value==0)].index.size
    # df_cat.loc[(df_cat.variable=="gluc")&(df_cat.value==1),"total"]=df_cat[(df_cat.variable=="gluc")&(df_cat.value==1)].index.size
    # df_cat.loc[(df_cat.variable=="gluc")&(df_cat.value==0),"total"]=df_cat[(df_cat.variable=="gluc")&(df_cat.value==0)].index.size
    # df_cat.loc[(df_cat.variable=="overweight")&(df_cat.value==1),"total"]=df_cat[(df_cat.variable=="overweight")&(df_cat.value==1)].index.size
    # df_cat.loc[(df_cat.variable=="overweight")&(df_cat.value==0),"total"]=df_cat[(df_cat.variable=="overweight")&(df_cat.value==0)].index.size
    # df_cat.loc[(df_cat.variable=="smoke")&(df_cat.value==1),"total"]=df_cat[(df_cat.variable=="smoke")&(df_cat.value==1)].index.size
    # df_cat.loc[(df_cat.variable=="smoke")&(df_cat.value==0),"total"]=df_cat[(df_cat.variable=="smoke")&(df_cat.value==0)].index.size
   
   
    # df_cat = df.melt(id_vars="cardio",value_vars=["active", "alco", "cholesterol", "gluc", "overweight", "smoke"])
    df_cat = df.melt(id_vars="cardio",value_vars=["active", "alco", "cholesterol", "gluc", "overweight", "smoke"]).value_counts().reset_index()
    df_cat.rename(columns = {0:'total'}, inplace = True) 
    df_cat=df_cat.sort_values(by=["variable"])


    np.float = float    
    np.int = int   #module 'numpy' has no attribute 'int'
    np.object = object    #module 'numpy' has no attribute 'object'
    np.bool = bool 

    # Draw the catplot with 'sns.catplot()'
    sns.catplot(x="variable", y="total", col="cardio", hue="value",data=df_cat, kind="bar")


    # Get the figure for the output
    fig = sns.catplot(x="variable", y="total", col="cardio", hue="value",data=df_cat, kind="bar").fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    # df_heat = df[df["ap_lo"]<=df["ap_hi"]]
    # df_heat = df_heat.drop(df_heat[df_heat['height'] < df_heat['height'].quantile(0.025)].index)
    # df_heat = df_heat.drop(df_heat[df_heat['height'] > df_heat['height'].quantile(0.975)].index)
    # df_heat = df_heat.drop(df_heat[df_heat['weight'] < df_heat['weight'].quantile(0.025)].index)
    # df_heat = df_heat.drop(df_heat[df_heat['weight'] > df_heat['weight'].quantile(0.975)].index)

    df_heat = df[(df["height"]>=df["height"].quantile(0.025))
                &(df["height"]<=df["height"].quantile(0.975))
                &(df["weight"]>=df["weight"].quantile(0.025))
                &(df["weight"]<=df["weight"].quantile(0.975))
                &(df["ap_lo"]<=df["ap_hi"])]
    
    # Calculate the correlation matrix
    corr=df_heat.corr()

    # Generate a mask for the upper triangle
    mask=np.triu(np.ones_like(corr))



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(9, 9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, annot=True, cmap="magma",mask=mask, fmt=".1f")


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
