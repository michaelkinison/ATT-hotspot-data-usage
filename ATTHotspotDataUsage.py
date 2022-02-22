#-------------------------------------------------------------------------------
# Name:        ATTDataUsage
# Purpose:     See how much data has been used on prepaid plan.
#
# Author:      mek02
#
# Created:     17/02/2022
# Copyright:   (c) mek02 2022
#-------------------------------------------------------------------------------

import sys
import requests
from bs4 import BeautifulSoup

# URL where login info is posted
loginurl = "https://www.paygonline.com/websc/logon.html"

# URL after successful login
homeurl = "https://www.paygonline.com/websc/home.html"

# Login details. Also token needed.
user = "YOUR_MOBILE_ROUTER_PHONE_NUMBER" # How do you log in?
password = "YOUR_PASSWORD" # What password do you use?
token = "" # No token needed, but it is used during login?

# Field names taken from page source
payload = {
    "phoneNumber": user,
    "password": password,
    "passwordFocus": token
}

def main():
    # Logging into the web page
    s = requests.Session()
    p = s.post(loginurl, data = payload)

    # Getting all HTML
    page = s.get(homeurl)
    page.content

    # Filtering HTML for the data we want
    soup = BeautifulSoup(page.content, 'html.parser')
    dataremaining = soup.find('p', class_="small pull-left groupInternal")
    resetdate = soup.find('div', class_="one half mobile align-center balance")

    # Output only the text we're interested in to a text file.
    # This can be used as input later on for a MagicMirror module
    sys.stdout = open("DataRemaining.txt", "w")
    print(dataremaining.get_text(" ", strip=True))
    print(resetdate.get_text(" ", strip=True))
    sys.stdout.close()

    # Log out of the web session
    s.close()

if __name__ == '__main__':
    main()
