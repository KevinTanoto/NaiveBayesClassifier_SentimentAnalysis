import streamlit as st
import pickle

import nltkmodules

from nltk.probability import FreqDist
from nltk.chunk import ne_chunk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet

st.title("Sentiment Analysis with Naive Bayes Classifier: Extracting Sentiment, Named Entities, and Antonyms")

st.write("In this project, we develop a sentiment analysis system using a Naive Bayes classifier. The system takes textual input and determines whether the sentiment expressed is negative, positive, or neutral. But it doesn't stop there. Our system goes beyond sentiment analysis and offers additional insights.") 

st.write("Alongside sentiment classification, our program utilizes natural language processing techniques to enhance the analysis. It employs Named Entity Recognition (NER) to extract important entities from the text using the ne_chunk.")

st.write("Furthermore, the program provides an intriguing feature by generating antonyms for the words present in the input sentences. Antonyms offer an interesting contrast, allowing us to explore the opposite sentiment and uncover additional insights within the text.")

st.write("Through this project, we aim to create a comprehensive sentiment analysis solution that goes beyond simple sentiment classification. By incorporating NER and antonym generation, we enable users to gain a more holistic understanding of the text and unlock valuable insights from their data.")

st.write("Model Accuracy: 79.4751")

file = open("mymodel.pickle","rb")
model  = pickle.load(file)


input_text = st.text_area("Enter a sentence:")
if st.button("Analyze Sentiment"):
    if input_text:
        # Apply the model to the user input
        sentiment = model.classify(FreqDist(input_text))

        st.success(f"Sentiment: {sentiment}")
    else:
        st.warning("Please enter a sentence for sentiment analysis.")


inpss = word_tokenize(input_text)
# inpss = input_text.split()
tags = pos_tag(inpss)
fd = FreqDist(inpss)
freqdist_res = fd.most_common()

table_data = [["Word", "Tag", "Antonyms", "Frequency"]]
for n,(name,count) in enumerate(freqdist_res) :

    
    synsets = wordnet.synsets(name)
    test = []
    for synset in synsets:
        for i in synset.lemmas():
            anto = [i.name() for i in i.antonyms()]
            test += anto

    # print(test)

    if test:
        res1 = test[0]
    else:
        res1 = "-"
    
    table_data.append([name, tags[n][1], res1, count])

st.table(table_data)


st.write("Named Entity Recognition: ")
entity = ne_chunk(tags)
st.table(entity)