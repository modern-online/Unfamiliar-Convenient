from mycroft import MycroftSkill, intent_handler

# =============================
# Necessary Code
class FirstSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
# =============================

    # This is where main part of your stuff will happen
    # CUSTOM CODE
    # ==============================================
    @intent_handler("first.intent") #NOTE: NOTICE THE CHANGE HERE
    def handle_intent(self, message):
        # Do smth
        self.speak("nothing much")
    # ==============================================

# ============================
# Necessary Code
def create_skill():
    return FirstSkill()
# ============================
