##Clock V2

# Wi-fi set clock

import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
import utime
from neopixel import Neopixel # type: ignore
import math
from machine import Timer

#The amount of time a second will take (in ms)
debug_time = 1000

wlan = network.WLAN(network.STA_IF)
wlan.active(True)


# Fill in your network name (ssid) and password here:
ssid = ''
password = ''

wlan.connect(ssid, password)

#Wait for connection
while(wlan.status() < 0 or wlan.status() > 3):
    print("Waiting")
    utime.sleep(1)

print("Querying the current time:")

#Ok defines if the request was succesfull
#no_error kills the process if the request is unsuccessful for 3 times
ok = 0
no_error = 0

while(ok == 0):
    ok = 0
    try:
        start = utime.ticks_ms()
        r = urequests.get("https://timeapi.io/api/Time/current/zone?timeZone=Europe/Bucharest") # Server that returns the current time.
        print("req took " + str(utime.ticks_ms() - start) + " ms")
        ok = 1
    except:
        print("Request error")
        no_error += 1
        if no_error > 3:
            print("Could not connect")
            ok = 1
    else:
        print("Request granted \n")

        #Show the time values
        print(r.json()['time']   )
        print(r.json()['hour']   )
        print(r.json()['minute'] )
        print(r.json()['seconds'])

        #Get the real time values
        hour   = r.json()['hour'  ]
        minute = r.json()['minute']
        seconds = r.json()['seconds']


        #Number of hours to be converted to AM-PM time, as this time format
        #can be used directly as pixel locations
        if(hour > 12):
            show_hour = hour - 12
        else:
            show_hour = hour
        #Minutes and seconds, to be converted to pixel locations
        #Divided by 5, because a normal clock has 12 locations (60 / 12 = 5)
        #Use floor() to get well defined values (0 - 12, incrementing every 5 changes)
        show_minute = math.floor(minute / 5)
        show_seconds = math.floor(seconds / 5)
        print(show_seconds)

        #Timer that will keep track of the time, as to not rely on wi-fi connection
        #initializatino
        timer_count = 0
        def seconds_timer_handler(timer):
            #make global
            global timer_count
            #increment
            timer_count += 1

        ##Prepare for lightning of the leds
        #-----------------------------------
        #num of pixels and their brightness
        numpix     = 24
        brightness = 20

        #assign colors to each clock tongue
        hour_color = (100, 0, 0)
        minute_color = (0, 100, 0)
        seconds_color = (0,0,100)

        #initialise the neopixel strip
        strip = Neopixel(numpix, 0, 28, "GRB")
        strip.brightness(brightness)

        #Set the clock with the global time from the request
        #---------------------------
        # As we use 2 leds per clock location,
        #The *2 and *2 + 1 operations are required
        #---------------------------
        #The hour color is dominant, it will be shown above the rest
        strip.set_pixel(show_seconds * 2 ,     seconds_color)
        strip.set_pixel(show_seconds  * 2 + 1, seconds_color)

        strip.set_pixel(show_minute * 2,      minute_color)
        strip.set_pixel(show_minute  * 2 + 1, minute_color)

        strip.set_pixel(show_hour * 2,     hour_color)
        strip.set_pixel(show_hour * 2 + 1, hour_color)

        strip.show()

        #Initialise the timer
        seconds_timer = Timer(mode=Timer.PERIODIC, period=debug_time, callback=seconds_timer_handler)

        #Memorise the pixel position the clock started
        old_seconds = show_seconds
        old_minute  = show_minute
        old_hour    = show_hour

        #Define the current timer as the same type of 0 - 12 variable as hours,min ... to be
        #used as pixel location

        old_timer = math.floor(timer_count / 5)

        while(True):
            #We will use the timer as a pixel location
            show_timer = math.floor(timer_count / 5)

            #add a new pixel to seconds, when the timer counts 5 seconds
            if(old_timer != show_timer):
                old_timer = show_timer
                show_seconds +=1


            if(show_timer >= 12):
                show_timer = 0

            if(show_seconds >= 12):
                show_seconds = 0
                show_minute += 1

            if(show_minute >= 12):
                show_minute = 0
                show_hour += 1

            if(show_hour >= 12):
                show_hour = 0

            if(show_hour != old_hour):
            #To prevent deletion of the other clock tongues, conditions were added
                if(old_hour != show_seconds and old_hour!= show_minute):
                    strip.set_pixel(old_minute * 2 ,     (0,0,0))
                    strip.set_pixel(old_minute  * 2 + 1, (0,0,0))
                strip.set_pixel(show_hour * 2 ,     hour_color)
                strip.set_pixel(show_hour * 2 + 1, hour_color)
                old_hour = show_hour
                strip.show()

            if(show_minute != old_minute):
            #To prevent deletion of the other clock tongues, conditions were added
                if(old_minute != show_seconds and old_minute!= show_hour):
                    strip.set_pixel(old_minute * 2 ,     (0,0,0))
                    strip.set_pixel(old_minute  * 2 + 1, (0,0,0))
                if(show_minute!= show_hour):
                    strip.set_pixel(show_minute * 2 ,     minute_color)
                    strip.set_pixel(show_minute  * 2 + 1, minute_color)
                old_minute = show_minute
                strip.show()

            if(show_seconds != old_seconds):
                #To prevent deletion of the other clock tongues, conditions were added
                if(old_seconds != show_minute and old_seconds!= show_hour):
                    strip.set_pixel(old_seconds * 2 ,     (0,0,0))
                    strip.set_pixel(old_seconds  * 2 + 1, (0,0,0))
                if(show_seconds != show_minute and show_seconds!= show_hour):
                    strip.set_pixel(show_seconds * 2 ,     seconds_color)
                    strip.set_pixel(show_seconds  * 2 + 1, seconds_color)
                old_seconds = show_seconds
                strip.show()
