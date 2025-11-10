import argparse
import pandas as pd

def evaluate_model(predictions_df, ground_truth_df, k=10):
    queries = ground_truth_df['Query'].unique()
    recalls = []
    for q in queries:
        true_urls = set(ground_truth_df[ground_truth_df['Query'] == q]['Assessment_url'].values)
        pred_urls = list(predictions_df[predictions_df['Query'] == q]['Assessment_url'].values)[:k]
        pred_set = set(pred_urls)
        if len(true_urls) > 0:
            recall = len(pred_set & true_urls) / len(true_urls)
            recalls.append(recall)
    mean_recall = sum(recalls) / len(recalls) if recalls else 0.0
    return mean_recall, recalls

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--pred', required=True)
    ap.add_argument('--truth', required=True)
    ap.add_argument('--k', type=int, default=10)
    args = ap.parse_args()
    pred = pd.read_csv(args.pred)
    truth = pd.read_csv(args.truth)
    mean_recall, recalls = evaluate_model(pred, truth, k=args.k)
    print(f"Mean Recall@{args.k}: {mean_recall:.4f}")
