# I2C PROGRAMMER FOR RTD2660 FROM RASPBERRY PI

# Optimized for PCB800099 and PCB800661 cards. This software programs the flash memory connected to RTD2660.
# Github: https://github.com/raparram/Programador-I2C-RTD2660-Rpi3

# Code base: https://github.com/mushketer888/pyrtd2660i2c
# Please! Visit this.

from smbus import SMBus
import time
import os
import crc
import sys
import array

print "Opening bus..."
bus = SMBus(1) # Choose the I2C bus to which the card is connected. Rpi3: 1

E_CC_READ = 2
E_CC_WRITE_AFTER_WREN = 3
E_CC_WRITE_AFTER_EWSR = 4
E_CC_ERASE = 5

class FlashDesc:
    def __init__(self, device_name,jedec_id,size_kb,page_size,block_size_kb):
        self.device_name = device_name;
        self.jedec_id = jedec_id;
        self.size_kb = size_kb;
        self.page_size = page_size;
        self.block_size_kb = block_size_kb;

FlashDevices = [
    #          name,         Jedec ID,    sizeK, page size, block sizeK
    FlashDesc("AT25DF041A" , 0x1F4401,      512,       256, 64),
    FlashDesc("AT25DF161"  , 0x1F4602, 2 * 1024,       256, 64),
    FlashDesc("AT26DF081A" , 0x1F4501, 1 * 1024,       256, 64),
    FlashDesc("AT26DF0161" , 0x1F4600, 2 * 1024,       256, 64),
    FlashDesc("AT26DF161A" , 0x1F4601, 2 * 1024,       256, 64),
    FlashDesc("AT25DF321" ,  0x1F4701, 4 * 1024,       256, 64),
    FlashDesc("AT25DF512B" , 0x1F6501,       64,       256, 32),
    FlashDesc("AT25DF512B" , 0x1F6500,       64,       256, 32),
    FlashDesc("AT25DF021"  , 0x1F3200,      256,       256, 64),
    FlashDesc("AT26DF641" ,  0x1F4800, 8 * 1024,       256, 64),
    # Manufacturer: ST 
    FlashDesc("M25P05"     , 0x202010,       64,       256, 32),
    FlashDesc("M25P10"     , 0x202011,      128,       256, 32),
    FlashDesc("M25P20"     , 0x202012,      256,       256, 64),
    FlashDesc("M25P40"     , 0x202013,      512,       256, 64),
    FlashDesc("M25P80"     , 0x202014, 1 * 1024,       256, 64),
    FlashDesc("M25P16"     , 0x202015, 2 * 1024,       256, 64),
    FlashDesc("M25P32"     , 0x202016, 4 * 1024,       256, 64),
    FlashDesc("M25P64"     , 0x202017, 8 * 1024,       256, 64),
    # Manufacturer: Windbond 
    FlashDesc("W25X10"     , 0xEF3011,      128,       256, 64),
    FlashDesc("W25X20"     , 0xEF3012,      256,       256, 64),
    FlashDesc("W25X40"     , 0xEF3013,      512,       256, 64),
    FlashDesc("W25X80"     , 0xEF3014, 1 * 1024,       256, 64), # PCB800099
    FlashDesc("W25Q80DV"   , 0xEF4014, 1 * 1024,       256, 64), # PCB800661
    # Manufacturer: Macronix 
    FlashDesc("MX25L512"   , 0xC22010,       64,       256, 64),
    FlashDesc("MX25L3205"  , 0xC22016, 4 * 1024,       256, 64),
    FlashDesc("MX25L6405"  , 0xC22017, 8 * 1024,       256, 64),
    FlashDesc("MX25L8005"  , 0xC22014,     1024,       256, 64),
    # Microchip
    FlashDesc("SST25VF512" , 0xBF4800,       64,       256, 32),
    FlashDesc("SST25VF032" , 0xBF4A00, 4 * 1024,       256, 32),
    FlashDesc(None , 0, 0, 0, 0)
]

