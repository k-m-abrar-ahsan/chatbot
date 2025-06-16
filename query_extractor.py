import re

def extract_sql_only(text):
    """Extract SQL query from text, handling various formats and cleaning up the output."""
    
    # Remove any markdown code block syntax
    text = re.sub(r'```sql|```', '', text)
    
    # Try to find SQL query with various patterns
    patterns = [
        # Pattern for SELECT queries with optional WHERE, GROUP BY, ORDER BY, etc.
        r'SELECT\s+.+?(?:FROM.+?(?:WHERE|GROUP\s+BY|ORDER\s+BY|LIMIT|$).+?)?(?:;|\s*)$',
        
        # Pattern for queries with UNION
        r'(?:SELECT\s+.+?FROM.+?)\s+UNION\s+(?:ALL\s+)?(?:SELECT\s+.+?FROM.+?)(?:;|\s*)$',
        
        # Pattern for basic SELECT queries
        r'SELECT\s+.+?FROM\s+.+?(?:;|\s*)$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            sql = match.group(0).strip()
            # Clean up any trailing characters
            sql = re.sub(r'\s*;\s*$', '', sql)
            return sql
            
    return None  # No SQL query found
