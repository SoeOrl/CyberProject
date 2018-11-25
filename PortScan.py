import socket
import threading
import datetime

IPs = open("IPs.txt","r")
ips = IPs.readlines()
ValidTargets = open("ValidPorts", "w")

def scan_ports_tcp(ip,i,out):
	answer=""
	try:
		print(ip.rstrip("\n\t") + '\n')
		answer = ip.rstrip("\n\t")+':'

		for port in range(0, 500):
			print("TCP " + ip.rstrip("\n\t") + ': '+ str(port))
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(0.5)
			#create a socket that usees ipv4, TCP socket
			

			#test to see if the connection succeeds
			result = sock.connect_ex((ip.rstrip("\n\t"), port))
			if result == 0:
				answer += (str(port) + ',')
				#print("The answer is: " + answer)
			sock.close()

	#exception if address not found
	except socket.gaierror:
		print('Error: Hostname not found')


	#error if cannot connect for whatever reason
	except socket.error:
		print('Error: Could not connect to server')
	#print("The answer is: " + answer)
	answer = answer.rstrip(',')
	out.insert(i,answer)

def scan_ports_udp(ip,i,out):
	answer=""
	try:
		print(ip.rstrip("\n\t") + '\n')
		answer = ip.rstrip("\n\t")

		
		for port in range(0, 2000):
			print("UDP: " + str(port) + str(i))
			#create a socket that usees ipv4, TCP socket

			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			#test to see if the connection succeeds
			result = sock.connect_ex((ip.rstrip("\n\t"), port))
			if result == 0:
				answer += (',' + str(port))
			sock.close()
				#print("The answer is: " + answer)

	#exception if address not found
	except socket.gaierror:
		print('Error: Hostname not found')


	#error if cannot connect for whatever reason
	except socket.error:
		print('Error: Could not connect to server')

	#print("The answer is: " + answer)
	out.insert(i,answer)

i = 0
threads = []
udp = []
tcp = []
starttime = datetime.datetime.now()
for target in ips:
	t = threading.Thread(target = scan_ports_tcp, args=(target.rstrip("\n\t"),i,tcp))
	i = i + 1
	#u = threading.Thread(target = scan_ports_udp, args=(target.rstrip("\n\t"),i,udp))
	threads.append(t)
	#threads.append(u)
	#i = i + 1

for j in range (i):
	threads[j].start()

for j in range (i):
	threads[j].join()

endtime = datetime.datetime.now()
total = endtime - starttime

for j in tcp:
	print(j)

print("Scanning Complete in: ", total)
