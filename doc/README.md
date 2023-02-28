## README
Před spuštěním programu je třeba mít nainstalovaný python minimální verze 3.9

### Konfigurace programu:
V ```/config/config.ini``` nastavit ip adresy v sekci ```[IP ADDRESSES]```. 
<br>```ip``` je ip adresa serveru. Zapisuje se ve formátu ```ip=ip_address,port```
<br>``` ip_range``` je rozsah ip adres, které bude program prohledávat. Zapisuje se ```ip_range=mensi_ip-vetsi_ip```
<br>```port_range``` je rozsah portů, které bude program prohledávat. Zapisuje se ```port_range=mensi_port-vetsi_port```
<br><br>Příklad konfigurace:
```
[IP ADDRESSES]
ip=192.168.1.191,8085
ip_range=192.168.1.191-192.168.1.199
port_range=8085-8090
```

### Spuštění programu
<br>Program lze spustit několika způsoby:<br>
a) Spustit program pomocí CMD nebo jiné příkazové řádky. Nejprve je potřeba otevřít příkazovou řádku ve složce ```/src/```.
Poté je potřeba napsat ```python main.py```.
<br><br>Příklad spuštění v aplikaci CMD:
```
C:\Users\Evžen\PycharmProjects\Alfa4\src>python main.py
```
b) Spustit program jako daemon v systému linux. Nejprve je potřeba vytvořit .service soubor pomocí příkazu 
```cat /etc/systemd/system/nazev_souboru.service```. Poté je potřeba soubor otevřít pomocí 
<br>```nano /etc/systemd/system/nazev_souboru.service```. Soubor je třeba nastavit následujícím způsobem:
```
[Unit]
Description=<Popis programu>
After=network.target

[Service]
User=<username>
ExecStart=<cesta k pythonu> <cesta k programu/main.py>
Restart=always

[Install]
WantedBy=multi-user.target
```
Poté je potřeba service restartovat pomocí ```sudo systemctl daemon-reload```. Poté se musí zapnout daemon pomocí <br>
```sudo systemctl start nazev_souboru.service```.

    