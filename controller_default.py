import thread
import time
import threading
import math

def control_robot(robot):
############################################################    
    class MazeBot():
        def __init__(self):
            self.x = 0
            self.y = 0
            self.facing = Direction.UP
            
            self.spaces_left = -1
            self.spaces_forward = -1
            self.spaces_right = -1
            
            self.tree = FractalTree(self.facing)
            self.currentTreePos = []
            #Tree pos works as follows
            #[1 3 2 2]
            #Branch 1 (of subbranch array)
            #Branch 3 (of subbranch array) (and all previous)
            #Branch 2 (of subbranch array) (and all previous)
            #Branch 2 (of subbranch array) (and all previous) (current branch)
            self.closeVirusCoord = []

            self.virusList = []
            self.deadEndSpaces = []
        
        def forward(self, dist):
            if (len(self.virusList) == 0):
                self.virusList = self.sense_virus()
                
            robot.step_forward(dist)
            if self.facing == Direction.UP:
                self.y = self.y + dist
            elif self.facing == Direction.LEFT:
                self.x = self.x - dist
            elif self.facing == Direction.DOWN:
                self.y = self.y - dist
            else:
                self.x = self.x + dist
            if(ThisMaze.find_coord_obj(self.x,self.y) == -1000):
                newCoord = Coord(self.x,self.y,self.facing)
                self.getCurrentBranch().coordArray.append(newCoord)
                ThisMaze.coordList.append(newCoord)
                print"I AM ADDING FORWARDDDDDDDDDDDDDDDD"
                
        def back(self, dist):
            if (len(self.virusList) == 0):
                self.virusList = self.sense_virus()
            robot.step_backward(dist)
            if self.facing == Direction.UP:
                self.y = self.y - dist
            elif self.facing == Direction.LEFT:
                self.x = self.x + dist
            elif self.facing == Direction.DOWN:
                self.y = self.y + dist
            else:
                self.x = self.x - dist
            if(ThisMaze.find_coord_obj(self.x,self.y) == -1000):
                newCoord = Coord(self.x,self.y,self.facing)
                self.getCurrentBranch().coordArray.append(newCoord)
                ThisMaze.coordList.append(newCoord)
                
        def turn_left(self, times):
            for i in range(times):
                robot.turn_left(1)
                if self.facing < Direction.RIGHT:
                    self.facing = self.facing + 1
                else:
                    self.facing = Direction.UP
                    
        def turn_right(self, times):
            for i in range(times):
                robot.turn_right(1)
                if self.facing > Direction.UP:
                    self.facing = self.facing - 1
                else:
                    self.facing = Direction.RIGHT
                    
        def sense_forward(self):
            self.spaces_forward = robot.sense_steps(robot.SENSOR_FORWARD)
            
        def sense_right(self):
            self.spaces_right = robot.sense_steps(robot.SENSOR_RIGHT)
            
        def sense_left(self):
            self.spaces_left = robot.sense_steps(robot.SENSOR_LEFT)
            
        def sense_three(self):
            self.spaces_left = -1
            self.spaces_right = -1
            self.spaces_forward = -1
            thread.start_new_thread(self.sense_forward, ())
            thread.start_new_thread(self.sense_right, ())
            thread.start_new_thread(self.sense_left, ())

        def sense_virus(self):
            tempList = robot.sense_viruses()
            for i in range(len(tempList)):
                tempCoord = tempList[i]
                xt = tempCoord[0]
                yt = tempCoord[1]
                if(self.facing == 1):
                    tempCoord[0] = yt * -1
                    tempCoord[1] = xt
                elif(self.facing == 2):
                    tempCoord[0] = xt * -1
                    tempCoord[1] = yt * -1
                elif(self.facing == 3):
                    tempCoord[0] = yt
                    tempCoord[1] = xt * -1
                tempCoord[0] = tempCoord[0] + self.x
                tempCoord[1] = tempCoord[1] + self.y
                tempList[i] = tempCoord
            self.virusList = tempList

        
        def virus_num(self):
            return robot.num_viruses_left()

        def findCloseVirus(self):
            distList = []
            smallestDist = 1000
            smallIndex = 1000
            for i in range(len(self.virusList)):
                tempCoord = self.virusList[i]
                dist = math.sqrt(pow(tempCoord[0]-self.x, 2) + pow(tempCoord[1]-self.y, 2))
                distList.append(dist)
                if(abs(dist) < smallestDist):
                    smallestDist = abs(dist)
                    smallIndex = i
            self.closeVirusCoord = self.virusList[smallIndex]
        
        def create_for_direction(self, theMaze):
            if(theMaze.find_coord_obj(self.x, self.y) == -1000):
                        theMaze.add_coord_obj(self.x, self.y, self.facing)
            spaces = [self.spaces_left, self.spaces_right, self.spaces_forward]
            for x in range (0,3):
                for i in range(0, int(spaces[x])):
                    xdiff = i+1 if (x < 2) else 0
                    if(x == 0):
                        xdiff = xdiff * -1
                    ydiff = 0
                    if (xdiff == 0):
                        ydiff = i+1
                    xt = xdiff
                    yt = ydiff
                    if(self.facing == 1):
                        xdiff = yt * -1
                        ydiff = xt
                    elif(self.facing == 2):
                        xdiff = xt * -1
                        ydiff = yt * -1
                    elif(self.facing == 3):
                        xdiff = yt
                        ydiff = xt * -1
                    if(theMaze.find_coord_obj(self.x + xdiff, self.y + ydiff) == -1000):
                        theMaze.add_coord_obj(self.x + xdiff, self.y + ydiff, self.facing)
        def getBranch(self, indexValues):
            startingBranch =  self.tree.rootBranch
            currentBranch = startingBranch.getBranch(0)
            for i in range(len(indexValues)):
                if(i+1 == len(indexValues)):
                    return 0
        #Return branch
        def doThing(self):
            ThisMaze.currentData()
            self.sense_three()
            while(self.spaces_forward == -1 or self.spaces_left == -1 or self.spaces_right == -1):
                qer = 1
            if(self.getIfDeadEnd()): #check if dead end. if so, return to origin of path / branch
                #should go back to origin of branch
                print "dead end, checking if space behind has not been traveled"
                index = self.getCoordBehindRobot(ThisMaze)
                if(index == -1000):
                    print "WOW THE COORD BEHIND THE ROBOT IS FREE TO EXPLOOOOOOOOOOOORE"    
                else:
                    print "attempting to travel to origin of current path"
                    self.travelToOriginOfCurrentPath()
            elif(self.spaces_left > 0 or self.spaces_right > 0): #check if it can go right or left. if so, check to see if there are current branches. Travel down the untravelled branches, make non-existant branches, etc.
               ## for i in range(len(self.tree.currentBranch.subBranches)):
                print 'heck'
                #check left first, then right
                if(self.spaces_left > 0):
                    index = self.getCoordLeftOfRobot(ThisMaze)
                    if(index == -1000):
                        branchId = self.getCurrentBranch().addSubBranchAtLocation(Coord((self.x,self.y,self.facing)))
                        currentTreePos.append(branchId)
                        self.turn_left(1)
                        self.forward(1)
                    else:
                        print'dont want to do that haha'
                    #if coordinate to left of robot is not traveled
                    #####create a new branch using that coordinate as the origin
                    #else
                    #####ignore that position
                    
                    print 'space left'
                    
                elif (self.spaces_right > 0):
                    index = self.getCoordLeftOfRobot(ThisMaze)
                    if(index == -1000):
                        branchId = self.getCurrentBranch().addSubBranchAtLocation(Coord((self.x,self.y,self.facing)))
                        currentTreePos.append(branchId)
                        self.turn_left(1)
                        self.forward(1)
                    else:
                        print'dont want to do that haha'
                    #if coordinate to left of robot is not traveled
                    #####create a new branch using that coordinate as the origin
                    #else
                    #####ignore that position
                    
                    print 'space left'
                    
            
            elif (self.getCoordBehindRobot(ThisMaze) == -1000 and self.check3Dead()):
                ##Space behind hasn't been explored and not at dead end
                print 'placeholder'
                self.turn_left(2)
            else: #Only space is in front
                self.forward(1)
                
                
            #CHECKS LEFT RIGHT AND FORWARD FOR EXPLORED    
        def check3Dead(self):
            if(self.spaces_left == 0 and self.spaces_right == 0 and self.spaces_forward == 0):
                print "THE GODS HAVE SPOKEEN"
                return True
            all3dead = True
            sidesChecked = [0,0,0]
            leftCoord = self.getCoordLeftOfRobot(ThisMaze)
            frontCoord = self.getCoordInFrontOfRobot(ThisMaze)
            rightCoord = self.getCoordRightOfRobot(ThisMaze)
            for i in range (len(self.getCurrentBranch().subBranches)):
                if(self.getCurrentBranch().subBranches[i].coordArray[0].equals(leftCoord)):
                    sidesChecked[0] = 1
                if (self.getCurrentBranch().subBranches[i].coordArray[0].equals(frontCoord)):
                    sidesChecked[1] = 1
                if(self.getCurrentBranch().subBranches[i].coordArray[0].equals(rightCoord)):
                    sidesChecked[2] = 1
                if(self.getCurrentBranch().subBranches[i].isExplored == False):
                    print "CURRENT BRANCH IS NOT EXPLORED"
                    return False
            #print "STILL UNEXPLORED BRANCHES"
            if(len(self.getCurrentBranch().subBranches) < 3):
                if(self.spaces_left != 0 and sidesChecked[0] == 0):
                    all3dead = False
                    print"q"
                elif(self.spaces_right != 0 and sidesChecked[2] == 0):
                    all3dead = False
                    print"r"
                elif(self.spaces_forward != 0 and sidesChecked[1] == 0):
                    all3dead = False
                    print "s"
                else:
                    print "t"
                
                
            return all3dead
                
        def getCoordRightOfRobot(self,maze):
            if(self.facing == 0):
                posX = self.x + 1 
                posY = self.y
            elif(self.facing == 1):
                posX = self.x
                posY = self.y -1 
            elif(self.facing == 2):
                posX = self.x -1
                posY = self.y 
            else:
                posX = self.x
                posY = self.y + 1
            return maze.find_coord_obj(posX, posY)
        def getCoordInFrontOfRobot(self,maze):
            if(self.facing == 0):
                posX = self.x 
                posY = self.y +1
            elif(self.facing == 1):
                posX = self.x +1
                posY = self.y 
            elif(self.facing == 2):
                posX = self.x
                posY = self.y - 1
            else:
                posX = self.x - 1 
                posY = self.y
            return maze.find_coord_obj(posX, posY)
        def getCoordBehindRobot(self,maze):
            if(self.facing == 0):
                posX = self.x 
                posY = self.y -1
            elif(self.facing == 1):
                posX = self.x -1
                posY = self.y 
            elif(self.facing == 2):
                posX = self.x
                posY = self.y + 1
            else:
                posX = self.x + 1 
                posY = self.y
            return maze.find_coord_obj(posX, posY)
        
        def getCoordLeftOfRobot(self, maze):
            if(self.facing == 0):
                posX = self.x - 1
                posY = self.y
            elif(self.facing == 1):
                posX = self.x
                posY = self.y +1
            elif(self.facing == 2):
                posX = self.x + 1
                posY = self.y
            else:
                posX = self.x 
                posY = self.y-1
            return maze.find_coord_obj(posX, posY)
            
        #
        #
        #
        # To do: in addition to checking dead end, check for dead branch
        #        
        #
        #
        #
        #
                
        def getIfDeadEnd(self):
            print self.spaces_left , "  " , self.spaces_forward , "  " , self.spaces_right
            if(self.spaces_left == 0 and self.spaces_forward == 0 and self.spaces_right == 0):
                self.deadEndSpaces.append(Coord(self.x, self.y, self.facing))
                return True
            else:
                return False
            
            
        def getCurrentBranch(self):
            currentBranch = self.tree.getRootBranch()
            ## self.tree.getRootBranch(), " AAAAAAAAAAAAAA"
            for i in range (len(self.currentTreePos)):
                currentBranch = currentBranch.getBranch(self.currentTreePos[i])
            return currentBranch
        
        def travelToOriginOfCurrentPath(self):
            currentBranch = self.getCurrentBranch()
            for i in range (len(currentBranch.coordArray)-1):
                v = len(currentBranch.coordArray) - 1 - (i+1)
                currentCoord = currentBranch.coordArray[v]
                if(self.getRelativeXDirectionToCoord(currentCoord) > 0):
                    ##point is to the right of robot
                    self.turn_right(1)
                    self.forward(1)
                    print"aaa"
                elif (self.getRelativeXDirectionToCoord(currentCoord) < 0):
                    ##Point is  to the left
                    self.turn_left(1)
                    self.forward(1)
                    print"bbb"
                elif (self.getRelativeYDirectionToCoord(currentCoord) > 0):
                    ##Point is in front (weird)
                    self.forward(1)
                    print "ccc"
                elif (self.getRelativeYDirectionToCoord(currentCoord) < 0):
                    self.back(1)
                    print "ddd"
                else:
                    print "!!!!!MAYDAY!!!!!"
            currentBranch.isExplored = True
                
        def getRelativeXDirectionToCoord(self, coord):
            return self.x - coord.x
        def getRelativeYDirectionToCoord(self, coord):
            return  coord.y - self.y
