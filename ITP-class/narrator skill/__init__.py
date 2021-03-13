# !/usr/local/bin/python3
# -*- coding: utf-8 -*-

# Vytas Jankauskas 2021
# Unfamiliar Convenient Project, in collaboration with Claire Glanois
# Project page: https://vjnks.com/works/unfamiliar-convenient-project-in-progress-46
# Repo: https://github.com/modern-online/Unfamiliar-Convenient/tree/main/ITP-class

# The script runs on Mycroft framework and requires Mycroft's virtual environment to work
# More on Mycroft: https://github.com/MycroftAI
# Primary module to communicate via Mycroft: mycroft-message-bus
# Additional modules used: transformers, torch

# This script was developed as one of educational templates into using Mycroft
# as part of 2021 NYU ITP spring semester class.


"""
The script allows to have a small conversation with the voice assistant,
generating some random outcomes based on gpt-2 text generation

"""


from mycroft import MycroftSkill, intent_file_handler

# Import machine learning modules
import torch  # pyTorch
import transformers  # huggingFace Transformers module
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Once you have your own model, adjust these accordingly
my_ML_model = False  # If do have a fine-tuned model, set to True
# Global path_finetuned_ML_model
my_ML_model_path = '/gpt2'  # path to your fine tuned model

# Increase the likelihood of high probability words by lowering the temperature (aka make it sound more 'normal')
temperature = 0.9
# Repetition penalty. In general makes sentences shorter and reduces repetition of words an punctuation.
repetition_penalty = 2
# Number of beams for 'beam search'
num_beams = 5


class Narrator(MycroftSkill):
    # initialiser that loads the skill into Mycroft system
    def __init__(self):
        MycroftSkill.__init__(self)

        # Initialize language generation model
        if my_ML_model:
            print("Loading my own machine learning model")
            self.model = GPT2LMHeadModel.from_pretrained(my_ML_model_path)

        else:
            print("Loading generic GPT-2 model")
            self.model = GPT2LMHeadModel.from_pretrained("distilgpt2")

        # Initialise a tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")

    # When the voice assistant's skill is called via designated phrase,
    # this get's triggered, and then tells what to do next
    @intent_file_handler('narrator.intent')
    def handle_narrator(self, message):
        self.speak_dialog('narrator', wait=True)

        # prompt human for input and use it as 'seed' for machine learning
        seed = self.get_response('Give me something to work with')
        self.log.info("SEED: " + seed)

        # brainstorm
        answer = self.generate_answer(seed, length_drift=40)

        # speak response aloud and wait for further comment from human
        self.speak_dialog(answer, wait=True)

        # gather additional input from the human
        additional_thoughts = self.get_response("Any further thoughts?")
        self.log.info("FURTHER THOUGHTS: " + additional_thoughts)

        if additional_thoughts:
            # sum all previous conversation data
            final_context = seed + answer + additional_thoughts

            # Final brainstorm
            final_brainstorm = self.generate_answer(
                final_context, length_drift=50)
            self.speak_dialog(final_brainstorm)

        else:
            self.speak_dialog(
                'Nothing more it say it seems. End of conversation.')

    # generates answer using machine learning
    def generate_answer(self, seed, length_drift):

        encode = self.tokenizer.encode(seed, return_tensors="pt")
        generate = self.model.generate(
            encode, max_length=length_drift, num_beams=num_beams, early_stopping=True, no_repeat_ngram_size=repetition_penalty, temperature=temperature)
        response = self.tokenizer.decode(generate[0, 0:].tolist(),
                                         clean_up_tokenization_spaces=True, skip_special_tokens=False)

        # Text cleaning function to go here
        # response = clean_text(seed, response)
        self.log.info("RESPONSE: " + response)
        return response


# simply cleans up machine-generated text
def clean_text(seed, response):
    # remove the question text from the generated answer
    output = response.replace(seed, '')
    # remove incomplete sencentes at the end, if any.
    output = output.rsplit('.', 1)[0]
    return output


def create_skill():
    return Narrator()
