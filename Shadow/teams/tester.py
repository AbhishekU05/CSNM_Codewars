import random
from teams.helper_function import Troops, Utils

team_name = "tester"
troops = [
    Troops.minion, Troops.dragon, Troops.valkyrie, Troops.archer,
    Troops.prince, Troops.wizard, Troops.giant, Troops.knight
]
# Total Elixr cost = 3 + 4 + 4 + 3 + 5 + 5 + 5 + 3 = 32
# Average Elixr cost = 4

deploy_list = Troops([])
team_signal = ""

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    my_troops = arena_data["MyTroops"]
    opp_troops = arena_data["OppTroops"]
    if my_tower.game_timer > 50:
        deploy_list.list_.append((my_tower.deployable_troops[0], (0, 0)))
    else:
        deploy_list.list_.append((my_tower.deployable_troops[0], (0, 0)))
    print(deploy_list.list_)