############################################################            
    class Coord():
        def __init__(self, x_val, y_val, direction):
            self.isDecision = False
            self.x = x_val
            self.y = y_val
            self.name = 'Position: (', self.x, ',', self.y, ')'
            self.directionTravelled = direction
        def equals(self, coord):
            return coord.x == self.x and coord.y == self.y
############################################################            
    class Wall():
        def __init__(self, orientation, val_pos, val_const):
            self.orient = orientation
            self.coord_pos = val_pos
            self.coord_neg = self.coord_pos - 1
            self.coord_const = val_const
            update_name()
                
        def update_name(self):
            if self.orient == Orientation.horizontal:
                self.name = "Wall inbetween y = ", self.coord_pos, "and y = ", self.coord_neg, ", with a constant of x =", self.coord_const, "and a horizontal orientation(", self.orient, ")"
            else:
                self.name = "Wall inbetween x = ", self.coord_pos, "and x = ", self.coord_neg, ", with a constant of y =", self.coord_const, "and a vertical orientation(", self.orient, ")"
############################################################                     
    class Maze():
        def __init__(self, bot):
            self.virusesLeft = bot.virus_num()
            self.counter = 1
            self.coordList = []
            self.bot = bot
        def currentData(self):
            print "Movement Number:", self.counter
            print ""
            print "Spaces left:", self.bot.spaces_left
            print "Spaces right:", self.bot.spaces_right
            print "Spaces forward:", self.bot.spaces_forward
            if self.bot.facing == Direction.UP:
                print "Facing direction: Forward, ", self.bot.facing
            elif self.bot.facing == Direction.LEFT:
                print "Facing direction: Left, ", self.bot.facing
            elif self.bot.facing == Direction.DOWN:
                print "Facing direction: Back, ", self.bot.facing
            else:
                print "Facing direction: Right, ", self.bot.facing
            print ""
            print "Robot Coordinates: (", self.bot.x, ",", self.bot.y, ")"
            print ""
            print "All viruses known: ", self.bot.virusList
            print "Target virus coordintates:", self.bot.closeVirusCoord
            print "Number of viruses left:", self.bot.virus_num()
            print "========================================================"
            print ""
            self.counter = self.counter + 1
            
        def add_coord_obj(self, c_x, c_y, dir):
            self.coordList.append(Coord(c_x, c_y, dir))

                
        def find_coord_obj(self, c_x, c_y):
            for i in range(len(self.coordList)):
                if (self.coordList[i].x == c_x) and (self.coordList[i].y == c_y):
                    return i
            return -1000
