"""
Name: normalize_text.py
Description: text file/corpus preprocessor and plotter
Instructions to run:
    python normalize_text.py myfile.txt <your-options>

    If it doesn't work try writing:
        python3 normalize_text.py myfile.txt <your-options>

    <your-options> for preprocessors could be:
        -s for stemmer
        -lr for lemmatizer
        -l for lowercase
        -st for stopwords
        -p for punctuation
"""

# Taking file input from command line
import sys
import nltk
import string
import matplotlib.pyplot as plt

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")

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

    # Initializing the preprocessors with empty values
    stemmer = None
    lemmatizer = None
    lower = False
    stopwords = None
    punctuation = False

    # Assigning values to the preprocessors which had their flags given by the user
    for arg in sys.argv[2:]:
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
        # For the lemmatizer we're also performing POS tagging, reasons for which are mentioned in detail in the discussion section of the report

        """
            This function takes in a tag which could be of the form JJ, VB, NN, RB, etc. and returns an ntlk.corpus.wordnet form
            to put inside the pos parameter of the lemmatize object.
        """

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

        # Creates a tuple which has the token and its Part Of Speech tag
        pos_tags = nltk.pos_tag(tokens)

        # Unpacking the pos_tags tuple for token, tag and then feeding the tag as an input to the get_wordnet_pos() in order to retrieve the pos value which will be used inside the lemmatizer
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

    # print("Number of tokens : " + str(sum(word_count.values())))  # Uncomment if you want to check the number of tokens remaining after preprocessing

    # Creating two arrays which would be used to plot data
    first_tokens = []
    first_count = []
    last_tokens = []
    last_count = []
    all_tokens = []
    all_count = []

    iterator_for_last_count = 0

    for token, count in sorted_word_count:
        all_tokens.append(token)
        all_count.append(count)

        if len(first_tokens) < 25:
            first_tokens.append(token)

        if len(first_count) < 25:
            first_count.append(count)

        if iterator_for_last_count >= (len(sorted_word_count) - 25):
            last_tokens.append(token)
            last_count.append(count)

        # token, count is the main output of this file
        if iterator_for_last_count < 25 or iterator_for_last_count >= (
            len(sorted_word_count) - 25
        ):
            if iterator_for_last_count == 0:
                print("The top 25 tokens with the highest word count:")
                print("             ---------------                  ")

            if iterator_for_last_count == len(sorted_word_count) - 25:
                print(" ")
                print("The bottom 25 tokens with the lowest word count:")
                print("             ---------------                  ")

            print(token, count)

        iterator_for_last_count += 1

    # Plotting the data for the top 25 word frequencies
    plt.figure(figsize=(13, 8))
    plt.bar(first_tokens, first_count)
    plt.title("Word frequency for the top 25 words", fontsize=14)
    plt.xlabel("Tokens", fontsize=8)
    plt.ylabel("Frequency", fontsize=8)
    plt.xticks(rotation=45, ha="right")
    plt.show()

    # Plotting the data for the last 25 word frequencies
    plt.figure(figsize=(13, 8))
    plt.bar(last_tokens, last_count)
    plt.title("Word frequency for the bottom 25 words", fontsize=14)
    plt.xlabel("Tokens", fontsize=8)
    plt.ylabel("Frequency", fontsize=8)
    plt.xticks(rotation=45, ha="right")
    plt.show()

    # Plotting the data for the all words log scaled
    plt.figure(figsize=(13, 8))
    plt.bar(all_tokens, all_count)
    plt.title("Word frequency for all words log scaled", fontsize=14)
    plt.xlabel("Tokens", fontsize=8)
    plt.ylabel("Frequency", fontsize=8)
    plt.xscale("log")
    plt.yscale("log")
    plt.xticks(rotation=45, ha="right")
    plt.show()

except FileNotFoundError:
    print("Error: File not found. Please check the file path.")
except Exception as e:
    print(e)
