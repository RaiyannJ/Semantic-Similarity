import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    sim = 0.0
    x = 0.0
    for k in vec1:
        if k in vec2:
            x+= vec1.get(k)*vec2.get(k)

    sim = x/(norm(vec1)*norm(vec2))

    return sim

def build_semantic_descriptors(sentences):
    d = {}

    for sentence in sentences:
        for word in sentence:
            if word not in d.keys():
                d[word] = {}
            if word in d.keys():
                for word2 in sentence:
                    if word != word2:
                        if word2 in d[word]:
                            d[word][word2] += 1
                        else:
                            d[word][word2] = 1

    return d

def build_semantic_descriptors_from_files(filenames):
    sentences = []

    for file in filenames:
        f = open(file, "r", encoding="latin1").read().lower()
        f = f.replace(",",  " ")
        f = f.replace("-",  "")
        f = f.replace("--",  " ")
        f = f.replace(":",  " ")
        f = f.replace(";",  " ")
        f = f.replace("!", ". ")
        f = f.replace("?", ". ")
        f = f.replace("\n", "")

        f = f.split(".")
        for line in f:
            wordList = line.split()

            for words in wordList:
                if not words.isalpha():
                    wordList.remove(words)
            sentences.append(wordList)

    return build_semantic_descriptors(sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    sim = []
    maxSim = 0
    word = word.lower()
    if word not in semantic_descriptors:
        return choices[0]

    for choice in choices:
        choice = choice.lower()

        if choice not in semantic_descriptors:
            sim.append(-1)
        elif norm(semantic_descriptors[choice]) == 0:
            sim.append(0)
        else:
            sim.append(similarity_fn(semantic_descriptors[word],semantic_descriptors[choice]))

    maxSim = max(sim)
    location = sim.index(maxSim)

    return choices[location]

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    questions = []
    correct = []

    f = open(filename, "r", encoding="latin1").read().lower()
    f = f.split("\n")

    for line in f:
        questions.append(line.split(" "))

    for question in questions:
        if most_similar_word(question[0], question[2:], semantic_descriptors, similarity_fn) == question[1]:
            correct.append(1)

        else:
            correct.append(0)
    return (sum(correct)/len(correct))*100
