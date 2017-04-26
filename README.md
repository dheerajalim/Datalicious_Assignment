# Datalicious_Assignment
This work is done as a part of assignment from Datalicious
Used : Python v 3.5.1

# Script Actions
### Task 1:
Go to google.com
Select search input
Put in Datalicious
Click Search
Wait till results are shown
Click first result from organic search
### Task 2:
Once clicked URL has been loaded, please check the below :
● A request was made to google analytics (apply filter “collect”)
● A request was made to host: dc.optimahub.com (apply filter “optimahub”)
### Task 3:
Check that in google analytics (from previous point), has the following parameters
● dt
● dp
Log the values into csv log file.

# Prerequisite
 #### Install BrowserMob Proxy to handle NEtwork Data
 ```
 $ pip install browsermob-proxy
 ```
 #### Install Python unittest framework
 
 # How to Use with Selenium Webdriver
 1. Download the files test_case.py and parameters.py
 2. Run the file test_case.py
 ```
 $ python test_case.py
 
 ```
 3. The Test result will produce a CSV LOG file along with status of the request
