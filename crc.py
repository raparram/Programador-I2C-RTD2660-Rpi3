##### CRC Methods
gCrc = 0

def InitCRC():
    global gCrc
    gCrc = 0

# def ProcessCRC(const uint8_t *data, int len)
def ProcessCRC(data, len):
    global gCrc
    # for (j = len; j; j--, data++):
    i = 0
    j = len
    while j:
        # gCrc ^= (*data << 8)
        # left shift
        l = list(data[0:1])[0]
        del data[0:1]
        gCrc ^= l
        # for(i = 8; i; i--) {
        i = 8
        while i:
            if (gCrc & 0x8000):
                gCrc ^= (0x1070 << 3)
            gCrc <<= 1
            i -= 1

        j -= 1

        # I think we were advancing the pointer here in c
        # not necessary in this python implementation
        # since we're effectively popping values off of the left side
        # the data "pointer" is always moving
        # data += 1


# uint8_t GetCRC() {
def GetCRC():
    global gCrc
    # return (uint8_t)(gCrc >> 8)
    return gCrc >> 8

#####