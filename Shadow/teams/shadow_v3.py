import random
from teams.helper_function import Troops, Utils

team_name = "Shadow_V3"
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
    "Wizard": ["Knight", "Wizard", "Giant", "Prince", "Dragon"]
    }
    
    # List of all close range and far range troops
    close_troops = ["Minion", "Knight", "Skeleton", "Valkyrie", "Prince", "Barbarian"]
    far_troops = ["Archer", "Dragon", "Musketeer", "Wizard"]
    tank_troops = ["Giant", "Balloon"]
    
    # Getting opponent troop data
    opp_troop_data = {}
    for troop in opp_troops:
        opp_troop_data[troop.name] = troop.position
        
    # Getting my troop data
    my_troop_data = {}
    for troop in my_troops:
        my_troop_data[troop.name] = troop.position
    
    # Checking weakness and deploying
    flag = 1 # Is true if we have already reacted to opponent's weakness or ignored it
    for troop_name in opp_troop_data.keys():
        if weakness[troop_name][0] == "everything":
            continue

        # Not react if we have already dealt with weakness and weakness not wizard!
        if set(my_troop_data.keys()) & set(weakness[troop_name]) and elixr < 4:
            if "Wizard" != troop_name:
                continue

        # Check if we can deal with weakness
        for mirror in weakness[troop_name]:
            flag = 3
            if mirror in deployable and opp_troop_data[troop_name][1] <= 25:
                if mirror in tank_troops:
                    deploy_list.list_.append((mirror, (0, 0)))
                elif mirror in close_troops:
                    deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], max(opp_troop_data[troop_name][1], 0))))
                else:
                    deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], max(opp_troop_data[troop_name][1]-5, 0))))
                flag = 0
                break
            if mirror in deployable and elixr >= 9.5 and mirror in far_troops:
                deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], 0)))
                flag = 2
                break
        if flag == 0 or flag == 2: # Stop checking for particular opposing troop if it has been addressed
            break

    # If we have dealt with all weaknesses, we shall go on the offensive
    if flag == 1:
        if my_troop_data:
            x_choice = my_troop_data[list(my_troop_data.keys())[0]][0]
        else:
            x_choice = random.choice((-20, 20))
        if "Wizard" in my_troop_data.keys():
            deploy_list.list_.append(("Wizard", (x_choice, 45)))
        elif "Giant" in my_troop_data.keys():
            deploy_list.list_.append(("Giant", (x_choice, 45)))
        else:
            deploy_list.list_.append((deployable[0], (x_choice, 45)))
        deploy_list.list_.append((deployable[0], (x_choice, 45)))

