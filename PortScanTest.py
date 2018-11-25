import tkinter as tk
import socket
import sys
import webbrowser
import paramiko
import os
import pexpect
import subprocess



#Port Scanner to be called from program to scan ports
#Ip to scan, begin port, end port, textbox to write results into

def getIPS():
	#subprocess.call([])
	os.system("ip neigh | egrep -o '((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)' > IPs.txt")

getIPS()

def FTPScan(ip,textBox):
	f1 = open('FTPScanResults', 'w+')

	# get the ips, users, and passwords from the file
	usr = [line.rstrip('\n') for line in open('Usernames.txt')]
	pw = [line.rstrip('\n') for line in open('Passwords.txt')]

	#this will need to read in from a file of ip addresses


	# username list 
	for l in usr :
	    name = str(l)

	    # password list 
	    for m in pw :
	        passw = str(m)
	        # Start the process to connect
	        child = pexpect.spawn("ftp " + ip)
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
	            strmatch = str(child.before)
	            if '530' in strmatch:
	            	textBox.insert(tk.END,"Connection Refused" + '\n')
	            	textBox.see("end")
	            	textBox.update_idletasks()
	            elif '230' in strmatch:
	            	textBox.insert(tk.END,"Connected" + '\n')
	            	f1.write(str(child.before) + " IP: " + str(ip) + " Username: " + name + " Password: " + passw + '\n')
	            	textBox.see("end")
	            	textBox.update_idletasks()
	#connection refused. 
	        #elif i == 1:
	         #   print('Connection refused')
	          #  f1.write('Connection refused. IP: ' + str(ip))
	#close connection either way
	child.sendline('bye')
	textBox.insert(tk.END, "Done")
	textBox.see("end")
	textBox.update_idletasks()
	f1.close()

def SSHScan(ip,textBox):
	Passwords = open("Passwords.txt","r")
	Usernames = open("Usernames.txt","r")
	ValidTargets = open("SSHScanResults", "w")
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	passes = Passwords.readlines()
	users = Usernames.readlines()

	for user in users:
		for password in passes:
			try:
				client.connect(ip.rstrip("\n\t"),22,user.rstrip("\n\t"),password.rstrip("\n\t"))
			except(paramiko.BadHostKeyException,paramiko.AuthenticationException, paramiko.SSHException, socket.error):
				textBox.insert(tk.END,"Unable to connect to " + ip.rstrip("\n\t") + " with " + user.rstrip("\n\t") + "," + password.rstrip("\n\t") + '\n')
				textBox.see("end")
				textBox.update_idletasks()
				client.close()
			else:
				client.close()
				textBox.insert(tk.END,"Connected to " + ip.rstrip("\n\t") + " with " + user.rstrip("\n\t") + "," + password.rstrip("\n\t") + '\n')
				ValidTargets.write("Connected to " + ip.rstrip("\n\t") + " with " + user.rstrip("\n\t") + "," + password.rstrip("\n\t") + '\n')
	textBox.insert(tk.END, "Done")
	textBox.see("end")
	textBox.update_idletasks()

def portScanner(IP,begin,end,textBox):
    #clear textbox from previous run
    textBox.delete(1.0, tk.END)
    ValidTargets = open("portScanResults", "w")
    ValidTargets.write("The ip you scanned is: " + str(IP).rstrip("\n\t") + '\n')
    if begin > end:
        textBox.insert(tk.END, "The Port Range you entered is invalid: " + str(begin) + " is greater than " + str(end))
        return
    try:
        for port in range(begin, end):

            #create a socket that usees ipv4, TCP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            #test to see if the connection succeeds
            result = sock.connect_ex((IP, port))
            if result == 0:
                #Print into TextBox if an open port is found
                textBox.insert(tk.END, str(port) +" is open\n")
                ValidTargets.write(str(port) +" is open\n")
                textBox.see("end")
                textBox.update_idletasks()
            sock.close()
        textBox.insert(tk.END, "Done")
        textBox.see("end")
        textBox.update_idletasks()

    #exception if address not found
    except socket.gaierror:
        textBox.insert(tk.END,'Error: Hostname not found')
        textBox.see("end")
        textBox.update_idletasks()
        

    #error if cannot connect for whatever reason
    except socket.error:
       textBox.insert(tk.END,'Error: Could not connect to server')
       textBox.see("end")
       textBox.update_idletasks()

        


