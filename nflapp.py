import streamlit as st
import pandas as pd 
import numpy as np 

st.title("NFL Records")

#read in data
DATA_URL = ('nfl_scores.csv')

def load_data():
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data = load_data()
#indicator for W/L/T
data['home_win'] = data['score_home'] > data['score_away']
data['away_win'] = data['score_home'] < data['score_away']
data['tie'] = data['score_home'] == data['score_away']
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

#chart of points by season
df_toy = data.copy()

df_toy['total_points'] = df_toy.score_home + df_toy.score_away #get total score column
df_toy = df_toy.loc[df_toy.schedule_season != 2021] #remove current season

df_toy = df_toy.groupby('schedule_season')['total_points'].sum()

st.write("Total Points By Season")
st.bar_chart(df_toy,use_container_width=1100)





#Wins by Season by Team
df_2 = data.copy()
df_2 = df_2.loc[df_2.schedule_playoff == False]
df_2 = df_2.loc[df_2.schedule_season != 2021]

#split home and away dataframes
df_h = df_2[['schedule_season','team_home','score_home','home_win']].copy()
df_a = df_2[['schedule_season','team_away','score_away','away_win']].copy()

#align names and concatenate
df_h = df_h.rename(columns={'home_win':'win','team_home':'team','score_home':'score'})
df_a = df_a.rename(columns={'away_win':'win','team_away':'team','score_away':'score'})

df_2 = pd.concat((df_a, df_h))

df_3 = df_2.groupby(['schedule_season','team'])['win'].sum().reset_index()
df_3 = df_3.astype({'win': 'int'})
df_3 = df_3.pivot_table(index='schedule_season',columns='team',values='win', aggfunc='sum', fill_value=0)

df_2 = df_2.groupby(['schedule_season','team'])['win'].sum().reset_index()
df_2 = df_2.set_index('schedule_season')

options = st.selectbox(
     'Select your team',list(df_2.team.unique()))

st.write(options,' Wins by Season')

df_filter = df_2.loc[df_2.team==options]


st.line_chart(df_filter['win'])








#create a data frame with the season year and superbowl winner
df_sb_a = data.loc[data.schedule_week == 'Superbowl'][['schedule_season','team_away','score_away','away_win']].copy()
df_sb_h = data.loc[data.schedule_week == 'Superbowl'][['schedule_season','team_home','score_home','home_win']].copy()

df_sb_h = df_sb_h.rename(columns={'home_win':'win','team_home':'team','score_home':'score'})
df_sb_a = df_sb_a.rename(columns={'away_win':'win','team_away':'team','score_away':'score'})

df_sb = pd.concat((df_sb_a, df_sb_h))

df_sb = df_sb.loc[df_sb.win == True][['schedule_season','team']]

nfl_dict = {"Oakland Raiders":"OAK.png","Denver Broncos":"DEN.png","Buffalo Bills":"BUF.png","New York Jets":"NYJ.png","Baltimore Colts":"IND.png","New England Patriots":"NE.png","Los Angeles Rams":"LA.png","Kansas City Chiefs":"KC.png","Chicago Bears":"CHI.png","New York Giants":"NYG.png",
            "Minnesota Vikings":"MIN.png","Philadelphia Eagles":"PHI.png","Cleveland Browns":"CLE.png","Miami Dolphins":"MIA.png","Green Bay Packers":"GB.png","Houston Oilers":"TEN.png","Atlanta Falcons":"ATL.png","Detroit Lions":"DET.png",
            "Washington Redskins":"WAS.png","San Francisco 49ers":"SF.png","St. Louis Cardinals":"ARI.png","San Diego Chargers":"LAC.png","Dallas Cowboys":"DAL.png","Pittsburgh Steelers":"PIT.png","New Orleans Saints":"NO.png",
            "Cincinnati Bengals":"CIN.png","Boston Patriots":"NE.png","Tampa Bay Buccaneers":"TB.png","Seattle Seahawks":"SEA.png","Los Angeles Raiders":"OAK.png",
            "Indianapolis Colts":"IND.png",
            "Phoenix Cardinals":"ARI.png",
            "Arizona Cardinals":"ARI.png",
            "Carolina Panthers":"CAR.png",
            "St. Louis Rams":"LA.png",
            "Jacksonville Jaguars":"JAX.png",
            "Baltimore Ravens":"BAL.png",
            "Tennessee Oilers":"TEN.png",
            "Tennessee Titans":"TEN.png",
            "Houston Texans":"HOU.png",
            "Los Angeles Chargers":"LAC.png",
            "Las Vegas Raiders":"OAK.png",
            "Washington Football Team":"WAS.png"}


year = st.selectbox(
     'Select a Season',list(df_sb.schedule_season.unique()))

team = list(df_sb.loc[df_sb.schedule_season == year]['team'])[0]


st.image('NFLteamlogos/'+nfl_dict[team], caption=team)
