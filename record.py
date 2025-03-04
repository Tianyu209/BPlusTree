class Record:
    """Record representing an NBA game with attributes from game.txt."""
    def __init__(self, game_date, team_id_home, pts_home, fg_pct_home, ft_pct_home, fg3_pct_home, ast_home, reb_home, home_team_wins):
        self.game_date = game_date
        self.team_id_home = int(team_id_home)
        self.pts_home = int(pts_home)
        self.FG_PCT_home = float(fg_pct_home)
        self.FT_PCT_home = float(ft_pct_home)
        self.FG3_PCT_home = float(fg3_pct_home)
        self.ast_home = int(ast_home)
        self.reb_home = int(reb_home)
        self.home_team_wins = int(home_team_wins)
    def serialize(self):
        return f"{self.game_date},{self.team_id_home},{self.pts_home},{self.FG_PCT_home},{self.FT_PCT_home},{self.FG3_PCT_home},{self.ast_home},{self.reb_home},{self.home_team_wins}"
    def size(self):
        return len(self.serialize().encode('utf-8'))