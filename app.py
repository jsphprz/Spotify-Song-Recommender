from flask import Flask, render_template, request
import spotify
from spotify import SpotifyRecom

app = Flask(__name__)

#Get your token here: https://developer.spotify.com/console/get-current-user/
#Insert your Spotify token here:
x = SpotifyRecom("TOKEN")

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
