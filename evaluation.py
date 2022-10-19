from algorithm_classification import THRESHOLD
import pandas as pd
import numpy as np
from algorithm_classification import matching_articles
from sklearn.metrics import confusion_matrix, auc
import matplotlib.pyplot as plt
import seaborn as sn


def join_dataframes(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    '''
    Merge two dataframes with an inner join on the attributes "Article Title" and "Topic of interest"
    :param df1: pandas dataframe
    :param df2: pandas dataframe
    :return: merged dataframe
    '''
    merged_dataframe = pd.merge(df1, df2, on=['Article Title', 'Topic of interest'], how='inner')
    return merged_dataframe


def get_auc(gold_standard: pd.DataFrame, alg_scoring_val: pd.DataFrame, alg_scoring_test: pd.DataFrame, graph=True):
    '''
    The function compares classification on validation DB and test DB with classification from gold standard.
    It selects the optimal threshold for validation DB and for test DB.
    It also reports classification score on the test DB using the validation optimal threshold.
    :param gold_standard: database with manual classification
    :param alg_scoring_val: VALIDATION database
    :param alg_scoring_test: TEST database
    :param graph: if True, it plots ROC curves, Threshold graphs, and Confusion Matrices
    :return:
    '''
    # check inputs
    if not gold_standard.shape[0] == alg_scoring_val.shape[0]:
        raise Exception("Dataframes are not of the same length. Check your inputs")

    # initialization
    algorithm_scores_val = list(alg_scoring_val['Score'])
    manual_classifications = list(gold_standard['Manual Classification'])

    FPRs_val = []
    TPRs_val = []
    ACCs_val = []
    SPECs_val = []
    CMs_val = []

    # +0.001 to assure last results contains all 0s (due to >= in matching_articles())
    thresholds_val = np.linspace(min(algorithm_scores_val), max(algorithm_scores_val) + 0.001, 1000)

    for threshold in thresholds_val:
        algorithm_classification = matching_articles(algorithm_scores_val, threshold)
        cm = confusion_matrix(manual_classifications, algorithm_classification)
        TN = cm[0][0]
        FP = cm[0][1]
        FN = cm[1][0]
        TP = cm[1][1]

        # Fall out or false positive rate
        FPR = FP / (FP + TN)
        # Sensitivity, hit rate, recall, or true positive rate
        TPR = TP / (TP + FN)
        # Accuracy
        ACC = (TP + TN)/(TP+FN+FP+TN)

        FPRs_val.append(FPR)
        TPRs_val.append(TPR)
        SPECs_val.append(1 - FPR)
        ACCs_val.append(ACC)
        CMs_val.append(cm)

    index_val = ACCs_val.index(max(ACCs_val))
    print("Analysis on VALIDATION Database")
    print("The AUC score is: ", round(auc(FPRs_val, TPRs_val), 4))
    print("Best accuracy of ", round(max(ACCs_val), 4), " with threshold of ", round(thresholds_val[index_val], 4))
    print("Specificity ( threshold = ", round(thresholds_val[index_val], 4), "): ", round(SPECs_val[index_val], 4))
    print("Sensitivity ( threshold = ", round(thresholds_val[index_val], 4), "): ", round(TPRs_val[index_val], 4))
    print('\n')


    merged_df = join_dataframes(alg_scoring_test, gold_standard)
    manual_classifications = merged_df.loc[:, ['Manual Classification']]
    algorithm_scores_test = merged_df.loc[:, ['Score']]
    algorithm_scores_test = list(alg_scoring_test['Score'])
    manual_classifications = list(manual_classifications['Manual Classification'])

    FPRs_test = []
    TPRs_test = []
    ACCs_test = []
    SPECs_test = []
    CMs_test = []

    thresholds_test = np.linspace(min(algorithm_scores_test), max(algorithm_scores_test) + 0.001, 1000)

    for threshold in thresholds_test:
        algorithm_classification = matching_articles(algorithm_scores_test, threshold)
        cm = confusion_matrix(manual_classifications, algorithm_classification)
        TN = cm[0][0]
        FP = cm[0][1]
        FN = cm[1][0]
        TP = cm[1][1]

        # Fall out or false positive rate
        FPR = FP / (FP + TN)
        # Sensitivity, hit rate, recall, or true positive rate
        TPR = TP / (TP + FN)
        # Accuracy
        ACC = (TP + TN)/(TP+FN+FP+TN)

        FPRs_test.append(FPR)
        TPRs_test.append(TPR)
        SPECs_test.append(1 - FPR)
        ACCs_test.append(ACC)
        CMs_test.append(cm)

    index_test = ACCs_test.index(max(ACCs_test))
    print("Analysis on TEST Database")
    print("The AUC score is: ", round(auc(FPRs_test, TPRs_test), 4))
    print("Best accuracy of ", round(max(ACCs_test), 4), " with threshold of ", round(thresholds_test[index_test], 4))
    print("Specificity ( threshold = ", round(thresholds_test[index_test], 4), "): ", round(SPECs_test[index_test], 4))
    print("Sensitivity ( threshold = ", round(thresholds_test[index_test], 4), "): ", round(TPRs_test[index_test], 4))
    print('\n')

    index = np.where(thresholds_test == thresholds_val[index_val])[0][0]
    print('TEST using the validated threshold')
    print("The accuracy with the set THRESHOLD of ", round(THRESHOLD, 4), " is ", round(ACCs_test[index], 4))
    print("Specificity with the set THRESHOLD of ", round(THRESHOLD, 4), "): ", round(SPECs_test[index], 4))
    print("Sensitivity with the set THRESHOLD of ", round(THRESHOLD, 4), "): ", round(TPRs_test[index], 4))

    if graph:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('ROC Curve')
        fig.tight_layout(pad=3.0)
        random_evaluator = np.linspace(0, 1, 100)

        ax1.plot(FPRs_val, TPRs_val)
        ax1.plot(random_evaluator, random_evaluator, '-.')
        ax1.set_title('Validation DB')
        ax1.set(xlabel='False Positive Rate', ylabel='True Positive Rate')
        ax1.relim([0.0, 1.0])
        ax1.relim([0.0, 1.0])

        ax2.plot(FPRs_test, TPRs_test)
        ax2.plot(random_evaluator, random_evaluator, '-.')
        ax2.set_title('Test DB')
        ax2.set(xlabel='False Positive Rate', ylabel='True Positive Rate')
        ax2.relim([0.0, 1.0])
        ax2.relim([0.0, 1.0])
        plt.show()

        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Threshold Graphs')
        fig.tight_layout(pad=3.0)
        marker_size = (plt.rcParams['lines.markersize'] ** 2)*4

        ax1.plot(thresholds_val, ACCs_val)
        ax1.plot(thresholds_val, TPRs_val)
        ax1.plot(thresholds_val, SPECs_val)
        ax1.scatter(thresholds_val[index_val], max(ACCs_val), c='#ff7f0e', marker='X', s=marker_size)
        ax1.legend(['Accuracy', 'Sensitivity', 'Specificity'])
        ax1.set_title('Validation DB')
        ax1.set(xlabel='Threshold', ylabel='%')
        ax1.relim([0.0, 1.0])
        ax1.relim([0.0, 1.0])

        ax2.plot(thresholds_test, ACCs_test)
        ax2.plot(thresholds_test, TPRs_test)
        ax2.plot(thresholds_test, SPECs_test)
        ax2.scatter(thresholds_test[index_test], max(ACCs_test), c='#ff7f0e', marker='X', s=marker_size)
        ax2.legend(['Accuracy', 'Sensitivity', 'Specificity'])
        ax2.set_title('Test DB')
        ax2.set(xlabel='Threshold', ylabel='%')
        ax2.relim([0.0, 1.0])
        ax2.relim([0.0, 1.0])
        plt.show()

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        fig.suptitle('Confusion Matrix')
        fig.tight_layout(pad=3.0)

        sn.heatmap(CMs_val[index_val], annot=True, annot_kws={"size": 16}, cbar=False, cmap='RdYlGn', ax=ax1)
        ax1.set(xlabel='Algorithm classification', ylabel='Ground truth')
        ax1.set_title('Validation DB')

        sn.heatmap(CMs_test[index_test], annot=True, annot_kws={"size": 16}, cbar=False, cmap='RdYlGn', ax=ax2)
        ax2.set(xlabel='Algorithm classification', ylabel='Ground truth')
        ax2.set_title('Test DB')

        sn.heatmap(CMs_test[index_val], annot=True, annot_kws={"size": 16}, cbar=False, cmap='RdYlGn', ax=ax3)
        ax3.set(xlabel='Algorithm classification', ylabel='Ground truth')
        ax3.set_title('Test DB with\nvalidated threshold')
        plt.show()


if __name__ == '__main__':
    gold_std = pd.read_csv("gold_standard.csv")
    alg_scores_val = pd.read_csv("validation_dataframe.csv")
    alg_scores_test = pd.read_csv("3_Group09_PartI_Database.csv")

    get_auc(gold_std, alg_scores_val, alg_scores_test)
