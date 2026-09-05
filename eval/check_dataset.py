import pandas as pd


df = pd.read_csv("data/incidents.csv")


print("Number of records:", len(df))

print("\nIncident distribution:")
print(df["true_label"].value_counts())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDataset columns:")
print(list(df.columns))