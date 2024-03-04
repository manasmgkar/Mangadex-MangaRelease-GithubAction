import requests
import os
import smtplib
import configparser
import json
import requests
import logging
import img2pdf

from email.message import EmailMessage
from PIL import Image
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

logging.basicConfig(filename='errors.log', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)
config = configparser.ConfigParser()
config.read('config/config.cfg')
id_items = config.items("manga")
base_url = config["mangadex_api_url"]["base_url"]
languages = config["manga_config"]["languages"]

def fetcher(key, id):
    try:
        with open("records.json", "r") as jsonFile:
            data = json.load(jsonFile)
    except Exception as e:
        logging.error(e)
        os.exit()
    #print(base_url)
    #print(data["mangas"][key]["id"])
    try:
        payload = {"translatedLanguage[]": languages, "order[chapter]" : "desc", "limit": 1}
        r = requests.get(
            f"{base_url}/manga/{id}/feed",
            params=payload,
        )
        #print([chapter["attributes"]["chapter"] for chapter in r.json()["data"]][0])
        if ([chapter["attributes"]["chapter"] for chapter in r.json()["data"]][0]) != data["mangas"][key]["latest"]:
            #print([chapter["attributes"]["chapter"] for chapter in r.json()["data"]])
            latestchapterdata = [chapter for chapter in r.json()["data"]]
            emailstatus = emailnotif(r.json()["data"])
            if emailstatus != True:
                data["mangas"][key]["email"] = "false"
                logging.error("something with email failed")
                #os.exit() commented out for now,enable if you want whole to fail
            else:
                try:
                     with open("records.json", "r") as jsonFile:
                        data = json.load(jsonFile)
                     
                     data["mangas"][key]["email"] = "true"
                     with open("records.json", "w") as jsonFile:
                        json.dump(data, jsonFile)   
                except Exception as e:
                    logging.error(e)
                    os.exit()
            """        
            chapteremailstatus = chapteremail(latestchapterdata)
            if chapteremailstatus != True:
                data["mangas"][key]["chapteremailed"] = "false"
                logging.error("something with email failed")
                # os.exit() commented out for now enale if you dont want new chapter to show up in json aswell
            else:
                try:
                     with open("records.json", "r") as jsonFile:
                        data = json.load(jsonFile)
                     
                     data["mangas"][key]["chapteremailed"] = "true"
                     with open("records.json", "w") as jsonFile:
                        json.dump(data, jsonFile)   
                except Exception as e:
                    logging.error(e)
                    os.exit()
            """
            try:
                with open("records.json", "r") as jsonFile:
                    data = json.load(jsonFile)
                     
                data["mangas"][key]["latest"] = ([chapter["attributes"]["chapter"] for chapter in r.json()["data"]][0])
                with open("records.json", "w") as jsonFile:
                    json.dump(data, jsonFile)   
            except Exception as e:
                logging.error(e)
                os.exit()
        else:
            print("already updated not running") 
            logging.info("already updated not running")      
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        logging.error(errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        logging.error(errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        logging.error(errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        logging.error(err)

def emailnotif(latestchapterdata):
     # get email and password from environment variables
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    EMAIL_RECIPIENT = os.environ.get('EMAIL_RECIPIENT')
    #print(EMAIL_PASSWORD)
    # set up email content
    #([chapter["attributes"]["chapter"] for chapter in r.json()["data"]][0])
    #chap = ([chapter["attributes"]["chapter"] for chapter in latestchapterdata][0])
    #print(str(chap))
    msg = EmailMessage()
    msg['Subject'] =  ([chapter["attributes"]["chapter"] for chapter in latestchapterdata][0]) + " has been released"
    #print(msg['Subject'])
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_RECIPIENT
    msg.set_content(([chapter["attributes"]["chapter"] for chapter in latestchapterdata][0]) + " has been released")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        logging.error(e)
        print(e)
        return False


for key, id in enumerate(id_items):
    fetcher(key ,id[1])

"""
def chapteremail(latestchapterdata):
    try:
        EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
        EMAIL_RECIPIENT = os.environ.get('EMAIL_RECIPIENT')
        id = ([chapter["id"] for chapter in latestchapterdata][0])
        latestchapter = ([chapter["attributes"]["chapter"] for chapter in latestchapterdata][0])
        #print(id)
        r = requests.get(
            f"{base_url}/at-home/server/{id}"
        )
        r_json = r.json()
        #print(r.status_code)
        host = r_json["baseUrl"]
        chapter_hash = r_json["chapter"]["hash"]
        data = r_json["chapter"]["data"]
        folder_path = f"Chapters/{latestchapter}"
        os.makedirs(folder_path, exist_ok=True)
        # fetch pages from mangadex
        for page in data:
            r = requests.get(f"{host}/data/{chapter_hash}/{page}")

            with open(f"{folder_path}/{page}", mode="wb") as f:
                f.write(r.content)
        imgs = []
        for fname in os.listdir(folder_path):
            if not fname.endswith(".png"):
                continue
            path = os.path.join(folder_path, fname)
            if os.path.isdir(path):
                continue
            imgs.append(path)
        publish = sorted(imgs, key=os.path.getmtime)
        with open(latestchapter+".html","a") as file:
            file.write('''<!DOCTYPE html>
                            <html>
                            <head>
                            <meta name="viewport" content="width=device-width, initial-scale=1">
                            <style>
                            img {
                            border: 1px solid #555;
                            display: block;
                            margin-left: auto;
                            margin-right: auto;
                            margin-top: 5px;
                            margin-bottom: 5px;	
                            }
                            </style>
                            </head>
                            <body>''')
            for image in publish:
                file.write('''<div class="card"><img src="'''+image+'''" align="center" style="width:50%; alt=" "/>''')
                file.write('\n')
            file.write('''</body>''')
            file.write('\n')
            file.write('''</html>''')    
        msg = MIMEMultipart()
        msg['Subject'] =  ([chapter["attributes"]["chapter"] for chapter in latestchapterdata][0]) + " has been released find attached chapter"
        #print(msg['Subject'])
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_RECIPIENT
        #email content

        message = """ """<html> here the upper commas for comment out stay for html tags,only other go
        <body>
        Attached is the chapter
        <br><br>
        </body>
        </html>
        msg.attach(MIMEText(message, 'html'))
        publish.append(latestchapter+".html")
        for a_file in publish:
            attachment = open(a_file, 'rb')
            file_name = os.path.basename(a_file)
            part = MIMEBase('application','octet-stream')
            part.set_payload(attachment.read())
            part.add_header('Content-Disposition',
                            'attachment',
                            filename=file_name)
            encoders.encode_base64(part)
            msg.attach(part)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_RECIPIENT, msg.as_string())
        return True
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        logging.error(errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        logging.error(errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        logging.error(errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        logging.error(err)
    except Exception as e:
        logging.error(e)
        return False
""" 
