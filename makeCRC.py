# CRC생성코드 파이썬용
crcTable = []


def gencrc(data, polynomial, crc):  #  crc를 만들어내는 함수
    for i in range(0, 8):
        if (data ^ crc) & 1:
            crc = (crc >> 1) ^ polynomial
        else:
            crc >>= 1
        data >>= 1
    return crc & 0xFFFF


def makecrctable():  # crc테이블을 생성하는 함수
    polynomial = 0xA001
    for i in range(0, 256):
        crcTable.append(gencrc(i, polynomial, 0))


def crc16(puscMsg, usDataLen):  # crc코드를 만들어 내는 함수
    uchCRCHi = 0xFF
    uchCRCLo = 0xFF
    i = 0
    while usDataLen != 0:
        usDataLen -= 1
        uindex = uchCRCHi ^ puscMsg[i]
        i += 1
        uchCRCHi = uchCRCLo ^ (crcTable[uindex] & 0xFF)
        uchCRCLo = (crcTable[uindex] >> 8) & 0xFF
    return (uchCRCHi << 8) | uchCRCLo