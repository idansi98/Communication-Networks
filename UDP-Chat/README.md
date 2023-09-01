# Chat - Computer Communication Networks 	:computer: :computer_mouse:
## Part 1

In this part, we will create client and server files in Python using [UDP protocol](https://en.wikipedia.org/wiki/User_Datagram_Protocol).  
We will run them locally on the computer, meaning both the server and the client are on the same computer.  Then, in order to better understand the traffic transferred between the client and the server, we will sniff the transport between the client and the server using [Wireshark](https://en.wikipedia.org/wiki/Wireshark) and check which packets are transferred between them.  
We will save the captured traffic to our computer as .pcapng files.  
  
## Part 2
In this part we would like to implement a simple chat. Our chat will behave similarly to a whatsapp group, where any member of the group can write, and any message someone writes is sent to all members of the group.  
When someone sends a message to the group - the message is sent to the server immediately. However, the server will send the appropriate messages to clients only when they contact the server.  
To do this, we will implement a server and a client in python. Our server opens a socket and listens on a port that will be received as an argument to the program (argument to "main").  
The server can receive 5 types of messages: registration, sending a message, changing name, leaving the group, and receiving new information.

### Illustartion
<p align="center">
  <img 
    width="700"
    src="https://user-images.githubusercontent.com/92651125/222916782-858a84b7-51ae-43c4-921b-7096a7c443f0.png"
  >
</p>
