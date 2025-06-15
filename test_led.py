# Bibliotheken laden
from gpiozero import LED
from time import sleep

# Initialisierung von GPIO17 als LED (Ausgang)
led_yellow = LED(17)
led_green = LED(27)
led_white = LED(26)
led_red = LED(19)
led_blue = LED(13)
while True:

    # LED einschalten
    # led_yellow.on()
    # led_white.on()
    # led_red.on()
    led_blue.on()
    # led_green.off()

    # 5 Sekunden warten
    sleep(1)

    # LED ausschalten
    # led_yellow.off()
    # led_white.off()
    # led_red.off()
    led_blue.off()
    # led_green.on()
    sleep(1)