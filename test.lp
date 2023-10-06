\* calendar_optim *\
Maximize
OBJ: activity_0 + activity_1
Subject To
_C1: - activity_0 + time_0_0 = 0
_C2: - activity_0 + place_0_0 + place_0_1 = 0
_C3: - activity_0 + person_0_0 = 0
_C4: - activity_1 + time_1_1 = 0
_C5: - activity_1 + place_1_1 = 0
_C6: - activity_1 + person_1_0 = 0
Binaries
activity_0
activity_1
person_0_0
person_1_0
place_0_0
place_0_1
place_1_1
time_0_0
time_1_1
End
