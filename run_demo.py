import pandas as pd
from sanitipy import DataCleaner

def main():
    df = pd.DataFrame({
        "A": [None, None, None, None],
        "B": [1, 1, 1, 1]
    })

    dc = DataCleaner(df)

    print("PROFILE:")
    print(dc.profile())

    print("\nQUALITY ISSUES:")
    print(dc.check_quality())
    
    print("\nQUALITY Score:")
    print(dc.quality_score())

if __name__ == "__main__":
    main()

