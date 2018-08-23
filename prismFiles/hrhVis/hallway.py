from environment import Simulation


class Hallway(Simulation):
    def __init__(self, configFile, matrixFile, staFile, traFile):
        Simulation.__init__(self, configFile, matrixFile)
        self.read_sta_file(staFile)
        self.read_tra_file(traFile)

    def read_sta_file(self, staFile):
        self.stateList = []
        with open(staFile, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line[0] != '(':
                a = line.find('(')
                b = line.find(')')
                s = line[a+1:b].split(',')
                state = []
                for i in xrange(0,len(s)):
                    state.append(int(s[i]))
                self.stateList.append(state)


    def read_tra_file(self, traFile):
        self.transList = []
        with open(traFile, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if len(line.split(' ')) > 3:
                s = line.replace('\n','').split(' ')
                trans = []
                try:
                    for i in xrange(0,len(s)):
                        if i < len(s)-1:
                            trans.append(int(s[i]))
                        else:
                            trans.append(float(s[i]))
                except ValueError:
                    trans.append(s[i])
                self.transList.append(trans)


    def hallway_move(self, movement, stateList, transList, gameState):
        self.draw()

        # Current State
        goal = gameState[1]
        count = gameState[3]
        gridState = self.get_state()
        robotX = gridState['moving_obstacles'][0][0]
        robotY = gridState['moving_obstacles'][0][1]
        humanX = gridState['agents'][0][0]
        humanY = gridState['agents'][0][1]
        if goal==1 and humanX==2 and humanY==4:
            reached = 1
        elif goal==2 and humanX==7 and humanY==0:
            reached = 2
        elif goal==3 and humanX==14 and humanY==2:
            reached = 3
        else:
            reached = 0
        
        # HUMAN MOVE (AGENT)
        if reached == 0:
            for agent in range(len(movement)):
                if movement[agent] == "keyboard":
                    self.move_agent(agent, self.get_key())
            self.draw()
        # print gameState
        # print stateList.index(gameState)


        # ESTIMATE GOAL
        # Determine new state
        gridState = self.get_state()
        robotX = gridState['moving_obstacles'][0][0]
        robotY = gridState['moving_obstacles'][0][1]
        humanX = gridState['agents'][0][0]
        humanY = gridState['agents'][0][1]
        # if goal==1 and humanX==2 and humanY==4:
        #     reached = 1
        # elif goal==2 and humanX==7 and humanY==0:
        #     reached = 2
        # elif goal==3 and humanX==14 and humanY==2:
        #     reached = 3
        # else:
        #     reached = 0
        # gameState = [1, gameState[1], gameState[2], robotX, robotY, humanX, humanY]
        gameState = [1, goal, reached, count, robotX, robotY, humanX, humanY]
        # print gameState
        # print stateList.index(gameState)
        
        # Find succ trans state
        ind = stateList.index(gameState)
        targ = 0
        for row in transList:
            if row[0] == ind:
                targ = row[2]

        gameState = stateList[targ]
        # print gameState



        # Check event
        if (self.handle_events()):
            return True, 0, goal, count, gameState


        # print gameState
        # print stateList.index(gameState)

        goal = gameState[1]
        count = gameState[3]
       
        
        # ROBOT MOVE (OBSTACLE)
        # Find succ trans state
        ind = targ
        targ = 0
        for row in transList:
            if row[0] == ind:
                targ = row[2]

        gameState = stateList[targ]
        rXnext = gameState[4]
        rYnext = gameState[5]

        if not (rXnext==robotX and rYnext==robotY):
            if rXnext == robotX-1:
                action = "west"
            elif rXnext == robotX+1:
                action = "east"
            elif rYnext == robotY+1:
                action = "south"
            elif rYnext == robotY-1:
                action = "north"

            self.move_obstacle(0, action)
            self.draw()
        # print gameState
        # print stateList.index(gameState)

        if (self.step_forward() or (rXnext==0 and reached>0)):
            return True, 0, goal, count, gameState

        return False, self.get_state(), goal, count, gameState



if __name__ == '__main__':
    configFile = 'hrh_config.txt'
    matrixFile = 'matrix.txt'
    staFile = 'hrh_full.sta'
    traFile = 'hrh_full.tra'
    hall = Hallway(configFile, matrixFile, staFile, traFile)

    gridState = hall.get_state()
    robotX = gridState['moving_obstacles'][0][0]
    robotY = gridState['moving_obstacles'][0][1]
    humanX = gridState['agents'][0][0]
    humanY = gridState['agents'][0][1]
    
    goal = 3
    reached = 0
    count = 0
    gameState = [0, goal, reached, count, robotX, robotY, humanX, humanY]

    done = False
    while not done:
        newGameState = gameState
        done, gridState, goal, count, gameState = hall.hallway_move(["keyboard"], hall.stateList, hall.transList, newGameState)
        print 'step: ' + str(hall.time_step) + ' goal: ' + str(goal) + ' count: ' + str(count)



