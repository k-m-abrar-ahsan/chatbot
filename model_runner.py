import re
from datetime import datetime
from llama_cpp import Llama

# Load LLaMA model
llm = Llama(
    model_path="models/llama-2-13b.Q4_K_M.gguf",
    n_ctx=4096,
    n_gpu_layers=32
)

def extract_all_sql(text):
    """Extract all SQL queries from a block of text."""
    # Remove markdown code block formatting
    text = re.sub(r'```sql|```', '', text)

    # Pattern to match multiple SELECT statements
    pattern = r"SELECT\s+.*?\s+FROM\s+.*?(?:;|(?=\nSELECT|\Z))"
    
    matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
    queries = [re.sub(r'\s*;\s*$', '', m.strip()) for m in matches]
    
    return queries if queries else None

def get_sql_queries(user_input):
    try:
        # Load the right prompt template
        if 'sales' in user_input or 'product' in user_input:
            with open("prompt_template_sales.txt", "r", encoding="utf-8") as f:
                template = f.read()
        else:
            with open("prompt_template.txt", "r", encoding="utf-8") as f:
                template = f.read()

        # Format prompt
        prompt = template.replace("{user_input}", user_input)

        # Run model
        response = llm(
            prompt,
            max_tokens=1024,
            stop=["\n\n", "\nUser:", "\nSQL:"]
        )

        raw_output = response["choices"][0]["text"].strip()
        print("🔍 Raw model output:", raw_output)

        # Extract all SQL queries
        queries = extract_all_sql(raw_output)
        if queries:
            for q in queries:
                print("✅ Cleaned SQL Query:", q)
            return queries
        else:
            print("❌ Error: No valid SQL found.")
            return None

    except Exception as e:
        print("❌ Error parsing model response:", e)
        return None
