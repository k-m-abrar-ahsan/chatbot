import re
import sqlite3

'''def extract_sql_only(text):
    """
    Extract the first SQL statement from the LLM output.
    Allows for missing semicolon and ignores explanations or labels.
    """
    match = re.search(
        r"\\b(SELECT|INSERT|UPDATE|DELETE)\\b[\\s\\S]+?(?:;|\\Z)",
        text,
        re.IGNORECASE
    )
    return match.group(0).strip() if match else None
'''
def execute_query(sql_query):
    try:
        cleaned_query = sql_query
        if not cleaned_query:
            print("❌ Debug: No valid SQL query found in extract_sql_only.")
            return {"error": "No valid SQL query found in response."}

        print("🧼 Cleaned SQL Query:", cleaned_query)

        conn = sqlite3.connect("database3.db")
        cursor = conn.cursor()
        print("🔍 Debug: Executing SQL:", cleaned_query) # NEW PRINT
        cursor.execute(cleaned_query)
        rows = cursor.fetchall()
        print(f"🔍 Debug: Fetched {len(rows)} rows.") # NEW PRINT

        # If no rows are returned
        if not rows:
            print("ℹ️ Query returned no results.")
            print("🔍 Debug: Returning empty list from execute_query.") # NEW PRINT
            return []

        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        print("🔍 Debug: Returning results from execute_query:", results) # NEW PRINT

        conn.close()
        return results

    except Exception as e:
        print("❌ SQL Execution Error:", e)
        print("🔍 Debug: Returning error from execute_query.") # NEW PRINT
        return {"error": str(e)}