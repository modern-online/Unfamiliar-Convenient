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
The script allows to ask a question within a specific context;
upon specifying the context, information is retrieved from Wiki,
at which point VA uses NLP to answer a specific question you 
might have in mind.

"""

from mycroft import MycroftSkill, intent_file_handler

# Import machine learning modules
import torch  # pyTorch
import transformers  # huggingFace Transformers module
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import wikipedia  # wikipediaAPI
import re


class Chatbot(MycroftSkill):
    # Initialiser that loads the skill into Mycroft system
    def __init__(self):
        MycroftSkill.__init__(self)
        # Use this instead of 'print' within a skill
        self.log.info("Loading Distilbert")
        # Initialize language generation model
        self.model = DistilBertForQuestionAnswering.from_pretrained(
            'distilbert-base-uncased-distilled-squad')
        # Initialise a tokenizer
        self.tokenizer = DistilBertTokenizer.from_pretrained(
            'distilbert-base-uncased-distilled-squad')
        self.log.info("Distilbert Loaded Successfully")

    # When the voice assistant's skill is called via designated phrase,
    # this get's triggered, and then tells what to do next
    @intent_file_handler('chatbot.intent')
    def handle_chatbot(self, message):
        # greet human with dialogue
        self.speak_dialog('chatbot', wait=True)

        # Prompt human for keyword to look wikipedia
        keyword = self.get_response('What keyword should I look up?')

        # Look keyword up on Wikipedia
        try:
            page = wikipedia.page(keyword)
        except wikipedia.exceptions.DisambiguationError as alternatives:
            self.speak_dialog(
                "There are multiple associations for this keyword")
            keyword = self.get_response(
                "Do you mean " + alternatives.options + "?")
            page = wikipedia.page(keyword)

        # Take a summary of a wiki page
        content = page.summary  # Can instead use 'page.content' if you want a full Wiki page
        # Clean the text
        context = clean_text(content)

        # Now ask for a specific question
        question = self.get_response("Ok, now what is your specific question?")

        # Find answer with the help of NLP
        answer = self.find_answer(context, question)

        # Speak the answer out
        if answer:
            self.speak_dialog("The answer is: " + answer)
        else:
            # sometimes machine learning fails to find an answer, in which case it will just read the wiki summary
            self.speak_dialog(
                "I couldn't find a specific answer, so here's a summary from Wikipedia! " + context)

    def find_answer(self, context, question):
        # Tokenizer converts words and spaces into 'tokens' or sets of values
        # The max matrix of the particular model is 512 tokens (text elements);
        # max_length and trucation ensure the downloaded text does not surpass this limit
        inputs = self.tokenizer(
            question, context, truncation=True, max_length=512, return_tensors='pt')
        # A ML model predicts the probability of tokens that correspond to the question
        answer_start_scores, answer_end_scores = self.model(**inputs).values()
        # Argmax function finds the higest probability among the predicted ones
        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1
        # The IDs (values) are then converted back to tokens (words)
        find_corr_tokens = self.tokenizer.convert_ids_to_tokens(
            inputs['input_ids'][0][answer_start:answer_end])
        # Tokens are stitched back into a string
        answer = self.tokenizer.convert_tokens_to_string(find_corr_tokens)

        return answer


def clean_text(text):
    # removes multiple whitespace and covnerts to lowercase
    temp = ' '.join(text.split()).lower()
    # Regex that removes all non English alphabet, alphanumeric, or whitespace characters
    temp = re.sub(r'[^a-z0-9 ]+', '', temp)
    # Converts text to a raw string
    cleaned_text = r"""{}""".format(temp)
    return cleaned_text


def create_skill():
    return Chatbot()