#main class that handles the switching of frames
class PortScan(tk.Tk):

    def __init__(self, *args, **kwargs):
        #init TKinter
        tk.Tk.__init__(self, *args, **kwargs)

        #where our stuff lives
        container = tk.Frame(self)

        #where to put the frames
        container.pack(side="top", fill="both", expand=True)

        #configure the base grids
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #all the frames we can use
        self.frames = {}

        #iterate through each page class and add it to the frames
        for F in (StartPage, PageAbout, PageRun, PageSSH, PageFTP):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        #show main page on start
        self.show_frame(StartPage)

    def show_frame(self, cont):

        #based on class define which frame to show
        frame = self.frames[cont]
        frame.tkraise()

#Initial Page
class StartPage(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)

		#create a label and place it top center
		label = tk.Label(self, text="Welcome to my Port Scanner")
		label.place(relx=0.5, rely=0.1, anchor="center")

		#create buttons that will take you to different screens
		buttonAbout = tk.Button(self, text="About",
				                command=lambda: controller.show_frame(PageAbout))
		buttonRun = tk.Button(self, text="Run Port Scan",
				                command=lambda: controller.show_frame(PageRun))
		buttonSSH = tk.Button(self, text="Run SSH Scan",
				                command=lambda: controller.show_frame(PageSSH))
		buttonFTP = tk.Button(self, text="Run FTP Scan",
				                command=lambda: controller.show_frame(PageFTP))

		#align the buttons how you want them
		buttonAbout.place(relx=0.5, rely=0.6, anchor="center")
		buttonRun.place(relx=0.5, rely=0.15, anchor="center")
		buttonSSH.place(relx=0.5,rely=0.3,anchor="center")
		buttonFTP.place(relx=0.5,rely=0.45,anchor="center")




#About Page
class PageAbout(tk.Frame):

	def __init__(self, parent, controller):

        #Simple button and Labels
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="About this Program")
		label.place(relx=0.5, rely=0.1, anchor="center")
		buttonAbout = tk.Button(self, text="Back",
				                command=lambda: controller.show_frame(StartPage))
		buttonAbout.place(relx=0.9, rely=0.9, anchor="center")

		labelName = tk.Label(self, text="Authors: Soeren Orlowski, Justin Spony, Amanda Suydam")
		labelName.place(relx=0.5, rely=0.3, anchor="center")

		labelDate = tk.Label(self, text="Date: 11/24/2018")
		labelDate.place(relx=0.5, rely=0.4, anchor="center")


class PageFTP(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="FTP Page")
		label.grid(column=0, row=0)

		#Two buttons on the page
		buttonBack = tk.Button(self, text="Back",
				                command=lambda: controller.show_frame(StartPage))
		buttonBack.place(relx=0.9, rely=0.9, anchor="center")

		#This button will run the portScanner with the given parameters
		buttonRun = tk.Button(self, text="Run",
				                command=lambda: FTPScan(default.get().rstrip("\n\t"),openPortsText))
		buttonRun.grid(column=1, row=4)

		#Create the variables in which the users input get stored and set defaults where they make sense
		textTarget=tk.StringVar(self,value="127.0.0.1")


		IPs = open("IPs.txt","r")
		ips = IPs.readlines()
		choices=[]
		for ip in ips:
			choices.append(ip)
		default = tk.StringVar(self,value="")
		default.set("None")
		popupMenu = tk.OptionMenu(self,default, *choices)
		popupMenu.grid(column=1,row=1)


		#Set the labels to act as prompts for the entry fields
		labelTarget = tk.Label(self, text="Select the Target IP")
		labelTarget.grid(column=0,row=1)

		#create the text output box
		openPortsText = tk.Text(self, width=50, height=20)
		openPortsText.grid(column=1,columnspan=2,row=5)

