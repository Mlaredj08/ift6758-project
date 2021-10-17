from enum import Enum
import os
import numpy as np


seasonTypes = {
    'R': 'Regular season',
    'P': 'Playoffs'
}

seasonCodes = {
    'Regular season': '02',
    'Playoffs': '03'
}

goalsCoordinates = {
    'left' : { 'x' : -85, 'y' : 0},
    'right' : { 'x' : 85, 'y' : 0}
}

class PlayersType(Enum):
    SHOOTER = 'Shooter'
    SCORER = 'Scorer'
    ASSIST = 'Assist'
    GOALIE = 'Goalie'


def get_season_type_label(season_code):
    return seasonTypes[season_code]

def get_season_years_label(season_years):
    return season_years[0:5] + ' - ' + season_years[4:]

def get_shooter_or_scorer_and_goalie(playersList):
    shooterOrScorer = None
    goalie = None

    if playersList is not None:
        for player in playersList:
            if player.playerType in [PlayersType.SHOOTER.value, PlayersType.SCORER.value]:
                shooterOrScorer = player
            elif  player.playerType == PlayersType.GOALIE.value:
                goalie = player

    return shooterOrScorer, goalie

def get_dict_from_list(objectsList, keyField):
    result = {}
    for object in objectsList:
        result[getattr(object, keyField)] = object

    return result

def none_to_na(object, keyField):
    return np.nan if object == None or object == {} or (type(object) == dict and keyField not in object) else get_field_value(object, keyField)

def get_field_value(object, keyField):
    return object[keyField] if type(object) == dict else getattr(object, keyField)

def create_folder_if_not_exists(folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

def get_coordinates_side(rinkSide, eventCoordinates):
    if rinkSide is not None:
        return rinkSide
    elif 'x' in eventCoordinates:
        if eventCoordinates['x'] < 0:
            return 'left'
        else:
            return 'right'

    return None

def get_opponent_goal_coordinates(shooterTeam, homeTeamTriCode, eventCoordinates, eventPeriodNumber, periodsDict):
    if eventPeriodNumber not in periodsDict:
        #SHOOTOUT period
        if 'x' not in eventCoordinates:
            return None
        elif eventCoordinates['x'] < 0:
            return goalsCoordinates['left']
        else:
            return goalsCoordinates['right']

    currentPeriod = periodsDict[eventPeriodNumber]
    rinkSide = None
    if homeTeamTriCode == shooterTeam:
        rinkSide = get_coordinates_side(currentPeriod.awayTeamRinkSide, eventCoordinates)
    else:
        rinkSide = get_coordinates_side(currentPeriod.homeTeamRinkSide, eventCoordinates)
    
    return goalsCoordinates[rinkSide] if rinkSide is not None else None
