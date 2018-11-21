import paramiko
import os

client = paramiko.SSHClient()
#set client to auto add signature
#automatically grab a set of password and username combos
#attempt to login
#if no error, login was a success
#if error it was not a success
#print out a list in the form:
#	IP,User,Password
