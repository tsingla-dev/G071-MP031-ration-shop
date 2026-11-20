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






later = pd.read_csv("data/raw/later.csv")

for column in ["shop_area", "block"]:
    print("\nColumn:", column)
    print("Training spellings:", list(train[column].unique()))
    print("Clean spellings:", list(later[column].unique()))








    print("\nTypical training values by block:")
print(train.groupby("block").median(numeric_only=True).T)

print("\nTypical later values by block:")
print(later.groupby("block").median(numeric_only=True).T)










north_stock = train.loc[train["block"] == "Block North", "stock_kg_morning"]
other_stock = train.loc[train["block"] != "Block North", "stock_kg_morning"]

print("Block North after dividing by 1000:", (north_stock / 1000).agg(["min", "mean", "max"]))
print("Other training blocks:", other_stock.agg(["min", "mean", "max"]))







sorted_targets = train["grain_kg"].sort_values(ascending=False)
print("\nLargest 30 grain_kg values:")
print(sorted_targets.head(30).tolist())