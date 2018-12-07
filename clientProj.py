import socket
import sys
import getpass

while 1:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket'
        sys.exit()

    host = '10.0.0.4';
    port = 7794;

    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print 'Hostname could not be resolved'
        sys.exit()


    s.connect((host, port))
    #print 'Socket connected'

    reply = s.recv(1024)
    
    while 'Successfully logged in.' not in reply:
        print reply

        msg = raw_input('')
        s.sendall(msg)

        pswd = getpass.getpass('Password:')
        s.sendall(pswd)
        reply = s.recv(1024)
    
    print reply

    opt = raw_input()
    s.sendall(opt)
    
    while 1:
        reply = s.recv(1024)
        print reply
        #msg = raw_input('Select an option from the menu:\n 1. Change Password\n 2. Logout\n 3. Send a message\n 4. View unread messages\n')
        #s.sendall(msg)
        #reply = s.recv(1024)
        #print reply
        if 'Select' in reply:
            opt = raw_input()
            s.sendall(opt)

        elif 'New message:' in reply:
             s.sendall(reply)
             reply = s.recv(1024)

        elif 'password' in reply:
            msg = getpass.getpass()
            s.sendall(msg)

        # if reply == 'Changing password':
        #     reply = 'Incorrect password.'

        #     while reply == 'Incorrect password.':
        #         msg = getpass.getpass('Incorrect password. Enter old password:')
        #         s.sendall(msg)
        #         reply = s.recv(1024)

        #     msg = getpass.getpass('Enter new password:')
        #     s.sendall(msg)

        #     reply = s.recv(1024)
        #     print reply

        elif reply == 'Logging out.':
            s.sendall(reply)
            s.close() # close connection 
            break

        elif 'Enter' in reply:
            msg = raw_input('')
            s.sendall(msg)

        # if reply == 'Enter the user that you would like to send a message to:':
        #     #print reply 
        #     msg = raw_input('')
        #     s.sendall(msg)
        #     reply = s.recv(1024)
        #     #print reply
        #     while reply != 'Enter your message: ':
        #         msg = raw_input('')
        #         s.sendall(msg)
        #         reply = s.recv(1024)
        #     print reply
        #     msg = raw_input('')
        #     s.sendall(msg)

        #if reply[:9] == 'Messages:':
            #print reply
            #pass

        # msg = raw_input('') # allow user to enter another option from menu
        # s.sendall(msg)



    
