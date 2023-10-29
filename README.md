# log_analyzer

Log Analyzer Script

The format for log analysis should be as follows:

'191.182.199.16 - - [12/Dec/2015:19:02:39 +0100] "GET /images/stories/raith/grillplatz.jpg HTTP/1.1" 
200 55303 "http://almhuette-raith.at/" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) 
Chrome/36.0.1985.143 Safari/537.36" 1756'

Steps:
1. Run the script.
2. Specify the folder to get the log file from (including the log file name).
3. The script will get you the following infomation from the log file:
- Number of Requests,
- IP Addresses, Most Requests Came From,
- 3 Longest Requests (with Duration, IP address, Request Method, URL, Date/Time)
4. The JSON file will be saved to the directory with the log file.
