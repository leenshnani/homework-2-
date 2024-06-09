import socket
import threading

# Server-side code
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind(('localhost', 8000))
server_socket.listen(5)

# Dictionary to store account details
accounts = {
    'دلامه': {'balance': 1000, 'password': '2382'},
    'ديانا': {'balance': 2000, 'password': '2461'},
    'لين': {'balance': 3000, 'password': '2971'}
}

def handle_client(conn, addr):
    print(f'New connection from {addr}')

    # Authenticate the client
    try:
        conn.send('Enter your username: '.encode())
        username = conn.recv(1024).decode().strip()
        conn.send('Enter your password: '.encode())
        password = conn.recv(1024).decode().strip()

        if username not in accounts or accounts[username]['password'] != password:
            conn.send('Invalid credentials. Disconnecting...'.encode())
            conn.close()
            return
    except:
        conn.send('Error during authentication. Disconnecting...'.encode())
        conn.close()
        return

    # Perform banking operations
    while True:
        try:
            conn.send('\nEnter your choice (balance/deposit/withdraw/exit): '.encode())
            choice = conn.recv(1024).decode().strip()

            if choice == 'balance':
                conn.send(f'Your balance is: {accounts[username]["balance"]} USD'.encode())
            elif choice == 'deposit':
                conn.send('Enter the amount to deposit: '.encode())
                amount = int(conn.recv(1024).decode().strip())
                accounts[username]['balance'] += amount
                conn.send(f'\nDeposit successful. Your new balance is: {accounts[username]["balance"]} USD'.encode())
            elif choice == 'withdraw':
                conn.send('\nEnter the amount to withdraw: '.encode())
                amount = int(conn.recv(1024).decode().strip())
                if amount > accounts[username]['balance']:
                    conn.send('\nInsufficient funds. Withdrawal failed.'.encode())
                else:
                    accounts[username]['balance'] -= amount
                    conn.send(f'\nWithdrawal successful. Your new balance is: {accounts[username]["balance"]} USD'.encode())
            elif choice == 'exit':
                conn.send(f'\nThank you for using our services. Your final balance is: {accounts[username]["balance"]} USD'.encode())
                conn.close()
                print(f'Client {addr} disconnected')
                return
            else:
                conn.send('Invalid choice. Please try again.'.encode())
        except:
            conn.send('Error during banking operation. Disconnecting...'.encode())
            conn.close()
            print(f'Client {addr} disconnected')
            return

while True:
    conn, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()