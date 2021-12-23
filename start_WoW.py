# start_WoW.py

'''
	Does as advertised.. starts World of Warcraft.
	Also starts out with a commandline interface asking for set up.
	For example, solo play, 5-man, 10-man, 20-man, 40-man raid.
	So will interact with mangos.conf also.

	TODO graceful exit.
	need to echo '.server shutdown 0' to the terminal running mangosd.
	then close realmd
	then stop mysqld service

	How to graceully exit: 
	https://stackoverflow.com/questions/50802812/open-terminal-run-command-return-to-same-terminal-later-and-execute-another-co

'''

import os
import subprocess
import threading
import re
import fcntl
import termios
import sys
import time
from PyInquirer import Token, prompt

kill_threads = False

def main():
	# prompt on how we should set this up.
	gamemode = ask_for_setup()

	# set up the mangosd config file... make sure we have a backup though.
	configure_mangosd(gamemode)

	# first, lets get the actual server up and running with commands.
	init_server()


def ask_for_setup():
	playstyle_question = [
		{
			'type': 'list',
			'name': 'gamemode',
			'message': 'How should I setup mangosd config file?',
			'choices': ['solo', '5-man', '10-man', '20-man', '40-man']
		}
	]
	answer = prompt(playstyle_question)
	return answer['gamemode']

def configure_mangosd(gamemode):
	file_path = '/home/jordan/WoW/mangos-tbc/WoW/run/etc/mangosd.conf'
	config_file = ''
	# TODO error handling here?
	with open(file_path, 'r') as file:
		config_file = file.read().split('\n')

	re_normal = r'Rate\.Creature\.Normal.*?'
	re_normal_stat = r'(?<=Normal\.).*?(?= )'
	re_elite = r'Rate\.Creature\.Elite\..Elite\.*?(?= )'
	re_elite_stat = r'(?<=Elite\.Elite\.).*?(?= )'
	re_world_boss = r'Rate\.Creature\.Elite\.WORLDBOSS\.*?'
	re_world_boss_stat = r'(?<=WORLDBOSS\.).*?(?= )'

	# okie dokie artichokie
	if gamemode == 'solo':
		# all normal values at 1, elite values at .2, world boss values at 1
		# noraml.
		# TODO why the index? Figure out how to actually dynamically change the line.
		i = 0
		for line in config_file:
			if re.match(re_normal, line):
				# extract whether its damage, spelldamage, or hp
				stat = re.findall(re_normal_stat, line)[0]
				line = "Rate.Creature.Normal.{} = {}".format(stat, 1)
				config_file[i] = line

			elif re.match(re_elite, line):
				stat = re.findall(re_elite_stat, line)[0]
				line = "Rate.Creature.Elite.Elite.{} = {}".format(stat, .2)
				config_file[i] = line

			elif re.match(re_world_boss, line):
				stat = re.findall(re_world_boss_stat, line)[0]
				line = "Rate.Creature.Elite.WORLDBOSS.{} = {}".format(stat, 1)
				config_file[i] = line

			i += 1

	elif gamemode == '5-man':
		# all normal values at .2, all elite values at .2
		i = 0
		for line in config_file:
			if re.match(re_normal, line):
				# extract whether its damage, spelldamage, or hp
				stat = re.findall(re_normal_stat, line)[0]
				line = "Rate.Creature.Normal.{} = {}".format(stat, .25)
				config_file[i] = line

			elif re.match(re_elite, line):
				stat = re.findall(re_elite_stat, line)[0]
				line = "Rate.Creature.Elite.Elite.{} = {}".format(stat, .25)
				config_file[i] = line

			i += 1

	elif gamemode == '10-man':
		# all normal values at .1, all elite values at .125, world boss values at .12
		i = 0
		for line in config_file:
			if re.match(re_normal, line):
					# extract whether its damage, spelldamage, or hp
					stat = re.findall(re_normal_stat, line)[0]
					line = "Rate.Creature.Normal.{} = {}".format(stat, .1)
					config_file[i] = line

			elif re.match(re_elite, line):
				stat = re.findall(re_elite_stat, line)[0]
				line = "Rate.Creature.Elite.Elite.{} = {}".format(stat, .125)
				config_file[i] = line

			elif re.match(re_world_boss, line):
				stat = re.findall(re_world_boss_stat, line)[0]
				line = "Rate.Creature.Elite.WORLDBOSS.{} = {}".format(stat, .12)
				config_file[i] = line

			i += 1

	elif gamemode == '20-man':
		# normal at .05, elite at .05, world boss at .05
		i = 0
		for line in config_file:
			if re.match(re_normal, line):
					# extract whether its damage, spelldamage, or hp
					stat = re.findall(re_normal_stat, line)[0]
					line = "Rate.Creature.Normal.{} = {}".format(stat, .04)
					config_file[i] = line

			elif re.match(re_elite, line):
				stat = re.findall(re_elite_stat, line)[0]
				line = "Rate.Creature.Elite.Elite.{} = {}".format(stat, .04)
				config_file[i] = line

			elif re.match(re_world_boss, line):
				stat = re.findall(re_world_boss_stat, line)[0]
				line = "Rate.Creature.Elite.WORLDBOSS.{} = {}".format(stat, .04)
				config_file[i] = line
					
			i += 1

	elif gamemode == '40-man':
		# the three usual suspects at .025
		i = 0
		for line in config_file:
			if re.match(re_normal, line):
					# extract whether its damage, spelldamage, or hp
					stat = re.findall(re_normal_stat, line)[0]
					line = "Rate.Creature.Normal.{} = {}".format(stat, .025)
					config_file[i] = line

			elif re.match(re_elite, line):
				stat = re.findall(re_elite_stat, line)[0]
				line = "Rate.Creature.Elite.Elite.{} = {}".format(stat, .025)
				config_file[i] = line

			elif re.match(re_world_boss, line):
				stat = re.findall(re_world_boss_stat, line)[0]
				line = "Rate.Creature.Elite.WORLDBOSS.{} = {}".format(stat, .025)
				config_file[i] = line
					
			i += 1

	# write it bro.
	with open(file_path, 'w') as file:
		file.write('\n'.join(config_file))

