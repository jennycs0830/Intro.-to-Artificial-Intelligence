from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        value,action=self.minimax(gameState,0,0)#call the minimax function
        print(action)
        return action
        raise NotImplementedError("To be implemented")


    def minimax(self,gameState,depth,agentIndex):
        if agentIndex>=gameState.getNumAgents():#if every agent in the game return the value and action, then we finish one round
            agentIndex=0#set agentIndex=0 means that it's time to player's turn
            depth+=1#depth represent of many round we going to do
        if gameState.isWin() or gameState.isLose() or (depth>=self.depth):#(case1: if player win or lose/ case2:if finish the expected number of round)
            return self.evaluationFunction(gameState), None#in this case, we evaluate the extent of nextState if it is a good choice
        if agentIndex==0:#is player's turn
            return self.max_agent(gameState,depth,agentIndex)#player should return the max value
        else:#is ghost turn
            return self.min_agent(gameState,depth,agentIndex)#ghost should return the min value
    
    def max_agent(self,gameState,depth,agentIndex):#for player
        bestValue=-float('inf')#to do the comparison, initial the value equal to -inf
        NextAction = None#variable use for record the best next action
        for action in gameState.getLegalActions(agentIndex):#travel all the possible legal actions
            NextState=gameState.getNextState(agentIndex,action)#get the nextstate correspond to the legal action
            value,_=self.minimax(NextState,depth,agentIndex+1)#we should get the low level of value first then we can do the comparison
            if value>bestValue:#to find the max value
                bestValue=value#record the max value
                NextAction=action#and record the next action
        return bestValue,NextAction
    
    def min_agent(self,gameState,depth,agentIndex):#for ghost
        bestValue=float('inf')#to do the comparison, initial the value equal to inf
        NextAction = None
        for action in gameState.getLegalActions(agentIndex):
            NextState=gameState.getNextState(agentIndex,action)
            value,_=self.minimax(NextState,depth,agentIndex+1)
            if value<bestValue:#to find the min value
                bestValue=value#record the min value
                NextAction=action#and return next action
        return bestValue,NextAction
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        """
        the difference between part2 and part 1 is the addition variable alpha and beta
        the initial value of alpha equal to -inf
        the initial value of beta equal to inf
        """
        value,action=self.minimax(gameState,0,0,float('-inf'),float('inf'))#call minimax function
        print(action)
        return action
        raise NotImplementedError("To be implemented")


    def minimax(self,gameState,depth,agentIndex,alpha,beta):
        if agentIndex>=gameState.getNumAgents():
            agentIndex=0
            depth+=1
        if gameState.isWin() or gameState.isLose() or (depth>=self.depth):
            return self.evaluationFunction(gameState), None
        if agentIndex==0:
            return self.max_agent(gameState,depth,agentIndex,alpha,beta)#add two addition variable
        else:
            return self.min_agent(gameState,depth,agentIndex,alpha,beta)
    
    def max_agent(self,gameState,depth,agentIndex,alpha,beta):
        bestValue=-float('inf')
        NextAction = None
        for action in gameState.getLegalActions(agentIndex):
            NextState=gameState.getNextState(agentIndex,action)
            value,_=self.minimax(NextState,depth,agentIndex+1,alpha,beta)
            if value>bestValue:
                bestValue=value
                NextAction=action
            """
            add the jdgmental of alpha and beta
            """
            if bestValue>beta:
                break
            if bestValue>alpha:
                alpha=max(alpha,bestValue)
        return bestValue,NextAction
    
    def min_agent(self,gameState,depth,agentIndex,alpha,beta):
        bestValue=float('inf')
        NextAction = None
        for action in gameState.getLegalActions(agentIndex):
            NextState=gameState.getNextState(agentIndex,action)
            value,_=self.minimax(NextState,depth,agentIndex+1,alpha,beta)
            if value<bestValue:
                bestValue=value
                NextAction=action
            if bestValue<alpha:
                break
            if bestValue<beta:
                beta=min(beta,bestValue)
        return bestValue,NextAction
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        """
        change the min_agent function in part 3
        the algorithm should change the outcomes to average-case, not worst-case
        """
        value,action=self.minimax(gameState,0,0,float('-inf'),float('inf'))
        print(action)
        return action
        raise NotImplementedError("To be implemented")


    def minimax(self,gameState,depth,agentIndex,alpha,beta):
        if agentIndex>=gameState.getNumAgents():
            agentIndex=0
            depth+=1
        if gameState.isWin() or gameState.isLose() or (depth>=self.depth):
            return self.evaluationFunction(gameState), None
        if agentIndex==0:
            return self.max_agent(gameState,depth,agentIndex,alpha,beta)
        else:
            return self.min_agent(gameState,depth,agentIndex,alpha,beta)
    
    def max_agent(self,gameState,depth,agentIndex,alpha,beta):
        bestValue=-float('inf')
        NextAction = None
        for action in gameState.getLegalActions(agentIndex):
            NextState=gameState.getNextState(agentIndex,action)
            value,_=self.minimax(NextState,depth,agentIndex+1,alpha,beta)
            if value>bestValue:
                bestValue=value
                NextAction=action
            if bestValue>beta:
                break
            if bestValue>alpha:
                alpha=max(alpha,bestValue)
        return bestValue,NextAction
    
    def min_agent(self,gameState,depth,agentIndex,alpha,beta):
        total_value=0
        actionNum=0
        NextAction = None
        for action in gameState.getLegalActions(agentIndex):
            NextState=gameState.getNextState(agentIndex,action)
            value,_=self.minimax(NextState,depth,agentIndex+1,alpha,beta)
            total_value+=value
            actionNum+=1
        bestValue=total_value/actionNum#calculate the average-case value
        return bestValue,NextAction
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    GhostStates = currentGameState.getGhostStates() #all the ghost states
    Pacman_Pos = currentGameState.getPacmanPosition()
    food_list = (currentGameState.getFood()).asList() #get all the food as list.
    capsule_list = currentGameState.getCapsules() #get all the capsules.
    no_food = len(food_list) #check that if there still have food or not
    no_capsule = len(capsule_list) #chenck if there still have capsule or not

    state_score=0 #variable for record the final score
    if currentGameState.getNumAgents() > 1:#>1 represent that there are ghost exist
        ghost_dis = min( [manhattanDistance(Pacman_Pos, ghost.getPosition()) for ghost in GhostStates])# search the nearest ghost distance
        if (ghost_dis <= 1):
            return -10000 #if nearest ghost distance is small than 1, this is the worst case so return -10000
        state_score -= 1.0/ghost_dis #minus the score with 1/(distance between player and ghost)
    #Feature 3 food positions
    current_food = Pacman_Pos
    for food in food_list: #calculate all the food distance and update the score
        closestFood = min(food_list, key=lambda x: manhattanDistance(x, current_food))
        state_score += 1.0/(manhattanDistance(current_food, closestFood)) #plus the score with 1/(the distance between player and food)
        current_food = closestFood #then change the pacman position to the previous eaten food
        food_list.remove(closestFood) # remove the food already been eaten
    #Feature 4 capsule positions, same idea as food position
    current_capsule = Pacman_Pos
    for capsule in capsule_list:
        closest_capsule = min(capsule_list, key=lambda x: manhattanDistance(x, current_capsule))
        state_score += 1.0/(manhattanDistance(current_capsule, closest_capsule))
        current_capsule = closest_capsule
        capsule_list.remove(closest_capsule)
    #Feature 4 Score of the game
    state_score += 8*(currentGameState.getScore())

    #Feature 5: remaining food and capsule
    state_score -= 6*(no_food + no_capsule)

    return state_score
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
