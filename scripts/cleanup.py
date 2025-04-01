import os
import shutil
import argparse

def delete_pycache_dirs(root_dir="."):
    """
    Recursively deletes all __pycache__ directories starting from root_dir.
    """
    deleted = 0
    for dirpath, dirnames, _ in os.walk(root_dir):
        for dirname in dirnames:
            if dirname == "__pycache__":
                full_path = os.path.join(dirpath, dirname)
                try:
                    shutil.rmtree(full_path)
                    print(f"Deleted: {full_path}")
                    deleted += 1
                except Exception as e:
                    print(f"Failed to delete {full_path}: {e}")
    print(f"\nTotal __pycache__ directories deleted: {deleted}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean up project directory.")
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="Root directory to start searching from (default: current directory)"
    )
    args = parser.parse_args()

    delete_pycache_dirs(args.root)
