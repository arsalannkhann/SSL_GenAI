"""
Analyze prediction failures to understand where the model is struggling.
"""
import argparse
import pandas as pd
from collections import defaultdict


def analyze_failures(predictions_df, ground_truth_df, k=10):
    """Analyze which queries failed and why."""
    queries = ground_truth_df['Query'].unique()
    
    failures = []
    successes = []
    
    for query in queries:
        true_urls = set(ground_truth_df[ground_truth_df['Query'] == query]['Assessment_url'].values)
        pred_urls = list(predictions_df[predictions_df['Query'] == query]['Assessment_url'].values)[:k]
        pred_set = set(pred_urls)
        
        if len(true_urls) > 0:
            recall = len(pred_set & true_urls) / len(true_urls)
            
            result = {
                'query': query,
                'recall': recall,
                'true_count': len(true_urls),
                'pred_count': len(pred_urls),
                'matched': len(pred_set & true_urls),
                'missed': list(true_urls - pred_set),
                'false_positives': list(pred_set - true_urls)
            }
            
            if recall < 0.5:
                failures.append(result)
            else:
                successes.append(result)
    
    return failures, successes


def print_analysis(failures, successes):
    """Print detailed analysis."""
    print(f"\n{'='*80}")
    print(f"ANALYSIS SUMMARY")
    print(f"{'='*80}")
    print(f"Total queries: {len(failures) + len(successes)}")
    print(f"Successful (recall >= 0.5): {len(successes)}")
    print(f"Failed (recall < 0.5): {len(failures)}")
    print(f"Success rate: {len(successes) / (len(failures) + len(successes)) * 100:.1f}%")
    
    if failures:
        print(f"\n{'='*80}")
        print(f"TOP 10 FAILURES")
        print(f"{'='*80}")
        
        # Sort by recall ascending
        failures.sort(key=lambda x: x['recall'])
        
        for i, f in enumerate(failures[:10], 1):
            print(f"\n{i}. Query: {f['query'][:100]}...")
            print(f"   Recall: {f['recall']:.2f}")
            print(f"   True assessments: {f['true_count']}")
            print(f"   Matched: {f['matched']}")
            print(f"   Missed: {len(f['missed'])}")
            if f['missed']:
                print(f"   Sample missed URLs:")
                for url in f['missed'][:3]:
                    print(f"     - {url}")
    
    # Analyze patterns
    print(f"\n{'='*80}")
    print(f"FAILURE PATTERNS")
    print(f"{'='*80}")
    
    if failures:
        avg_recall = sum(f['recall'] for f in failures) / len(failures)
        avg_missed = sum(len(f['missed']) for f in failures) / len(failures)
        print(f"Average recall on failures: {avg_recall:.3f}")
        print(f"Average missed assessments: {avg_missed:.1f}")
        
        # Check for common words in failed queries
        failed_queries = [f['query'].lower() for f in failures]
        word_freq = defaultdict(int)
        for q in failed_queries:
            for word in q.split():
                if len(word) > 3:
                    word_freq[word] += 1
        
        print(f"\nMost common words in failed queries:")
        for word, count in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {word}: {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pred', required=True, help='Predictions CSV')
    parser.add_argument('--truth', required=True, help='Ground truth CSV')
    parser.add_argument('--k', type=int, default=10)
    args = parser.parse_args()
    
    pred = pd.read_csv(args.pred)
    truth = pd.read_csv(args.truth)
    
    failures, successes = analyze_failures(pred, truth, k=args.k)
    print_analysis(failures, successes)
