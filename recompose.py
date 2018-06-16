#encoding:utf-8
from os import listdir
from os.path import isfile, join
import codecs

owner = "1" # Идентификатор основного лица анализа
all_info = []

# Друзья первого уровня
owner_friends = [ n.strip() for n in open( join("friends","6310468.txt") ).readline().split(',') ]
for txt_id in owner_friends + [owner]:
    # Если у нас есть вся нужная информация о текущем ID, сосчитать количество его друзей и поместить в массив
    if not isfile( join("friends","%s.txt" % txt_id) ): continue
    if not isfile( join("info","%s.txt" % txt_id) ): continue
    #if txt_id == owner: continue; # не ставить основного человека в список
    with codecs.open( join("info", txt_id+".txt") ) as f:
        pairs = [ l.split('|') for l in f.readline().split(';') ]
        info = dict( pairs )
    with codecs.open( join("friends", txt_id+".txt") ) as f:
        friend_list = f.readline().split(',')
        nb_friends = len( friend_list )
    all_info.append( [info['first_name']+' '+info['last_name'], nb_friends] )

# Отсортировать массив и вывести в файл out.csv
sorted_info = sorted( all_info, key = lambda e:(e[1],e[0]), reverse=True)
with open('out.csv', 'wb') as f:
	for info in sorted_info:
	    f.write( info[0] + ';' + str(info[1]) + '\n\r' )

exit()

# Отрисовка графа связей -- без фильтрации несколько минут, а получающийся файл размером 300 Мб
# обрабатывается совсем уж медленно (пробовал yEd, пока не пробовал Gephi)

import networkx as nx
G = nx.DiGraph()
owner_friends_list = [f.replace('.txt','') for f in listdir("friends") if isfile(join("friends", f))]
for owner_friend in owner_friends_list:
    if owner_friend not in owner_friends: continue
    G.add_edge( owner, owner_friend )
    if not isfile( join("friends","%s.txt" % owner_friend) ): continue
    with codecs.open( join("friends", owner_friend + ".txt") ) as f:
        friend_list = f.readline().split(',')
        for friend in friend_list: G.add_edge( owner_friend, friend )
    with codecs.open( join("info", owner_friend + ".txt") ) as f:
        pairs = [ l.split('|') for l in f.readline().split(';') ]
        info = dict( pairs )
    G.nodes[owner_friend]['label'] = info['first_name'] + ' ' + info['last_name']
    G.nodes[owner_friend]['img'] = join( 'photo', info['photo_50'].rsplit('/', 1)[-1].split('?')[0] )
nx.write_graphml( G, 'out.graphml', encoding='utf-8' )
