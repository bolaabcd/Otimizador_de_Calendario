from pulp import *


class activity:
	def __init__(self, timesID=[],placesID=[],peopleID=[],value=1):
		self.times = timesID
		self.places = placesID
		self.people = peopleID
		self.value = value

def getIncompTimes(times):
	ans = []
	for i,t1 in enumerate(times):
		for j,t2 in enumerate(times):
			if i < j and t2[0] <= t1[0] < t2[1] or t2[0] < t1[1] <= t2[1]:
				ans.append((i,j))
	return ans

def getProblem(times,nplaces,npeople,activities):
	ntimes = len(times)
	incomptimes = getIncompTimes(times)
	# Preparing variables
	rti = range(ntimes)
	rpl = range(nplaces)
	rpe = range(npeople)
	rac = range(len(activities))
	prob = LpProblem("calendar_optim", LpMaximize)
	timeVars = LpVariable.dicts("time", (rac, rti), cat = "Binary")
	placeVars = LpVariable.dicts("place", (rac, rpl), cat = "Binary")
	peopleVars = LpVariable.dicts("person", (rac, rpe), cat = "Binary")
	actiVars = LpVariable.dicts("activity", (rac), cat = "Binary")
	# Constraints
	goal = []
	for i,act in enumerate(activities):
		# Objective function
		goal.append((actiVars[i],act.value))

		# No two activities at the same place and time
		for j,act2 in enumerate(activities):
			if i != j:
				for t1,t2 in incomptimes:
					for p in rpl:
						if t1 in act.times and t2 in act2.times and p in act.places and p in act2.places:
							prob += timeVars[i][t1]+timeVars[j][t2]+placeVars[i][p]+placeVars[j][p] <= 3

		# No two activities with the same person at the same time
		for j,act2 in enumerate(activities):
			if i != j:
				for t1,t2 in incomptimes:
					for p in rpe:
						if t1 in act.times and t2 in act2.times and p in act.people and p in act2.people:
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


if __name__ == "__main__":
	print("Debugging...")
	act1 = activity([0], [1], [0], 1)
	act2 = activity([1], [1], [0], 1)
	times = [(1,3),(2,4)]
	prob = getProblem(times,2,2,[act1,act2])
	print(prob)
	prob.writeLP("test.lp")
	prob.solve()
	print("Status:", LpStatus[prob.status])
	# Print the value of the variables at the optimum
	for v in prob.variables():
		print(v.name, "=", v.varValue)
	
	# Print the value of the objective
	print("objective=", value(prob.objective))

