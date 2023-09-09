import copy
def main():
    b = LoadFromFile("test.txt")
    DebugPrint(b)
    print(BFS(b))
    #print(DFS(b))
    print(bidirectionalsearch(b))

#arguments: file
#returns: 2d tuple of board
def LoadFromFile(filepath):
    board = []
    n = 0
    with open(filepath, 'r') as file:
        count = 0
        for line in file:
            line1 = []
            if count == 0:
                n = file
            else:
                row = line.strip().split("\t")
                for element in row:
                    if element == "*":
                        line1.append("0")
                    else:
                        line1.append(element)
                board.append(tuple(line1))
            count += 1
    return tuple(board)

#arguments: 2d tuple of board
#returns: nothing, prints out board
def DebugPrint(state):
    s = ""
    for element in state:
        for number in element:
            s += number + "    "
        print(s)
        s = ""

#arguments: 2d tuple of board
#returns: 2d tuple of board
def FindHole(state):
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == "0":
                return tuple([i, j])

#arguments: 2d tuple of board, tuple pair of hole location, tuple pair being switched
#returns: 2d tuple of board
def switch(state, hole, switched):
    newState = list(list(row) for row in copy.deepcopy(state))
    hole_row, hole_col = hole
    switch_row, switch_col = switched
    newState[hole_row][hole_col], newState[switch_row][switch_col] = newState[switch_row][switch_col], newState[hole_row][hole_col]
    return tuple(tuple(row) for row in newState)


#arguments: 2d tuple of board
#returns: 2d tuple of resulting neighbor moves, ((int, 1d list))
def ComputeNeighbors(state):
    neighbor = []
    hole = []
    hole = FindHole(state)
    row, col = hole
    if col + 1 <= len(state) -1:
        neighbor.append([state[row][col + 1], switch(state, hole, (row, col + 1))])
    if col - 1 >= 0:
        neighbor.append([state[row][col - 1], switch(state, hole, (row, col - 1))])
    if row + 1 <= len(state) -1:
        neighbor.append([state[row + 1][col], switch(state, hole, (row + 1, col))])
    if row - 1 >= 0:
        neighbor.append([state[row - 1][col], switch(state, hole, (row - 1, col))])
    
    return neighbor

#arguments: 2d tuple of board
#returns: return True/False, is the state the goal state
def IsGoal(state):
    position = 0
    n = len(state)
    for i in range(n):
        for j in range(n):
            if not int(state[i][j]) == position + 1:
                return False
            if i == n-1 and j == n-2:
                return True
            position += 1


#arguments: 2d tuple of board
#returns: 1d array of tile path to reach goal
def BFS(state):
    frontier = [(0, state)]
    discovered = set(state)
    parents = {(0, state): None}
    path = []
    while len(frontier) != 0:
        current_state = frontier.pop(0)
        discovered.add(current_state[1])
        if IsGoal(current_state[1]):
            while parents.get((current_state[0], current_state[1])) != None:
                path.insert(0, current_state[0])
                current_state = parents.get((current_state[0], current_state[1]))
            return path
        for neighbor in ComputeNeighbors(current_state[1]):
            if neighbor[1] not in discovered:
                frontier.append(neighbor)
                discovered.add(neighbor[1])
                parents.update({(neighbor[0], neighbor[1]): current_state})
    print("FAIL")
    return None

#arguments: 2d tuple of board
#returns: 1d array of tile path to reach goal
def DFS(state):
    frontier = [(0, state)]
    discovered = set(state)
    parents = {(0, state): None}
    path = []
    while len(frontier) != 0:
        current_state = frontier.pop(0)
        discovered.add(current_state[1])
        if IsGoal(current_state[1]):
            while parents.get((current_state[0], current_state[1])) != None:
                path.insert(0, current_state[0])
                current_state = parents.get((current_state[0], current_state[1]))
            return path
        for neighbor in ComputeNeighbors(current_state[1]):
            if neighbor[1] not in discovered:
                frontier.insert(0, neighbor)
                discovered.add(neighbor[1])
                parents.update({(neighbor[0], neighbor[1]): current_state})
    print("FAIL")
    return None

#arguments: len of state, int
#returns: 2d tuple of goal board
def findGoal(n):
    Total = n**2
    count = 1
    End_state = []
    for i in range(n):
        row = []
        for j in range(n):
            if count == Total:
                row.append("0")
            else:
                row.append(str(count))
            count+=1
        End_state.append(tuple(row))
    
    return tuple(End_state)

#arguments: 2d tuple of board
#returns: 1d array of tile path to reach goal
def bidirectionalsearch(state):
    goal = findGoal(len(state))
    frontier = [(0, state)]
    frontier2 = [(0, goal)]
    discovered1 = set([state])
    discovered2 = set([goal])
    parents1 = {state: []}
    parents2 = {goal: []}
    path = []
    while len(frontier) != 0 and len(frontier2) != 0:
        currentState1 = frontier.pop(0)
        currentState2 = frontier2.pop(0)
        
        discovered1.add(currentState1[1])
        discovered2.add(currentState2[1])
            
        if len(discovered1.intersection(discovered2)) > 0:
            intersect = list(discovered1.intersection(discovered2))[0]
            forwardPath = parents1[intersect]
            backwardsPath = list(reversed(parents2[intersect]))
            return forwardPath + backwardsPath


        for neighbor in ComputeNeighbors(currentState1[1]):
            if neighbor[1] not in discovered1:
                frontier.append(neighbor)
                discovered1.add(neighbor[1])
                parents1.update({neighbor[1]: parents1[currentState1[1]] + [neighbor[0]]})

        for neighbor in ComputeNeighbors(currentState2[1]):
            if neighbor[1] not in discovered2:
                frontier2.append(neighbor)
                discovered2.add(neighbor[1])
                parents2.update({neighbor[1]: parents2[currentState2[1]] + [neighbor[0]]})

    return None


main()
