import socket
import sys
from thread import *
from getpass import getpass

HOST = '10.0.0.4'
PORT = 7794

users = {
    'user1': {
        'pswd': '1111',
        'conn': None,
        'status': 0,
        'msgs': []
    },
    'user2': {
        'pswd': '2222',
        'conn': None,
        'status': 0,
        'msgs': []       
    },
    'user3': {
        'pswd': '3333',
        'conn': None,
        'status': 0,
        'msgs': []       
    }
    
}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

try:
    s.bind((HOST,PORT))
except socket.error, msg:
    print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

s.listen(10)
print('Socket listening')

connections = []
def clientthread(conn):

    while 1:
        connections.append(conn)

        conn.send('Enter username: ')
        username = conn.recv(1024)
        pswd = conn.recv(1024)

        while username not in users or pswd != users[username]['pswd']:
            conn.send('Incorrect username or password.\nEnter username: ')
            # conn.send('Enter username: ')

            username = conn.recv(1024)
            pswd = conn.recv(1024)

        users[username]['status'] = 1
        conn.send('Successfully logged in. \nYou have ' + str(len(users[username]['msgs'])) + ' unread messages.')
        currUser = username
        # connexns[-1].user = username
        # conns[username] = conn
        users[username]['conn'] = conn
        opt = ''
        # conn.send('Select an option from the menu:\n 1. Change Password\n 2. Logout\n 3. Send a message\n 4. View unread messages\n')
        # opt = conn.recv(1024)
        while opt != "Logging out.":
            conn.send('Select an option from the menu:\n 1. Change Password\n 2. Logout\n 3. Send a message\n 4. View unread messages\n 5. Broadcast message.')
            opt = conn.recv(1024)

            if opt == '1':
                conn.send('Changing password.')
                pswd = conn.recv(1024)

                while pswd != users[username]['pswd']:
                    conn.send('Incorrect password.')
                    pswd = conn.recv(1024)

                conn.send('Enter new password: ')


                #conn.send('1')
                users[username]['pswd'] = conn.recv(1024)
                #users[username]['pswd'] = pswd
                #_users[int(username[:-1])-1].pswd = users[username]
                conn.send('Password changed.')
                    

            elif opt == '2':
                conn.send('Logging out.')
                users[username]['status'] = 0
                opt = conn.recv(1024)
                conn.close()
                break

            elif opt == '3':
                conn.send('Enter the user that you would like to send a message to:')
                user = conn.recv(1024)
                while user not in users:
                    conn.send('The user does not exist. Enter a valid user:')
                    user = conn.recv(1024)
                    #recip = raw_input('Enter the user that you would like to send a message to:')
                #print int(user[-1:])-1
                conn.send('Enter your message: ')
                msg = conn.recv(1024)
                #print msg
                if users[user]['status'] == 0:
                    # u = _users[int(user[-1:])-1]
                    # u.msgs.append(msg)
                    users[user]['msgs'].append(msg)
                    #_users[int(user[-1:])-1].msgs + msg+ "\n"
                    # print _users[0].pswd
                    # print _users[1].pswd
                    # print _users[2].pswd
                else:
                    users[user]['conn'].send('New message: ' + msg)

            elif opt == '4':
                msg = 'Messages:\n'
                # + _users[int(currUser[-1:])-1].msgs
                for m in users[currUser]['msgs']:
                    msg = msg + m + '\n'
                users[currUser]['msgs'] = []
                conn.send(msg)

            elif opt == '5':
                conn.send('Enter your message: ')
                msg = conn.recv(1024)
                #print msg
                for user in users:
                    if users[user]['status'] == 1:
                        users[user]['conn'].send('New message: ' + msg)

            else:
                conn.send('Please enter a valid option:\n')

            # opt = conn.recv(1024)

        break

while(1):
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    # connexns.append(Connect(conn))
    # print conn
    start_new_thread(clientthread ,(conn,))

s.close()
    

