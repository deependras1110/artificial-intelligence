import sys

# constructing the map in a 2D Array
def construct_map(map_file):
    for route in map_file:
        if route.upper() == 'END OF INPUT':
            print route
            break
        else:
            print route
            temp = route.strip().split(" ")
            # print temp
            s = temp[0]
            d = temp[1]
            if s in places:
                pass
            else:
                places.append(s)
            if d in places:
                pass
            else:
                places.append(d)

    places.sort()

    for i in range(len(places)):
        map.append([])
        for j in range(len(places)):
            map[i].append(-1)
        map[i][i] = 0

    for route in map_file:
        if route.upper() == 'END OF INPUT':
            break
        else:
            temp = route.strip().split(" ")
            s = temp[0]
            d = temp[1]
            c = temp[2]
            map[places.index(s)][places.index(d)] = int(c)
            map[places.index(d)][places.index(s)] = int(c)
    return

# To backtrack and print the route
def find_route(result, visited_array):

    path = []

    # Recursive function to backtrack
    def back_track(destination_node, visited_array):
        if destination_node is None: 
            return
        else: 
            for visited_node in visited_array:
                if visited_node["node"] == destination_node:
                    path.append(destination_node)
                    back_track(visited_node["parent"], visited_array) 

    if result:
        print "distance: " + str(result["cummilative_cost"]) + " km"
        print "route:"
        back_track(result["current_node"], visited_array)
        path.reverse()
        for i in range(0, len(path) - 1):
            print places[path[i]] + " to " + places[path[i+1]] + ": " + str(map[path[i]][path[i+1]]) + " km"
    else:
        print "distance: infinity"
        print "route:"
        print "none" 
    return

# adding heuristic values to an array based on index
def map_heuristic_values(heuristic_file):
    for heuristic in heuristic_file:
        if heuristic.upper() == 'END OF INPUT':
            break
        else:
            record = heuristic.split(" ")
            heuristics[places.index(record[0])] = int(record[1])
    return

# Sorting fringe based on uniform cost search as well as A* search
def sort_fringe(fringe, heuristic_flag):
    if(len(fringe) > 1):
        for node_i in range(0, len(fringe) - 1):
            small = node_i
            for node_j in range(node_i+1, len(fringe)):
                s = fringe[small]["cummilative_cost"]
                n = fringe[node_j]["cummilative_cost"]
                if heuristic_flag:
                    s += fringe[small]["heuristic_cost"]
                    n += fringe[node_j]["heuristic_cost"]
                if(s > n):
                    small = node_j
            temp = fringe[small]
            fringe[small] = fringe[node_i]
            fringe[node_i] = temp
        return fringe
    else:
        return fringe

# To check if a node is present in visited array
def check_visited(current_node_index, visited_array):
    for node in visited_array:
        if current_node_index == node["node"]:
            return True
    return False

# Managing uninformed uniform cost search management
def uninf_uniform_cost_search():
    dest = places.index(destination)
    fringe = []
    visited = []
    result = False
    fringe.append({
        "current_node"      : places.index(source),
        "cummilative_cost"  : 0,
        "parent"            : None
    })
    while(len(fringe) > 0):
        if fringe[0]["current_node"] == dest:
            visited.append({
                "node"  : fringe[0]["current_node"],
                "parent": fringe[0]["parent"]
            })
            result = fringe[0]
            break
        elif check_visited(fringe[0]["current_node"], visited):
            del fringe[0]
            continue
        else:
            visited.append({
                "node"  : fringe[0]["current_node"],
                "parent": fringe[0]["parent"]
            })
            for i in range(len(map[fringe[0]["current_node"]])):
                if map[fringe[0]["current_node"]][i] > 0:
                    fringe.append({
                        "current_node"      : i,
                        "cummilative_cost"  : fringe[0]["cummilative_cost"]+map[fringe[0]["current_node"]][i],
                        "parent"            : fringe[0]["current_node"]
                    })
            del fringe[0]
            fringe = sort_fringe(fringe, False)
    find_route(result, visited)
    return

# Managing informed A* search management
def inf_aStar_search():
    dest = places.index(destination)
    fringe = []
    visited = []
    result = False
    fringe.append({
        "current_node"      : places.index(source),
        "cummilative_cost"  : 0,
        "heuristic_cost"    : heuristics[places.index(source)],
        "parent"            : None
    })
    while(len(fringe) > 0):
        if fringe[0]["current_node"] == dest:
            visited.append({
                "node"  : fringe[0]["current_node"],
                "parent": fringe[0]["parent"]
            })
            result = fringe[0]
            break
        elif check_visited(fringe[0]["current_node"], visited):
            del fringe[0]
            continue
        else:
            visited.append({
                "node"  : fringe[0]["current_node"],
                "parent": fringe[0]["parent"]
            })
            for i in range(len(map[fringe[0]["current_node"]])):
                if map[fringe[0]["current_node"]][i] > 0:
                    fringe.append({
                        "current_node"      : i,
                        "cummilative_cost"  : fringe[0]["cummilative_cost"]+map[fringe[0]["current_node"]][i],
                        "heuristic_cost"    : heuristics[i],
                        "parent"            : fringe[0]["current_node"]
                    })
            del fringe[0]
            fringe = sort_fringe(fringe, True)
    find_route(result, visited)
    return

# Initial Start
if len(sys.argv) > 4: 

    # Global Varaibles
    places = []
    map = []

    # Command Line Arguements
    search_technique = sys.argv[1]
    construct_map(open(sys.argv[2], "r").read().split("\n"))
    source           = sys.argv[3]
    destination      = sys.argv[4]
    
    if search_technique.lower() == "uninf":
        uninf_uniform_cost_search()
    elif search_technique.lower() == "inf":
        if len(sys.argv) > 5: 
            heuristics = [0] * len(places)
            heuristic_file = sys.argv[5]
            map_heuristic_values(open(sys.argv[5], "r").read().split("\n"))
            inf_aStar_search()
        else:
            print "Undefined heuristic file"
    else:
        print "Irregular search technique defined"