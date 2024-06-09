import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))
msg=client_socket.recv(1024).decode()
# Authenticate the client
username = input(msg)
client_socket.send(username.encode())
msg=client_socket.recv(1024).decode()
password = input(msg)
client_socket.send(password.encode())

# Handle banking operations
while True:
    msg = client_socket.recv(1024).decode()
    print(msg)
    choice = input()
    client_socket.send(choice.encode())

    if choice == 'balance':
        balance = client_socket.recv(1024).decode()
        print(balance)
    elif choice == 'deposit':
        msg=client_socket.recv(1024).decode()
        amount = int(input(msg))
        client_socket.send(str(amount).encode())
        response = client_socket.recv(1024).decode()
        print(response)
    elif choice == 'withdraw':
        msg=client_socket.recv(1024).decode()
        amount = int(input(msg))
        client_socket.send(str(amount).encode())
        response = client_socket.recv(1024).decode()
        print(response)
    elif choice == 'exit':
        final_balance = client_socket.recv(1024).decode()
        print(final_balance)
        client_socket.close()
        break
    else:
        print('Invalid choice. Please try again.')