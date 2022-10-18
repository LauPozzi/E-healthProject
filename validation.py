import pandas as pd
import numpy as np
from algorithm_classification import matching_articles
from sklearn.metrics import confusion_matrix, auc
import matplotlib.pyplot as plt


def get_auc(gold_standard: pd.DataFrame, alg_scoring: pd.DataFrame, graph=True):
    if not gold_standard.shape[0] == alg_scoring.shape[0]:
        raise Exception("Dataframes are not of the same length. Check your inputs")

    algorithm_scores = list(alg_scoring['Score'])
    manual_classifications = list(gold_standard['Manual Classification'])

    FPRs = []
    TPRs = []
    ACCs = []
    SPECs = []
    # +0.1 to assure last results contains all 0s (due to >= in matching_articles())
    thresholds = np.linspace(min(algorithm_scores), max(algorithm_scores) + 0.001, 1000)
    for threshold in thresholds:
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

        ACC = (TP + TN)/(TP+FN+FP+TN)

        FPRs.append(FPR)
        TPRs.append(TPR)
        SPECs.append(1-FPR)
        ACCs.append(ACC)

    print("The AUC score is: ", round(auc(FPRs, TPRs), 4))
    print("Best accuracy of ", round(max(ACCs), 4), " with threshold of ", round(thresholds[ACCs.index(max(ACCs))], 4))

    if graph:
        plt.figure()
        plt.plot(FPRs, TPRs)
        random_evaluator = np.linspace(0, 1, 100)
        plt.plot(random_evaluator, random_evaluator, '-.')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.0])
        plt.show()
        plt.figure()
        plt.plot(thresholds, ACCs)
        plt.plot(thresholds, TPRs)
        plt.plot(thresholds, SPECs)
        marker_size = (plt.rcParams['lines.markersize'] ** 2)*4
        plt.scatter(thresholds[ACCs.index(max(ACCs))], max(ACCs), c='#ff7f0e', marker='X', s=marker_size)
        plt.legend(['Accuracy', 'Sensitivity', 'Specificity'])
        plt.xlabel('Threshold')
        plt.ylabel('%')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.0])
        plt.show()


if __name__ == '__main__':
    gold_std = pd.read_csv("gold_standard.csv")
    alg_scores = pd.read_csv("validation_dataframe.csv")
    get_auc(gold_std, alg_scores)
