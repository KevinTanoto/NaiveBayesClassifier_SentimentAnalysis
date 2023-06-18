from nltk.probability import FreqDist
from nltk.corpus import stopwords, wordnet
from nltk.chunk import ne_chunk
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier, accuracy
import random
import pickle
from nltk.tag import pos_tag

def create_model():
    positive = open("positive(1).txt").read()
    negative = open("negative(1).txt").read()

    pos_word = word_tokenize(positive)
    neg_word = word_tokenize(negative)

    stop_word = stopwords.words('english')

    pos_word = [w for w in pos_word if w not in stop_word]
    neg_word = [w for w in neg_word if w not in stop_word]

    all_words  = pos_word

    for i in neg_word:
        all_words.append(i)

    all_words = [w for w in all_words if w not in [",",".","?","!"]]

    all_words = FreqDist(all_words)

    # fd = all_words.most_common(10)

    # return fd


    word_feature = list(all_words.keys())

#     # word_feature = list(all_words.keys())[:5]

#     # fd = all_words.most_common(3)

    document = []

    for sent in positive.split("\n"):
        document.append((sent, "positive"))

    for sent in negative.split("\n"):
        document.append((sent, "negative"))

    feature_sets =[]
    # tes_feature = []

    for sent, label in document:
        feature  ={}

        words = word_tokenize(sent)
        for w in word_feature:
            feature[w] = (w in words)
            # if w in words:
            #     tes_feature.append((words, w))
        feature_sets.append((feature,label))


    random.shuffle(feature_sets)

    train_count = int(0.9 * len(feature_sets))

    train_data = feature_sets[:train_count]
    test_data =  feature_sets[train_count:]

    classifier = NaiveBayesClassifier.train(train_data)

    print(accuracy(classifier, test_data) * 100)

    file = open("mymodel.pickle", "wb")
    pickle.dump(classifier, file)
    file.close()

    return classifier

def analysis_res():
    
    inp = str(input("Show Analysis Result [yes/no]<case sensitive>: "))
    if inp == "yes":

        inpss = word_tokenize(inp_op)
        tags = pos_tag(inpss)
        fd = FreqDist(inpss)
        freqdist_res = fd.most_common()

        print("Word\tTag\tAntonyms\tFrequency\n")
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
            
            print("{}\t{}\t{}\t{}\n".format(name, tags[n][1], res1 ,count))

        entity = ne_chunk(tags)
        entity.draw()

def load_model():

    try:
        file = open("mymodel.pickle","rb")
        classifier  = pickle.load(file)
        file.close()
    except:
        print("File doesn't exist")
        print('training data...')
        classifier = create_model()

    return classifier

def insert_op():
    
    while True:
        inp =  str(input("Insert Your Opinion [5-30]: "))
        if len(inp) >= 5 and len(inp) <= 30:
            opinion_list.append(inp)
            break
     


inp = 0
opinion_list = []

while inp != 3:

    if len(opinion_list) == 0:
        print("No Opinion Inserted")
    else:
        for n, i in enumerate(opinion_list):
            print("{}. {}".format( n +1, i))


    print("\nOpinion List")
    print("1. Insert Opinion")
    print("2. Analyze Opinion")
    print("3. Exit\n")

    inp = int(input("Choose [1-3]: "))
    if inp == 1:
        insert_op()
    if inp == 2:
        if len(opinion_list) == 0:
            print("Insert Opinion First \n")
        else:
            inps = int(input(f"Choose Opinion [{1} - {len(opinion_list)}]: "))
            inp_op = opinion_list[inps-1]

            wordsss = word_tokenize(inp_op)

            pos = 0
            neg = 0

            for w in wordsss:
                result = load_model().classify(FreqDist(w))
                print(w,result)
                if result == "pos":
                    pos += 1
                elif result == "neg":
                    neg += 1
            
            if neg > pos:
                print("Your Opinion is categorized as negative \n")
            elif neg < pos:
                print("Your Opinion is categorized as positive \n")
            else:
                print("Your Opinion is categorized as neutral \n")

            analysis_res()