from ift6758.data import GameBuilder
import json
import numpy as np
import os
import requests
import tqdm


def createGameID(year, gameTypes):
    """Returns an array of all game IDs defined by the season years and gameTypes.

    IMPORTANT: This function is currently only implemented to deal with 02
    and 03 game IDs, future implementations might deal with other gameTypes.

    Args:
        year: See nhl_data.
        gameTypes: See nhl_data.
    """
    ids = np.array([])
    for y in year:
        for g in gameTypes:
            ids = np.append(ids, createGameNum(y, g))
    return ids


def createGameNum(year, type):
    """Helper function to distribute the logic for game ID creation as a function
    of the game type. Regular season games have a different id format to playoff
    games.

    Args:
        year: See nhl_data.
        type: See nhl_data.
    """
    createNum = {
        # '01': lambda year: preseasonID(year),  # Not implemented yet
        '02': lambda year: regularID(year),
        '03': lambda year: playoffID(year),
        # '04': lambda year: allstarID(year),  # Not implemented yet
    }
    return createNum[type](year)


def regularID(year):
    """Returns an array of game IDs for regular season games for the given year.

    Args:
        year: See nhl_data.
    """
    ids = np.array([])
    if year > 2016:
        num = 1271
    else:
        num = 1230
    for i in range(1, num + 1):
        ids = np.append(ids, str(year) + '02' + str(i).zfill(4))
    return ids


def playoffID(year):
    """Returns an array of game IDs for playoff games for the given year. The
    playoff IDs follow these rules:

    - First digit is always 0.
    - Second digit is a value between 1 and 4 (4 rounds).
    - Third digit is a value dependent on the second digit, it is the number of
    matchups per round (8/2^(i-1)).
    - Fourth digit is the game number between 1 and 7, we do not know if 7 is reached.

    IMPORTANT: The playoff format specified here is has only been verified for
    seasons from the years > 2012. It might produce the correct game IDs for
    older games but it has not been verified.

    Args:
        year: See nhl_data.
    """
    ids = np.array([])
    for i in range(1, 5):
        for j in range(1, 8 // 2**(i - 1) + 1):
            for k in range(1, 8):  # This is the only part where there can be false IDs
                ids = np.append(ids, str(year) + '03' + '0' + str(i) + str(j) + str(k))
    return ids


def getData(IDs, path, light=False):
    """Returns a dictionnary of the play-by-play data in the folder specified
    by path associated to the game IDs specified by IDs. The IDs can be modified
    at will to have custom loading of the data.

    IMPORTANT: This function assumes a linear single level database. i.e. it
    assumes all play-by-play files are stored in a single directory specified by
    path. All play-by-play files should be specified by their unique game ID.

    Args:
        IDs: List of game IDs that specify which data files to download (and load if
        light=False).
        path: See nhl_data.
        light: See nhl_data.
    """
    url = "https://statsapi.web.nhl.com/api/v1/game/ID/feed/live"
    out = dict()
    for i in tqdm.tqdm(IDs):
        d = fetch_data(i, path, url, light)
        if d != 0:
            out[i] = d
    if light:
        return list(out.keys())  # Only care about the IDs
    else:
        return out


def fetch_data(ID, path, url, light):
    """Returns the data associated to ID if the game associated to ID exists
    and contains events.

    Args:
        ID: GameID for which we want to check if it exists and if it was played.
        path: See nhl_data.
        url: URL of the NHL API play-by-play data.
    """
    dat_path = path + '/' + str(ID) + '.json'
    if os.path.isfile(dat_path) and not light:
        with open(dat_path, 'r') as f:
            return json.load(f)
    elif os.path.isfile(dat_path) and light:
        return ID
    else:
        d = requests.get(url.replace('ID', ID))
        if d.status_code == 200:  # Might want to change this to < 400 but I don't know what a 300 status means physically
            data = d.json()
            g = GameBuilder()
            game = g.build(data)
            if len(game.events) > 0:  # Always store game data if the game was played
                with open(dat_path, 'w') as f:
                    json.dump(data, f)
                if light:
                    return ID
                else:
                    return data
        else:
            return 0  # 0 means game does not exist or was not played


def nhl_data(year, gametypes, path, light=False):
    """Acquires the play-by-play data specified by year and gametypes. If light
    if True only the game IDs are returned by the function. If light is False a
    dictionnary of the game data is returned. Irrespective of light's value, this
    function downloads the game data of PLAYED games from the NHL play-by-play API
    into the database specified by path.

    Args:
        year: Iterable object of int containing all years for which to
        create the game IDs. Specifying the year 2017 will create game IDs
        for the 2017-2018 season.
        gameTypes: Iterable object of strings containing all game types for
        which to create game IDs. Valid gameTypes are: 02 -> regular season
        and 03 -> playoffs.
        path: Specifies the location of the game database.
        light: Boolean value specifying if a list of valid IDs is returned or if
        a dictionnary of game data is returned.
    """
    ids = createGameID(year, gametypes)
    out = getData(ids, path, light)
    return out
