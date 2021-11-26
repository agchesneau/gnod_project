from random import randint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import pickle
from sklearn import cluster, datasets
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


cid = input('Please input your Spotify client id : ')
csecret = input('Please input your Spotify secret id : ')
print()


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid,
                                                           client_secret=csecret))


my_songs = pd.read_csv('./my_songs.csv')
top100 = pd.read_csv('./top100.csv')
# unpickling
kmeans = pickle.load(open('kmeans_model', 'rb'))
scaler = pickle.load(open('standardscaler', 'rb'))




i = 'yes'

while (i == 'yes') or (i =='y'):

    input_t = input('Song title :')
    input_a = input('Artist :')
    print()

    input_t = input_t.lower()
    input_a = input_a.lower()
    title = input_t
    if (input_t in top100['title'].values) & (input_a in top100['artist'].values):
        while title == input_t :
            rnb = randint(1, 100)
            title = top100['title'][rnb]
            artist = top100['artist'][rnb]
        print('This song is a hit song ! Here is another one : ', title,' by ',artist)
    else :
        search = sp.search(q=input_t+' '+input_a,limit=1)
        try :
            audiof = sp.audio_features(search['tracks']['items'][0]['uri'])
            audiof = pd.DataFrame.from_dict(audiof).select_dtypes(include = 'number')
            track_prep = scaler.transform(audiof)
            cluster_nb = kmeans.predict(track_prep)[0]
            while title == input_t :
                filtered = my_songs[my_songs['cluster'] == cluster_nb].reset_index()
                rnb = randint(1, len(filtered['title']))
                title = filtered['title'][rnb]
                artist = filtered['artist'][rnb]
            print('Here is a similar song from my saved songs : ', title,' by ',artist)
        except :
            print('This song can not be found in the database.')
    print()
    i = input('Do you want to try again ? Type yes or no : ')
    

