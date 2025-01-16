# Taking file input from command line
import sys
import nltk
import string
import matplotlib.pyplot as plt

# nltk.download("stopwords")

# Opening the file based on the text argument
try:
    if ".txt" not in sys.argv[1]:
        raise Exception(
            "Should be of the form: python normalize_text.py myfile.txt (<your-options>)"
        )

    # Reading the contents of the file and closing it after we're done
    file = open(sys.argv[1])
    content = file.read()
    file.close()

    # Initializing the pre-processors with empty values
    stemmer = None
    lemmatizer = None
    lower = False
    stopwords = None
    punctuation = False

    # Assigning values to the pre-processors which had their flags given by the user
    for arg in sys.argv:
        match arg:
            case "-s":
                # If flag -s was given then a stemmer object would be assigned to the stemmer variable
                stemmer = nltk.stem.PorterStemmer()
            case "-lr":
                # If flag -lr was given then a lemmatizer object would be assigned to the lemmatizer variable
                lemmatizer = nltk.stem.WordNetLemmatizer()
            case "-l":
                # If flag -l was given then the lower flag would be assigned a value of True
                lower = True
            case "-st":
                # If flag -st was given then a list of all possible stopwords would be assigned to the stopwords variable
                stopwords = nltk.corpus.stopwords.words("english")
            case "-p":
                # If flag -p was given then the punctuation flag would be assigned a value of True
                punctuation = True

    # Tokenize
    tokens = nltk.word_tokenize(content)

    # Below we process for all the flags that the user wanted i.e. value not null or false

    if lower:
        tokens = [token.lower() for token in tokens]

    if stemmer:
        tokens = [stemmer.stem(token) for token in tokens]

    if lemmatizer:
        # For the lemmatizer we're also performing POS tagging, reasons for which are mentioned in the pdf document

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
        # punctuations needed to be including with certain symbols which were in the text file but not counted as part of the python string.punctuation list
        extended_punctuation = string.punctuation + ",.;“’--”!*:?...."
        tokens = [token for token in tokens if token not in extended_punctuation]

    # Creating a dictionary which would include the word and its corresponding word count
    word_count = {}

    # Looping through all tokens, checking if the token exists in the dictionary then increment its value(count) by 1 or just initialize it with a value of 1
    for token in tokens:
        if token in word_count:
            word_count[token] += 1
        else:
            word_count[token] = 1

    # Sorting the tokens according to their count
    sorted_word_count = sorted(word_count.items(), key=lambda kv: kv[1], reverse=True)

    # print("Number of tokens : " + str(sum(word_count.values())))      # Uncomment if you want to check the number of tokens remaining after pre-processing

    # Creating two arrays which would be used to plot data
    s_tokens = []
    s_count = []

    for token, count in sorted_word_count:
        s_tokens.append(token)
        s_count.append(count)

        # token, count is the main output of this file
        print(token, count)

    # Plotting the data and using a log-scale for the x and y axes
    plt.figure(figsize=(10, 6))
    plt.bar(s_tokens, s_count)
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Word Frequency", fontsize=14)
    plt.xlabel("Tokens", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.show()


except FileNotFoundError:
    print("Error: File not found. Please check the file path.")
except Exception as e:
    print(e)
