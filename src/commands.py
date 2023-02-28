import socket
import configparser
import ipaddress
import logging


def writeinfo(text):
    logging.basicConfig(filename="../log/programlog.log", encoding='utf-8', level=logging.DEBUG)
    logging.info(text)


class TranslateScan:
    def __init__(self):
        self.ip_addresses = None
        self.ports = None

    def load_file(self):
        """
        Metoda, ktera nacte konfiguracni soubor a nastavi ip adresy a porty ze souboru
        :return:
        """
        try:
            config = configparser.ConfigParser()
            config.read("../config/config.ini")
            ip_range = config.get("IP ADDRESSES", "ip_range").split("-")
            port_range = config.get("IP ADDRESSES", "port_range").split("-")
            first_ip, last_ip = int(ipaddress.IPv4Address(ip_range[0])), int(
                ipaddress.IPv4Address(ip_range[len(ip_range) - 1]))
            first_port, last_port = int(port_range[0]), int(port_range[len(port_range) - 1])

            self.ip_addresses = [str(ipaddress.IPv4Address(ip)) for ip in range(first_ip, last_ip + 1)]
            self.ports = [int(port) for port in range(first_port, last_port + 1)]
        except Exception:
            raise Exception("Nelze spravne nacist soubor")

    def scan(self):
        """
        Metoda, ktera prohleda nastavene ip adresy a porty a vrati list platnych ip adres a portu - tedy tech, kteri
        odpovedeli pomoci TRANSLATEPONG
        :return: list tuplu ve formatu (ip_adresa:port)
        """
        valid_addresses = []
        self.load_file()

        for ip in self.ip_addresses:
            for port in self.ports:
                try:
                    s = socket.socket()
                    s.settimeout(0.1)
                    s.connect((ip, int(port)))

                    s.send(bytes('TRANSLATEPING"NemnaC4bPrekladac"', 'utf-8'))
                    data = s.recv(1024)
                    data_string = data.decode("utf-8")

                    if data_string[:13] == "TRANSLATEPONG":
                        writeinfo(data_string)
                        valid_addresses.append((ip, port))

                    s.close()

                except Exception:
                    pass

        return valid_addresses

    def run(self, word):
        """
        Metoda pro spusteni hledani slovicka. Metoda nejdriv projede vlastni seznam slov, pokud se v nem hledane slovo
        nenachazi tak hleda v platnych ip adresach a portech. Metoda se ukonci pokud dostane odpoved ze se slovo
        naslo, nebo kdyz projede cely seznam.
        :param word: hledane slovo - string
        :return: TRANSLATEDSUC nebo TRANSLATEDERR - odviji se od toho zda bylo slovo nalezeno ci ne
        """
        correct_word = TranslateLocl().run(word).decode("utf-8")
        ips = self.scan()

        if len(ips) > 0:
            for ip, port in ips:
                if correct_word[:13] != "TRANSLATEDSUC":
                    s = socket.socket()
                    s.connect((ip, int(port)))
                    s.settimeout(3)

                    s.send(bytes('TRANSLATELOCL"' + word + '"', 'utf-8'))
                    data = s.recv(1024)
                    data_string = data.decode("utf-8")

                    if data_string[:13] == "TRANSLATEDSUC":
                        return bytes(data_string, 'utf-8')
                    writeinfo(data_string)

                    s.close()

            writeinfo(correct_word)

        return bytes(correct_word, 'utf-8')


class TranslatedErr:
    """
    Metoda, ktera vraci TRANSLATEDERR, pokud se slovo nenajde
    """
    def run(self):
        return bytes('TRANSLATEDERR"Slovo neni ve slovniku"', "utf-8")


class TranslatedSuc:
    """
    Metoda, ktera vraci TRANSLATEDSUC, pokud se slovo najde
    """
    def run(self, word):
        return bytes('TRANSLATEDSUC"' + word + '"', "utf-8")


class TranslateLocl:
    def __init__(self):
        self.word_dictionary = {
            "bee": "včela",
            "printer": "tiskárna",
            "desk": "stůl",
            "backpack": "baťoh",
            "apple": "jablko"
        }

    def run(self, key):
        """
        Metoda, ktera hleda slovo v lokalnim slovniku. Vraci TRANSLATEDSUC pokud se slovo najde,
        TRANSLATEDERR pokud ne.
        """
        if key in self.word_dictionary.keys():
            return TranslatedSuc().run(self.word_dictionary[key])
        else:
            return TranslatedErr().run()


class TranslatePing:
    def run(self, parameter=None):
        """
        Metoda, ktera vraci TRANSLATEPONG. Je pouzita v pripade, kdy na vstup prijde TRANSLATEPING
        ne.
        """
        return bytes('TRANSLATEPONG"NemnaC4b"', "utf-8")



