# Test Data Information

## Source
The test data comes from `Gen_AI Dataset.xlsx`, specifically from the **Test-Set** sheet (Sheet 2).

## Statistics
- **Total Test Queries**: 9
- **Format**: Excel (.xlsx) → CSV → JSON
- **Column**: Single "Query" column

## Test Queries Overview

### Query Lengths
- **Shortest**: 86 characters
- **Longest**: 5,573 characters  
- **Average**: 2,067 characters

### Query Types
The 9 test queries cover various hiring scenarios:

1. **Multi-skill Technical Assessment** (60 min)
   - Python, SQL, JavaScript proficiency

2. **AI/ML Research Engineer Position** (Long JD)
   - NLP, Computer Vision, Generative AI
   
3. **Analyst Role** (45 min)
   - Cognitive and personality tests

4. **Presales Specialist** (30+ min)
   - Commercial operations, technical skills

5. **Sales Graduates** (30 min)
   - New graduate assessment

6. **Marketing Content Writer**
   - Creative, publishing, content skills

7. **Product Manager** (3-4 years exp)
   - SDLC, Jira, Confluence expertise

8. **Finance & Operations Analyst**
   - Financial modeling, business partnering

9. **Customer Support Executive**
   - English communication, international call center

## File Locations

### Source Files
- `Gen_AI Dataset.xlsx` (Sheet: Test-Set)

### Generated Files
- `data/test-set.csv` - CSV export from Excel
- `data/test-queries.json` - JSON format for frontend
- `frontend/public/data/test-queries.json` - Frontend copy

## Frontend Integration

The test queries are loaded in the QueryInput component via:
1. **Primary**: Fetch from `/data/test-queries.json` (JSON format)
2. **Fallback**: Parse `/data/test-set.csv` (CSV format)

## JSON Format

```json
{
  "queries": [
    "Query 1 text...",
    "Query 2 text...",
    ...
  ],
  "count": 9
}
```

## Usage

### Via Frontend
1. Open the application
2. Select "Select from Test Dataset" radio button
3. Choose from the dropdown (9 options available)
4. The selected query populates the textarea (editable)
5. Click "Get Recommendations"

### Via Script
```python
import json

# Load test queries
with open('data/test-queries.json', 'r') as f:
    data = json.load(f)
    queries = data['queries']
    
# Use in recommendations
from src.recommender import recommend_assessments

for query in queries:
    results = recommend_assessments(query, top_k=10)
    print(f"Query: {query[:50]}...")
    print(f"Found {len(results)} recommendations")
```

## Regenerating Test Data

If you need to regenerate the JSON files:

```bash
# Run the verification script
python verify_test_data.py

# This will:
# 1. Read data/test-set.csv
# 2. Create data/test-queries.json
# 3. Copy to frontend/public/data/test-queries.json
```

## Notes

- The Test-Set sheet contains only **9 queries** (not 276+ as initially thought)
- Each query represents a realistic hiring scenario
- Queries vary significantly in length (86 to 5,573 characters)
- Some queries are short requirements, others are full job descriptions
- All queries are valid and properly formatted
- The CSV parser handles multi-line entries correctly

## Validation

To verify test data integrity:

```bash
# Check query count
wc -l data/test-set.csv  # Should show 10 lines (header + 9 queries)

# Validate JSON
cat data/test-queries.json | python -m json.tool

# Test frontend access
curl http://localhost:3000/data/test-queries.json
```

## Expected Behavior

When "Select from Test Dataset" is chosen:
✅ Dropdown shows "Query #1" through "Query #9"  
✅ Each option shows first 80 characters of the query  
✅ Selecting an option populates the textarea  
✅ User can edit the selected query before submitting  
✅ Count indicator shows "(9 available)"  

---

**Last Updated**: November 12, 2025  
**Status**: ✅ Working correctly
