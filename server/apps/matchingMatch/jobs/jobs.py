from django.conf import settings
from time import time
import requests
import json
import random
from datetime import datetime

timeZone = datetime.now()


def schedule_api():
    print("Now : %s" % timeZone.second)
    print("This is SCHEDULER APPS PROCESSING")
