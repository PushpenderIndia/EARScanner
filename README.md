<h1 align="center">EARScanner</h1>
<p align="center">
    <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3.8-green.svg">
  </a>
  <a href="https://github.com/PushpenderIndia/EARScanner/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/License-BSD%203-lightgrey.svg">
  </a>
  <a href="https://github.com/PushpenderIndia/EARScanner/releases">
    <img src="https://img.shields.io/badge/Release-1.0-blue.svg">
  </a>
    <a href="https://github.com/PushpenderIndia/EARScanner">
    <img src="https://img.shields.io/badge/Open%20Source-%E2%9D%A4-brightgreen.svg">
  </a>
</p>

<p align="center">
  <img src="https://github.com/PushpenderIndia/technowlogger/blob/master/img/hacker-gif.gif" alt="Hacker GIF" width=200 height=200/>
</p>
             
                        This small python script can do really awesome work.
                        
Execution After Redirect (EAR) / Long Response Redirection Vulnerability Scanner written in python3, Can Scan Single & Multiple URLs, MultiThreaded, Fast & Reliable, Can Fuzz All URLs of target website &amp; then can scan them for EAR

## Disclaimer
<p align="center">
  :computer: This project was created only for good purposes and personal use.
</p>

THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. YOU MAY USE THIS SOFTWARE AT YOUR OWN RISK. THE USE IS COMPLETE RESPONSIBILITY OF THE END-USER. THE DEVELOPERS ASSUME NO LIABILITY AND ARE NOT RESPONSIBLE FOR ANY MISUSE OR DAMAGE CAUSED BY THIS PROGRAM.

## Features
- [x] Works on Windows/Linux
- [x] MultiThreaded [Fast]
- [x] Uses GoBuster for Content Discovery (Fuzzing)
- [x] Can Scan Single URL
- [x] Can Scan Multiple URLs
- [x] Can Save Vulnerable URLs in text format
- [X] Reliable & Easy to Use [Very Less False Positive]  

## Tested On
[![Kali)](https://www.google.com/s2/favicons?domain=https://www.kali.org/)](https://www.kali.org) **Kali Linux**

[![Windows)](https://www.google.com/s2/favicons?domain=https://www.microsoft.com/en-in/windows/)](https://www.microsoft.com/en-in/windows/) **Windows 10**

## Prerequisite
- [x] Python 3.X
- [x] Few External Modules

## How To Use in Linux
```bash
# Navigate to the /opt directory (optional)
$ cd /opt/

# Clone this repository
$ git clone https://github.com/PushpenderIndia/EARScanner.git

# Navigate to EARScanner folder
$ cd EARScanner

# Installing dependencies
$ sudo apt install python3-pip 
$ pip3 install -r requirements.txt

# Installing GoBuster (For More Installation Method, Visit: https://github.com/OJ/gobuster)
# NOTE: GoBuster Tool is Only Required for using --fuzz-scan flag
# PS: You need at least go 1.16.0 to compile gobuster.
$ go install github.com/OJ/gobuster/v3@latest

# Help Menu
$ chmod +x EARScanner.py
$ python3 EARScanner.py --help

# Scanning Single URL
$ python3 EARScanner.py -u https://example.com/admin/dashboard.php

# Scanning Multiple URLs
$ python3 EARScanner.py -uL url_list.txt

# Automatically FUZZ URLs and Scan Them for EAR 
$ python3 EARScanner.py -f https://www.example.com
```

## How To Use in Windows
```bash
# Install dependencies 
$ Install latest python 3.x

# Clone this repository or Download this project
$ git clone https://github.com/PushpenderIndia/EARScanner.git

# Navigate to EARScanner folder
$ cd EARScanner

# Installing dependencies
$ pip install -r requirements.txt

# Help Menu
$ python EARScanner.py --help

# Scanning Single URL
$ python EARScanner.py -u https://example.com/admin/dashboard.php

# Scanning Multiple URLs
$ python EARScanner.py -uL url_list.txt

# Automatically FUZZ URLs and Scan Them for EAR 
$ python EARScanner.py -f https://www.example.com
```

## Available Arguments 

| Short Hand                | Full Hand                         | Description |
| ----------                | ---------                         | ----------- |
| -h                        | --help                            | show this help message and exit                                                                |
| -u URL                    | --url URL                         | Scan Single URL for EAR                                                                        |
| -uL FILE_CONTAINING_URLS  | --url-list FILE_CONTAINING_URLS   | Provide a File Containing URLs [PRO_TIP: Fuzz ALL URLs using tools such as ffuf,gobuster,disbuter,etc & then pass urls_list.txt using this argument] [NOTE: One URL in One Line]. |
| -f FUZZ_AND_SCAN          | --fuzz-scan FUZZ_AND_SCAN         | Provide a domain for scanning [It will Fuzz ALL URLs using GoBuster & Then It will scan them.] |
| -w WORDLIST               | --wordlist WORDLIST               | Provide a wordlist for fuzzing. [Only Use With --fuzz-scan]. default=content_discovery_all.txt |
| -t TIMEOUT                | --timeout TIMEOUT                 | HTTP Request Timeout. default=60                                                               |
| -th THREADNUMBER          | --thread THREADNUMBER             | Parallel HTTP Request Number. default=100                                                      |
| -c CONTENTLENGTH          | --content-length CONTENTLENGTH    | Any Content Length for Confirming EAR Vulnerability. default=200                               | 
| -o OUTPUT                 | --output OUTPUT                   | Output filename [Script will save vulnerable urls by given name]. default=vulnerable.txt       |                    

## Screenshots:

#### Help Menu
![](/img/help.PNG)

#### Single URL Scan
![](/img/single.PNG)

#### Multiple URL Scan
![](/img/multiple.PNG)

#### Auto FUZZ & Scan
![](/img/fuzz_scan.PNG)

## Contribute

* All Contributors are welcome, this repo needs contributors who will improve this tool to make it best.
