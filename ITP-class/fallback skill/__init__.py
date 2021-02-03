# !/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""

Mycroft Voice Assistant Fallback Skill that uses text generation 
(GPT-2 and Huggingface Transformers library) to provide answers 
to questions it does not understan.  

This script was written for the Unfamiliar Virtual Convenient - 
Growing your Voice Assistant workshop at the School of Machines, 
Berlin, led by Vytautas Jankauskas and Claire Glanois in early 2020.

The script needs Mycroft voice assistant installed
More on Mycroft: https://github.com/MycroftAI

Vytas has further adapted it for the 2021 NYU ITP Master's programme. 
Feel free to tune and shape it according to your project.

# Project page: 
# https://vjnks.com/works/unfamiliar-convenient-project-in-progress-46
# Repo: 
# https://github.com/modern-online/Unfamiliar-Convenient/tree/main/ITP-class

"""
# Mycroft fallback skill object
from mycroft.skills.core import FallbackSkill

import random

# Import machine learning modules
import torch  # pyTorch
import transformers  # huggingFace Transformers module
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# GPT-2 parameters

# Once you have your own model, adjust these accordingly
my_ML_model = False  # If do have a fine-tuned model, set to True
# Global path_finetuned_ML_model
my_ML_model_path = '/gpt2'  # path to your fine tuned model

# More parameters are available and more detail about gpt-2 parameters can be found here: https://huggingface.co/blog/how-to-generate
# Maximum length of the generated answer, counted in characters and spaces.
length_drift = 30
# Increase the likelihood of high probability words by lowering the temperature (aka make it sound more 'normal')
temperature = 0.7
# Repetition penalty. In general makes sentences shorter and reduces repetition of words an punctuation.
repetition_penalty = 2
# Number of beams for 'beam search'
num_beams = 5

# Required: Class constructor for Mycroft skills
# See https://mycroft-ai.gitbook.io/docs/skill-development/skill-types/fallback-skill fpr structure


class MLdriftFallback(FallbackSkill):

    def __init__(self):
        super(MLdriftFallback, self).__init__(name='Weird Answers Skill')

        # Initialize language generation model
        if my_ML_model:
            print("Loading my own machine learning model")
            self.model = GPT2LMHeadModel.from_pretrained(my_ML_model_path)
        else:
            print("Loading generic GPT-2 model")
            self.model = GPT2LMHeadModel.from_pretrained("distilgpt2")

        # Initialise a tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")

    def initialize(self):
        """
            Registers the fallback handler.
            The second argument is the priority associated to the request;
            Because there are several fallback skills available, priority helps
            to tell Mycroft how 'sensitively' this particular skill should be triggered.
            Lower number means higher priority, however number 1-4 are bypassing other skills.
        """
        self.register_fallback(self.handle_MLdrift, 6)

    def fantasize(self, question):
        """
            Generate a response
        """

        question += "? "

        # Say a splash phrase since the generation might take a while
        splash_phrases = ["Lemme think for a minute", "Give me a minute to think about my answer",
                          "I need some time to think about this", "Hold on while I think this through"]
        self.speak(random.choice(splash_phrases))

        opinion_tiggers = [" I", " My",
                           " To be honest,", " Frankly,", "Well,"]
        opinion = random.choice(opinion_tiggers)

        # Generate machine learning text based on parameters
        encode = self.tokenizer.encode(
            question + opinion, return_tensors="pt")
        generate = self.model.generate(
            encode, max_length=length_drift, num_beams=num_beams, early_stopping=True, no_repeat_ngram_size=repetition_penalty, temperature=temperature)
        response = self.tokenizer.decode(generate[0, 0:].tolist(),
                                         clean_up_tokenization_spaces=True, skip_special_tokens=True)
        print(response)

        # Text cleaning function to go here
        response = clean_text(question, response)

        # Speak generated text aloud
        self.speak(response)

    def handle_MLdrift(self, message):
        """
            Several gpt-2 drifts from the last utterance, with a possible mode
        """
        # Obtain what the human said
        utterance = message.data.get("utterance")
        # Only keep last part as context else too big? >>>
        self.fantasize(utterance)
        return True

    # Required: Skill creator must make sure the skill is removed when the Skill is shutdown by the system.
    def shutdown(self):
        """
            Remove the skill from list of fallback skills
        """
        self.remove_fallback(self.handle_MLdrift)
        super(MLdriftFallback, self).shutdown()


# simply cleans up machine-generated text
def clean_text(question, generated):
    # remove the question text from the generated answer
    output = generated.replace(question, '')
    # remove incomplete sencentes at the end, if any.
    output = output.rsplit('.', 1)[0] + '.'
    return output


def create_skill():
    return MLdriftFallback()
