# tcs-install

Mod installer/manager for old TT Games, like LEGO Star Wars: The Complete Saga.

### :warning: Warning
This project is currently a Work In Progress. It lacks of many basic features, but will be added soon. tcs-install was not tested in other games than LSW:TCS.

## Usage
You will need Python `>= 3.7.x` preinstalled and in your `PATH` to use the installer.

To install a mod, do:
```sh
python3.exe PATH/TO/install_mod.py PATH/TO/TCS/ PATH/TO/MOD.ZIP
```

## ZIP structure
The structure of a mod's ZIP that contains one character (`CHAR1`) would be the following:
```
/
|- chars.json
|- CHARS/
   |- CHAR1.GHG
   |- CHAR1.TXT
```

## JSON specifications
The basic structure of a mod's `chars.json` containing one character (`CHAR1`) would be like the following:
```json
[
	{
		"name": "CHAR1",
		"names": {
			"english": "Character One"
		},
		"price": 10000,
		"folder": "CLONE"
	}
]
```
Where `"name"` is the filename (without the extension) of the character's `.txt` and `.ghg` files, `"names"` the names to be shown to the user in each language, `"price"` the price in the shop, and `"folder"` the folder under `"CHARS/"` where the GHG and TXT should be located.
