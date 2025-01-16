# Taking file input from command line
import sys
import nltk
import string

# nltk.download("stopwords")

file = open(sys.argv[1])
content = file.read()
file.close()

stemmer = None
lemmatizer = None
lower = False
stopwords = None
punctuation = False

for arg in sys.argv:
    match arg:
        case "-s":
            stemmer = nltk.stem.PorterStemmer()
        case "-lr":
            lemmatizer = nltk.stem.WordNetLemmatizer()
        case "-l":
            lower = True
        case "-st":
            stopwords = nltk.corpus.stopwords.words("english")
        case "-p":
            punctuation = True

# Tokenize
tokens = nltk.word_tokenize(content)

if lower:
    tokens = [token.lower() for token in tokens]

if stemmer:
    tokens = [stemmer.stem(token) for token in tokens]

if lemmatizer:

    def get_wordnet_pos(tag):
        if tag.startswith("J"):
            return nltk.corpus.wordnet.ADJ
        elif tag.startswith("V"):
            return nltk.corpus.wordnet.VERB
        elif tag.startswith("N"):
            return nltk.corpus.wordnet.NOUN
        elif tag.startswith("R"):
            return nltk.corpus.wordnet.ADV
        else:
            return None

    pos_tags = nltk.pos_tag(tokens)

    tokens = [
        lemmatizer.lemmatize(token, pos=pos) if pos else token
        for token, tag in pos_tags
        for pos in [get_wordnet_pos(tag)]
    ]


if stopwords:
    tokens = [token for token in tokens if token.lower() not in stopwords]

if punctuation:
    extended_punctuation = string.punctuation + ",.;“’--”!*:?...."
    tokens = [token for token in tokens if token not in extended_punctuation]

word_count = {}

for token in tokens:
    if token in word_count:
        word_count[token] += 1
    else:
        word_count[token] = 1

sorted_word_count = sorted(word_count.items(), key=lambda kv: kv[1], reverse=True)

for token, count in sorted_word_count:
    print(token, count)

# print("Number of tokens : " + str(sum(word_count.values())))
