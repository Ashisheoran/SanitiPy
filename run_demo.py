import pandas as pd
from sanitipy import DataCleaner

def main():
    # df = pd.DataFrame({
    #     "age": [25, None, 30, None, 40, None],
    #     "salary": [50000, 52000, None, 51000, None, 52000],
    #     "department": ["HR", "HR", "IT", None, "IT", "IT"],
    #     "user_id": ["u1", "u2", "u3", "u4", "u5", "u6"],  # high cardinality
    #     "is_active": [1, 1, 1, 1, 1, 1],  # constant column
    # })

    # # introduce duplicate row
    # df = pd.concat([df, df.iloc[[0]]], ignore_index=True)


    # df = pd.concat([df, df.iloc[[0]]], ignore_index=True) 

    # df = pd.DataFrame({
    # "all_missing": [None, None, None, None],
    # "value": [1, 2, 3, 4]
    #  })

    # df = pd.DataFrame({
    # "user_id": [f"user_{i}" for i in range(100)],
    # "age": [25, 26, 27, 28] * 25
    # })

    # df = pd.DataFrame({
    # "A": [1, 1, 1, 1, 2, 2],
    # "B": ["x", "x", "x", "x", "y", "y"]
    # })

    # df = pd.DataFrame({
    # "income": [20000, 22000, 21000, 23000, 1000000, None],
    # "category": ["A", "A", "B", None, "B", "B"]
    # })

    df = pd.DataFrame({
    "user_id": [f"user_{i}" for i in range(50)]
    })

    dc = DataCleaner(df)

    print(dc.check_quality())


    dc = DataCleaner(df)
    import pprint

    print("PROFILE:")
    pprint.pprint(dc.profile())

    print("\nQUALITY ISSUES:")
    pprint.pprint(dc.check_quality())
    
    print("\nQUALITY Score:")
    pprint.pprint(dc.quality_score())

    print("\nSUGGESTED FIXES:")
    pprint.pprint(dc.suggest_fixes())

if __name__ == "__main__":
    main()

