## Files

- **dracula-novel.txt**: The full text of Bram Stoker’s Dracula downloaded from Project Gutenberg which serves as the input text file.
- **normalize_text.py**: The python file which contains the full code required for the text normalization done in this project.
- **output.txt**: A text file which serves as a reference for the sample output mentioned in the report.
- **README.md**: Provides an explanation for how to run the code and the files existing in this folder.
- **Report.pdf**: Serves as a detailed project report.

## Project Overview and Report

This project includes a normalize_text.py module that performs text preprocessing tasks. While it's currently tailored to work within this specific repository and not configured to handle arbitrary inputs out of the box, it can be easily adapted to process any text file with minimal changes, primarily by modifying the input parsing logic. The module has been successfully tested on a sample dataset from **Project Gutenberg**, and the results are documented in the accompanying `Report.pdf`, which also provides a comprehensive breakdown of the design decisions, preprocessing steps, and implementation details.

## Prerequisites

1. **Python 3.10** or higher is required for compatibility with the `match...case` syntax, which was introduced in **Python 3.10**.
2. **NLTK** (Natural Language Toolkit) must be installed on your machine. You can install it via `pip`:
3. `matplotlib` library must also be installed on your machine.

```python
pip install nltk
```

The code already handles downloading the necessary resources like stopwords using:

```python
nltk.download('stopwords')
```

## Running the code

You can run the code by writing the following command in your terminal:

```
python3 normalize_text.py dracula-novel.txt [<your-options>]
```

**<your-options>** are optional flags you can give which can run various preprocessors on the input text file.

### Preprocessor options are:-

- `-s` for stemmer
- `-lr` for lemmatizer
- `-l` for lowercase
- `-st` for stopwords
- `-p` for punctuation
