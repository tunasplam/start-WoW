# start-WoW
My script that I used to start and configure my private CMangos WoW Server of Linux

However, I don't play it anymore and don't even have WoW installed on my machine anymore. As such, this has not been run or tested for a year or so.

## Description

My early childhood consisted of Ultima Online and World of Warcraft.
When I was older I wanted to rediscover that childhood so I found CMaNGOS (https://cmangos.net/).
I used this script to start and configure my private Burning Crusade CMaNGOS server.

Since I played the game solo but still wanted to experience end game content, I added a startup feature that optimized the settings in the server config file based on which gamemode I wanted to play on. There are seperate settings for:
- solo play
- 5 - man instances
- 10 - man instances
- 20 - man instances
- 40 - man instances

You can use this if you want to but I really just have this here to prove to people that I can code (somewhat).

### Installing

A lot needs to be changed if this wants to run. Honestly, unless you want to fiddle with the program a bit, this is only meant to run on my machine. There are several reasons for this:
  - there was a weird bug with mysqld package at the time so in order to start the realm server I had to temporaryily degrade a package with pacman and then reupgrade it. Because of this, the program requires sudo priveledges AND assumes you use and arch based distro. Honestly, I am sure this issue was fixed though so I bet that code could be removed.

  - I hardcoded the terminal that I used rather than use some sort of system variable for default terminal

  - It is littered with hardcoded filepaths that are specific to my machine and how I installed wine, the CMangos servers, and WoW.

  - I also never figured out how to gracefully shut down the servers. Oh well. I was able to play the game without problems at that point so I let it be.

In conclusion, I basically wrote this ASAP so I could play WoW.

### Who to Blame for this Mess?
Jordan Porter
