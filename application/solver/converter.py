from pulp import *
from itertools import combinations

class ActivityIDs:
    def __init__(self, timesID=[], placesID=[], peopleID=[], value=1):
        self.times = timesID
        self.places = placesID
        self.people = peopleID
        self.value = value

# Gets incompatible times
def getIncompTimes(times):
    ans = [(i,i) for i in range(len(times))]
    tenum = enumerate(times)
    for (i, ins1), (j, ins2) in combinations(tenum,2):
        for a, b in ins1:
            out = False
            for c, d in ins2:
                if a <= c < b or a < d <= b:
                    ans.append((i, j))
                    out = True
                    break
            if out:
                break
    return ans

# Check if makes sense (doesn't begin after ends, no intersection inside a time-option)
def checkTimes(times):
    for time_option in times:
        for a, b in time_option:
            assert(a <= b)
        for (a, b), (c, d) in combinations(time_option,2):
            assert(not(a <= c < b or a < d <= b))

# Get pulp problem, which is ready to be solved by some solver
def getProblem(times, nplaces, npeople, activitiesID):
    checkTimes(times)
    ntimes = len(times)
    incomptimes = getIncompTimes(times)

    # Preparing variables
    rti = range(ntimes)
    rpl = range(nplaces)
    rpe = range(npeople)
    rac = range(len(activitiesID))
    prob = LpProblem("calendar_optim", LpMaximize)
    timeVars = LpVariable.dicts("time", (rac, rti), cat = "Binary")
    placeVars = LpVariable.dicts("place", (rac, rpl), cat = "Binary")
    peopleVars = LpVariable.dicts("person", (rac, rpe), cat = "Binary")
    actiVars = LpVariable.dicts("activity", (rac), cat = "Binary")
    # Constraints
    goal = []
    for i, act in enumerate(activitiesID):
        # Objective function
        goal.append((actiVars[i], act.value))

        # No two activitiesID at the same place and time
        pairs = []
        for j, act2 in enumerate(activitiesID):
            if i != j:
                for t1, t2 in incomptimes:
                    if t1 in act.times and t2 in act2.times:
                        pairs.append((j, act2, t1, t2))
        for j, act2, t1, t2 in pairs:
            for p in rpl:
                if p in act.places and p in act2.places:
                    prob += timeVars[i][t1]+timeVars[j][t2]+placeVars[i][p]+placeVars[j][p] <= 3

        # No two activitiesID with the same person at the same time
        pairs = []
        for j, act2 in enumerate(activitiesID):
            if i != j:
                for t1, t2 in incomptimes:
                    if t1 in act.times and t2 in act2.times:
                        pairs.append((j,act2,t1,t2))
        for j, act2, t1, t2 in pairs:
            for p in rpe:
                if p in act.people and p in act2.people:
                    prob += timeVars[i][t1]+timeVars[j][t2]+peopleVars[i][p]+peopleVars[j][p] <= 3

        # Each chosen activity has exactly one person, place and time attached to it.
        onetime = []
        oneplace = []
        oneperson = []
        for j in act.times:
            onetime.append((timeVars[i][j],1))
        for j in act.places:
            oneplace.append((placeVars[i][j],1))
        for j in act.people:
            oneperson.append((peopleVars[i][j],1))
        prob += LpAffineExpression(onetime) == actiVars[i]
        prob += LpAffineExpression(oneplace) == actiVars[i]
        prob += LpAffineExpression(oneperson) == actiVars[i]
    prob += LpAffineExpression(goal)
    return prob

# This is for debugging, effectively lets a human see what choices were made, at stdout
def seeSolution(prob):
    prob.solve(GLPK()) # Set solver here
    print("Status:", LpStatus[prob.status])

    # Print the value of the variables at the optimum
    for v in prob.variables():
        print(v.name, "=", v.varValue)
    
    # Print the value of the objective
    print("objective=", value(prob.objective))

# Manually checks some cases
if __name__ == "__main__":
    print("Debugging...")
    act1 = activity([0], [0,1], [0], 1)
    act2 = activity([1], [1], [0], 1)
    times = [((1, 3), (3, 4)), ((5, 5), (6, 10),)]
    prob = getProblem(times, 2, 2, [act1, act2])
    print(prob)
    prob.writeLP("test.lp")
    seeSolution(prob)
    
    
    print("\n\n\nIf no places times and people, answer should be 0:")
    acts = [activity([], [], [], 1) for i in range(10)]
    prob = getProblem([], 0, 0, acts)
    print(prob)
    seeSolution(prob)

    N = 20
    print(f"\n\n\nBigger test, all are possible, answer should be {N}:")
    acts = [activity(range(i+1) ,range(i+1) ,range(i+1) ,1) for i in range(N)]
    times = [[((i+1)*(j+1), (i+1)*(j+1)+j) for j in range(i+1)] for i in range(N)]
    prob = getProblem(times, N, N, acts)
    seeSolution(prob)
    # 0m11,823s -> default, N = 15
    # 0m7,548s -> GLPK, N = 15
    # 1m2,272s -> default, N = 20
    # 0m36,996s -> GLPK , N = 20
