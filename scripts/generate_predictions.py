import argparse
import pandas as pd
from src.recommender import recommend_assessments

def main(inp: str, outp: str, k: int):
    df = pd.read_csv(inp)
    rows = []
    for q in df['Query'].astype(str).tolist():
        recs = recommend_assessments(q, top_k=k)
        for r in recs:
            rows.append({
                'Query': q,
                'Assessment_url': r.get('url')
            })
    out_df = pd.DataFrame(rows)
    out_df.to_csv(outp, index=False)
    print(f"Saved {len(out_df)} rows to {outp}")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--out', dest='outp', required=True)
    ap.add_argument('--top_k', type=int, default=10)
    args = ap.parse_args()
    main(args.inp, args.outp, args.top_k)
