from typing import List


class Period():
    
    num:int = None
    periodType:str = None
    homeTeamRinkSide:str = None
    awayTeamRinkSide:str = None

    def __init__(self, num, period_type, homeTeam_rinkSide, awayTeam_rinkSide):
        self.num = num
        self.periodType = period_type
        self.homeTeamRinkSide = homeTeam_rinkSide
        self.awayTeamRinkSide = awayTeam_rinkSide


class Player():
    
    playerId:int = None
    fullName:str = None
    playerType:str = None

    def __init__(self, player_id, full_name, player_type):
        self.playerId = player_id
        self.fullName = full_name
        self.playerType = player_type


class Event():
    
    eventTypeId:str = None
    secondaryType:str = None
    description:str = None
    periodNumber:int = None
    periodTime:str = None
    periodRemainingTime:str = None
    periodType:str = None
    coordinates:dict = None
    shooterTeam:str = None
    players:list = None
    emptyNet:bool = None

    def __init__(self, eventTypeId, secondary_type, description, period_number, period_time, period_remaining_time,\
        period_type, coordinates, shooter_team, players, empty_net):
        self.eventTypeId = eventTypeId
        self.secondaryType = secondary_type
        self.description = description
        self.periodNumber = period_number
        self.periodTime = period_time
        self.periodRemainingTime = period_remaining_time
        self.periodType = period_type
        self.coordinates = coordinates
        self.shooterTeam = shooter_team
        self.players = players
        self.emptyNet = empty_net


class Team():
    
    name:str = None
    triCode:str = None
    goals:int = None
    shotsOnGoal:int = None
    shootoutScores:int = None
    shootoutAttempts:int = None    
    powerPlay:bool = None

    def __init__(self, name, tri_code, goals, shots_on_goal, shootout_scores, shootout_attempts, power_play):
        self.name = name
        self.triCode = tri_code
        self.goals = goals
        self.shotsOnGoal = shots_on_goal
        self.shootoutScores = shootout_scores
        self.shootoutAttempts = shootout_attempts
        self.powerPlay = power_play


class Game():
    
    seasonYears:str = None
    seasonType:str = None
    venueName:str = None
    startDatetime:str = None
    endDatetime:str = None
    homeTeam:Team = None
    awayTeam:Team = None
    events:List[Event] = None
    periods:dict = None

    def __init__(self, season_years, season_type, venue_name, start_datetime, end_datetime,\
                 home_team, away_team, events, periods):
        self.seasonYears = season_years
        self.seasonType = season_type
        self.venueName = venue_name
        self.startDatetime = start_datetime
        self.endDatetime = end_datetime
        self.homeTeam = home_team
        self.awayTeam = away_team
        self.events = events
        self.periods = periods
