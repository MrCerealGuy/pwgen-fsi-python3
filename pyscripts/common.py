#!/usr/bin/python

#     ____.    __________                        .______________
#    |    |__ _\______   \ ____   ____           |   \__    ___/
#    |    |  |  \       _// __ \_/ ___\   ______ |   | |    |   
#/\__|    |  |  /    |   \  ___/\  \___  /_____/ |   | |    |   
#\________|____/|____|_  /\___  >\___  >         |___| |____|   
#                      \/     \/     \/                       

# Copyright 2022: "JuRec-IT Version" Andreas Zahnleiter <a.zahnleiter@jurec-it.de>
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

def header():
    print(Fore.GREEN + "     ____.    __________                        .______________")
    print("    |    |__ _\______   \ ____   ____           |   \__    ___/")
    print("    |    |  |  \       _// __ \_/ ___\   ______ |   | |    |   ")
    print("/\__|    |  |  /    |   \  ___/\  \___  /_____/ |   | |    |   ")
    print("\________|____/|____|_  /\___  >\___  >         |___| |____|   ")
    print("                      \/     \/     \/                       " + Style.RESET_ALL)
    return
    
def print_copyright():
    print("Copyright (C) 2022 Andreas Zahnleiter <a.zahnleiter@jurec-it.de>")
    print("Copyright (C) 2009-2010 dogbert Support <by@vinafix.com>")
    return
    
def codeToBytes(code):
	numbers = (int(code[0:5]), int(code[5:10]), int(code[10:15]), int(code[15:20]))
	bytes = []
	for i in numbers:
		bytes.append(i % 256)
		bytes.append(i / 256)
	return bytes

def byteToChar(byte):
	if byte > 9:
		return chr(ord('a') + byte - 10)
	else:
		return chr(ord('0') + byte)
        
def wait_for_exit():
    print(Fore.RED + "Please note that the password is encoded for US QWERTY keyboard layouts." + Style.RESET_ALL)
    if (os.name == 'nt'):
        print("Press a key to exit...")
        input()
    return
    
def formatted_password(password):
    password_formatted = Back.GREEN + Fore.WHITE + password + Style.RESET_ALL
    return password_formatted