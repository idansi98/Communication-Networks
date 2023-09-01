# Ido Aharon 319024600
# Idan Simai 206821258
import socket
import sys
import os


# This function deals with handling the client.
def client_handler(client_sock, message):
    line = message.partition("\r\n")[0]
    file_path = line.split(" ")[1]
    file_path = "files" + file_path
    # Checking whether the path is redirect.
    if file_path == "files/redirect":
        client_sock.send("HTTP/1.1 301 Moved Permanently\r\nConnection: close\r\n"
                         "Location: /result.html\r\n\r\n".encode())
        return True
    # Checking whether this path actually exists.
    if os.path.exists(file_path):
        for current_line in message.split("\r\n"):
            if "Connection:" in current_line:
                connection_str = current_line.split(" ")[1]
                # keep-alive or closed
                if connection_str == "keep-alive":
                    connection = False
                elif connection_str == "closed":
                    connection = True
                break
        # Checking if this is the "/" path, and then concatenate the index.html string so the client will receive it.
        if file_path[-1:] == "/":
            file_path = file_path + "index.html"
        size = os.stat(file_path).st_size
        message_to_client = f"HTTP/1.1 200 OK\r\nConnection: {connection_str}\r\nContent-Length: {size}\r\n\r\n"
        file = open(file_path, "rb")
        data = file.read()
        file.close()
    else:
        client_sock.send("HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n".encode())
        return True
    client_sock.send(message_to_client.encode() + data)
    return connection


def main():
    # Creating the tcp socket.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if not (sys.argv[1]).isnumeric():
        return
    server.bind(('', int(sys.argv[1])))
    server.listen(5)
    # While loop that runs forever to get clients.
    while True:
        client_sock, client_addr = server.accept()
        connection = True
        while True and connection:
            client_sock.settimeout(1)
            # If there's no answer in 1 second, close the socket with client.
            try:
                data = client_sock.recv(1024).decode()
                if len(data) == 0:
                    client_sock.close()
                    break
                message = (data.partition("\r\n\r\n"))[0]
                print(message)
                print()
                # Use the client_handler function to determine about closing the socket or not.
                if client_handler(client_sock, message):
                    connection = False
                    client_sock.close()
            except socket.timeout:
                client_sock.close()
                break


if __name__ == '__main__':
    main()
