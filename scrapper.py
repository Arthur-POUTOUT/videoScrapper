import sys
from bs4 import BeautifulSoup
import requests
import re
import json

from scrapperHelper import videoScrapper

def scrap(input, output, numComments):
    """
    Create the url and a videoScrapper for eachone of them
    """
    listId = input["videos_id"]
    dict = {}
    for id in listId:
        url = f"https://www.youtube.com/watch?v={id}"
        scrapper = videoScrapper(url)
        dict[id]=scrapper.getData(numComments)

    resJson = json.dumps(dict, indent=4)

    with open(output,"w") as f:
        f.write(resJson)

# Test arg number
if len(sys.argv) != 5 :
    raise Exception("Invalid usage\nUsage : scrapper.py --input input.json --output output.json")

# Test input and output
if sys.argv[1] == "--input":
    input = sys.argv[2]
    output = sys.argv[4]
    if not sys.argv[3] == "--output":
        raise Exception("Invalid usage\nUsage : scrapper.py --input input.json --output output.json")
else:
    input = sys.argv[4]
    output = sys.argv[2]
    if not (sys.argv[1] == "--output" and sys.argv[3] == "--input"):
        raise Exception("Invalid usage\nUsage : scrapper.py --input input.json --output output.json")

# Test json file
if not (sys.argv[2][-5:] == ".json" and sys.argv[4][-5:] == ".json"):
    raise Exception("Invalid usage\nUsage : scrapper.py --input input.json --output output.json")



with open(input, "r") as file:
    inputData = json.loads(file.read())

    numComments = 10
    scrap(inputData, output, numComments)
