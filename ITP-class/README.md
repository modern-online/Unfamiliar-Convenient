# Mycroft skills/scripts as course templates

Please refer to [Mycroft](https://mycroft.ai/) open-source voice-assistant platform's website for more information.  


### Narrator Skill

The skill uses natural-language-processing (gpt-2) to give an 'opinion' on a topic determined by the human. It is a conversation-type skill with two levels of interaction. 

Additional Python modules required for running the script are [Transformers](https://github.com/huggingface/transformers) and Pytorch.
The modules need to be installed inside Mycroft's default virtual environment (source /mycroft-core/.venv/bin/activate) to work. 
The skill needs to be placed in /opt/Mycroft/skills folder as per Mycroft's documentation.

### Fallback Skill

The fallback skill, originally coded by [Claire Glanois](https://github.com/claireaoi), adapted for NYU-ITP spring semester class 2021. 

The skill uses natural-language-processing (gpt-2) to generate random answers for questions/utterances it cannot understand.

Additional Python modules required for running the script are [Transformers](https://github.com/huggingface/transformers) and Pytorch.
The modules need to be installed inside Mycroft's default virtual environment (source /mycroft-core/.venv/bin/activate) to work. 
The skill needs to be placed in /opt/Mycroft/skills folder as per Mycroft's documentation.

### piggyback.py 

When a human utterance is detected and resolved by Mycroft, this 'plug-in' forces additional 'contextualisation' in a domain of choice. For example, if you ask Mycroft to look up 'Planet Jupiter', after providing the original answer it will provide additional information within a context ('popcorn' by default).

This is done by:
1) Capturing human utterance via Mycroft before adequate skillsget triggered,
2) Extracting keywords from utterace via NLP, 
3) Summing extracted keywords with chosen context keywords, 
4) Executing a Google search and retrieving links (5 by default),
5) Picking a random link, downloading its contents (HTML),
6) Parsing the page, extracting summary with the help of NLP,
7) Sending (emitting) text to Mycroft after the original inquiry has been answered

Additional modules used: googlesearch, newspaper, nltk, spacy. 
These need to be installed inside Mycroft's activated virtual environment (source /mycroft-core/.venv/bin/activate).
The script also needs to be launched from within the environment. 

If running for the first time, don't forget to download the scapy model (for keyword extraction): python3 -m spacy download en_core_web_sm (this is a small model, you have other models, so check Scapy docs)
