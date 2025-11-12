#!/usr/bin/env python3
"""
Test script to verify test-set.csv data and create a simplified version for frontend.
Handles CSV files with multi-line quoted entries properly.
"""
import csv
import json

def load_test_queries():
    """Load and display test queries from test-set.csv"""
    print("Loading test-set.csv with proper CSV parsing...")
    
    try:
        queries = []
        
        # Use Python's CSV reader which handles quoted multi-line entries properly
        with open('data/test-set.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                query = row.get('Query', '').strip()
                if query:  # Only add non-empty queries
                    queries.append(query)
        
        print(f"\n✅ Successfully loaded {len(queries)} queries")
        
        # Show first 3 queries
        print("\n📋 First 3 queries:")
        for i, query in enumerate(queries[:3], 1):
            print(f"\n{i}. {query[:200]}{'...' if len(query) > 200 else ''}")
        
        # Save as JSON for easier frontend consumption
        output = {
            'queries': queries,
            'count': len(queries)
        }
        
        with open('data/test-queries.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Created data/test-queries.json with {len(queries)} queries")
        print("   Frontend can now use this JSON file for easier parsing")
        
        # Also copy to frontend public folder
        try:
            with open('frontend/public/data/test-queries.json', 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            print(f"✅ Copied to frontend/public/data/test-queries.json")
        except Exception as e:
            print(f"⚠️  Could not copy to frontend: {e}")
        
        return queries
        
    except Exception as e:
        print(f"❌ Error loading test data: {e}")
        import traceback
        traceback.print_exc()
        return []


if __name__ == "__main__":
    queries = load_test_queries()
    
    if queries:
        print(f"\n✅ Test data is valid and ready to use!")
        print(f"   Total queries available: {len(queries)}")
        
        # Show query length statistics
        lengths = [len(q) for q in queries]
        print(f"\n📊 Query Statistics:")
        print(f"   Shortest: {min(lengths)} characters")
        print(f"   Longest: {max(lengths)} characters")
        print(f"   Average: {sum(lengths)//len(lengths)} characters")
    else:
        print(f"\n⚠️  No test queries found")
