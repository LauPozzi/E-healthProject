from algorithm_classification import THRESHOLD
from validation import get_auc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn

#TODO: documentation
def join_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    merged_dataframe = pd.merge(df1, df2, on=['Article Title', 'Topic of interest'], how='inner')
    return merged_dataframe


if __name__ == '__main__':
    gold_std = pd.read_csv("gold_standard.csv")
    alg_scores = pd.read_csv("3_Group09_PartI_Database.csv")

    merged_df = join_dataframes(alg_scores, gold_std)

    ACCs, TPRs, FPRs, SPECs, thresholds, CMs = get_auc(merged_df.loc[:, ['Manual Classification']], merged_df.loc[:, ['Score']])

    index = np.where(thresholds == THRESHOLD)[0][0]
    print("\nThe accuracy with the set THRESHOLD of ", round(THRESHOLD, 4), " is ", round(ACCs[index], 4))
    print("Specificity with the set THRESHOLD of ", round(THRESHOLD, 4), "): ", round(SPECs[index], 4))
    print("Sensitivity with the set THRESHOLD of ", round(THRESHOLD, 4), "): ", round(TPRs[index], 4))

    plt.figure()
    sn.heatmap(CMs[index], annot=True, annot_kws={"size": 16}, cbar=False, cmap='RdYlGn')
    plt.ylabel('Ground truth')
    plt.xlabel('Algorithm classification')
    plt.show()
