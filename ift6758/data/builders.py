from ift6758.data import Period, Player, Event, Game, Team, get_season_type_label, get_season_years_label, get_dict_from_list


class PeriodBuilder():
    
    def get_period_info(self, periodData):
        num = periodData["num"]
        period_type = periodData["periodType"]
        homeTeam_rinkSide = periodData["home"]["rinkSide"] if 'rinkSide' in periodData["home"] else None
        awayTeam_rinkSide = periodData["away"]["rinkSide"] if 'rinkSide' in periodData["away"] else None

        return (num, period_type, homeTeam_rinkSide, awayTeam_rinkSide)
    

    def build(self, periodData):
        num, period_type, homeTeam_rinkSide, awayTeam_rinkSide = self.get_period_info(periodData)
        return Period(num, period_type, homeTeam_rinkSide, awayTeam_rinkSide)


    def build_list(self, periodsData):
        return [self.build(periodData) for periodData in periodsData]


class PlayerBuilder():
    
    def get_player_info(self, playerData):
        player_type = playerData["playerType"]
        id = playerData["player"]["id"]
        full_name = playerData["player"]["fullName"]

        return (id, player_type, full_name)
    

    def build(self, playerData):
        id, player_type, full_name = self.get_player_info(playerData)
        return Player(id, full_name, player_type)


    def build_list(self, playersData):
        return [self.build(playerData) for playerData in playersData]


class EventBuilder():
    
    def get_event_info(self, current_event):
        resultDict = current_event['result']
        eventTypeId = resultDict['eventTypeId']
        description = resultDict['description']
        secondary_type = resultDict['secondaryType'] if 'secondaryType' in resultDict else None
        empty_net = resultDict['emptyNet'] if 'emptyNet' in resultDict else None

        current_event_details = current_event['about']
        period_number = current_event_details['period']
        period_time = current_event_details['periodTime']
        period_remaining_time = current_event_details['periodTimeRemaining']
        period_type = current_event_details['periodType']
        coordinates = current_event['coordinates']

        shooter_team = current_event["team"]["triCode"] if "team" in current_event else None
        players = PlayerBuilder().build_list(current_event["players"]) if "players" in current_event else None

        return (eventTypeId, secondary_type, description, period_number, period_time, period_remaining_time,\
            period_type, coordinates, shooter_team, players, empty_net)
    

    def build(self, current_event):
        eventTypeId, secondary_type, description, periodNumber, periodTime, periodRemainingTime, periodType,\
            coordinates, shooter_team, players, empty_net = self.get_event_info(current_event)
        return Event(eventTypeId, secondary_type, description, periodNumber, periodTime, periodRemainingTime,\
            periodType, coordinates, shooter_team, players, empty_net)
    

    def build_list(self, eventsData):
        return [self.build(event) for event in eventsData]


class TeamBuilder():
    
    def get_teams_info(self, game_dict):
        game_teams = game_dict['gameData']['teams']

        away_team_info = game_teams['away']
        away_team_name = away_team_info['name']
        away_team_tricode = away_team_info['triCode']

        home_team_info = game_teams['home']
        home_team_name = home_team_info['name']
        home_team_tricode = home_team_info['triCode']

        return (away_team_name, away_team_tricode, home_team_name, home_team_tricode)
    
    def get_teams_goals_info(self, game_dict):
        game_linescore_teams_info = game_dict['liveData']['linescore']['teams']

        game_linescore_home_team_info = game_linescore_teams_info['home']
        home_team_goals = game_linescore_home_team_info['goals']
        home_team_shotsOnGoal = game_linescore_home_team_info['shotsOnGoal']
        home_team_powerPlay = game_linescore_home_team_info['powerPlay']

        game_linescore_away_team_info = game_linescore_teams_info['away']
        away_team_goals = game_linescore_away_team_info['goals']
        away_team_shotsOnGoal = game_linescore_away_team_info['shotsOnGoal']
        away_team_powerPlay = game_linescore_away_team_info['powerPlay']

        return (home_team_goals, home_team_shotsOnGoal, home_team_powerPlay,\
            away_team_goals, away_team_shotsOnGoal, away_team_powerPlay)
    
    def get_teams_shootout_info(self, game_dict):
        game_linescore_shootout_Info = game_dict['liveData']['linescore']['shootoutInfo']

        game_linescore_home_team_shootout = game_linescore_shootout_Info['home']
        home_team_sos = game_linescore_home_team_shootout['scores']
        home_team_soa = game_linescore_home_team_shootout['attempts']

        game_linescore_away_team_shootout = game_linescore_shootout_Info['away']
        away_team_sos = game_linescore_away_team_shootout['scores']
        away_team_soa = game_linescore_away_team_shootout['attempts']

        return (home_team_sos, home_team_soa, away_team_sos, away_team_soa)

    def build(self, game_dict):
        away_team_name, away_team_tricode, home_team_name, home_team_tricode = self.get_teams_info(game_dict)
        home_team_goals, home_team_shotsOnGoal, home_team_powerPlay,\
            away_team_goals, away_team_shotsOnGoal, away_team_powerPlay = self.get_teams_goals_info(game_dict)
        home_team_sos, home_team_soa, away_team_sos, away_team_soa = self.get_teams_shootout_info(game_dict)
        
        homeTeam = Team(home_team_name, home_team_tricode, home_team_goals, home_team_shotsOnGoal,\
                            home_team_sos, home_team_soa, home_team_powerPlay)
        awayTeam = Team(away_team_name, away_team_tricode, away_team_goals, away_team_shotsOnGoal,\
                            away_team_sos, away_team_soa, away_team_powerPlay)
        
        return (homeTeam, awayTeam)


class GameBuilder():
    
    def get_game_info(self, game_dict):
        game_info = game_dict['gameData']

        season_info = game_info['game']
        season_years = get_season_years_label(season_info['season'])
        season_type = get_season_type_label(season_info['type'])
        game_venue_name = game_info['venue']['name']

        game_start_and_end_time = game_info['datetime']
        game_start_datetime = game_start_and_end_time['dateTime']
        game_end_datetime = game_start_and_end_time['endDateTime'] if 'endDateTime' in game_start_and_end_time else None

        return (season_years, season_type, game_venue_name, game_start_datetime, game_end_datetime)
    
    def build(self, game_dict):
        seasonYears, seasonType, venueName, startDatetime, endDatetime = self.get_game_info(game_dict)
        homeTeam, awayTeam = TeamBuilder().build(game_dict)
        gameLiveData = game_dict['liveData']
        events = EventBuilder().build_list(gameLiveData['plays']['allPlays'])
        periods = get_dict_from_list(PeriodBuilder().build_list(gameLiveData["linescore"]["periods"]), 'num')

        return Game(seasonYears, seasonType, venueName, startDatetime, endDatetime, homeTeam, awayTeam, events, periods)