import pandas as pd
import numpy as np
from algorithm_classification import matching_articles
from sklearn.metrics import confusion_matrix, auc
import matplotlib.pyplot as plt


def get_auc(gold_standard: pd.DataFrame, alg_scoring: pd.DataFrame, graph: bool = True):
    if not gold_standard.shape[0] == alg_scoring.shape[0]:
        raise Exception("Dataframes are not of the same length. Check your inputs")

    algorithm_scores = list(alg_scoring['Score'])
    manual_classifications = list(gold_standard['Manual Classification'])

    FPRs = []
    TPRs = []
    # +0.1 to assure last results contains all 0s (due to >= in matching_articles())
    for threshold in np.linspace(min(algorithm_scores), max(algorithm_scores) + 0.1, 100):
        algorithm_classification = matching_articles(algorithm_scores, threshold)
        cm = confusion_matrix(manual_classifications, algorithm_classification)
        TP = cm[0][0]
        FN = cm[0][1]
        FP = cm[1][0]
        TN = cm[1][1]

        # Fall out or false positive rate
        FPR = FP / (FP + TN)
        # Sensitivity, hit rate, recall, or true positive rate
        TPR = TP / (TP + FN)

        FPRs.append(FPR)
        TPRs.append(TPR)

    print("The AUC score is: ", auc(FPRs, TPRs))

    if graph:
        plt.plot(FPRs, TPRs)
        random_evaluator = np.linspace(0, 1, 100)
        # plt.plot(random_evaluator, random_evaluator)
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')


if __name__ == '__main__':
    gold_std = pd.read_csv("gold_standard.csv")
    alg_scores = pd.read_csv("export_dataframe_match.csv")
    get_auc(gold_std, alg_scores)
