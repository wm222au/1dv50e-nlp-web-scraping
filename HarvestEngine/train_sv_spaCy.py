from __future__ import unicode_literals, print_function

from training.addresses_data_sv import ADDRESSES_DATA, ADDRESSES_LABEL, FULL_ADDRESSES_LABEL
from training.addresses_text_sv import ADDRESSES_TEST

import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


def main(model=None, new_model_name="temp", output_dir=None, n_iter=30):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    random.seed(0)
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("sv")  # create blank Language class
        print("Created blank 'sv' model")
    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe("ner")

    # add new entity label to entity recognizer
    ner.add_label(ADDRESSES_LABEL)
    ner.add_label(FULL_ADDRESSES_LABEL)

    if model is None:
        optimizer = nlp.begin_training()
    else:
        optimizer = nlp.resume_training()
    move_names = list(ner.move_names)
    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        sizes = compounding(1.0, 4.0, 1.001)
        # batch up the examples using spaCy's minibatch
        for itn in range(n_iter):
            random.shuffle(ADDRESSES_DATA)
            batches = minibatch(ADDRESSES_DATA, size=sizes)
            losses = {}
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
            print("Losses", losses)

    # test the trained model
    for i, text in enumerate(ADDRESSES_TEST):
        doc = nlp(text)
        print("Entities in model_type 'Addresses' from document number: '%s'" % i)
        for num, ent in enumerate(doc.ents):
            print(num + 1, ' - ', ent.text, 'Label: ', ent.label_)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(f'{output_dir}/{new_model_name}')
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta["name"] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)


main(None, f"current_{ADDRESSES_LABEL}_v14", Path("./models"), 35)

# 2, 4, 7, 8, 10!, 11
# 10 is probably the one to use
