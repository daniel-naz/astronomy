import argparse
import sys
import urllib.parse
import requests
import draw_utils as du
import astrometry_client as ac
import math


def createlink(annotations):
    bad_chars = set("~/")

    def is_safe(name):
        return not any(c in bad_chars for c in name)

    found_name = None

    for ann in annotations:
        names = ann.get('names', [])
        for n in names:
            if is_safe(n):
                found_name = n
                break
        if found_name:
            break

    if found_name:
        lat = 32.07
        lng = 34.76
        elev = 0
        fov = 120.0

        name_encoded = urllib.parse.quote(found_name)

        stellarium_url = (
            f"https://stellarium-web.org/skysource/{name_encoded}"
            f"?fov={fov}&lat={lat}&lng={lng}&elev={elev}"
        )
        print(f"View in Stellarium: {stellarium_url}")


parser = argparse.ArgumentParser(
    description="Upload an image to astrometry.net and save result"
)

parser.add_argument(
    '-a', '--api',
    help='Your API key for astrometry.net',
)

parser.add_argument(
    '-f', '--file',
    help='Path to the image file you want to upload (example: "myimage.jpg")'
)

parser.add_argument(
    '-o', '--output',
    help='Name of the output image file to save (example: "solved.png")'
)

args = parser.parse_args()

if len(sys.argv) == 1:
    print("Submit a new file:")
    API_KEY = input("Enter your API key: ")
    FILE_PATH = input("Enter the image file name (with extension): ")
    OUTPUT_IMAGE = input("Enter the output image file name (with extension): ")
    PRINTS = True
    MODE = "submit"

else:
    if not args.api or not args.file or not args.output:
        print("Error: If using arguments, you must provide -a, -f, and -o")
        sys.exit(1)

    API_KEY = args.api
    FILE_PATH = args.file
    OUTPUT_IMAGE = args.output
    PRINTS = False
    MODE = "submit"

if MODE == "submit":
    session = ac.login(API_KEY, PRINTS)
    subid = ac.submit_file(session, FILE_PATH, PRINTS)
    jobid = ac.get_job_id(subid, None, PRINTS)
    ac.await_job(jobid, None, PRINTS)
    annotations = ac.fetch_annotations(jobid, PRINTS)

    createlink(annotations)

    du.draw_annotations(FILE_PATH, OUTPUT_IMAGE, annotations, PRINTS)
