# Ido Aharon 319024600
# Idan Simai 206821258
import socket
import sys


# Function that deals with loging to the chat.
def login(names_dict, messages_dict, data, port, names, sock, addr):
    mylist = data.split()
    names_dict[port] = mylist[1]
    # If the user is already logged in.
    if mylist[1] in names:
        sock.sendto("Illegal request".encode('utf-8'), addr)
        return
    messages_dict[port] = []
    # Append the joining message for everyone expect from the current user.
    for key in messages_dict:
        if key != port:
            messages_dict[key].append(names_dict[port] + " has joined")
    # If no other users.
    if len(names) == 0:
        names.append(names_dict[port])
        sock.sendto("".encode('utf-8'), addr)
        return
    names_rev = names.copy()
    names_rev.reverse()
    names_rev = ', '.join(names_rev)
    sock.sendto(names_rev.encode('utf-8'), addr)
    names.append(names_dict[port])


# Function that deals with sending messages to the chat.
def send_messages_for_all(port, names_dict, names, messages_dict, data, sock, addr):
    # If the user isn't logged in.
    if names_dict[port] not in names:
        sock.sendto("Illegal request".encode('utf-8'), addr)
        return
    get_new_data(messages_dict, names_dict, port, sock, addr, data, names)
    message = data[2:]
    st = names_dict[port] + ": " + message
    # Append the sent message to all the users expect from the current user.
    for key in messages_dict:
        if key != port:
            messages_dict[key].append(st)


# Function that deals with changing the name.
def name_change(messages_dict, names_dict, data, port, names, sock, addr):
    # If the user isn't logged in.
    if names_dict[port] not in names:
        sock.sendto("Illegal request".encode('utf-8'), addr)
        return
    get_new_data(messages_dict, names_dict, port, sock, addr, data, names)
    # Change the name in every data structure involved.
    mylist = data.split()
    message = names_dict[port]
    index = names.index(names_dict[port])
    names_dict[port] = mylist[1]
    names[index] = mylist[1]
    # Append the name changing message to all the users expect from the current user.
    message = message + " changed his name to " + names[index]
    for key in messages_dict:
        if key != port:
            messages_dict[key].append(message)


# Function that deals with leaving the group chat.
def leave_group(names_dict, messages_dict, port, names, data, sock, addr):
    # If the user isn't logged in.
    if names_dict[port] not in names:
        sock.sendto("Illegal request".encode('utf-8'), addr)
        return
    message = names_dict[port]
    # Delete the user from every data structure involved.
    names.remove(names_dict[port])
    del names_dict[port]
    del messages_dict[port]
    message = message + " has left the group"
    # Append the name leaving message to all the users expect from the current user.
    for key in messages_dict:
        messages_dict[key].append(message)


# Function that deals with getting new data the was sent in the group chat.
def get_new_data(messages_dict, names_dict, port, sock, addr, data, names):
    # If the user isn't logged in.
    if names_dict[port] not in names:
        sock.sendto("Illegal request".encode('utf-8'), addr)
        return
    all_messages = ""
    # If no messages are ready to be received.
    if len(messages_dict[port]) == 0:
        sock.sendto("".encode('utf-8'), addr)
        return
    # Create the one long message which is made of concatenation of all the pending messages.
    for message in messages_dict[port]:
        all_messages += message + '\n'
    messages_dict[port] = []
    sock.sendto(all_messages.encode('utf-8'), addr)


# Main function for the program.
def main():
    # Check if the port is valid.
    if not (sys.argv[1]).isnumeric():
        return
    port = int(sys.argv[1])
    if port > 65535 or port < 1:
        return
    names = []
    names_dict = dict()
    messages_dict = dict()
    # Open a new socket for communication.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Allocate the socket s the port.
    s.bind(('', port))
    # Choose the right option due to the client's request.
    while True:
        data_bits, addr = s.recvfrom(1024)
        data = data_bits.decode('utf-8')
        if data[0] == '1' and data[1] == ' ':
            login(names_dict, messages_dict, data, addr[1], names, s, addr)
        elif data[0] == '2' and data[1] == ' ':
            send_messages_for_all(addr[1], names_dict, names, messages_dict, data, s, addr)
        elif data[0] == '3' and data[1] == ' ':
            name_change(messages_dict, names_dict, data, addr[1], names, s, addr)
        elif data[0] == '4' and len(data) == 1:
            leave_group(names_dict, messages_dict, addr[1], names, data, s, addr)
        elif data[0] == '5' and len(data) == 1:
            get_new_data(messages_dict, names_dict, addr[1], s, addr, data, names)
        else:
            s.sendto("Illegal request".encode('utf-8'), addr)


if __name__ == "__main__":
    main()
