import smbus
from time import *

# flags for backlight control

LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00

Bl = 0b00001000 # backlight bit
En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit


# ALTERNATIVE ADDRESSES (1 JUMPER SET)
#000 27
#100 26
#010 25
#110 24
#001 23
#101 22
#011 21
#111 20

class PCF8574T:
    def __init__(self, address=0x27, port=1, backlight=False):
        self.address = address
        self.bus = smbus.SMBus(port)
        self.__backlight = backlight

        self.command(0x03)
        self.command(0x03)
        self.command(0x03)

        if self.nibble_mode():
            self.command(0x02)    

    def backlight(self,backlight=None):
        if backlight is not None:
            self.__backlight = backlight
        return self.__backlight

    def nibble_mode(self):
        return True;

    def write(self, data):
        self.__write(data,select=True,readwrite=False)
    
    def command(self, command):
        if command & 0b1110000 == 0x20: # looking for function set command
            # print("FUNCTON SET %02x %02x" % (command,command & 0xe0))
            if self.nibble_mode():
                command = command & ~LCD_8BITMODE
            else:
                command = command | LCD_8BITMODE            
        self.__write(command,select=False,readwrite=False)
    
    def __write(self,cmd,select=False,readwrite=False):
        mode = 0
        if select:
            mode = mode | Rs
        if readwrite:
            mode = mode | Rw
        if self.__backlight:
            mode = mode | Bl          
        
        self.__write_two_nibble(mode | (cmd & 0xF0))
        self.__write_two_nibble(mode | ((cmd << 4) & 0xF0))        

    def __write_two_nibble(self, data):
        self.bus.write_byte(self.address, data & ~En)
        # strobe: clocks EN to latch command
        self.bus.write_byte(self.address, data | En)
        sleep(.0005)
        self.bus.write_byte(self.address, data & ~En)
        sleep(.0002)  


    # Write a command and argument
    #def write_cmd_arg(self, cmd, data):
    #    self.bus.write_byte_data(self.address, cmd, data)
    #    sleep(0.0001)

    # Write a block of data
    #def write_block_data(self, cmd, data):
    #    self.bus.write_block_data(self.address, cmd, data)
    #    sleep(0.0001)

    # Read a single byte
    def read(self):
        return self.bus.read_byte(self.address)

    # Read
    def read_data(self, cmd):
        return self.bus.read_byte_data(self.address, cmd)

    # Read a block of data
    def read_block_data(self, cmd):
        return self.bus.read_block_data(self.address, cmd)
      
