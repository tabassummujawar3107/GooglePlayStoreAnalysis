# Importing Libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import os

warnings.filterwarnings('ignore')

# Load the CSV file
file_path = rfile_path = r"C:\Users\Dell\OneDrive\Desktop\googles\googleplaystore.csv";
df = pd.read_csv(file_path)
  
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found at {file_path}")

df = pd.read_csv(file_path)
df.head(4)

# Checking specific rows
df.iloc[10474:10494]

# Set the option to display all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Checking the shape of the dataset
print(f'The number of Rows are "{df.shape[0]}", and the number of columns are "{df.shape[1]}"')

# Displaying column names
print(f'The name of the columns are: {df.columns}')

# Checking dataset information
df.info()

# Summarizing numerical columns
df.describe()

# Removing a problematic row
df.drop(10472, axis=0, inplace=True)

# Converting 'Reviews' column to integer
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce').fillna(0).astype(int)

# Handling 'Size' column
df['Size'].fillna("0", inplace=True)

def convert_into_bytes(column_name):
    if isinstance(column_name, str):
        column_name = column_name.replace(",", "")
        if 'k' in column_name:
            return float(column_name.replace("k", "")) * 1024
        elif 'M' in column_name:
            return float(column_name.replace("M", "")) * 1024 * 1024
        elif 'Varies with device' in column_name:
            return np.nan
    return column_name

df['Size'] = df['Size'].apply(convert_into_bytes)

# Cleaning 'Installs' column
df['Installs'] = df['Installs'].astype(str).str.replace('[+,]', '', regex=True)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce').fillna(0).astype(int)

# Creating 'Installs_category' column
bins = [-1, 0, 10, 1000, 10000, 100000, 1000000, 10000000, 10000000000]
labels = ['no', 'Very low', 'Low', 'Moderate', 'More than moderate', 'High', 'Very High', 'Top Notch']
df['Installs_category'] = pd.cut(df['Installs'], bins=bins, labels=labels)

# Cleaning 'Price' column
df['Price'] = df['Price'].astype(str).str.replace("$", "").astype(float)

# Checking for missing values
df.isnull().sum().sort_values(ascending=False)

# Plot missing values
plt.figure(figsize=(16, 6))
sns.heatmap(df.isnull(), yticklabels=False, cbar=False, cmap='viridis')

plt.figure(figsize=(16, 6))
missing_percentage = df.isnull().sum()/len(df) * 100
missing_percentage.plot(kind='bar')
plt.xlabel('Columns')
plt.ylabel('Percentage')
plt.title('Percentage of Missing Values in Each Column')

# Handling missing values in Rating column
df['Rating'].fillna(df['Rating'].mean(), inplace=True)

# Checking duplicates
df.drop_duplicates(inplace=True)

# Insights from Data
print(df['Category'].value_counts().head(10))
print(df.groupby('Category')['Installs'].sum().sort_values(ascending=False).head(10))
print(df.groupby('Category')['Reviews'].sum().sort_values(ascending=False).head(10))
print(df.groupby('Category')['Rating'].mean().sort_values(ascending=False).head(10))

# Plot rating distribution
plt.figure(figsize=(16, 6))
sns.kdeplot(df['Rating'], color="blue", shade=True)
plt.title('Rating Distribution')

# Scatter plot between Rating, Reviews, and Installs
plt.figure(figsize=(16, 6))
sns.scatterplot(x='Rating', y='Reviews', hue='Installs_category', data=df)

plt.figure(figsize=(16, 6))
sns.scatterplot(x=np.log10(df['Reviews'] + 1), y=np.log10(df['Installs'] + 1), data=df)

# Line plot for trends
sns.lmplot(data=df, x='Reviews', y='Installs')

plt.show()
