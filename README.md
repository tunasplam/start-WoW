# start-WoW
My script that I used to start and configure my private CMangos WoW Server on Debian.

## Description

My early childhood consisted of Ultima Online and World of Warcraft. When I was older I wanted to rediscover that childhood so I found CMaNGOS (https://cmangos.net/). I used this script to start and configure my private CMaNGOS servers.

Since I played the game solo but still wanted to experience end game content, I added a startup feature that optimized the settings in the server config file based on which gamemode I wanted to play on. There are seperate settings for:
- solo play
- 5 - man instances
- 10 - man instances
- 20 - man instances
- 40 - man instances

### Setup

This assumes you have mangos installed and configured. it also requires a `Wow.exe` client. I have only used this for the classic and tbc mangos servers but I am sure it works for the second expansion as well.

These env vars need to be set:

```
    SERVER_BIN_PATH # path to mangos/run/bin with mangosd and realmd startup scripts 
    WOW_EXE_PATH # path to directory where Wow.exe is found.
```

### Usage

`python start_wow.py -h`

```
usage: start_wow.py [-h] -m MODE

Mode to set up server with.

options:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  Specify the mode ('solo', '5-man', '10-man', '20-man', '40-man')
```

Once run, the script will wait 2 minutes before starting the WoW client in order to give your server time to boot. You may need to wait longer after the client starts, especially if you have the playerbot plugins installed. You can check in a separate terminal to ensure that both realm processes started.

```
ps aux | grep mangosd
ps aux | grep realmd
```
