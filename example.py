from HD44780LCD import HD44780LCD
from time import *
from pcf8574t import PCF8574T



device = PCF8574T(address=0x27,backlight=True)
lcd = HD44780LCD(device)

lcd.custom_char(0,[0x0,0x0,0x0,0x0,0x0,0x0,0x4,0x0])
lcd.display_string("Welcome to\0\0\0\0\0\0", 1)
lcd.display_string("\0\0\0\0\0\0\0\0\0PIP2008", 2)
lcd.on(backlight=True)

#sleep(1.2)
#lcd.off()
#
