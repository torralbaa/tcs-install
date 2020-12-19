#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  install_mod.py
#  Copyright 2020 Alvarito050506 <donfrutosgomez@gmail.com>
#
#  You can freely use, distribute and/or modify
#  this file and its content without any restrictions
#  other than keeping this comment and the attribution
#  above. You may add your details to the list
#  if you modify this file.
#

import sys
import os
import re
import fnmatch
import shutil
import json

from tempfile import mkdtemp
from zipfile import ZipFile
from os.path import isdir, isfile

def win_glob(name, folder):
	regex = re.compile(fnmatch.translate(name), re.IGNORECASE);
	files = [];
	for file in os.listdir(folder):
		if regex.match(file):
			files.append(file);
	return files;

def win_exists(name, folder):
	return True if len(win_glob(name, folder)) >= 1 else False;

def get_avaiable(file, max):
	i = 0;
	avaiable = [];
	not_avaiable = [0];
	for line in file:
		tmp = line.rstrip("\r\n").rstrip("\n");
		if not tmp or tmp.startswith(";") or tmp.startswith(" "):
			continue;
		match = re.match("^([0-9]+)\s+([a-zA-Z]+\s+)*\"(.*)\"\s*(//.*)*$", tmp);
		if not match:
			if tmp == "\n" or tmp == "\r\n":
				continue;
			else:
				return (-1, []);
		not_avaiable.append(int(match.group(1)));
		i += 1;
	if i == 0:
		return (0, [-1]);
	avaiable = [x for x in range(not_avaiable[0], not_avaiable[-1] + 1)];
	avaiable = list(set(not_avaiable) ^ set(avaiable));
	return (0, avaiable);

def char_proc(char, tmp, folder, id):
	try:
		char_dir = char["folder"];
		char_name = char["name"];
		char_names = char["names"];
	except:
		print("Error: Invalid character description.");
		return -1;
	try:
		char_price = char["price"];
	except:
		print("Error: By now, all characters must have a price.");
		return -2;
	chars_folder = f"{folder}/CHARS/";
	text_folder = f"{folder}/STUFF/TEXT/";
	char_ghg = f"{tmp}/CHARS/{char_name}.GHG";
	char_txt = f"{tmp}/CHARS/{char_name}.TXT";
	if not (isdir(f"{chars_folder}/{char_dir}") and isdir(f"{tmp}/CHARS/")):
		print("Error: Invalid character folder.");
		return -3;
	if not (isfile(char_ghg) and isfile(char_txt)):
		print("Error: Missing character files.");
		return -4;
	txt_file = open(char_txt, "a");
	txt_file.write(f"name_id={id}\r\n");
	txt_file.close();
	shutil.copyfile(char_ghg, f"{chars_folder}/{char_dir}/{char_name}.GHG");
	shutil.copyfile(char_txt, f"{chars_folder}/{char_dir}/{char_name}.TXT");
	for lang in char_names.__iter__():
		lang_path = f"{text_folder}/{lang.upper()}.TXT";
		if isfile(lang_path):
			name = char_names[lang];
			lang_file = open(lang_path, "a");
			lang_file.write(f"{id} \"{name}\"\r\n");
			lang_file.close();
			chars_file = open(f"{chars_folder}/CHARS.TXT", "a");
			chars_file.write("char_start\r\n");
			chars_file.write(f"\tdir \"{char_dir}\"\r\n");
			chars_file.write(f"\tfile \"{char_name}\"\r\n");
			chars_file.write("char_end\r\n");
			chars_file.close();
			collection_file = open(f"{chars_folder}/COLLECTION.TXT", "a");
			collection_file.write(f"collect \"{char_name}\" buy_in_shop {char_price}\r\n");
			collection_file.close();
	return 0;

def main(argc, argv):
	lang = open(f"{argv[1]}/STUFF/TEXT/ENGLISH.TXT", "r+");
	err, avaiable = get_avaiable(lang, 9999);
	lang.close();
	if err < 0:
		print("Error: While reading the language file.");
		return -1;
	if len(avaiable) < 1:
		print("Error: No extra IDs avaiable.");
		return -1;
	zip = ZipFile(argv[2], "r");
	tmp = mkdtemp(prefix="lswtcsmod");
	zip.extractall(tmp);
	print(tmp);
	zip.close();
	chars_file = open(f"{tmp}/chars.json", "r");
	chars = json.load(chars_file);
	chars_file.close();
	i = len(avaiable) - 1;
	for char in chars:
		if i <= 0:
			print("Error: No extra IDs avaiable.");
			break;
		char_proc(char, tmp, argv[1], avaiable[i]);
		i -= 1;
	shutil.rmtree(tmp);
	return 0;


sys.exit(main(len(sys.argv), sys.argv));

