from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

print("test")

if __name__ == '__main__':
    section_excel_file = Path(PROJECT_ROOT, "inputs", "HRCT_Sections.xlsx")
    sections_df = pd.read_excel(section_excel_file)

    for idx, row in sections_df.iterrows():
        print(f"From {row['Page Start']} to {row['Page End']}")
