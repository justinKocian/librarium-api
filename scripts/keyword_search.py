# scripts/keyword_search.py

import os

def search_keyword(base_dir, keyword, output_file):
    with open(output_file, "w") as out:
        out.write(f"Searching for '{keyword}' in {base_dir}...\n\n")
        for root, _, files in os.walk(base_dir):
            for filename in files:
                if filename.endswith(".py"):
                    path = os.path.join(root, filename)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            for i, line in enumerate(f, start=1):
                                if keyword in line:
                                    out.write(f"{path}:{i}: {line}")
                    except Exception as e:
                        out.write(f"Error reading {path}: {e}\n")
        out.write("\nSearch complete.\n")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_file = os.path.join(os.path.dirname(__file__), "search_results.txt")
    search_keyword(base_dir, "slowapi", output_file)
