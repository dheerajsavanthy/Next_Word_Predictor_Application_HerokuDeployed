#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st

st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=50)

st.write(
    """
    # AIDI 1002-02 AI ALGORITHMS FINAL PROJECT
    Welcome to our Next Word Predictor! :wave:

    This app is built with some interesting piece of code we've worked and 
    collaborated on as a team. Plus there's a peek at behind the scenes — we stored
    in our [repository](https://github.com/dheerajsavanthy/HerokuDeploy), if you're curious to know :wink:

    For this interface, we've used the help of Streamlit's amazing community which has
    always been our best source of ideas. So if anything listed here catches your eye,
    ask about it in their [forums](https://discuss.streamlit.io)!
    """
)

st.warning(
    """
    ✏️ **NOTE:** The suggestions given by the predictor are based on some books. While we're happy with the results, it may not align with your **writing style** yet :wink:
"""
)

st.markdown("<br>", unsafe_allow_html=True)


"""
# Next Word Generator
[![Star](https://img.shields.io/github/languages/code-size/dheerajsavanthy/HerokuDeploy)](https://github.com/dheerajsavanthy/HerokuDeploy)	
"""
st.markdown("<br>", unsafe_allow_html=True)


train_data = 'republic.txt'

first_possible_words = {}
second_possible_words = {}
transitions = {}

def expandDict(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)
    
def get_next_probability(given_list):   #returns dictionary
    probability_dict = {}
    given_list_length = len(given_list)
    for item in given_list:
        probability_dict[item] = probability_dict.get(item, 0) + 1
    for key, value in probability_dict.items():
        probability_dict[key] = value / given_list_length
    return probability_dict

def trainMarkovModel():
    for line in open(train_data, encoding="utf8"):
        tokens = line.rstrip().lower().split()
        tokens_length = len(tokens)
        for i in range(tokens_length):
            token = tokens[i]
            if i == 0:
                first_possible_words[token] = first_possible_words.get(token, 0) + 1
            else:
                prev_token = tokens[i - 1]
                if i == tokens_length - 1:
                    expandDict(transitions, (prev_token, token), 'END')
                if i == 1:
                    expandDict(second_possible_words, prev_token, token)
                else:
                    prev_prev_token = tokens[i - 2]
                    expandDict(transitions, (prev_prev_token, prev_token), token)
    
    first_possible_words_total = sum(first_possible_words.values())
    for key, value in first_possible_words.items():
        first_possible_words[key] = value / first_possible_words_total
        
    for prev_word, next_word_list in second_possible_words.items():
        second_possible_words[prev_word] = get_next_probability(next_word_list)
        
    for word_pair, next_word_list in transitions.items():
        transitions[word_pair] = get_next_probability(next_word_list)
    

def next_word(tpl):
    #print(transitions)
    if(type(tpl) == str):   #it is first word of string.. return from second word
        d = second_possible_words.get(tpl)
        if (d is not None):
            return list(d.keys())
    if(type(tpl) == tuple): #incoming words are combination of two words.. find next word now based on transitions
        d = transitions.get(tpl)
        if(d == None):
            return []
        return list(d.keys())
    return None #wrong input.. return nothing
    

trainMarkovModel()  #generate first, second words list and transitions

########## demo code below ################
print("Usage: start typing.. program will suggest words. Press tab to chose the first suggestion or keep typing\n")

c=st.text_input("Type your word here")
sent=''
last_suggestion=[]
sent = sent.join(c)
tkns = sent.split()

if st.button('Predict next word(s)'):
    if(len(tkns)<2):
        last_suggestion = next_word(tkns[0].lower())
        st.write(last_suggestion[0])
    else:
        last_suggestion = next_word((tkns[-2].lower(), tkns[-1].lower()))
        sent = sent + " " + last_suggestion[0] 
        st.write(last_suggestion[0])

st.image("https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/twitter/259/mage_1f9d9.png", width=50)