class PageSSH(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="SSH Page")
		label.grid(column=0, row=0)

		#Two buttons on the page
		buttonBack = tk.Button(self, text="Back",
				                command=lambda: controller.show_frame(StartPage))
		buttonBack.place(relx=0.9, rely=0.9, anchor="center")

		#This button will run the portScanner with the given parameters
		buttonRun = tk.Button(self, text="Run",
				                command=lambda: SSHScan(default.get().rstrip("\n\t"),openPortsText))
		buttonRun.grid(column=1, row=4)

		#Create the variables in which the users input get stored and set defaults where they make sense
		textTarget=tk.StringVar(self,value="127.0.0.1")


		IPs = open("IPs.txt","r")
		ips = IPs.readlines()
		choices=[]
		for ip in ips:
			choices.append(ip)
		default = tk.StringVar(self,value="")
		default.set("None")
		popupMenu = tk.OptionMenu(self,default, *choices)
		popupMenu.grid(column=1,row=1)


		#Set the labels to act as prompts for the entry fields
		labelTarget = tk.Label(self, text="Select the Target IP")
		labelTarget.grid(column=0,row=1)

		#create the text output box
		openPortsText = tk.Text(self, width=50, height=20)
		openPortsText.grid(column=1,columnspan=2,row=5)

class PageRun(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="Port Scan Page")
		label.grid(column=0, row=0)

		#Two buttons on the page
		buttonBack = tk.Button(self, text="Back",
				                command=lambda: controller.show_frame(StartPage))
		buttonBack.place(relx=0.9, rely=0.9, anchor="center")

		#This button will run the portScanner with the given parameters
		buttonRun = tk.Button(self, text="Run",
				                command=lambda: portScanner(default.get().rstrip("\n\t"),textLow.get(),textHigh.get(),openPortsText))
		buttonRun.grid(column=1, row=4)

		#Create the variables in which the users input get stored and set defaults where they make sense
		textTarget=tk.StringVar(self,value="127.0.0.1")
		textLow = tk.IntVar(self)
		textHigh = tk.IntVar(self, value=65535)

		IPs = open("IPs.txt","r")
		ips = IPs.readlines()
		choices=[]
		for ip in ips:
			choices.append(ip)
		default = tk.StringVar(self,value="")
		default.set("None")
		popupMenu = tk.OptionMenu(self,default, *choices)
		popupMenu.grid(column=1,row=1)


		#set Entry fields and align them to the left of the labels
		#inputTarget = tk.Entry(self, width=50,  textvariable=textTarget)
		#inputTarget.grid(column=1, row=1)

		inputLowPort = tk.Entry(self, width=50,  textvariable=textLow)
		inputLowPort.grid(column=1, row=2)

		inputHighPort = tk.Entry(self, width=50,  textvariable=textHigh)
		inputHighPort.grid(column=1, row=3)

		#Set the labels to act as prompts for the entry fields
		labelTarget = tk.Label(self, text="Select the Target IP")
		labelTarget.grid(column=0,row=1)

		labelLowPort = tk.Label(self, text="Enter the start port")
		labelLowPort.grid(column=0,row=2)

		labelLowPort = tk.Label(self, text="Enter the end port")
		labelLowPort.grid(column=0,row=3)

		#create the text output box
		openPortsText = tk.Text(self, width=50, height=20)
		openPortsText.grid(column=1,columnspan=2,row=5)





app = PortScan()
app.geometry("700x500")
app.title("Pi Port Scanner")
app.mainloop()
