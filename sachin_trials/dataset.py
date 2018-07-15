import pandas
import os
import json
with open('player_rating.json', 'r') as f:
    player_rating = json.loads(f.read())


class OptaData:
    def __init__(self, base_path):
        """
        Initialize training/testing data
        """
        self.base_path = base_path
        self.X, self.P, self.Y, goalkeeper, defender, midfielder, forward  = self.load_data()

    def get_csv_files(self):
        for root, folders, files in os.walk(self.base_path):
            for file in files:
                if '.csv' in file:
                    yield(root + '/' + file)


    def load_data(self):
        """
        Load data from file
        Args:
        Returns:
        """

        X = []; Y = []; P = []; positions={}; goalkeeper = []; defender = []; midfielder = []; forward = []
        label_dict = {}
        with open('columns', 'r') as columns_file:
            columns = columns_file.read().splitlines()
        with open('form_columns', 'r') as form_columns_file:
            form_columns = form_columns_file.read().splitlines()

        for csv_file in self.get_csv_files():
            df = pandas.read_csv(csv_file, usecols=columns)
            df = df.fillna(value=0.0)
            replace_outcome = {1.0:1.0, 0.0:-1.0}
            df["outcome"].replace(replace_outcome, inplace=True)

            for game_id in df.game_id.unique():
                df_game = df.loc[df['game_id'] == game_id]

                df_position_team = df_game.loc[df_game['event_type'] == 'Team set up']
                for index, row in df_position_team.iterrows():
                    positions_id = row['player_position'].replace(' ','').split(',')
                    involved = row['involved'].replace(' ','').split(',')
                    for index, position in enumerate(positions_id):
                        if position != 5:
                            positions[float(involved[index])] = position
                df_substitute = df_game.loc[df_game['event_type'] == 'Player on']
                for index, row in df_substitute.iterrows():
                    if row['player_position'] == 'Defender':
                        positions[float(row['player_id'])] = 2
                    elif row['player_position'] == 'Midfielder':
                        positions[float(row['player_id'])] = 3
                    elif row['player_position'] == 'Forward':
                        positions[float(row['player_id'])] = 4


                for player_id in df_game.player_id.unique():
                    if player_id == 0.0:
                        continue
                    df_player = df_game.loc[df_game['player_id'] == player_id]
                    features = []
                    for feature in form_columns:
                        total = (df_player[feature]).sum()
                        if total:
                            success = (df_player[feature]*df_player['outcome']).sum()
                            features.append(success/total)
                        else:
                            features.append(0.0)
                    if str(game_id) in player_rating:
                        if str(player_id) in player_rating[str(game_id)]:
                            arr = [str(game_id), str(player_id)] + features
                            arr.append(player_rating[str(game_id)][str(player_id)])
                            if positions[player_id] == 1 or True:
                                goalkeeper.append(arr)
                            elif positions[player_id] == 2:
                                defender.append(arr)
                            elif positions[player_id] == 3:
                                midfielder.append(arr)
                            elif positions[player_id] == 4:
                                forward.append(arr)

                            X.append(features)
                            P.append(positions[player_id])
                            Y.append(player_rating[str(game_id)][str(player_id)])
                        else:
                            print ("Player missing : ", game_id, player_id)
                    else:
                        print ("Game missing : ", game_id)
            return X, P, Y, goalkeeper, defender, midfielder, forward



od = OptaData('./data/Full Datasets - Opta/MLS/')
print(od.X)
