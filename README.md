## Code Encryption Tool
[![GitHub](https://img.shields.io/github/license/oldentomato/Code_encryption)](https://github.com/Oldentomato/Code_Encryption/blob/main/LICENSE)
[![BCH compliance](https://bettercodehub.com/edge/badge/Oldentomato/Code_Encryption?branch=main)](https://bettercodehub.com/)
[![Build Version](https://img.shields.io/github/v/release/oldentomato/Code_Encryption)](https://github.com/Oldentomato/Code_Encryption/releases)
> modules
- python 3.9.6
- pymongo 4.3.3
- rsa 4.9
- Werkzeug 2.2.2  
- pycryptodome 3.16.0

> Introdution  
- I used gitigore or git secret when uploading DB URL or code with personal information on GitHub. But the downside of this is that I always had to carry around key files that weren't uploaded when working elsewhere. This program issues a private key and a public key, which is uploaded to the private database and can be imported from anywhere.

> How to Use
- Sign up for the program. ID is not duplicated.
    - In Database  
    ![DatabaseScreenShot](https://github.com/Oldentomato/Code_Encryption/blob/main/readme_imgs/dbimage.png)
        - Files Array is a list of files in which encryption code was detected in your project.
          
    **At run time, the program must be in the project file.**  
    ~~Need Install OpenSSL~~


- Download your public, private key (private key will upload your DB and write gitignore automally)
- Write this code above the code you want to encrypt.  
 ___#encryption_underline___   
 (Supported File Types: .py .cs .js .ts)  
- Encryption with ProjectName It will detects files marked #encryption_underline.
- When decrypting, press the Descrypion button with the Filename(ProjectName).


