import sys
sys.path.append("./lib")


from time import *



# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set

LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00


class HD44780LCD:
    #initializes objects and lcd
    cc_empty          = [0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0]
    cc_battery_empty  = [0x0e,0x11,0x11,0x11,0x11,0x11,0x11,0x1f]
    cc_battery_level1 = [0x0e,0x11,0x11,0x11,0x11,0x11,0x1f,0x1f]
    cc_battery_level2 = [0x0e,0x11,0x11,0x11,0x11,0x1f,0x1f,0x1f]
    cc_battery_level3 = [0x0e,0x11,0x11,0x11,0x1f,0x1f,0x1f,0x1f]
    cc_battery_level4 = [0x0e,0x11,0x11,0x1f,0x1f,0x1f,0x1f,0x1f]
    cc_battery_level5 = [0x0e,0x11,0x1f,0x1f,0x1f,0x1f,0x1f,0x1f]
    cc_battery_full   = [0x0e,0x1f,0x1f,0x1f,0x1f,0x1f,0x1f,0x1f]
    
   
    def __init__(self,device=None):
        self.lcd_device = device

        cmd = LCD_FUNCTIONSET
        cmd = cmd | LCD_2LINE | LCD_5x8DOTS
        self.lcd_device.command( cmd )
        
        self.off(backlight=None)
        self.clear()
        self.home()
        self.lcd_device.command(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        for i in range(0,8):
            self.custom_char(i,HD44780LCD.cc_empty)
        
        sleep(0.2)

    def on(self,backlight=None):
        self.lcd_device.backlight(backlight)      
        self.lcd_device.command(LCD_DISPLAYCONTROL | LCD_DISPLAYON )

    def off(self,backlight=None):
        self.lcd_device.backlight(backlight)
        self.lcd_device.command(LCD_DISPLAYCONTROL | LCD_DISPLAYOFF )


    #turn on/off the lcd backlight
    def backlight(self, state):
        if state in ("on","On","ON"):
            self.lcd_device.backlight = True
            self.lcd_device.command(0)            
        elif state in ("off","Off","OFF"):
            self.lcd_device.backlight = False
            self.lcd_device.command(0)
        else:
            print("Unknown State!")
        

    # put string function
    def display_string(self, string, line):
        if line == 1:
            self.lcd_device.command(LCD_SETDDRAMADDR)
        if line == 2:
            self.lcd_device.command(LCD_SETDDRAMADDR | 0x40)
        if line == 3:
            self.lcd_device.command(LCD_SETDDRAMADDR | 0x14)
        if line == 4:
            self.lcd_device.command(LCD_SETDDRAMADDR | 0x54)

        for char in string:
            self.lcd_device.write(ord(char))

    def custom_char(self,number,data):
        self.lcd_device.command(LCD_SETCGRAMADDR|number*8)
        for b in data:
            self.lcd_device.write(b)
 

    # clear lcd
    def clear(self,home=True):
        self.lcd_device.command(LCD_CLEARDISPLAY)
        if home:
            self.home()

    # set to home
    def home(self):
        self.lcd_device.command(LCD_RETURNHOME)
        
    
     
