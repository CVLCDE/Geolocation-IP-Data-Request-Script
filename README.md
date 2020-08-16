# Geolocation-IP-Data-Request-Script
Made this for work but I figured I'd keep it here too. 

This script uses the Batch Endpoint from https://ip-api.com/docs/api:batch to request geolocation data from a text file of IPs. 

The Batch endpoint can handle groups of 100 IPs every 60 seconds or so. The script reads all IPs into a list, loops through that list in groups of 100, and then sends each group to the API. The API will time you out if you send too many requests to it at once, so it sleeps for about 60 seconds each time before sending another group. 

In the headers of the response that you get from each request, there are two attributes given to let you know how long you have to wait before you get timed out and how long you have to wait before you are "unbanned". I tried to have the program sleep for the exact amount of time needed before getting unbanned, but Python's sleep() function doesn't seem to always be accurate, so I have it sleep for an extra 2 seconds to act as a buffer. 

Results are outputted to a text file.

It took me around 7 hours to get results form 162,000 IPs. 
