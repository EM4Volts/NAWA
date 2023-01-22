#encoding = utf-8
import os
import struct
from nawa_data.fileporters.utils.util import to_int

def little_endian_to_float(bs):
    return struct.unpack("<f", bs)[0]

def little_endian_to_int(bs):
    return int.from_bytes(bs, byteorder='little')

def create_dir(dirpath):
	if not os.path.exists(dirpath):
		os.makedirs(dirpath)

def read_header(fp):
	Magic = fp.read(4)
	if list(Magic) == [68, 65, 84, 0]:
		FileCount = little_endian_to_int(fp.read(4))
		FileTableOffset = little_endian_to_int(fp.read(4))
		ExtensionTableOffset = little_endian_to_int(fp.read(4))
		NameTableOffset = little_endian_to_int(fp.read(4))
		SizeTableOffset = little_endian_to_int(fp.read(4))
		hashMapOffset = little_endian_to_int(fp.read(4))
		print(
'''FileCount: %08x
FileTableOffset: %08x
ExtensionTableOffset:%08x
NameTableOffset:%08x
SizeTableOffset:%08x
hashMapOffset:%08x
'''%
			(FileCount, FileTableOffset, ExtensionTableOffset,NameTableOffset,SizeTableOffset,hashMapOffset)
		)
		return (FileCount, FileTableOffset, ExtensionTableOffset,NameTableOffset,SizeTableOffset,hashMapOffset)
	else:
		print('[-] error magic number detected')
		return False

def get_fileinfo(fp, index, FileTableOffset, ExtensionTableOffset, NameTableOffset, SizeTableOffset):
	fp.seek(FileTableOffset + index * 4)
	FileOffset = little_endian_to_int(fp.read(4))
	fp.seek(ExtensionTableOffset + index * 4)
	Extension = fp.read(4).decode('utf-8')
	fp.seek(SizeTableOffset + index * 4)
	Size = little_endian_to_int(fp.read(4))
	fp.seek(NameTableOffset)
	FilenameAlignment = little_endian_to_int(fp.read(4))
	i = 0
	while i < index:
		if list(fp.read(FilenameAlignment))[FilenameAlignment-1] == 0:
			i += 1
	Filename = fp.read(256).split(b'\x00')[0].decode('ascii')
	return index,Filename,FileOffset,Size,Extension

def extract_file(fp, filename, FileOffset, Size, extract_dir):
	create_dir(extract_dir)
	fp.seek(FileOffset)
	FileContent = fp.read(Size)
	outfile = open(extract_dir + '/'+filename,'wb')
	outfile.write(FileContent)
	outfile.close()
	if filename.find('wtp') > -1 and False:  # Removed due to not needed anymore when using Blender DTT import.
		wtp_fp = open(extract_dir + '/'+filename,"rb")
		content = wtp_fp.read(Size)
		dds_group = content.split(b'DDS ')
		dds_group = dds_group[1:]
		for i in range(len(dds_group)):
			dds_fp = open(extract_dir + '/'+filename.replace('.wtp','_%d.dds'%i), "wb")
			dds_fp.write(b'DDS ')
			dds_fp.write(dds_group[i])
			dds_fp.close()
		wtp_fp.close()
		#os.remove("%s/%s"%(extract_dir,filename))

def get_all_files(path):
	pass

def extract_hashes(fp, extract_dir, FileCount, hashMapOffset, fileNamesOffset):
	create_dir(extract_dir)

	# file_order.metadata
	# Filename Size
	fp.seek(fileNamesOffset)
	fileNameSize = little_endian_to_int(fp.read(4))

	# Filenames
	fileNames = []
	for i in range(FileCount):
		fileNames.append(fp.read(fileNameSize))

	# Extraction
	filename = 'file_order.metadata'
	extract_dir_sub = extract_dir + '\\' + filename
	outfile = open(extract_dir_sub,'wb')

	# Header
	outfile.write(struct.pack('<i', FileCount))
	outfile.write(struct.pack('<i', fileNameSize))

	#Filenames
	for fileName in fileNames:
		outfile.write(fileName)

	outfile.close()

	# hash_data.metadata
	# Header
	fp.seek(hashMapOffset)
	preHashShift = to_int(fp.read(4))
	bucketOffsetsOffset = to_int(fp.read(4))
	hashesOffset = to_int(fp.read(4))
	fileIndicesOffset = to_int(fp.read(4))

	# Bucket Offsets
	fp.seek(hashMapOffset + bucketOffsetsOffset)
	bucketOffsets = []
	while fp.tell() < (hashMapOffset + hashesOffset):
		bucketOffsets.append(to_int(fp.read(2)))

	# Hashes
	fp.seek(hashMapOffset + hashesOffset)
	hashes = []
	for i in range(FileCount):
		hashes.append(fp.read(4))

	# File Indices
	fp.seek(hashMapOffset + fileIndicesOffset)
	fileIndices = []
	for i in range(FileCount):
		fileIndices.append(to_int(fp.read(2)))
 
	# Extraction
	filename = 'hash_data.metadata'
	extract_dir_sub = extract_dir + '\\' + filename
	outfile = open(extract_dir_sub,'wb')

		# Header
	outfile.write(struct.pack('<i', preHashShift))
	outfile.write(struct.pack('<i', bucketOffsetsOffset))
	outfile.write(struct.pack('<i', hashesOffset))
	outfile.write(struct.pack('<i', fileIndicesOffset))

		# Bucket Offsets
	for i in bucketOffsets:
		#print(bucketOffsets)
		outfile.write(struct.pack('<H', i))

		# Hashes
	for i in hashes:
		outfile.write(i)

		# File Indices
	for i in fileIndices:
		#print(i)
		outfile.write(struct.pack('<H', i))

	outfile.close()


def main(filename, extract_dir):
	fp = open(filename,"rb")
	headers = read_header(fp)
	if headers:
		FileCount, FileTableOffset, ExtensionTableOffset,NameTableOffset,SizeTableOffset,hashMapOffset = headers

		for i in range(FileCount):
			extract_dir_sub = ''
			index,Filename,FileOffset,Size,Extension = get_fileinfo(fp, i, FileTableOffset,ExtensionTableOffset, NameTableOffset,SizeTableOffset)
			if extract_dir != '':
				extract_dir_sub = extract_dir
				extract_file(fp, Filename, FileOffset, Size, extract_dir_sub)
        
		extract_hashes(fp, extract_dir, FileCount, hashMapOffset, NameTableOffset)

	return Filename

