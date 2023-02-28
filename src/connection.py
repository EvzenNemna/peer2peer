import socket
import threading
import configparser
import commands


class Connection:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("../config/config.ini")
        ip_addresses = config.get("IP ADDRESSES", "ip").split(",")

        self.server_address = (ip_addresses[0], int(ip_addresses[1]))
        self.server_socket = socket.socket()

        self.server_socket.bind(self.server_address)
        self.commands = {}
        self.is_conn_open = True
        self.server_socket.listen()

    def multi_user(self):
        """
        Metoda, ktera dovoluje pripojeni vice klientu najednou.
        """
        connection = None
        try:
            while self.is_conn_open:
                connection, client_inet_address = self.server_socket.accept()

                thread = threading.Thread(target=self.user_connection, args=(connection, ))
                thread.start()

        except Exception:
            connection.close()
            commands.writeinfo("Client connection closed")

            self.server_socket.close()
            commands.writeinfo("Server is closed")

            raise Exception()

    def user_connection(self, connection):
        """
        Metoda pro pripojeni klienta a zpracovani jeho prikazu.
        :param connection: connection uzivatele
        """
        try:
            while self.is_conn_open:
                data = connection.recv(1024)
                data_string = data.decode("utf-8")

                command = data_string[:13]
                parameter = data_string[13:].replace('"', '')

                translate_ping = commands.TranslatePing()
                translate_locl = commands.TranslateLocl()
                translate_scan = commands.TranslateScan()

                self.commands = {
                    'TRANSLATEPING': translate_ping,
                    'TRANSLATELOCL': translate_locl,
                    'TRANSLATESCAN': translate_scan
                }

                if command in self.commands.keys():
                    newline = bytes("\r\n", "utf-8")
                    connection.send(self.commands[command].run(parameter) + newline)
                    commands.writeinfo(self.commands[command].run(parameter).decode('utf-8'))

        except Exception:
            connection.close()
            commands.writeinfo("Client connection closed")

            self.server_socket.close()
            commands.writeinfo("Server is closed")

            raise Exception()
