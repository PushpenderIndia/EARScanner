import requests
requests.packages.urllib3.disable_warnings()
import concurrent.futures

from colorama import init
from colorama import Fore, Back, Style
init()
import argparse
import pyfiglet
import sys 
import os 
import platform

class EAR_Scanner:
    def __init__(self):
        self.vulnerable_urls      = []
        self.progress             = []
        self.errors               = []

    def get_arguments(self):
        banner = pyfiglet.figlet_format("            EAR Scanner")
        print(banner+"\n")
        parser = argparse.ArgumentParser(description=f'{Fore.RED}EAR Scanner v1.0 {Fore.YELLOW}[Author: {Fore.GREEN}Pushpender Singh{Fore.YELLOW}] [{Fore.GREEN}https://github.com/PushpenderIndia{Fore.YELLOW}]')
        parser._optionals.title = f"{Fore.GREEN}Optional Arguments{Fore.YELLOW}"
        parser.add_argument("-u", "--url", dest="url", help=f"{Fore.GREEN}Scan Single URL for EAR{Fore.YELLOW}")
        parser.add_argument("-uL", "--url-list", dest="file_containing_urls", help=f"{Fore.GREEN}Provide a File Containing URLs {Fore.YELLOW}[PRO_TIP: {Fore.GREEN}Fuzz ALL URLs using tools such as ffuf,gobuster,disbuter,etc & then pass urls_list.txt using this argument{Fore.YELLOW}] [NOTE: {Fore.RED}One URL in One Line{Fore.YELLOW}].")    
        parser.add_argument("-f", "--fuzz-scan", dest="fuzz_and_scan", help=f"{Fore.GREEN}Provide a domain for scanning [It will Fuzz ALL URLs using GoBuster & Then It will scan them.] {Fore.YELLOW}") 
        parser.add_argument("-w", "--wordlist", dest="wordlist", help=f"{Fore.GREEN}Provide a wordlist for fuzzing. {Fore.YELLOW}[Only Use With {Fore.GREEN}--fuzz-scan{Fore.YELLOW}]. {Fore.WHITE}default=content_discovery_all.txt{Fore.YELLOW}", default='content_discovery_all.txt') 
        parser.add_argument("-t", "--timeout", dest="timeout", help=f"{Fore.GREEN}HTTP Request Timeout. {Fore.WHITE}default=60{Fore.YELLOW}", default=60)
        parser.add_argument("-th", "--thread", dest="ThreadNumber", help=f"{Fore.GREEN}Parallel HTTP Request Number. {Fore.WHITE}default=100{Fore.YELLOW}", default=100)
        parser.add_argument("-c", "--content-length", dest="ContentLength", help=f"{Fore.GREEN}Any Content Length for Confirming EAR Vulnerability. {Fore.WHITE}default=200{Fore.YELLOW}", default=200)
        parser.add_argument("-o", "--output", dest="output", help=f"{Fore.GREEN}Output filename [Script will save vulnerable urls by given name]. {Fore.WHITE}default=vulnerable.txt{Fore.YELLOW}", default='vulnerable.txt')

        return parser.parse_args()

    def start(self):
        self.arguments = self.get_arguments()
        print(f"{Fore.YELLOW}           [Author: {Fore.GREEN}Pushpender Singh{Fore.YELLOW}] [{Fore.GREEN}https://github.com/PushpenderIndia{Fore.YELLOW}]\n\n{Style.RESET_ALL}")
        self.ThreadNumber         = int(self.arguments.ThreadNumber)
        self.timeout              = int(self.arguments.timeout)
        self.content_length       = int(self.arguments.ContentLength)

        if self.arguments.url:
            self.check_ear(self.arguments.url)
        elif self.arguments.file_containing_urls:
            self.file_containing_urls = self.arguments.file_containing_urls
            print("="*85)
            print(f'{Fore.YELLOW}[*] Initiating {Fore.GREEN}Exection After Redirect{Fore.YELLOW} (EAR) Vulnerability Scanner ...{Style.RESET_ALL}')
            print("="*85)
            final_url_list = []

            with open(self.file_containing_urls) as f:
                data_list = f.readlines()
            
            for url in data_list:
                if url != '\n':
                    final_url_list.append(url.strip())

            self.total = len(final_url_list)  # Used in showing progressbar 

            # Multi-Threaded Implementation
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.ThreadNumber)
            futures = [executor.submit(self.check_ear, url) for url in final_url_list]
            concurrent.futures.wait(futures)    
        elif self.arguments.fuzz_and_scan:

            print("="*85)
            print(f'{Fore.YELLOW}[*] Fuzzing URLs using {Fore.GREEN}GoBuster{Fore.YELLOW} Tool ...{Style.RESET_ALL}')
            print("="*85)
            url = self.arguments.fuzz_and_scan
            if platform.system() == 'Windows':
                command = f'gobuster.exe dir -w {self.arguments.wordlist} -t {self.timeout} -x php,asp,aspx,jsp -u {url} -o urls_list.txt -q -e'
            else:
                command = f"gobuster dir -w {self.arguments.wordlist} -t {self.timeout} -x php,asp,aspx,jsp -u {url} -o urls_list.txt -q -e"

            try:
                os.system(command)
            except KeyboardInterrupt:
                pass 
            print("="*85)
            print(f'{Fore.YELLOW}[*] Initiating {Fore.GREEN}Exection After Redirect{Fore.YELLOW} (EAR) Vulnerability Scanner ...{Style.RESET_ALL}')
            print("="*85)      
            final_url_list = []

            with open('urls_list.txt') as f:
                data_list = f.readlines()
            
            for url in data_list:
                if url != '\n':
                    final_url_list.append(url.split(' ')[0].strip())

            self.total = len(final_url_list)  # Used in showing progressbar 

            # Multi-Threaded Implementation
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.ThreadNumber)
            futures = [executor.submit(self.check_ear, potential_url) for potential_url in final_url_list]
            concurrent.futures.wait(futures)          
        else:
            print(f"{Fore.RED}[!] Please Provide either {Fore.YELLOW}File Containing list{Fore.RED} or {Fore.YELLOW}Single URL{Fore.RED}, {Fore.GREEN}type {sys.argv[0]} --help for more.{Style.RESET_ALL}")
            sys.exit()

        # Saving Result
        if self.arguments.output:
            output_filename = self.arguments.output
            if not output_filename.endswith('txt'):
                output_filename = output_filename.split('.')[0] + ".txt"
            if len(self.vulnerable_urls) != 0:
                with open(output_filename, 'w') as f:
                    for vuln_url in self.vulnerable_urls:
                        f.write(vuln_url+"\n") 
                print()
                print("="*85)
                print(f'{Fore.GREEN}[+] Vulnerable URLs: {Fore.YELLOW}{self.arguments.output}{Style.RESET_ALL}')
                print("="*85)       

    def check_ear(self, url):
        try:
            response = requests.get(url, timeout=60, verify=False, allow_redirects=False)
            # Step-1: Checking Whether Status Code is 302
            status_code = response.status_code
            if status_code == 302:
                # Step-2: Checking Whether 'Location' Header is Present
                if 'Location' in response.headers.keys():
                    response_length = len(response.text)
                    if response_length >= self.content_length:
                        if self.arguments.url:
                            print(f'{Fore.GREEN}[+] [302] {Fore.WHITE}{url} {Fore.YELLOW}[Location: {Fore.GREEN}{response.headers["Location"]}{Fore.WHITE}] {Fore.YELLOW}[Status: {Fore.GREEN}100% Vulnerable{Fore.YELLOW}]{Style.RESET_ALL}') 
                        self.vulnerable_urls.append(url)
                    else:
                        if self.arguments.url:
                            print(f'{Fore.GREEN}[+] [302] {Fore.WHITE}{url} {Fore.YELLOW}[Location: {Fore.GREEN}{response.headers["Location"]}{Fore.WHITE}] {Fore.YELLOW}[Status: {Fore.GREEN}Might Be Vulnerable{Fore.YELLOW}]{Style.RESET_ALL}')                    
                        self.vulnerable_urls.append(url)
            else:
                if self.arguments.url:
                    print(f'{Fore.YELLOW}[-] [{status_code}] {Fore.WHITE}{url}{Fore.YELLOW} ... not vulnerable!{Style.RESET_ALL}  ')
        
            if self.arguments.file_containing_urls or self.arguments.fuzz_and_scan:
                self.progress.append(1)
                print(f'\r{Fore.YELLOW}[*] ProgressBar: {Fore.WHITE}{len(self.progress)}/{self.total} {Fore.YELLOW}[Errors: {Fore.RED}{len(self.errors)}{Fore.YELLOW}] [Vulnerable: {Fore.GREEN}{len(self.vulnerable_urls)}{Fore.YELLOW}] ... {Style.RESET_ALL}', end="")
        except Exception as e:
            if self.arguments.url:
                print(f'{Fore.RED}[!] {Fore.YELLOW}[ERROR] : {e} {Fore.YELLOW}[{Fore.GREEN}{url}{Fore.YELLOW}]{Style.RESET_ALL}')
            
            elif self.arguments.file_containing_urls or self.arguments.fuzz_and_scan:
                self.errors.append(1)
                self.progress.append(1)
                print(f'\r{Fore.YELLOW}[*] ProgressBar: {Fore.WHITE}{len(self.progress)}/{self.total} {Fore.YELLOW}[Errors: {Fore.RED}{len(self.errors)}{Fore.YELLOW}] [Vulnerable: {Fore.GREEN}{len(self.vulnerable_urls)}{Fore.YELLOW}] ... {Style.RESET_ALL}', end="")

if __name__ == '__main__':
    test = EAR_Scanner()
    test.start()
        
