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
            
            self.tree = FractalTree()
            self.tree.addSubBranchAtLocation(Coord(0,0))
            self.currentTreePos = [0]
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
                
        def back(self, distance):
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
                        theMaze.add_coord_obj(self.x, self.y)
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
                        theMaze.add_coord_obj(self.x + xdiff, self.y + ydiff)
        def doThing(self):
            ThisMaze.currentData()
            self.sense_three()
            if(getIfDeadEnd()):

            elif(spaces_left != 0 or spaces_right != 0):
                for i in range(len(self.tree.currentBranch.subBranches)):
                    print 'fuck'
                
            
##            self.alignedHorizontal = False
##            for i in range(0, len(self.virusList)):
##                tempCoord = self.virusList[i]
##                if(self.facing == 0 or self.facing == 2):
##                    if(tempCoord[0] == self.x):
##                        self.alignedHorizontal = True
##                else:
##                    if(tempCoord[1] == self.y):
##                        self.alignedHorizontal = True
##                        
##            if(len(self.closeVirusCoord) == 0):
##                self.findCloseVirus()
##                        
##            for i in range(0, len(self.virusList)):
##                tempCoord = self.virusList[i]
##                if(tempCoord[0] == self.x and tempCoord[1] == self.y):
##                    self.sense_virus()
##                    if(tempCoord[0] == self.closeVirusCoord[0] and tempCoord[1] == self.closeVirusCoord[1]):
##                        self.findCloseVirus()
##                    break
##
##                
##            
##                
##            cVX = self.closeVirusCoord[0]
##            cVY = self.closeVirusCoord[1]
##            aboveVal = 0
##            rightVal = 0
##            aboveVal = cVY-self.y
##            rightVal = cVX-self.x
##            directionArray = [-1,-1,-1,-1]
##            exception = False
##            if(aboveVal < rightVal):
##                if(aboveVal > 0):
##                    directionArray[0] = Direction.UP
##                    upUsed = True
##                elif (aboveVal < 0):
##                    directionArray[0] = Direction.DOWN
##                    downUsed = True
##                else:
##                    #On same y level
##                    directionArray[3] = Direction.DOWN
##                    directionArray[2] = Direction.UP
##                    exception = True
##                    if(rightVal > 0):
##                        directionArray[0] = Direction.RIGHT
##                        directionArray[1] = Direction.LEFT
##                    elif (rightVal < 0):
##                        directionArray[0] = Direction.LEFT
##                        directionARray[1] = Direction.RIGHT
##                if(upUsed):
##                    directionArray[1] = Direction.LEFT
##                else:
##                    directionArray[1] = Direction.RIGHT
##                directionArray[2] = Direction.UP
##                directionArray[3] = Direction.DOWN
##                if(rightVal > 0 and not exception):
##                    directionArray[1] = Direction.RIGHT
##                elif (rightVal < 0):
##                    directionArray[2] = Direction.LEFT
##                self.alignedHorizontal = False
##            for i in range(0, len(self.virusList)):
##                tempCoord = self.virusList[i]
##                if(self.facing == 0 or self.facing == 2):
##                    if(tempCoord[0] == self.x):
##                        self.alignedHorizontal = True
##                else:
##                    if(tempCoord[1] == self.y):
##                        self.alignedHorizontal = True
##                        
##            if(len(self.closeVirusCoord) == 0):
##                self.findCloseVirus()
##                        
##            for i in range(0, len(self.virusList)):
##                tempCoord = self.virusList[i]
##                if(tempCoord[0] == self.x and tempCoord[1] == self.y):
##                    self.sense_virus()
##                    if(tempCoord[0] == self.closeVirusCoord[0] and tempCoord[1] == self.closeVirusCoord[1]):
##                        self.findCloseVirus()
##                    break
##
##                
##            
##                
##            cVX = self.closeVirusCoord[0]
##            cVY = self.closeVirusCoord[1]
##            aboveVal = 0
##            rightVal = 0
##            aboveVal = cVY-self.y
##            rightVal = cVX-self.x
##            directionArray = [-1,-1,-1,-1]
##            exception = False
##            if(aboveVal < rightVal):
##                if(aboveVal > 0):
##                    directionArray[0] = Direction.UP
##                    upUsed = True
##                elif (aboveVal < 0):
##                    directionArray[0] = Direction.DOWN
##                    downUsed = True
##                else:
##                    #On same y level
##                    directionArray[3] = Direction.DOWN
##                    directionArray[2] = Direction.UP
##                    exception = True
##                    if(rightVal > 0):
##                        directionArray[0] = Direction.RIGHT
##                        directionArray[1] = Direction.LEFT
##                    elif (rightVal < 0):
##                        directionArray[0] = Direction.LEFT
##                        directionARray[1] = Direction.RIGHT
##                if(upUsed):
##                    directionArray[1] = Direction.LEFT
##                else:
##                    directionArray[1] = Direction.RIGHT
##                directionArray[2] = Direction.UP
##                directionArray[3] = Direction.DOWN
##                if(rightVal > 0 and not exception):
##                    directionArray[1] = Direction.RIGHT
##                elif (rightVal < 0):
##                    directionArray[2] = Direction.LEFT
##                
##            else:
##                if(rightVal > 0):
##                    directionArray[1] = Direction.RIGHT
##                elif (rightVal < 0):
##                    directionArray[2] = Direction.LEFT
##                else:
##                    #On same x level
##                    directionArray[3] = Direction.RIGHT
##                    directionArray[2] = Direction.LEFT
##                    exception = True
##                    if(aboveVal > 0):
##                        directionArray[1] = Direction.UP
##                    elif (rightVal < 0):
##                        directionArray[2] = Direction.DOWN
##                if(aboveVal > 0 and not exception):
##                    directionArray[1] = Direction.UP
##                elif (aboveVal < 0):
##                    directionArray[2] = Direction.DOWN
##            finalDirection = -1;
##            disallowedDirections = set()
##            breakOut = False
##            for d in directionArray:
##                a = -1
##                if(d == Direction.UP):
##                    a = Coord(self.x, self.y+1)
##                elif(d == Direction.LEFT):
##                    a = Coord(self.x-1, self.y)
##                elif(d == Direction.DOWN):
##                    a = Coord(self.x, self.y-1)
##                else:
##                    a = Coord(self.x+1, self.y)
##                for p in self.paths:
##                    sp = p.getStartPosition()
##                    if(sp.x == a.x and sp.y == a.y):
##                        if(p.isDeadEnd()):
##                            #CANT GO THIS WAY BECAUSE IT IS A DEAD END!
##                            #SO DO NOTHING
##                            disallowedDirections.add(d)
##                        else:
##                            finalDirection = d
##                            breakOut = True
##                            break
##                if(breakOut):
##                    break
##            if (finalDirection == -1):
##                for d in directionArray:
##                    if(not (d in disallowedDirections)):
##                        finalDirection = d
##            if(finalDirection == -1):
##                print 'shit'
##            while(self.facing != finalDirection):
##                self.turn_left(1)
##            self.forward(1)
            
        def getIfDeadEnd(self):
            if(self.spaces_left == 0 and self.spaces_forward == 0 and self.spaces_right == 0):
                self.deadEndSpaces.append(Coord(self.x, self.y))
                return True
            else:
                return False
############################################################            
    class Coord():
        def __init__(self, x_val, y_val):
            self.isDecision = False
            self.x = x_val
            self.y = y_val
            self.name = 'Position: (', self.x, ',', self.y, ')'
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
            
        def add_coord_obj(self, c_x, c_y):
            self.coordList.append(Coord(c_x, c_y))

                
        def find_coord_obj(self, c_x, c_y):
            for i in range(len(self.coordList)):
                if (self.coordList[i].x == c_x) and (self.coordList[i].y == c_y):
                    return i
            return -1000
############################################################
    class FractalTree():
        def __init__(self):
            self.rootBranch = []
            
############################################################ 
    class FractalBranch():
        def __init__(self):
            self.subBranches = []
            self.coordArray = []
            self.decisionCoords = []
        def __init__(self, coord):
            self.subBranches = []
            self.coordArray = []
            self.decisionCoords = []
            self.startCoord = coord
        def add(self, coord):
            self.coordArray.append(coord)
        def split_path(self):
            newPath = Path()
            return newPath
        def getStartPos(self):
            return coordArray[0]
        def addSubBranchAtLocation(self, c):
            ##c is a coord object
             self.subBranches.append(FractalBranch(c))

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
