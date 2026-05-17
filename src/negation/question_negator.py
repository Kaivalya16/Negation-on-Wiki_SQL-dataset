import spacy

nlp = spacy.load("en_core_web_sm")


AUXILIARIES = [
    "is", "are", "was", "were",
    "has", "have", "had",
    "can", "could",
    "will", "would",
    "should",
    "do", "does", "did"
]


def negate_question(question):

    doc = nlp(question)

    tokens = [token.text for token in doc]

    # -----------------------------------
    # STEP 1:
    # If auxiliary exists
    # insert NOT after auxiliary
    # -----------------------------------

    for i, token in enumerate(doc):

        if token.text.lower() in AUXILIARIES:

            tokens.insert(i + 1, "not")

            return clean_sentence(tokens)

    # -----------------------------------
    # STEP 2:
    # Find ROOT verb
    # -----------------------------------

    root_verb = None

    for token in doc:

        if token.dep_ == "ROOT" and token.pos_ == "VERB":

            root_verb = token

            break

    # -----------------------------------
    # STEP 3:
    # Add do/does/did not
    # -----------------------------------

    if root_verb:

        verb_index = root_verb.i

        lemma = root_verb.lemma_

        tag = root_verb.tag_

        # Present tense
        if tag in ["VB", "VBP"]:

            replacement = f"do not {lemma}"

        # Third person singular
        elif tag == "VBZ":

            replacement = f"does not {lemma}"

        # Past tense
        elif tag == "VBD":

            replacement = f"did not {lemma}"

        else:

            replacement = f"do not {lemma}"

        tokens[verb_index] = replacement

        return clean_sentence(tokens)

    # -----------------------------------
    # STEP 4:
    # Fallback
    # -----------------------------------

    return "not " + question


# -----------------------------------
# Clean formatting
# -----------------------------------

def clean_sentence(tokens):

    sentence = " ".join(tokens)

    # Fix punctuation spacing
    sentence = sentence.replace(" ?", "?")
    sentence = sentence.replace(" .", ".")
    sentence = sentence.replace(" ,", ",")

    return sentence