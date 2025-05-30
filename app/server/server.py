from socket import * # todo: import only used functions

server_s = socket(AF_INET, SOCK_STREAM)
server_s.bind(('0.0.0.0', 1337))
server_s.listen(5)
print('Waiting For Clients...')
while(1):
    (client_s, client_addr) = server_s.accept()
    print('Connection Established!')
    reply = 'Whats Up?!\r\n'
    client_s.sendall(reply.encode('utf-8'))
    client_s.close()
    print('Connection Closed!')