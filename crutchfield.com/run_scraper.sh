#!/bin/bash

# scrape these hardcoded categories

time python scrape.py "http://www.crutchfield.com/g_51000/Powered-Subwoofers.html?tp=114&showAll=Y"
time python scrape.py "http://www.crutchfield.com/g_510/Enclosed-Subwoofers.html?tp=112&showAll=Y"
time python scrape.py "http://www.crutchfield.com/g_520/Component-Subwoofers.html?tp=111&showAll=Y"

