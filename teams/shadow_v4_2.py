import random
from teams.helper_function import Troops, Utils

team_name = "Shadow_V4_2"
troops = [
    Troops.minion, Troops.dragon, Troops.valkyrie, Troops.archer,
    Troops.prince, Troops.wizard, Troops.skeleton, Troops.barbarian
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
    "Minion": ["Minion", "Archer", "Musketeer", "Wizard"],
    "Knight": ["everything"],
    "Skeleton": ["Skeleton", "Valkyrie", "Dragon", "Wizard"],
    "Dragon": ["Minion", "Dragon", "Wizard", "Archer", "Musketeer"],
    "Valkyrie": ["Minion", "Dragon", "Valkyrie", "Prince", "Wizard"],
    "Musketeer": ["everything"],
    "Giant": ["Minion", "Skeleton", "Barbarian", "Dragon", "Archer", "Musketeer", "Knight", "Valkyrie", "Wizard", "Prince"],
    "Prince": ["Minion", "Skeleton", "Barbarian", "Dragon"], 
    "Barbarian": ["Skeleton", "Barbarian", "Valkyrie", "Minion", "Dragon", "Wizard"],
    "Balloon": ["Minion", "Archer", "Musketeer", "Dragon", "Wizard"],
    "Wizard": ["Knight", "Prince", "Giant", "Wizard"]
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
    offense = True # Is true if we have already reacted to opponent's weakness or ignored it
    for troop_name in opp_troop_data.keys():
        if weakness[troop_name][0] == "everything":
            continue
        
        offense = False # We are on defense as opponent is on offense

        # Not react if we have simultaneously dealt with this weakness and some other weakness using some troop if elixr < 5
        # React if weakness is wizard as wizard is op
        if set(my_troop_data.keys()) & set(weakness[troop_name]) and elixr < 5:
            if "Wizard" != troop_name:
                continue
        
        mirror_deployed = False # Check if we have dealt with weakness

        # Check if we can deal with weakness
        for mirror in weakness[troop_name]:
            if mirror not in deployable:
                continue
            
            mirror_deployed = True
            if opp_troop_data[troop_name][1] <= 45:
                if mirror in close_troops:
                    deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], opp_troop_data[troop_name][1])))
                elif mirror in tank_troops:
                    deploy_list.list_.append((mirror, (0, 0)))
                else:
                    deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], max(opp_troop_data[troop_name][1]-10, 0))))
            else:
                if mirror in far_troops:
                    deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], 0)))
                elif mirror in tank_troops:
                    deploy_list.list_.append((mirror, (opp_troop_data[troop_name][0], 0)))
                else:
                    mirror_deployed = False

    # If we have dealt with all weaknesses, we shall go on the offensive
    if offense:
        if my_troop_data:
            x_choice = my_troop_data[list(my_troop_data.keys())[0]][0]
            y_choice = min(my_troop_data[list(my_troop_data.keys())[0]][1], 45)
        else:
            x_choice = random.choice((-20, 20))
            y_choice = 0
        if "Wizard" in deployable:
            deploy_list.list_.append(("Wizard", (x_choice, y_choice)))
        elif "Prince" in deployable:
            deploy_list.list_.append(("Prince", (x_choice, y_choice)))
        else:
            deploy_list.list_.append((deployable[0], (x_choice, y_choice)))
        deploy_list.list_.append((deployable[0], (x_choice, y_choice)))
