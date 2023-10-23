#Potentiometer adc
from machine import Pin, ADC
import utime
from neopixel import Neopixel

Pot_val = ADC(27)
numpix = 24
brightness = 1

delay = 0.01
strip = Neopixel(numpix, 0, 28, "GRB")

while True:
    
    value = 0
    value += round(Pot_val.read_u16() / 400)
    if (value < 5):
        value = 0
    print(value)
    strip.fill((value,0,0))
    strip.show()