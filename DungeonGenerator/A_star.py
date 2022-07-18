from DungeonGenerator.APriorityQueue import APriorityQueue
import numpy as np

def getDistToRoom(x,y,room):
    if room.x <= x <= room.x + room.width:
        return min(abs(room.y - y),abs(y - (room.y+room.length)))
    if room.y <= y <= room.y + room.length:
        return min(abs(room.x - x),abs(x - (room.x+room.width)))
    if x <= room.x:
        return min( np.linalg.norm([x-room.x, y-room.y]),
                    np.linalg.norm([x-room.x, (y-(room.y+ room.length))]))
    if x >= room.x+room.width:
        return min( np.linalg.norm([x-(room.x+room.width), y-room.y]),
                    np.linalg.norm([x-(room.x+room.width), y-(room.y+ room.length)]))
def initFrontier(grid, r_start):
    front = []
    if r_start.x > 0:
        for i in range(r_start.length):
            front.append((r_start.x-1,r_start.y+i))
    if r_start.x + r_start.width < len(grid)-1:
        for i in range(r_start.length):
            front.append((r_start.x+r_start.width,r_start.y+i))
    if r_start.y > 0:
        for i in range(r_start.width):
            front.append((r_start.x+i,r_start.y-1))
    if r_start.y + r_start.length < len(grid)-1:
        for i in range(r_start.width):
            front.append((r_start.x+i,r_start.y+r_start.length))
    return front
    
def a_star(grid, r_start, r_end, wh):
    frontier = APriorityQueue()
    camino = {}
    g = {}
    maxH = 0
    for i in initFrontier(grid, r_start):
        cost = 1
        g[i] = cost
        h = getDistToRoom(i[0],i[1],r_end)
        if(h > maxH):
            maxH = h
        f = cost + h
        frontier.insert([i,f])
        camino[i] = None

    last: Tuple[int,int]
    while not frontier.isEmpty():
        current = frontier.pop()

        if grid[current[0][0]][current[0][1]] == 0:
            color = 234*(1-(getDistToRoom(current[0][0],current[0][1],r_end)/maxH))
            if color < 0:
                color = 0
            wh.addBox(current[0][0],current[0][1],(242, color, 114),3)
        wh.update()

        if getDistToRoom(current[0][0]+0.5,current[0][1]+0.5,r_end) == 0.5:
            last = current[0]
            break
        neighbors = []
        if current[0][0] > 0 and grid[current[0][0]-1][current[0][1]] != 1:
            neighbors.append((current[0][0]-1,current[0][1]))
        if current[0][1] > 0 and grid[current[0][0]][current[0][1]-1] != 1:
            neighbors.append((current[0][0],current[0][1]-1))
        if current[0][0] < len(grid)-1 and grid[current[0][0]+1][current[0][1]] != 1:
            neighbors.append((current[0][0]+1,current[0][1]))
        if current[0][1] < len(grid)-1 and grid[current[0][0]][current[0][1]+1] != 1:
            neighbors.append((current[0][0],current[0][1]+1))
        for n in neighbors:
            cost = g[current[0]] + 1
            if n not in g or cost < g[n]:
                g[n] = cost
                h = getDistToRoom(n[0],n[1],r_end)
                f = cost + h
                frontier.insert([n,f])
                camino[n] = current[0]
    
    ultimo = last

    while camino[last] != None:
        if grid[last[0]][last[1]] == 0:
            grid[last[0]][last[1]] = 2
            wh.addBox(last[0],last[1],(105, 158, 191),2)
            wh.update()
        last = camino[last]
    if grid[last[0]][last[1]] == 0:
            grid[last[0]][last[1]] = 2
            wh.addBox(last[0],last[1],(105, 158, 191),2)
            wh.update()

    primero = last

    grid[ultimo[0]][ultimo[1]] = 4
    wh.addBox(ultimo[0],ultimo[1],(56, 134, 154))
    grid[primero[0]][primero[1]] = 4
    wh.addBox(primero[0],primero[1],(56, 134, 154))
    
    wh.deleteBoxes(3)
    return grid