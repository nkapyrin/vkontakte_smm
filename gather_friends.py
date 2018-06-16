#encoding:utf-8

# https://vk.com/dev/methods
import vk, urllib, pickle, time, os, codecs
token = '000'; # Ключ для обращений через Ваше приложение в ВК (не забудьте дать ему нужные полномочия: wall, friends...)
session = vk.Session( access_token=token )
api = vk.API( session )

owner = "1" # ВПИСАТЬ ВЛАДЕЛЬЦА СТРАНИЦЫ
# Получить можно, например, зайдя в "Видео" основного объекта анализа, и проанализировав на адресную строку браузера

# Функция, которая заставляет нас ждать 0,3 секунды с отправки прошлого запроса
prev_request_time = time.time()
def cool_down():
    global prev_request_time
    while time.time() - prev_request_time < 0.34: time.sleep(0.1);
    prev_request_time = time.time();

# Аватары будут находиться в папке [photo]
def save_avatar(user_info):
    photoUrl = info[u"photo_50"]
    filename = os.path.join('photo', photoUrl.rsplit('/', 1)[-1].split('?')[0])
    if not os.path.exists(filename):
        cool_down()
        urllib.urlretrieve(photoUrl, filename)

# Сохранённые списки друзей будут находиться в папке [friends]
def get_friends( user_id ):
    filename = os.path.join(u'friends', u'%s.txt' % user_id)
    if not os.path.exists( filename ):
        cool_down()
        # Для отключённого пользователя невозможно получить список друзей
        try: friends = api.friends.get( user_id=user_id, count=10000, version=3.0 )
        except: friends = []
        with open(filename, 'wb') as f: f.write( ', '.join( str(l) for l in friends ) )
    else:
        with open(filename, 'rb') as f:
            friends = [ l.strip() for l in f.readline().split(',') ]
    return friends

# Сохранённый набор информации по друзям будет находиться в папке [info]
def get_info( user_id ):
    filename = os.path.join(u'info', u'%s.txt' % user_id)
    if not os.path.exists( filename ):
        cool_down()
        info = api.users.get( user_id=user_id, version=3.0, fields='photo_50' )
        with codecs.open(filename, 'wb', encoding="utf-8") as f: f.write( ';'.join( [ "%s|%s" % (k,info[0][k]) for k in info[0].keys() ]) )
    else:
        with codecs.open(filename, 'rb', encoding="utf-8") as f:
            # Делаем словарь из списка пар [поле|значение] инфо о друге
            pairs = [ l.split('|') for l in f.readline().split(';') ]
            info = [dict( pairs )]
    return info[0]

friend_list = get_friends( owner )
info = get_info(owner)
save_avatar(info)

for i,user_id in enumerate( friend_list ):
    print "%d/%d" % (i, len(friend_list))

    get_friends( user_id )
    info = get_info( user_id )
    save_avatar( info )
