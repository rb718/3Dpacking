# 3Dpacking

Packing Module
===========================


Pack n items into n boxes such that fewest boxes are used. 
Two criteria can be used:
1) Minimum volume: The box with the Minimum volume is chosen.
2) Max items: The box with the max number of items is chosen. 

Either of them can be used. 

The main function is in pack_boxes.py
There are two functions:
pack_boxes(): for http requests
pack_boxes_json(): for json files

Usage: 
pack_boxes(request, [account_key, criteria])
pack_boxes_json(jsonfile, [account_key, criteria]
