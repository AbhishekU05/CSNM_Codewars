import random
from teams.helper_function import Troops, Utils

team_name = "Abhishek"
troops = [
    Troops.skeleton, Troops.dragon, Troops.valkyrie, Troops.archer,
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
    opp_troops = arena_data["OppTroops"]
    
    elixr = my_tower.total_elixir # Current elixr
    
    deployable = my_tower.deployable_troops # Deployable troops
    
    # List of all troop weakness
    weakness = {
    "Archer": ["everything"],
    "Minion": ["Wizard", "Archer", "Dragon", "Musketeer"],
    "Knight": ["everything"],
    "Skeleton": ["Valkyrie", "Wizard", "Dragon"],
    "Dragon": ["Wizard", "Dragon", "Archer", "Musketeer", "Minion"],
    "Valkyrie": ["Wizard", "Dragon", "Minion", "Prince"],
    "Musketeer": ["everything"],
    "Giant": ["Wizard", "Skeleton", "Barbarian", "Minion", "Prince"],
    "Prince": ["Dragon", "Skeleton", "Minion"],
    "Barbarian": ["Wizard", "Dragon", "Valkyrie", "Minion"],
    "Balloon": ["Archer", "Wizard", "Dragon", "Musketeer", "Minion"],
    "Wizard": ["Wizard", "Prince", "Dragon", "Knight"]
    }
    
    # Getting opponent troop data
    opp_troop_data = {}
    for troop in opp_troops:
        opp_troop_data[troop.name] = troop.position
    
    # Checking weakness and deploying
    flag = True
    for troop_name in opp_troop_data.keys():
        if weakness[troop_name][0] == "everything":
            flag = True
            continue
        for mirror in weakness[troop_name]:
            if mirror in deployable and opp_troop_data[troop_name][1] <= 35:
                deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], 0)))
                flag = False
                break
            if mirror in deployable and elixr >= 9.5:
                deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], 0)))
                flag = False
                break
        if not flag:
            break
    
    if elixr >= 9.5 and flag:
        while elixr >= 4:
            if "Wizard" in deployable:
                deploy_list.list_.append(("Wizard", (0, 0)))
                elixr -= 5
            elif "Giant" in deployable:
                deploy_list.list_.append(("Giant", (0, 0)))
                elixr -= 5
            else:
                deploy_list.list_.append((deployable[0], (0, 0)))
                elixr -= 4
        
        
        
        
        
        
        
