import sys, os


PROJECT_ROOT = os.path.dirname((os.path.dirname(__file__)))
sys.path.append(PROJECT_ROOT)

WEBSITE_DATA = os.path.join(
    PROJECT_ROOT, "data", "scraped_data_cleaned.txt"
)
