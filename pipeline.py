from dagster import op, job
import os

@op
def scrape():
    os.system("python src/scraper.py")

@op
def load():
    os.system("python src/load_raw.py")

@op
def transform():
    os.system("dbt run")

@op
def yolo():
    os.system("python src/yolo_detect.py")

@job
def medical_pipeline():
    scrape()
    load()
    transform()
    yolo()
