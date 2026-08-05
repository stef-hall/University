from collections import deque

def heuristic(mine, opp, empty, B):
    rules = [ (0,-1),(-1,0),(-1,1),(1,0),(0,1),(1,-1)]

    queue = deque()
    distance = {}

    for x in range(B):
        start = (x,0)
        if start in mine:
            distance[start] = 0
            queue.appendleft(start)
        elif start in empty:
            distance[start] = 1
            queue.append(start)

    while queue:
        current = queue.popleft()

        if current[1] == B-1: # This is the win condition
            return distance[current]

        for diff in rules:
            neighbour = (current[0] + diff[0], current[1] + diff[1])

            if neighbour in mine:
                cost = 0
            elif neighbour in empty:
                cost = 1
            else:
                continue

            total_distance = distance[current] + cost
            if (neighbour not in distance) or (total_distance < distance[neighbour]):
                distance[neighbour] = total_distance
                if cost == 0:
                     queue.appendleft(neighbour)
                else:
                     queue.append(neighbour)

    return (B * B)