def SPICommonCommand( cmd_type, cmd_code, read_length, write_length, write_value):
    read_length &= 3
    write_length &= 3
    write_value &= 0xFFFFFF
    # uint8_t
    reg_value = (cmd_type << 5) | (write_length << 3) | (read_length << 1)

    bus.write_i2c_block_data(0x4a,0x60, [reg_value])
    bus.write_i2c_block_data(0x4a,0x61, [cmd_code])

    if write_length == 3:
        bus.write_i2c_block_data(0x4a,0x64, [write_value >> 16])
        bus.write_i2c_block_data(0x4a,0x65, [write_value >> 8])
        bus.write_i2c_block_data(0x4a,0x66, [write_value])
    elif write_length == 2:
        bus.write_i2c_block_data(0x4a,0x64, [write_value >> 8])
        bus.write_i2c_block_data(0x4a,0x65, [write_value])
    elif write_length == 3:
        bus.write_i2c_block_data(0x4a,0x64, [write_value])

    bus.write_i2c_block_data(0x4a,0x60, [reg_value | 1]) # Execute the command
    # uint8_t b;
    b = bus.read_i2c_block_data(0x4a,0x60,1)
    print b
    b=b[0]
    while (b & 1):
        b = bus.read_i2c_block_data(0x4a,0x60,1)
        b=b[0]
    if read_length == 0:
        return 0
    elif read_length == 1:
        return bus.read_i2c_block_data(0x4a,0x67,1)[0]
    elif read_length == 2:
        return (bus.read_i2c_block_data(0x4a,0x67,1)[0] << 8) | bus.read_i2c_block_data(0x4a,0x68,1)[0]
    elif read_length == 3:
        return (bus.read_i2c_block_data(0x4a,0x67,1)[0] << 16) | (bus.read_i2c_block_data(0x4a,0x68,1)[0] << 8) | bus.read_i2c_block_data(0x4a,0x69,1)[0]

def SPIRead( address, data, len):
    bus.write_i2c_block_data(0x4a,0x60, [0x46])
    bus.write_i2c_block_data(0x4a,0x61, [0x3])
    bus.write_i2c_block_data(0x4a,0x64, [address>>16])
    bus.write_i2c_block_data(0x4a,0x65, [address>>8])
    bus.write_i2c_block_data(0x4a,0x66, [address])
    bus.write_i2c_block_data(0x4a,0x60, [0x47]) # Execute the command
    # uint8_t b;
    b = bus.read_i2c_block_data(0x4a,0x60,1)[0]

    while(b & 1):
        b = bus.read_i2c_block_data(0x4a,0x60,1)[0]
        # TODO: add timeout and reset the controller

    while (len > 0):
        read_len = len # int32_t
        if (read_len > 64):
            read_len = 64

        bytedata = bytearray()
        itr = read_len
        while(itr > 0):
            bytedata += bytearray([bus.read_i2c_block_data(0x4a,0x70,1)[0]])
            itr -= 1

        data += bytedata
        len -= read_len
def SetupChipCommands(jedec_id):
    manufacturer_id = GetManufacturerId(jedec_id)
    if manufacturer_id == 0xEF:
        # These are the codes for Winbond
        bus.write_i2c_block_data(0x4a,0x62, [0x6])  # Flash Write enable op code
        bus.write_i2c_block_data(0x4a,0x63, [0x50]) # Flash Write register op code
        bus.write_i2c_block_data(0x4a,0x6a, [0x3])  # Flash Read op code.
        bus.write_i2c_block_data(0x4a,0x6b, [0xb])  # Flash Fast read op code.
        bus.write_i2c_block_data(0x4a,0x6d, [0x2])  # Flash program op code.
        bus.write_i2c_block_data(0x4a,0x6e, [0x5])  # Flash read status op code.
    else:
        printf("Can not handle manufacturer code %02x\n", manufacturer_id)

def SPIComputeCRC(start, end):
    bus.write_i2c_block_data(0x4a,0x64, [start >> 16])
    bus.write_i2c_block_data(0x4a,0x65, [start >> 8])
    bus.write_i2c_block_data(0x4a,0x66, [start])

    bus.write_i2c_block_data(0x4a,0x72, [end >> 16])
    bus.write_i2c_block_data(0x4a,0x73, [end >> 8])
    bus.write_i2c_block_data(0x4a,0x74, [end])

    bus.write_i2c_block_data(0x4a,0x6f, [0x84])
    
    b = bus.read_i2c_block_data(0x4a,0x6f,1)[0]
    while (not (b & 0x2)):
        b = bus.read_i2c_block_data(0x4a,0x6f,1)[0]
    # TODO: add timeout and reset the controller
    return bus.read_i2c_block_data(0x4a,0x75,1)[0]

def ShouldProgramPage(buffer, size):
    # for (uint32_t idx = 0; idx < size; ++idx) {
    idx = 0
    while idx < size:
        if (buffer[idx] != 0xff):
            return True;
        ++idx
    return False;

