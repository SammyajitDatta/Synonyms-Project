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
    magnitudeVec1, magnitudeVec2 = map(norm,(vec1,vec2))
    dotProductV1V2 = 0
    for key in vec1:
        if key in vec2.keys():
            dotProductV1V2 += vec1[key] * vec2[key]
    return dotProductV1V2/(magnitudeVec1*magnitudeVec2)

def build_semantic_descriptors(sentences):
    semantic_descriptors_dictionary = {}
    words = []
    dict_map = {}
    for s in sentences:
        for w in s:
            if w not in dict_map:
                dict_map[w] = len(words)
                words.append(w)
    sentences = [sorted([dict_map[i] for i in s if len(i) > 0])
                 for s in sentences if len(s) > 0]
    out_dict = [{} for i in range(len(words))]
    for s in sentences:
        if len(s) == 1:
            continue
        wordSet = [s[0]]
        for j in range(len(s)-1):
            if s[j] != s[j+1]:
                wordSet.append(s[j+1])
        for j in range(len(wordSet)):
            for k in range(j+1, len(wordSet)):
                out_dict[wordSet[j]][wordSet[k]] = out_dict[wordSet[j]].get(wordSet[k], 0) + 1
    for i in range(len(words)):
        semantic_descriptors_dictionary[words[i]] = {}
    for i in range(len(words)):
        for j, val in out_dict[i].items():
            semantic_descriptors_dictionary[words[i]][words[j]] = val
            semantic_descriptors_dictionary[words[j]][words[i]] = val

    return semantic_descriptors_dictionary


#Under assumption that hyphenated words such as ex-husband become exhusband.

def build_semantic_descriptors_from_files(filenames):
    sentences = []
    for i in range(len(filenames)):
        file = open(filenames[i], "r", encoding="latin1")
        strippedSentences = file.read().lower()
        strippedSentences = strippedSentences.replace("!",".")
        strippedSentences = strippedSentences.replace("?", ".")
        strippedSentences = strippedSentences.replace(",", " ")    
        strippedSentences = strippedSentences.replace("--"," ")
        strippedSentences = strippedSentences.replace(":", " ")
        strippedSentences = strippedSentences.replace(";", " ")
        strippedSentences = strippedSentences.replace("-", " ")
        strippedSentences = strippedSentences.replace("\n", " ")
        sentences+=[splitwords.split() for splitwords in strippedSentences.split(".") if splitwords != ""]
        file.close()
    return build_semantic_descriptors(sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    bestSimilarty = -2
    empty = ""
    if word.lower() not in semantic_descriptors.keys():
        return choices[0]
    current_similarity = 0
    for i in range(len(choices)):
        if choices[i].lower() not in semantic_descriptors.keys():
            current_similarity = -1
        else:
            current_similarity = similarity_fn(semantic_descriptors[word.lower()],semantic_descriptors[choices[i].lower()])
        if current_similarity > bestSimilarty:
            bestSimilarty = current_similarity
            empty = choices[i]
    return empty
        
def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    file = open(filename, "r", encoding="latin1")
    fileLines = file.read().lower().split("\n")
    correct = 0
    total = len(fileLines)
    fileLines = [i.split() for i in fileLines]
    for i in range(len(fileLines)):
        if most_similar_word(fileLines[i][0],fileLines[i][2:],semantic_descriptors,similarity_fn) == fileLines[i][1]:
            correct+=1
    file.close()
    return correct*100/total

if __name__ == "__main__":
    semantic_desc = build_semantic_descriptors_from_files(["sw.txt", "wp.txt"])
    res = run_similarity_test("test.txt", semantic_desc, cosine_similarity)
    print(res, "% of the guesses were correct.")
    #The code runs around roughly 3 seconds on most computers.
