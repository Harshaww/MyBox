# fix_paths.py
import os

# The correct path — points to the CSV sitting right next to the scripts
BASE = os.path.dirname(os.path.abspath(__file__))
CSV  = os.path.join(BASE, "final_movie_data.csv").replace("\\", "/")

# Every file that needs fixing and what to replace
fixes = {
    "dashboard_page.py": [
        (
            r'csv_path = r"C:\Users\harsh\OneDrive\Desktop\final_project\final_movie_data.csv"',
            f'csv_path = r"{CSV}"'
        ),
    ],
    "search_movie.py": [
        (
            r'csv_path = r"C:\Users\harsh\OneDrive\Desktop\final_project\final_movie_data.csv"',
            f'csv_path = r"{CSV}"'
        ),
    ],
    "genre.py": [
        (
            r'csv_path=r"C:\Users\harsh\OneDrive\Desktop\final_project\final_movie_data.csv"',
            f'csv_path=r"{CSV}"'
        ),
    ],
    "movie_data.py": [
        (
            r'CSV_PATH: str = r"C:\Users\harsh\OneDrive\Desktop\final_project\final_movie_data.csv"',
            f'CSV_PATH: str = r"{CSV}"'
        ),
    ],
}

for filename, replacements in fixes.items():
    filepath = os.path.join(BASE, filename)
    if not os.path.exists(filepath):
        print(f"SKIP — {filename} not found")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            changed = True
            print(f"FIXED — {filename}")
        else:
            print(f"SKIP  — {filename} (pattern not found, may already be fixed)")

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

print("\nDone. Run: python main_app.py")