def ProgramFlash(fname,chip_size):
    masiv=open(fname,"rb")
    print "Erasing..."
    SPICommonCommand(E_CC_WRITE_AFTER_EWSR, 1, 0, 1, 0); #// Unprotect the Status Register
    SPICommonCommand(E_CC_WRITE_AFTER_WREN, 1, 0, 1, 0); #// Unprotect the flash
    SPICommonCommand(E_CC_ERASE, 0xc7, 0, 0, 0); #// Chip Erase
    print "Done"
    b=0
    addr = 0
    buffer = bytearray()
    #res = array.array('c')
    crc.InitCRC();
    #RTD266x can program only 256 bytes at a time.
    print "chip size %x" % chip_size
    while addr<(chip_size):
        while b & 0x40:
            b = bus.read_i2c_block_data(0x4a,0x6f,1)[0]

        print "Writing addr %x\r" % addr
        buffer=masiv.read(256)
        res=[]
        for i in buffer:
            res.append(ord(i))
        #print type(buffer)
        #res.fromfile(masiv, 256)
        #print buffer
        if True:
            
            # Set program size-1
            bus.write_i2c_block_data(0x4a,0x71, [255]);

              # Set the programming address
            bus.write_i2c_block_data(0x4a,0x64, [addr >> 16]);
            bus.write_i2c_block_data(0x4a,0x65, [addr >> 8]);
            bus.write_i2c_block_data(0x4a,0x66, [addr]);

            for bajt in res:
                bus.write_i2c_block_data(0x4a,0x70, [bajt]) 

            bus.write_i2c_block_data(0x4a,0x6f, [0xa0]); 
       
        crc.ProcessCRC(list(res), len(buffer))
        addr += 256;
    print "done"
    masiv.close();

    # Wait for programming cycle to finish
    while b & 0x40:
        b = bus.read_i2c_block_data(0x4a,0x6f,1)[0]
  
    SPICommonCommand(E_CC_WRITE_AFTER_EWSR, 1, 0, 1, 0x1c); #// Unprotect the Status Register
    SPICommonCommand(E_CC_WRITE_AFTER_WREN, 1, 0, 1, 0x1c); #// Protect the flash

    # uint8_t data_crc = GetCRC();
    data_crc = crc.GetCRC()
    # uint8_t chip_crc = SPIComputeCRC(0, chip_size - 1);

    # Temporarily disabling CRC
    chip_crc = SPIComputeCRC(0, chip_size - 1)
    # chip_crc = 0
    # 

    print "Received data CRC {0:02X}\n".format(data_crc);
    print "Chip CRC {0:02X}\n".format(chip_crc);
    return data_crc == chip_crc;

def GetFileSize(file):
    return os.stat.st_size(file)
    return 0;

# void PrintManufacturer(uint32_t id) {
def PrintManufacturer(id):
    if id == 0x20:
        print "ST"
    elif id == 0xef:
        print "Winbond"
    elif id == 0x1f:
        print "Atmel"
    elif id == 0xc2:
        print "Macronix"
    elif id == 0xbf:
        print "Microchip"
    else:
        print "Unknown"

def FindChip(jedec_id):
    for chip in FlashDevices:
        if (chip.jedec_id == jedec_id):
            print "flash matches!"
            return chip
    print "What is this flash chip?"
    print ">>> Review wiki to add new flash chip !"
    exit(0)
    return None    
    
def GetManufacturerId(jedec_id):
    return jedec_id >> 16

print "Enter ISP?"
bus.write_i2c_block_data(0x4a,0x6f, [0x80])
print "Send SPI command"
jedec_id = SPICommonCommand(E_CC_READ, 0x9f, 3, 0, 0);
print "JEDEC ID: 0x{:02X}\n".format(jedec_id);
chip = FindChip(jedec_id);

print "Manufacturer "
PrintManufacturer(GetManufacturerId(chip.jedec_id));
print "\n"
print "Chip: {}\n".format(chip.device_name)
print "Size: {}KB\n".format(chip.size_kb)

#   // Setup flash command codes
SetupChipCommands(jedec_id)
b = SPICommonCommand(E_CC_READ, 0x5, 1, 0, 0)
print "Flash status register: 0x{:02X}\n".format(b)
ticks = time.time()
filenam= sys.argv[1]

#Program chip
print "Flashing \"{0}\" to controller".format(os.path.abspath(filenam))
ProgramFlash(filenam,256* 1024)
duration = time.time() - ticks
remainder = duration % (60 * 60)
hour_secs = duration - remainder
hours = hour_secs/(60 * 60)
duration -= hour_secs
remainder = duration % (60)
min_secs = duration - remainder
mins = min_secs/(60)
duration -= min_secs
secs = duration
print "run time: {0}:{1}:{2}".format(hours, mins, secs)

exit()
