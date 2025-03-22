import random
from teams.helper_function import Troops, Utils

team_name = "Shadow_V1"
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
    
    # If game just started, wait for sometime
    if my_tower.game_timer < 1:
        return
    
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
    "Prince": ["Dragon", "Wizard", "Skeleton", "Minion"],
    "Barbarian": ["Wizard", "Dragon", "Minion", "Prince"],
    "Balloon": ["Archer", "Wizard", "Dragon", "Musketeer", "Minion"],
    "Wizard": ["Giant", "Wizard", "Prince", "Dragon"]
    }
    
    # Getting opponent troop data
    opp_troop_data = {}
    for troop in opp_troops:
        opp_troop_data[troop.name] = troop.position
        
    # Getting my troop data
    my_troop_data = {}
    for troop in my_troops:
        my_troop_data[troop.name] = troop.position
    
    # Checking weakness and deploying
    flag = True # Is true if we have already reacted to opponent's weakness or ignored it
    for troop_name in opp_troop_data.keys():
        if weakness[troop_name][0] == "everything":
            continue
            
        # Not react if we have already dealt with weakness and weakness not wizard!
        if set(my_troop_data.keys()) & set(weakness[troop_name]) and elixr < 4:
            if "Wizard" != troop_name:
                # print(troop_name, "weakness dealt with", set(my_troop_data.keys()) & set(weakness[troop_name]))
                continue
            
        # Check if we can deal with weakness
        for mirror in weakness[troop_name]:
            if mirror in deployable and opp_troop_data[troop_name][1] <= 40:
                deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], max(opp_troop_data[troop_name][1]-10, 0))))
                flag = False
                break
            if mirror in deployable and elixr >= 9.5:
                deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], 0)))
                flag = False
                break
        if not flag:
            break

    # If we have dealt with all weaknesses, we shall go on the offensive
    if flag:
        if "Giant" in my_troop_data.keys():
            if my_troop_data["Giant"][1] > 50:
                deploy_list.list_.append((deployable[0], (my_troop_data["Giant"][0], 49)))
                elixr -= 4
        if elixr >= 9.7 and "Giant" in deployable:
            deploy_list.list_.append(("Giant", (0, 25)))
            elixr -= 5
        if elixr >= 5:
            for deploy in deployable:
                if deploy != "Giant":
                    deploy_list.list_.append((deploy, (0 ,0)))

