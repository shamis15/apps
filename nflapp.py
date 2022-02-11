import streamlit as st
import pandas as pd 
import numpy as np 
from deta import Deta

deta = Deta(st.secrets["deta_key"])
db = deta.Base("prop_bets-db")

#deta = Deta(st.secrets["deta_key"])
#db = deta.Base("nfl")


add_selectbox = st.sidebar.selectbox(
    "Select League ",
    ("NFL", "NFL Draft","Super Bowl Predictions")
)

if add_selectbox == "NFL":
   

    st.title("NFL Records")



    #read in data
    DATA_URL = ('nfl_scores.csv')

    def load_data():
        data = pd.read_csv(DATA_URL)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        return data

    data = load_data()
    logos = pd.read_csv("https://raw.githubusercontent.com/leesharpe/nfldata/master/data/logos.csv")

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
        'Select Team',list(df_2.team.unique()))

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

    nfl_dict = {"Oakland Raiders":"OAK","Denver Broncos":"DEN","Buffalo Bills":"BUF","New York Jets":"NYJ",
                "Baltimore Colts":"IND","New England Patriots":"NE","Los Angeles Rams":"LA","Kansas City Chiefs":"KC",
                "Chicago Bears":"CHI","New York Giants":"NYG","Minnesota Vikings":"MIN","Philadelphia Eagles":"PHI",
                "Cleveland Browns":"CLE","Miami Dolphins":"MIA","Green Bay Packers":"GB","Houston Oilers":"TEN",
                "Atlanta Falcons":"ATL","Detroit Lions":"DET","Washington Redskins":"WAS","San Francisco 49ers":"SF",
                "St. Louis Cardinals":"ARI","San Diego Chargers":"LAC","Dallas Cowboys":"DAL","Pittsburgh Steelers":"PIT",
                "New Orleans Saints":"NO","Cincinnati Bengals":"CIN","Boston Patriots":"NE","Tampa Bay Buccaneers":"TB",
                "Seattle Seahawks":"SEA","Los Angeles Raiders":"OAK","Indianapolis Colts":"IND","Phoenix Cardinals":"ARI",
                "Arizona Cardinals":"ARI","Carolina Panthers":"CAR","St. Louis Rams":"LA","Jacksonville Jaguars":"JAX",
                "Baltimore Ravens":"BAL","Tennessee Oilers":"TEN","Tennessee Titans":"TEN","Houston Texans":"HOU",
                "Los Angeles Chargers":"LAC","Las Vegas Raiders":"OAK","Washington Football Team":"WAS"}


    year = st.selectbox(
        'Select a Season',list(df_sb.schedule_season.unique()))

    team = list(df_sb.loc[df_sb.schedule_season == year]['team'])[0]
    logo_image = logos.loc[logos.team == nfl_dict[team]]['team_logo'].item()


    st.image(logo_image, caption=team)



elif add_selectbox == "NFL Draft":
    st.title('NFL Draft')

    st.write('Wanting a first round draft spot? Figure out the position with the best chance.')

    draft_df = pd.read_csv('nfl_draft.csv') #read in draft data

    first_round = draft_df.loc[draft_df['round'] == 1] #limit df to season and 1st round

    #get count by position
    positions = first_round.groupby('position')['round'].count().reset_index().rename(columns={'round':'number_players'})
    positions = positions.sort_values(by='number_players', ascending=False)
    positions['pct'] = positions.number_players/positions.number_players.sum() #get percentage of picks
    positions['rank'] = positions.number_players.rank(ascending=False).astype(int)

    #st.metric('label', value, delta=None, delta_color="normal")

    pos = st.selectbox('Select Position',list(positions.position))

    col1, col2 =st.columns(2)

    
    col1.metric(label='Percentage of First Round Pick',value=str(round(100*positions.loc[positions.position == pos]['pct'].item(),2))+'%')
    col2.metric(label='Rank amoung positions',value=positions.loc[positions.position == pos]['rank'].item())


    #graph of all position 1st rounders by years
    seasons = first_round.loc[first_round.position == pos].groupby('year')['position'].count().reset_index().rename(columns={'position':'number_players'})
    seasons = seasons.set_index('year')

    st.bar_chart(seasons['number_players'])

else:

    with st.form("my_form"):
        st.write("Inside the form")
        name = st.text_input("Your name")
        coin = st.selectbox('What will the coin toss be?',
        ('Heads', 'Tails'))
        sack = st.selectbox('Who will have the fist sack of the game?',
        ('Bengals', 'Rams'))
        anthem = st.slider("Will the anthem be over or under 1m 50 sec", 0.00,2.3)
        color = color = st.color_picker('What color will the Gatorade bath be?', '#00f900')
        score = st.selectbox('What will the first score be?',('Field goal/Safety','Touchdown'))
        team_score = st.selectbox('Who will score first?',('Bengals','Rams'))
        mvp = st.selectbox('Who will be the Super Bowl',('Burrow','Stafford','others'))
        winner = st.selectbox('Who will win the game?',('Bengals','Rams'))
        commercial = st.selectbox('Which commercial will appear first?',('Coke','Budweiser'))
        eminem = st.selectbox('Will Eminem perform Silm Shady?',("Yes","No"))
        field_goal = st.slider('Will the longest field goal be over or under 45 yards?', 0,60)
        tie_breaker = st.text_input('Tie Breaker: Total Combined Score')
        submitted = st.form_submit_button("Save Picks")


        # Every form must have a submit button.
    if submitted:
        db.put({"name": name,"coin": coin,"sack": sack,"anthem": anthem,"color": color,"score": score,"team_score": team_score,"mvp": mvp,"winner": winner,
        "commercial": commercial,"eminem": eminem, "field_goal": field_goal,"tie_breaker": tie_breaker})


    db_content = db.fetch().items
    df = pd.DataFrame(db_content)
    #df = df[['name',df.columns]]
    #st.write(list(df.columns))
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.dataframe(df)

    coin_df = df.groupby("coin")['name'].count()
    heads = coin_df.iloc[0]/df['name'].count()
    tails = coin_df.iloc[1]/df['name'].count()

    sack_df = df.groupby("sack")['name'].count()
    bengals = coin_df.iloc[0]/df['name'].count()
    rams = coin_df.iloc[1]/df['name'].count()
    

    st.write(sack_df)

    col1, col2 = st.columns(2)
    
    col1.metric(label='Percentage of Heads',value=heads)
    col2.metric(label='Percentage of Tails',value=tails)




    #st.metric('label', value, delta=None, delta_color="normal")
