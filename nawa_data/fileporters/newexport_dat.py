import math
import os
from nawa_data.fileporters.utils.ioUtils import write_string, write_Int32, write_buffer, write_uInt32, write_Int16
from typing import List
import zlib
import os

def crc32(text: str) -> int:
    return zlib.crc32(text.encode('ascii')) & 0xFFFFFFFF

def next_power_of_2_bits(x: int) -> int:
    return 1 if x == 0 else (x - 1).bit_length()

class HashData:
    preHashShift: int
    bucketOffsets: List[int]
    hashes: List[int]
    fileIndices: List[int]

    def __init__(self, preHashShift: int):
        self.preHashShift = preHashShift
        self.bucketOffsets = []
        self.hashes = []
        self.fileIndices = []

    def getStructSize(self):
        return 4 + 2*len(self.bucketOffsets) + 4*len(self.hashes) + 4*len(self.fileIndices)

    def write(self, file):
        bucketsOffset = 4*4
        hashesOffset = bucketsOffset + len(self.bucketOffsets)*2
        fileIndicesOffset = hashesOffset + len(self.hashes)*4

        write_uInt32(file, self.preHashShift)
        write_uInt32(file, bucketsOffset)
        write_uInt32(file, hashesOffset)
        write_uInt32(file, fileIndicesOffset)

        for bucketOffset in self.bucketOffsets:
            write_Int16(file, bucketOffset)
        for hash in self.hashes:
            write_uInt32(file, hash)
        for fileIndex in self.fileIndices:
            write_Int16(file, fileIndex)

def generateHashData(files) -> bytes:
    preHashShift = min(31, 32 - next_power_of_2_bits(len(files)))
    bucketOffsetsSize = 1 << (31 - preHashShift)
    bucketOffsets = [-1] * bucketOffsetsSize
    hashes = [0] * len(files)
    fileIndices = list(range(len(files)))
    fileNames = [os.path.basename(i) for i in files.copy()]

    # generate hashes
    for i in range(len(files)):
        fileName = os.path.basename(files[i])
        hash = crc32(fileName.lower())
        otherHash = (hash & 0x7FFFFFFF)
        hashes[i] = otherHash
    # sort by first half byte (x & 0x70000000)
    # sort indices & hashes at the same time
    hashes, fileIndices, fileNames = zip(*sorted(zip(hashes, fileIndices, fileNames), key=lambda x: x[0] & 0x70000000))
    # generate bucket list
    for i in range(len(files)):
        bucketOffsetsIndex = hashes[i] >> preHashShift
        if bucketOffsets[bucketOffsetsIndex] == -1:
            bucketOffsets[bucketOffsetsIndex] = i

    hashData = HashData(preHashShift)
    hashData.bucketOffsets = bucketOffsets
    hashData.hashes = hashes
    hashData.fileIndices = fileIndices
    return hashData
def to_string(bs, encoding = 'utf8'):
	return bs.split(b'\x00')[0].decode(encoding)

def main(export_filepath, file_list):
    files = file_list
    fileNumber = len(files)
    hashData = generateHashData(files)

    fileExtensionsSize = 0
    fileExtensions = []
    for fp in files:
        fileExt = fp.split('.')[-1]
        fileExt += '\x00' * (3 - len(fileExt))
        fileExtensionsSize += len(fileExt) + 1
        fileExtensions.append(fileExt)

    nameLength = 0                              
    for fp in files:
        fileName = os.path.basename(fp)
        if len(fileName)+1 > nameLength:
            nameLength = len(fileName)+1

    fileNames = []                             
    for fp in files:
        fileName = os.path.basename(fp)
        fileNames.append(fileName)

    hashMapSize = hashData.getStructSize()

    # Header
    fileID = 'DAT'
    fileNumber = fileNumber
    fileOffsetsOffset = 32
    fileExtensionsOffset = fileOffsetsOffset + (fileNumber * 4)
    fileNamesOffset = fileExtensionsOffset + fileExtensionsSize
    fileSizesOffset = fileNamesOffset + (fileNumber * nameLength) + 4
    hashMapOffset = fileSizesOffset + (fileNumber * 4)

    #fileOffsets
    fileOffsets = []
    currentOffset = hashMapOffset + hashMapSize
    for fp in files:
        currentOffset = (math.ceil(currentOffset / 16)) * 16
        fileOffsets.append(currentOffset)
        currentOffset += os.path.getsize(fp)

    # fileSizes
    fileSizes = []
    for fp in files:
        fileSizes.append(os.path.getsize(fp))

    # WRITE
        # Header
    dat_file = open(export_filepath, 'wb')
    write_string(dat_file, fileID)
    write_Int32(dat_file, fileNumber)
    write_Int32(dat_file, fileOffsetsOffset)
    write_Int32(dat_file, fileExtensionsOffset)
    write_Int32(dat_file, fileNamesOffset)
    write_Int32(dat_file, fileSizesOffset)
    write_Int32(dat_file, hashMapOffset)
    write_buffer(dat_file, 4)

        # fileOffsets
    for value in fileOffsets:
        write_Int32(dat_file, value)

        # fileExtensions
    for value in fileExtensions:
        write_string(dat_file, value)

        # nameLength
    write_Int32(dat_file, nameLength)

        # fileNames
    for value in fileNames:
        write_string(dat_file, value)
        if len(value) < nameLength:
            write_buffer(dat_file, nameLength - len(value) - 1)

        # fileSizes
    for value in fileSizes:
        write_Int32(dat_file, value)

        # hashMap
    hashData.write(dat_file)

        # Files
    for i, fp in enumerate(files):
        dat_file.seek(fileOffsets[i])
        fileData = open(fp, 'rb')
        fileContent = fileData.read()
        dat_file.write(fileContent)
        fileData.close()

    dat_file.close()