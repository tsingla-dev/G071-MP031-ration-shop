import pandas as pd

train = pd.read_csv("data/raw/train.csv")
extra_duplicates = train.duplicated().sum()

print("Extra duplicate rows:", extra_duplicates)

holdout = pd.read_csv("data/raw/holdout_features.csv")
train_only_columns = []

for column in train.columns:
    if column not in holdout.columns and column != "grain_kg":
        train_only_columns.append(column)

print("Extra train-only columns:", train_only_columns)