############################################################
    class FractalTree():
        def __init__(self, facing):
            self.rootBranch = FractalBranch(Coord(0,0,facing), facing)
        
        def getRootBranch(self):
            return self.rootBranch

            
############################################################ 
    class FractalBranch():
        def __init__(self, facing):
            self.subBranches = []
            self.coordArray = []
            self.decisionCoords = []
            self.originalDirection = facing
            self.isExplored = False
        def __init__(self, coord, facing):
            self.subBranches = []
            self.coordArray = [coord]
            self.decisionCoords = []
            self.startCoord = coord
            self.originalDirection = facing
            self.isExplored = False
        def add(self, coord):
            self.coordArray.append(coord)
        def split_path(self):
            newPath = Path()
            return newPath
        def getStartPos(self):
            return coordArray[0]
        def addSubBranchAtLocation(self, c):
            ##c is a coord object
             self.subBranches.append(FractalBranch(c, self.facing))
             return len(subBranches)

        def getBranch(self, num):
            return subBranches[num]
        def isAbsDeadEnd(self, deadEndPos):
            checkBool = True
            for x in (len(subBranches)):
                checkBool = checkBool and subBranches[x].isAbsDeadEnd()
            if(len(subBranches == 0)):
               for x in (len(deadEndPos)):
                   ##add compare method
                   if(deadEndPos[x] == coordArray[len(coordArray)-1]):
                       return True
            return checkBool
            
############################################################
    class Direction():
        UP = 0
        LEFT = 1
        DOWN = 2
        RIGHT = 3
    class Orientation():
        horizontal = 0
        vertical = 1
############################################################
############################################################
    OMHSBot = MazeBot()
    ThisMaze = Maze(OMHSBot)
    OMHSBot.sense_virus()
    while(True):
        OMHSBot.doThing()
    
    pass
