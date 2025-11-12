"""
Script to fix the catalog by extracting assessment names from URLs
and enriching metadata.
"""
import json
import pandas as pd
from pathlib import Path

def extract_name_from_url(url: str) -> str:
    """Extract assessment name from URL slug."""
    if not url:
        return ""
    
    # Get the last part of URL path
    slug = url.rstrip("/").split("/")[-1]
    
    # Convert slug to title case
    name = slug.replace("-", " ").replace("_", " ")
    name = " ".join(word.capitalize() for word in name.split())
    
    return name

def infer_type_from_name(name: str) -> str:
    """Infer test type (K=technical, P=behavioral) from name."""
    name_lower = name.lower()
    
    # Technical keywords
    technical_keywords = [
        'java', 'python', 'javascript', 'sql', 'c++', 'c#', 'ruby', 'php',
        'html', 'css', 'react', 'angular', 'node', 'git', 'api', 'database',
        'programming', 'coding', 'software', 'developer', 'technical',
        'data', 'analyst', 'excel', 'tableau', 'power bi', 'automata',
        'algorithm', 'debug', 'fix', 'code', 'script'
    ]
    
    # Behavioral keywords
    behavioral_keywords = [
        'communication', 'leadership', 'personality', 'behavioral', 'interpersonal',
        'teamwork', 'collaboration', 'sales', 'customer', 'service', 'management',
        'professional', 'cognitive', 'reasoning', 'aptitude', 'judgement'
    ]
    
    if any(kw in name_lower for kw in technical_keywords):
        return "K"
    elif any(kw in name_lower for kw in behavioral_keywords):
        return "P"
    
    return "K"  # Default to technical

def infer_duration(name: str) -> str:
    """Infer typical duration based on assessment type."""
    name_lower = name.lower()
    
    if 'entry' in name_lower or 'basic' in name_lower:
        return "20-30 minutes"
    elif 'advanced' in name_lower or 'professional' in name_lower:
        return "45-60 minutes"
    elif 'solution' in name_lower:
        return "30-45 minutes"
    else:
        return "30 minutes"

def extract_skills_from_name(name: str) -> list:
    """Extract relevant skills from assessment name."""
    name_lower = name.lower()
    skills = []
    
    # Technical skills mapping
    skill_keywords = {
        'java': 'Java',
        'python': 'Python',
        'javascript': 'JavaScript',
        'sql': 'SQL',
        'c++': 'C++',
        'c#': 'C#',
        'html': 'HTML',
        'css': 'CSS',
        'react': 'React',
        'angular': 'Angular',
        'node': 'Node.js',
        'excel': 'Excel',
        'tableau': 'Tableau',
        'power bi': 'Power BI',
        'communication': 'Communication',
        'leadership': 'Leadership',
        'sales': 'Sales',
        'customer service': 'Customer Service',
    }
    
    for keyword, skill in skill_keywords.items():
        if keyword in name_lower:
            skills.append(skill)
    
    return skills if skills else ["General Assessment"]

def fix_catalog():
    """Fix the catalog by enriching it with proper metadata."""
    print("🔧 Fixing catalog data...")
    
    catalog_path = Path("data/catalog.json")
    
    # Load existing catalog
    with open(catalog_path, "r") as f:
        items = json.load(f)
    
    print(f"📊 Processing {len(items)} items...")
    
    # Fix each item
    fixed_items = []
    for item in items:
        url = item.get("url", "")
        
        # Extract name from URL if missing
        if not item.get("name"):
            item["name"] = extract_name_from_url(url)
        
        # Infer type
        if not item.get("type"):
            item["type"] = infer_type_from_name(item["name"])
        
        # Infer duration
        if not item.get("duration"):
            item["duration"] = infer_duration(item["name"])
        
        # Extract skills
        if not item.get("skills"):
            item["skills"] = extract_skills_from_name(item["name"])
        
        # Keep or enhance description
        if not item.get("description") or item["description"] == "Assessment from Train-Set":
            item["description"] = f"{item['name']} - {'Technical' if item['type'] == 'K' else 'Behavioral'} Assessment"
        
        fixed_items.append(item)
    
    # Save fixed catalog
    with open(catalog_path, "w") as f:
        json.dump(fixed_items, f, indent=2)
    
    print(f"✅ Fixed {len(fixed_items)} items")
    
    # Show sample
    print("\n📋 Sample fixed items:")
    for item in fixed_items[:3]:
        print(f"  - {item['name']} ({item['type']}, {item['duration']})")
        print(f"    Skills: {', '.join(item['skills'])}")
        print(f"    URL: {item['url']}")
        print()

if __name__ == "__main__":
    fix_catalog()
