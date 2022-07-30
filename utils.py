# Represents a group of questions that the player can be asked, storing the common helping verb that comes at 
# the beginning of the questions ("is", "does", etc.) only once for the whole group. Also tracks whether the 
# questions are mutually exclusive to one another: if yes, then only one question from the group can be asked per game
class QuestionGroup:
    def __init__(self, leadup, group, mutually_exclusive):
        self.leadup = leadup
        self.group = group
        self.mutually_exclusive = mutually_exclusive

IS = "Is"
DOES = "Does"
HAS = "Has"
WOULD = "Would"

answer_intros = ["You must be thinking of", "I got it! It's", "You're thinking of"]

# Construct all question groups anew, for a new game
def renew_all_questions():
    all_questions = []

    for proto_group in [
    ["on the taller side",
    "on the shorter side"],

    ["from North America",
    "from South America",
    "from Asia",
    "from Europe",
    "from Africa",
    "from Australia"],

    ["on the younger side",
    "on the older side",
    "over 40 years old",
    "under 40 years old"],

    ["alive",
    "deceased"]
    ]:
        all_questions.append(QuestionGroup(IS, proto_group, True))
        
    all_questions.append(QuestionGroup(IS, 
    ["an actor",
    "a musician",
    "a businessperson",
    "a salesperson",
    "a scientist",
    "an artist",
    "a politician",
    "an activist",
    "a vegetarian or vegan",
    "an athlete",
    "funny",
    "married",
    "divorced",
    "well-liked",
    "religious",
    "controversial",
    "retired",
    "considered good looking",
    "on TV a lot",
    "considered a good role model"],
    False))

    all_questions.append(QuestionGroup(DOES, 
    ["have dark hair",
    "have blonde hair",
    "have red hair",
    "have dyed hair"], 
    True))

    all_questions.append(QuestionGroup(DOES,
    ["own a restaurant",
    "own a beauty parlor",
    "own multiple buildings",
    "own a sports team",
    "work with animals",
    "do a lot of charity work",
    "have siblings",
    "have a mustache",
    "have a beard",
    "have children",
    "appear in commercials",
    "usually wear a hat",
    "travel a lot",
    "have pets",
    "speak multiple languages",
    "wear fancy clothes",
    "lead a team of other people"],
    False))

    all_questions.append(QuestionGroup(HAS,
    ["written books",
    "written songs",
    "recieved an award",
    "fought in a war",
    "been portrayed in a movie",
    "taught classes",
    "made history"],
    False))

    all_questions.append(QuestionGroup(WOULD,
    ["be recognized by children",
    "be recognized by your parents"],
    False))
    
    return all_questions

DIMENSION = 128

BACKGROUND = b'''
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
'''

ICON = b'''
iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACoSURBVDhPtZLBDYUgDIY7ixuY
eGUNvLmBC3jtFC8M4A5s4Aiu4BL/ax/PxGhFjPHwHUrLR6HQZ17whLcEE3zbgIgSdQcfrTpTIJvrBj5MKY6jxCqSNUNyFERGtS/+rRGq4S/dYHQwwsmJbu1AuSc4woO+R4feyBUIpKOT
+yuXgl6m4YKdUy4EMgHj3lvygsCnra8UPWKOjEA/lP5CBpv5xJuCMh4KFnwB0zIs5gyxGBcAAAAASUVORK5CYII=
'''
