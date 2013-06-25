#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, sys
import struct

n = 0
SECTOR_SIZE = 512

def logo():
  print """

**********************************************	
	
	coder by KoNaN 2013
	
	rmbr.py [--param=value]
	
	Params:
	-h, --help
	-i file, --input=file
	
**********************************************
	"""
#++++++++++++++++

# read usign byte from data block
def read_ub(data):
	return struct.unpack('B',data[0])[0]

# read unsigned short int (2 bytes) from data block
def read_us(data):
	return struct.unpack('<H',data[0:2])[0]

# read an unsigned int (4 bytes) from data block
def read_ui(data):
	return struct.unpack('<I',data[0:4])[0]

#++++++++++++++++++
class PartitionTable:
	
	def __init__(self,data):
		
		for x in range (0,4):
			begin = (16*x)
			end = (16*(x+1))			
			#print "init %s end %s" % (begin,end)
		
			data_tmp = data[begin:end]
			PartitionEntry(data_tmp)	
			



class PartitionEntry:
	def __init__(self,data):
		global n
		global SECTOR_SIZE
		n = n + 1
		self.Status = read_ub(data)
		self.StartHead = read_ub(data[1])
		tmp = read_ub(data[2])
		self.StartSector = tmp & 0x3F
		self.PartType = read_ub(data[4])
		self.strPartType = self.strPartitionT(self.PartType)
		
		if self.PartType <> 0: 
			print "%s - %s | start sector: %s | offset: %s" % (n, 
			self.strPartType,
			self.StartSector,
			self.StartSector * SECTOR_SIZE)  
	 
	
	
	def strPartitionT(self,valueT):		
		type_partitions = {
			0x00:"Empty",
			0x01:"DOS 12-bit FAT",
			0x02:"XENIX root",
			0x03:"XENIX usr",
			0x04:"DOS 3.0 16-bit FAT up 32MB",
			0x05:"DOS 3.3 Extend Partition",
			0x06:"DOS 3.31 16-bit FAT over 32MB",
			0x07:"Windows NT NTFS - exFAT",
			0x08:"Advanced Unix",
			0x09:"AIX data partition",
			0x0B:"32 bit FAT",
			0x0C:"32 bit FAT using int 13 extansions",
			0x0F:"Extended Partition",
			0x10:"Opus",
			0x11:"Hidden 12-bit FAT",
			0x12:"Compaq diagnostics"			   
			}
		
		
		
		for k,v in type_partitions.iteritems():
				if hex(valueT) == hex(k):
					return v
		
		
	

	def check_status(self):
		if(self.Status == 0x00):
			print "Not bootable"
		else:
			if(self.Status == 0x80):
				print "Bootable"
			else:
				print "Invalid bootable byte"

#++++++++++++++++++

class MBR:
	
	def __init__(self,data):
		
		self.BootCode = data[:440] 
		self.DiskSig = data[440:444] 
		self.Unused = data[444:446]
		self.PartitionTable = PartitionTable(data[446:510])
		self.MBRSign = data[510:512]
		
		
	def check_mbr_sig(self):
		mbr_sig = read_us(self.MBRSign)
		if (mbr_sig == 0xAA55):
			print "\nCorrect MBR signature: 0x%04X" % (mbr_sig) 
		else:
			print "\nIncorrect MBR signature: 0x%04X" % (mbr_sig) 




if __name__ =="__main__":
	
	try:
		opts, args = getopt.getopt(sys.argv[1:],"i:h",["help","input="])
	except getopt.GetoptError,err:
		print str(err) 
		logo()
		sys.exit(2)
			
	input = None	
		
	for o,a in opts:
		if o in ("-h","--help"):
			logo()
			sys.exit()
		if o in ("-i","--input"):
			input = a
		else:
			assert False, "Unable option"	
			
	if not input:
		logo()
		sys.exit()
		

# open files

f = open(input,'rb')
data = f.read()

print "Read: %d bytes\n" % (len(data))
print "Partitions:"
print "--------------------------------------"
master_mbr = MBR(data)
master_mbr.check_mbr_sig()





f.close()



			