def start_mysqld():

	#check to see if mysqld is running
	check_server_status = "systemctl show mysqld"
	process = subprocess.Popen(check_server_status.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()

	# if it is not started, then start it up.
	if "Server is operational" not in str(output):
		# soo... for now mysqld uses an old version of icu.. but everything else on the
		# computer uses the new version. Temporarily install the old icu package,
		# then re update the package after the mysqld server is started.
		old_icu_install_cmd = "sudo pacman -U /var/cache/pacman/pkg/icu-65.1-2-x86_64.pkg.tar.xz"
		process = subprocess.Popen(old_icu_install_cmd.split(), stdout=subprocess.PIPE)
		output, error = process.communicate()

		# TODO requires unlock. Maybe run python as sudo?
		start_command = "systemctl start mysqld"
		process = subprocess.Popen(start_command.split(), stdout=subprocess.PIPE)

		# reupdate icu
		reup_icu_cmd = "sudo pacman -S icu"
		process = subprocess.Popen(reup_icu_cmd.split(), stdout=subprocess.PIPE)
		output, error = process.communicate()

		time.sleep(1)

	print("mysqld service up and running.")

def init_server():

	start_mysqld()

	realmd_thread = threading.Thread(target=init_realmd)
	realmd_thread.start()

	mangosd_thread = threading.Thread(target=init_mangosd)
	mangosd_thread.start()

	# get the pid for the terminal session running mangosd so that we can
	# use it later for shutdown.
	# see shutdown docs to figure out what this all means.
	# piping unix commands with python is tricky. See:
	# https://stackoverflow.com/questions/13332268/how-to-use-subprocess-command-with-pipes
	# TODO not used yet bc havent figured out shutdown_mangosd() method yet.
	ps = subprocess.Popen(('ps', '-A'), stdout=subprocess.PIPE)
	output = subprocess.check_output(('grep', 'bash'), stdin=ps.stdout)
	ps.wait()
	
	# last process listed has info we want. pid is in index where index % 4 = 1.
	# so itll be in -3
	output = output.split()
	mangosd_pid = re.findall(r'[0-9]+', str(output[-3]))
	print(mangosd_pid)


	#wow_thread = threading.Thread(target=start_wow)
	#wow_thread.start()
	start_wow()

	# send server shutdown command to mangosd.
	# for now just end the thread.
	#sys.exit()

	# HEHE TODO
	# using global var is hacky to say the least.
	kill_threads = True

	# turn off mysqld service.
	mysqld_shutdown_cmd = "systemctl stop mysqld"
	process = subprocess.Popen(mysqld_shutdown_cmd.split(), stdout=subprocess.PIPE)	

	print("All over.")

def init_realmd():
	mangos_root = "/home/jordan/WoW/mangos-tbc/WoW/run"
	realmd_cmd = ['konsole', '--noclose', '-e',
		'{}/bin/realmd -c {}/etc/realmd.conf'.format(
		mangos_root, mangos_root)]

	process = subprocess.Popen(realmd_cmd, stdout=subprocess.PIPE)
	output, error = process.communicate()
	# TODO check exit status. Like maybe for some reason mysqld is not running?
	print("Started realmd.")

	# TODO does not work.
	if kill_threads:
		return


def init_mangosd():
	mangos_root = "/home/jordan/WoW/mangos-tbc/WoW/run"
	mangosd_cmd = ['konsole', '--noclose', '-e',
		'{}/bin/mangosd -c {}/etc/mangosd.conf -a {}/etc/playerbot.conf'.format(
		mangos_root, mangos_root, mangos_root)]

	process = subprocess.Popen(mangosd_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	output, error = process.communicate()

	if kill_threads:
		return


def start_wow():
	# omitting --noclose on this command will mean that quitting WoW client
	# will trigger the graceful shutdown on the servers.
	wow_cmd = ['konsole', '-e',
	'wine', '/home/jordan/.wine/drive_c/TBC-2.4.3.8606-enGB-Repack/Wow.exe',
	'-openglv']
	process = subprocess.Popen(wow_cmd, stdout=subprocess.PIPE)
	output, error = process.communicate()	


''' TODO figure out '''
def shutdown_mangosd(mangosd_pid):
	'''
	# okay, need to figure out what pid for terminal session running mangosd is.
	# then open(/dev/pts/{PID NUM}m 'w') as fd and use that fd to use
	# fcntl.ioctl to wrtie commands to that terminal.
	'''

	with open("/dev/pts/{}".format(mangosd_pid), 'w') as fd:
		# do we need to put a newline at the end of this command?
		for c in ".server shutdown 0\n":
			fcntl.ioctl(fd, termios.TIOCSTI, c)

	print("Shutdown mangosd (i think..)")

main()
