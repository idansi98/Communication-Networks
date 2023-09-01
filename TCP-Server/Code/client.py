# Ido Aharon 319024600
# Idan Simai 206821258

import socket
import sys


# Main function for the program.
def main():
    # Check if the port is valid.
    if not (sys.argv[2]).isnumeric():
        return
    ip = sys.argv[1]
    server_port = int(sys.argv[2])
    if server_port > 65535 or server_port < 1:
        return
    # Open a new socket for communication.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Loop for the client to send his request to the server.
    while True:
        x = input()
        if x == 4:
            break
        s.sendto(x.encode(), (ip, server_port))
        data, addr = s.recvfrom(1024)
        new_data = data.decode('utf-8')
        if len(new_data) == 0:
            continue
        new_data = new_data.split('\n')
        # Print the data from the server.
        for str1 in new_data:
            if len(str1) != 0:
                print(str1)
    s.close()


if __name__ == "__main__":
    main()
