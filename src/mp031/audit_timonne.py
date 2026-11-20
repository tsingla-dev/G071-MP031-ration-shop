'''audit results to find sentinel val and stuck sensor:

**sentinel_value**
- present: true
- column: `cards_attached`
- value: `-999`
- count: `65`

**stuck_sensor**
- present: true
- column: `biometric_failures`
- start_date: `2026-03-30`
- end_date: `2026-04-17`
- repeated reading: `64`
- affected rows: `119`

**Additional verification:**
- `-999` occurs 65 times in train.csv and 0 times in later.csv.
- The biometric_failures column reports exactly 64 across all 19 dates from March 30 to April 17.
- Readings vary immediately before and after this period.

'''

import pandas as pd

train = pd.read_csv("data/raw/train.csv")
later = pd.read_csv("data/raw/later.csv")

print("TRAIN DATA:")
print(train.head())

print("\nNUMERIC COLUMN FREQUENCIES:")

numeric_cols = train.select_dtypes(include="number").columns

for col in numeric_cols:
    print("\nColumn:", col)
    print(train[col].value_counts().head(20))

print("\nSENTINEL CHECK:")

sentinel_col = "cards_attached"
sentinel_value = -999

count = (train[sentinel_col] == sentinel_value).sum()

print("Present:", count > 0)
print("Column:", sentinel_col)
print("Value:", sentinel_value)
print("Count:", count)


DATE_COL = "date"

train[DATE_COL] = pd.to_datetime(train[DATE_COL])

train = train.sort_values(DATE_COL).reset_index(drop=True)

print("\nSTUCK SENSOR CHECK:")

for col in numeric_cols:

    values = train[col]
    dates = train[DATE_COL]

    groups = values.ne(values.shift()).cumsum()

    for group_id in groups.unique():

        mask = groups == group_id

        readings = values[mask]
        stretch_dates = dates[mask]

        if (
            len(readings) >= 3
            and stretch_dates.nunique() >= 3
            and readings.notna().all()
        ):

            print("\nColumn:", col)
            print("Reading:", readings.iloc[0])
            print("Start date:", stretch_dates.min().strftime("%Y-%m-%d"))
            print("End date:", stretch_dates.max().strftime("%Y-%m-%d"))
            print("Number of rows:", len(readings))


print("\nVERIFYING STUCK SENSOR:")

col = "biometric_failures"

start = pd.Timestamp("2026-03-30")
end = pd.Timestamp("2026-04-17")

before = train[train["date"] < start].tail(10)
after = train[train["date"] > end].head(10)

print("\nBEFORE THE STRETCH:")
print(before[["date", col]])

print("\nAFTER THE STRETCH:")
print(after[["date", col]])

print("\nREADINGS DURING THE STRETCH:")
during = train[
    (train["date"] >= start) &
    (train["date"] <= end)
]

print(during.groupby("date")[col].agg(
    ["count", "nunique", "min", "max"]
))

print("\nLATER DATA SENTINEL COMPARISON:")

later_count = (later["cards_attached"] == -999).sum()

print("Column: cards_attached")
print("Value: -999")
print("Count in train.csv:", count)
print("Count in later.csv:", later_count)