from neopixel import Neopixel # type: ignore
import utime
import machine

#number of pixels
numpix = 24

#max brightness
brightness = 40

delay = 0.01

strip = Neopixel(numpix, 0, 28, "GRB")


#Color definition
indigo     = ( 75,   0, 130)
teal       = (  0, 128, 128)
beige      = (245,245,220  )
red        = (100,   0,   0)
pink       = (255, 0, 151)
dark_green = (61, 207, 52 )
yellow     = (251, 255, 0 )

#trail class
class Trail:
    # Instance attribute
    color_gradiant_array = []
    color = [0,0,0]

    def __init__(self, trail_length, color, end_position):
        self.trail_length   = trail_length
        self.color          = color
        self.end_position   = end_position

        self.color_gradiant_array = [[0] * 3 ] * self.trail_length
        #create gradiant
        for i in range (self.trail_length):
            exponent = (1 / 2 ** i)
            if(exponent < 0.007):
                 exponent = 0.007
            self.color_gradiant_array[i] =[(round(self.color[0] / exponent)),
                                           (round(self.color[1] / exponent)),
                                           (round(self.color[2] / exponent)) ]
            #print(exponent)

    def light(self):
        for i in range (self.trail_length):
             self.position = self.end_position + i
             if(self.position > numpix - 1):
                self.position -= numpix

             strip.set_pixel(self.position, self.color_gradiant_array[i])


        if(self.end_position > numpix - 1):
             self.end_position -= numpix
        self.end_position += 1

        utime.sleep(delay)


strip.fill((0,0,0))
strip.brightness(2)
trail_list = []
color_choice = 0;
color_list = [indigo,teal,pink,beige,red,dark_green,yellow,]

for i in range (4):
    trail_list.append(Trail(6, color_list[i], i * 6))
#idee
    #Adauga butoane pentru trail length, color choice etc. Se apasa butonul, daca nu este apasat pentru 3 secunde, ledul de pe placa se aprinde si dupa se stinge
while True:
    for i in trail_list:
        i.light()
    strip.show()
    strip.fill((0,0,0))
