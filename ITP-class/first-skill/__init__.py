from mycroft import MycroftSkill, intent_handler
import torch
import transformers
from transformers import GPT2Tokenizer, GPT2LMHeadModel


model_path = "/opt/mycroft/skills/first-skill/gpt2"

# =============================
# Necessary Code
class FirstSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.log.info("Loading Model")
        self.model = GPT2LMHeadModel.from_pretrained(model_path)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.log.info("Model and Tokenizer Loaded Successfully!")
# =============================

    # This is where main part of your stuff will happen
    # CUSTOM CODE
    # ==============================================
    @intent_handler("first.intent") #NOTE: NOTICE THE CHANGE HERE
    def handle_intent(self, message):
        # Do smth
        self.speak("nothing much")
        # Capture human response
        human_said = self.get_response("what would you like to talk about")

        max_length = 50 # length of generated text
        temperature = .9 # sanity

        tokenized = self.tokenizer.encode(human_said, return_tensors="pt")
        generate = self.model.generate(tokenized, do_sample=True, max_length=max_length, temperature=temperature, top_k=50)
        response = self.tokenizer.decode(generate[0, 0:].tolist(), clean_up_tokenization_spaces=True, skip_special_tokens=False)
        
        response = response.replace(human_said, "")
        response = response.rsplit('.', 1)[0] + "."

        # speak out generated text
        self.speak(response)

    # ==============================================

# ============================
# Necessary Code
def create_skill():
    return FirstSkill()
# ============================
