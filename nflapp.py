import streamlit as st
import pandas as pd 
import numpy as np 
from deta import Deta

deta = Deta(st.secrets["deta_key"])
db = deta.Base("nfl_prop_bets-db-2")

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

    st.title('Super Bowl LVI')

    st.write('Here is how it works:')
    st.write("1.Fill out your predictions  \n2.If you want to be part of the pool - venmo me $5. WINNER TAKES ALL  \n3.Enjoy the Super Bowl!")
    

    
    with st.form("my_form"):
        st.write("Inside the form")
        name = st.text_input("Your name (first and last)")
        coin = st.selectbox('What will the coin toss be?',
        ('Heads', 'Tails'))
        sack = st.selectbox('Who will have the first sack of the game?',
        ('Bengals', 'Rams'))
        anthem = st.selectbox("Will the anthem be over or under 1m 50 sec",('Under','Over'))
        color = color = st.color_picker('What color will the Gatorade bath be?', '#00f900')
        color2 = st.selectbox('Just to be clear - what color did you choose?',('Red','Orange','Blue','Other'))
        score = st.selectbox('What will the first score be?',('Field goal/Safety','Touchdown'))
        team_score = st.selectbox('Who will score first?',('Bengals','Rams'))
        mvp = st.selectbox('Who will be the Super Bowl MVP',('Burrow','Stafford','others'))
        winner = st.selectbox('Who will win the game?',('Bengals','Rams'))
        commercial = st.selectbox('Which commercial will appear first?',('Coke','Budweiser'))
        eminem = st.selectbox('Will Eminem perform Slim Shady?',("Yes","No"))
        field_goal = st.selectbox('Will the longest field goal be over or under 45 yards?',('Over 45','Under 45'))
        tie_breaker = st.slider('Tie Breaker: Total Combined Score',0,100)
        submitted = st.form_submit_button("Save Picks")


        # Every form must have a submit button.
    if submitted:
        db.put({"name": name,"coin": coin,"sack": sack,"anthem": anthem,"color": color,"color2": color2,"score": score,"team_score": team_score,"mvp": mvp,"winner": winner,
        "commercial": commercial,"eminem": eminem, "field_goal": field_goal,"tie_breaker": tie_breaker})


    db_content = db.fetch().items
    df = pd.DataFrame(db_content)
    #st.write(list(df.columns))
    order = [9,1,10,0,3,11,12,8,14,4,5,6,13]
    cols = [df.columns[i] for i in order]
    df = df[cols]
    if st.checkbox('Show prediction by person'):
        st.dataframe(df)

    #coin
    coin_df = df.groupby("coin")['name'].count()
    Heads = coin_df.iloc[0]/df['coin'].count()
    Tails = coin_df.iloc[1]/df['coin'].count()

    #sack
    sack_df = df.groupby("sack")['name'].count()
    Bengals = sack_df.iloc[0]/df['sack'].count()
    Rams = sack_df.iloc[1]/df['sack'].count()

    #anthem
    anthem_df = df.groupby("anthem")['name'].count()
    Over = anthem_df.iloc[0]/df['anthem'].count()
    Under = anthem_df.iloc[1]/df['anthem'].count()

    #color 
    color2_df = df.groupby("color2")['name'].count()
    Blue = color2_df.iloc[0]/df['color2'].count()
    Orange = color2_df.iloc[1]/df['color2'].count()
    Other = color2_df.iloc[2]/df['color2'].count()
    Red = color2_df.iloc[3]/df['color2'].count()

    #score
    score_df = df.groupby("score")['name'].count()
    Field_goal = score_df.iloc[0]/df['score'].count()
    Touchdown = score_df.iloc[1]/df['score'].count()

    #team score
    team_score_df = df.groupby("team_score")['name'].count()
    Bengals2 = team_score_df.iloc[0]/df['team_score'].count()
    Rams2 = team_score_df.iloc[1]/df['team_score'].count()

    #mvp 
    mvp_df = df.groupby("mvp")['name'].count()
    Burrow = mvp_df.iloc[0]/df['mvp'].count()
    Other2 = mvp_df.iloc[1]/df['mvp'].count()
    Stafford = mvp_df.iloc[2]/df['mvp'].count()

    #winner
    winner_df = df.groupby("winner")['name'].count()
    Bengals3 = winner_df.iloc[0]/df['winner'].count()
    Rams3 = winner_df.iloc[1]/df['winner'].count()
    
    #commercial
    commercial_df = df.groupby("commercial")['name'].count()
    Budweiser = commercial_df.iloc[0]/df['commercial'].count()
    Coke = commercial_df.iloc[1]/df['commercial'].count()

    #eminem
    eminem_df = df.groupby("eminem")['name'].count()
    No = eminem_df.iloc[0]/df['eminem'].count()
    Yes = eminem_df.iloc[1]/df['eminem'].count()
    
    #longest yard
    
    field_goal_df = df.groupby("field_goal")['name'].count()
    No = field_goal_df.iloc[0]/df['field_goal'].count()
    Yes = field_goal_df.iloc[1]/df['field_goal'].count()




    #tie breaker
    tie_score = df['tie_breaker'].astype(int).mean()


    

    if st.checkbox('Need some help deciding? See what other people are predicting?'):
        st.header('What will the coin toss be?')

        col1, col2 = st.columns(2)
        
        col1.metric(label='Heads',value=f'{100*Heads:.0f}%')
        col2.metric(label='Tails',value=f'{100*Tails:.0f}%')

        st.subheader('Who will be sacked first?')

        col1, col2 = st.columns(2)
        
        col1.metric(label='Bengals',value=f'{100*Bengals:.0f}%')
        col2.metric(label='Rams',value=f'{100*Rams:.0f}%')


        st.subheader('Will the anthem be over or under 1m 50sec?')

        col1, col2 = st.columns(2)
        
        col1.metric(label='Under 1.50',value=f'{100*Under:.0f}%')
        col2.metric(label='Over',value=f'{100*Over:.0f}%')

        st.subheader('What color will the Gatorade bath be?')

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(label='Red',value=f'{100*Red:.0f}%')
        col2.metric(label='Blue',value=f'{100*Blue:.0f}%')
        col3.metric(label='Orange',value=f'{100*Orange:.0f}%')
        col4.metric(label='Other',value=f'{100*Other:.0f}%')


        st.subheader('Who will score first?')

        col1, col2 = st.columns(2)

        col1.metric(label='Bengals',value=f'{100*Bengals2:.0f}%')
        col2.metric(label='Rams',value=f'{100*Rams2:.0f}%')


        st.subheader('What will the first score be?')

        col1, col2 = st.columns(2)

        col1.metric(label='Field Goal/ Safety',value=f'{100*Field_goal:.0f}%')
        col2.metric(label='Touchdown',value=f'{100*Touchdown:.0f}%')


        st.subheader('Who will be the Super Bowl MVP?')

        col1, col2, col3 = st.columns(3)

        col1.metric(label='Burrow',value=f'{100*Burrow:.0f}%')
        col2.metric(label='Stafford',value=f'{100*Stafford:.0f}%')
        col3.metric(label='Other',value=f'{100*Other2:.0f}%')


        st.subheader('Who will win the game?')

        col1, col2 = st.columns(2)

        col1.metric(label='Bengals',value=f'{100*Bengals3:.0f}%')
        col2.metric(label='Rams',value=f'{100*Rams3:.0f}%')
        
        st.subheader('Which commerical will appear first?')

        col1, col2 = st.columns(2)

        col1.metric(label='Budweiser',value=f'{100*Budweiser:.0f}%')
        col2.metric(label='Coke',value=f'{100*Coke:.0f}%')
        
        st.subheader('Will Eminem perform Slim Shady')
        
        col1, col2 = st.columns(2)

        col1.metric(label='Yes',value=f'{100*Yes:.0f}%')
        col2.metric(label='No',value=f'{100*No:.0f}%')


        st.subheader('TIE BREAKER: What will the total combined score be?')

        st.metric(label='Avg Combined Score', value=f'{tie_score:.0f}')

