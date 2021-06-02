from flask import Flask, render_template, request
import spotify
from spotify import SpotifyRecom

app = Flask(__name__)

#Get your token here: https://developer.spotify.com/console/get-current-user/
#Insert your Spotify token here:
x = SpotifyRecom("BQAF7lP7OHWO9r_IapnI6MjTm4Ga5BM9yk9a19iPtZuvpAEXAcHYJI4ScWpivR6aIYyIRGbUOsqHWZoj40jpBPmTsT_YIuZ9LAntNuCV9YqbADg-PR_WLu686mkRQS0H8IjSeqwZCV2n8rV-OB-pA2HXxKd0dPGMWT6oR6It-g0mK1iV1Ca9pEBL9a6SihzZe9kHfW2S9_Fs_zSzDNghrM66WswiqkmEZJZUK4JopTO3qSfbuN0C8CK5pUI3I1M2x0RlJs3pEVLR5fthHn9_CQ")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        numsong = request.form['num_tracks_to_visualise']
        dispsongs = x.get_last_played_tracks(numsong)
        return render_template('home.html', songs = numsong, display = dispsongs)
    else:
        return render_template('home.html')

@app.route('/recommendation', methods=['GET', 'POST'])
def reco():
    if request.method == 'POST':
        ind = request.form['index']
        dispsongs = x.get_last_played_tracks(ind)
        reco = x.get_track_recommendations(dispsongs)
        return render_template('home.html', index=ind, recom=reco)

if __name__=='__main__':
    app.run(debug=True)
