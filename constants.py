from os import name
from math import inf

sign = '\\' if name == 'nt' else '/'

sections = {
    "1"	: {"name" : "Str 1",        "start" :   0,      "end" :	670},
    "2"	: {"name" : "Turn 1",       "start" :	670,    "end" :	900},
    "3"	: {"name" : "Turn 2",       "start" :	900,    "end" :	990},
    "4"	: {"name" : "Str 2-3",      "start" :	990,    "end" :	1030},
    "5"	: {"name" : "Turn 3",       "start" :	1030,   "end" :	1330},
    "6"	: {"name" : "Str 3-4",      "start" :	1330,   "end" :	1580},
    "7"	: {"name" : "Turn 4",       "start" :	1580,   "end" :	1880},
    "8"	: {"name" : "Str 4-5",      "start" :	1880,   "end" :	2000},
    "9"	: {"name" : "Turn 5",       "start" :	2000,   "end" :	2200},
    "10": {"name" : "Str 5-6",      "start" :	2200,   "end" :	2430},
    "11": {"name" : "Turn 6",       "start" :	2430,   "end" :	2580},
    "12": {"name" : "Str 6-7",      "start" :	2580,   "end" :	2770},
    "13": {"name" : "Turn 7",       "start" :	2770,   "end" :	2980},
    "14": {"name" : "Str 7-8",      "start" :	2980,   "end" :	3310},
    "15": {"name" : "Turn 8",       "start" :	3310,   "end" :	3520},
    "16": {"name" : "Str 8-9",      "start" :	3520,   "end" :	3530},
    "17": {"name" : "Turn 9",       "start" :	3530,   "end" :	3620},
    "18": {"name" : "Turn 10",      "start" :	3620,   "end" :	3840},
    "19": {"name" : "Str 10-11",    "start" :   3840,   "end" :	3880},	
    "20": {"name" : "Turn 11",      "start" :	3880,   "end" :	4020},
    "21": {"name" : "Turn 12",      "start" :	4020,   "end" :	4120},
    "22": {"name" : "Turn 13",      "start" :	4120,   "end" :	4200},
    "23": {"name" : "Turn 14",      "start" :	4200,   "end" :	4400},
    "24": {"name" : "Str 14-0",     "start" :	4400,   "end" :	inf}
}

physical_columns  = ['SUS_TRAVEL_LF',
                     'SUS_TRAVEL_RF',
                     'SUS_TRAVEL_LR',
                     'SUS_TRAVEL_RR',
                     'BRAKE_TEMP_LF',
                     'BRAKE_TEMP_RF',
                     'BRAKE_TEMP_LR',
                     'BRAKE_TEMP_RR',
                     'TYRE_PRESS_LF',
                     'TYRE_PRESS_RF',
                     'TYRE_PRESS_LR',
                     'TYRE_PRESS_RR',
                     'TYRE_TAIR_LF',
                     'TYRE_TAIR_RF',
                     'TYRE_TAIR_LR',
                     'TYRE_TAIR_RR',
                     'WHEEL_SPEED_LF',
                     'WHEEL_SPEED_RF',
                     'WHEEL_SPEED_LR',
                     'WHEEL_SPEED_RR',
                     'BUMPSTOPUP_RIDE_LF',
                     'BUMPSTOPUP_RIDE_RF',
                     'BUMPSTOPUP_RIDE_LR',
                     'BUMPSTOPUP_RIDE_RR',
                     'BUMPSTOPDN_RIDE_LF',
                     'BUMPSTOPDN_RIDE_RF',
                     'BUMPSTOPDN_RIDE_LR',
                     'BUMPSTOPDN_RIDE_RR',
                     'BUMPSTOP_FORCE_LF',
                     'BUMPSTOP_FORCE_RF',
                     'BUMPSTOP_FORCE_LR',
                     'BUMPSTOP_FORCE_RR']
