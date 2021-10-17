import pandas as pd
import numpy as np
import seaborn as sns; sns.set_theme()
import matplotlib.pyplot as plt
import os

PATHS = [
   'csv/2018-2019_season_shots_and_goals_events.csv',
   'csv/2019-2020_season_shots_and_goals_events.csv',
   'csv/2020-2021_season_shots_and_goals_events.csv',
]

FIGURES_PATH = 'figures/'

DISTANCE_BINS = list(range(0, 200, 15))

def get_data_df(path):
    return pd.read_csv(path, sep=',')

def q1_visualisation(df):
    df_2018_2019 = df[df.Season == '2018/2019']
    df_grouped_shots = df_2018_2019.groupby(['Secondary Type', 'Type'])
    ids = df_grouped_shots.size().index
    shot_types = list(set([id[0] for id in ids]))
    labels = shot_types
    shots = df_grouped_shots.Game.count().loc[shot_types, 'SHOT'].values
    goals = df_grouped_shots.Game.count().loc[shot_types, 'GOAL'].values
    totals = shots + goals
    labels_sorted = [x for _, x in sorted(zip(totals, labels))]
    shots_sorted = [x for _, x in sorted(zip(totals, shots))]
    goals_sorted = [x for _, x in sorted(zip(totals, goals))]

    ratios = goals * 100 / totals
    labels_sorted_2 = [x for _, x in sorted(zip(ratios, labels))]


    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

    ax1.bar(labels_sorted, shots_sorted, label='Shots')
    ax1.bar(labels_sorted, goals_sorted, bottom=shots_sorted,
        label='Goals')
    ax1.set_xlabel('Shot types')
    ax1.set_ylabel('Number')
    ax1.set_title('Number of shots and goals per shot types over the 2018/2019 season')
    ax1.legend()
    ax1.set_xticklabels(labels_sorted, rotation=45)

    ax2.bar(labels_sorted_2, sorted(ratios))
    ax2.set_xlabel('Shot types')
    ax2.set_ylabel('Ratio goals/ total shots (%)')
    ax2.set_title('Ratio goals over total shots per shot types over the 2018/2019 season')
    ax2.set_xticklabels(labels_sorted_2, rotation=45)
    fig.savefig(os.path.join(FIGURES_PATH, '5-1.png'))

def preprocess_dataset_q2_3(df):
    df_2018_to_2020 = df.dropna()
    df_2018_to_2020['Shooter/Scorer Coordinate'] = list(zip(df_2018_to_2020['Shooter/Scorer X Coordinate'], df_2018_to_2020['Shooter/Scorer Y Coordinate']))
    df_2018_to_2020['Opponent Goal Coordinate'] = list(zip(df_2018_to_2020['Opponent Goal X Coordinate'], df_2018_to_2020['Opponent Goal Y Coordinate']))
    a = np.dstack((df_2018_to_2020['Shooter/Scorer X Coordinate'], df_2018_to_2020['Shooter/Scorer Y Coordinate']))[0]
    b = np.dstack((df_2018_to_2020['Opponent Goal X Coordinate'], df_2018_to_2020['Opponent Goal Y Coordinate']))[0]
    df_2018_to_2020['Shot Distance'] = np.linalg.norm(a-b, axis=1)
    df_2018_to_2020['Shot Distance Binned'] = pd.cut(df_2018_to_2020['Shot Distance'], DISTANCE_BINS)
    return df_2018_to_2020

def q2_visualisation(df):
    def get_values_from_season(season):
        goals_ = df_grouped.loc[season, :, 'GOAL'].values
        totals_ = df_grouped_totals[season].values
        return goals_ * 100 / totals_

    df_grouped = df.groupby(['Season', 'Shot Distance Binned', 'Type']).size()
    df_grouped_totals = df_grouped.groupby(level=[0, 1]).sum()
    seasons = ['2018/2019', '2019/2020', '2020/2021']
    labels = ['{}-{}'.format(bin, bin+15) for bin in DISTANCE_BINS[:6]]

    fig, ax = plt.subplots(figsize=(8, 8))
    for season in seasons:
        ax.plot(labels, get_values_from_season(season)[:len(labels)], label=season)

    ax.set_xlabel('Shots distances bins (ft)')
    ax.set_ylabel('Ratio goals/total shots (%)')
    ax.set_title('Ratio goals over total shots per distance bins over 3 seasons')
    ax.legend()
    ax.set_xticklabels(labels, rotation=45)
    fig.savefig(os.path.join(FIGURES_PATH, '5-2.png'))

def q3_visualisation(df):
    df = df[df.Season == '2018/2019']
    df_grouped = df.groupby(['Secondary Type', 'Shot Distance Binned', 'Type']).size()
    values = df_grouped.values.reshape((7, 13, 2))
    ratios = values[:, :, 0] * 100 / values.sum(axis=2)
    ratios = np.nan_to_num(ratios)
    mask_under_30 = values.sum(axis=2) < 30
    ratios[mask_under_30] = 0
    ratios = ratios[:, :6]
    fig, ax = plt.subplots(figsize=(14,10))
    sns.heatmap(
        ratios,
        xticklabels=['{}-{}'.format(bin, bin+15) for bin in DISTANCE_BINS[:6]],
        yticklabels=[list(df_grouped.index)[i][0] for i in range(0, len(df_grouped.index), 26)],
        annot=True,
        cmap="YlGnBu",
        ax=ax,
        cbar_kws={'label': 'Ratio of goals/total shots (%)'}
    )
    ax.set_ylabel('Type of shot')
    ax.set_xlabel('Shots distances bins (ft)')
    fig.savefig(os.path.join(FIGURES_PATH, '5-3.png'))

if __name__ == "__main__":
    df = pd.concat([get_data_df(path) for path in PATHS])
    df['Season'] = df.Game.astype(str).str[:4] + '/' + (df.Game.astype(str).str[:4].astype(int) + 1).astype(str)

    q1_visualisation(df)

    df_preprocessed = preprocess_dataset_q2_3(df)

    q2_visualisation(df_preprocessed)

    q3_visualisation(df_preprocessed)