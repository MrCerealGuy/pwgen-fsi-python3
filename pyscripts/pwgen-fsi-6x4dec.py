#!/usr/bin/python

#     ____.    __________                        .______________
#    |    |__ _\______   \ ____   ____           |   \__    ___/
#    |    |  |  \       _// __ \_/ ___\   ______ |   | |    |   
#/\__|    |  |  /    |   \  ___/\  \___  /_____/ |   | |    |   
#\________|____/|____|_  /\___  >\___  >         |___| |____|   
#                      \/     \/     \/                       

# Copyright 2022: "JuRec-IT Version" Andreas Zahnleiter <a.zahnleiter@jurec-it.de>
# Copyright 2009:  dogbert <dogber1@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# This script generates master passwords which can be used to unlock
# the BIOS passwords of most Fujitsu Siemens laptops (Lifebook, Amilo etc.).

import os
import colorama
from colorama import Fore, Back, Style
from common import header, codeToBytes, byteToChar, wait_for_exit, formatted_password, print_copyright

colorama.init()

# someone smacked his head onto the keyboard
XORkey = "<7#&9?>s"

def decryptCode(bytes):
	# swap two bytes
	#bytes[2], bytes[6] = bytes[6], bytes[2]
	#bytes[3], bytes[7] = bytes[7], bytes[3]
	
	for i in range(len(bytes)):
		bytes[i] = int(bytes[i])

	# interleave the nibbles 
	bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5], bytes[6], bytes[7] = ((bytes[3] & 0xF0) | (bytes[0]  & 0x0F), (bytes[2] & 0xF0) | (bytes[1] & 0x0F), (bytes[5] & 0xF0) | (bytes[6] & 0x0F), (bytes[4] & 0xF0) | (bytes[7] & 0x0F), (bytes[7] & 0xF0) | (bytes[4] & 0x0F), (bytes[6] & 0xF0) | (bytes[5] & 0x0F), (bytes[1] & 0xF0)  | (bytes[2] & 0x0F), (bytes[0] & 0xF0) | (bytes[3] & 0x0F))

	# apply XOR key
	for i in range(len(bytes)):
		bytes[i] = int(bytes[i]) ^ ord(XORkey[i])

	# final rotations
	bytes[0] = ((bytes[0] << 1) & 0xFF) | (bytes[0] >> 7)
	bytes[1] = ((bytes[1] << 7) & 0xFF) | (bytes[1] >> 1)
	bytes[2] = ((bytes[2] << 2) & 0xFF) | (bytes[2] >> 6)
	bytes[3] = ((bytes[3] << 8) & 0xFF) | (bytes[3] >> 0)
	bytes[4] = ((bytes[4] << 3) & 0xFF) | (bytes[4] >> 5)
	bytes[5] = ((bytes[5] << 6) & 0xFF) | (bytes[5] >> 2)
	bytes[6] = ((bytes[6] << 4) & 0xFF) | (bytes[6] >> 4)
	bytes[7] = ((bytes[7] << 5) & 0xFF) | (bytes[7] >> 3)

	# len(solution space) = 10+26
	bytes = [x % 36 for x in bytes]

	masterPwd = ""
	for x in bytes:
		masterPwd += byteToChar(x)
	return masterPwd

# Print the clear screen code '\033[2J'
print(colorama.ansi.clear_screen())

header()

print(Fore.CYAN + "Master Password Generator for FSI laptops (6x4 digits version)" + Style.RESET_ALL)
print("")
print_copyright()
print("")
print("When asked for a password, enter these:")
print("First password:  3hqgo3")
print("Second password: jqw534")
print("Third password:  0qww294e")
print("")
print("You will receive a hash code with six blocks, each with four numbers, ")
print("e.g. 1234-4321-1234-4321-1234-4123")
print("")
print("Please enter the hash: ")
inHash = input().strip().replace('-', '').replace(' ', '')
inHash = inHash[4:]
password = decryptCode(codeToBytes(inHash))
print("")
print("The master password is: " + formatted_password(password))
print("")

wait_for_exit()

