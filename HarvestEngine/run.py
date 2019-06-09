from scraper.en_urls import LIST as EN_LIST
from scraper.sv_urls import LIST as SV_LIST, DISPLACY_LIST
from scraper.framework import parse_urls as frame_parse
from scraper.automation import parse_urls as auto_parse
from scraper.network_request import parse_urls as nr_parse
from training.addresses_data_en import ADDRESSES_LABEL as EN_LABEL
from training.addresses_data_sv import ADDRESSES_LABEL as SV_LABEL
from training.addresses_text_sv import ADDRESSES_TEST
from scraper.tokenization import filter_text
import spacy
from spacy import displacy
import plac
import time

from src.table import scraper_with_nlp_comparison_matrix

model = './models/Adresser'
ner_model = f"./models/current_Adresser_v6"

nlp = spacy.load(ner_model)

# if "ner" not in nlp.pipe_names:
# ner = nlp.create_pipe("ner")
# nlp.add_pipe(ner)
# otherwise, get it, so we can add labels to it
# else:
ner = nlp.get_pipe("ner")

ner.add_label(SV_LABEL)
ner.add_label(SV_LABEL)


def engine_run(language='sv'):
    if language == 'sv':
        label = SV_LABEL
        list = SV_LIST
    else:
        label = EN_LABEL
        list = EN_LIST

    frame = frame_parse(list)

    run_nlp(label, f"./models/current_{label}", frame)


def run_nlp(label, ner_model, content):
    nlp = spacy.load(ner_model)

    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe("ner")

    ner.add_label(label)

    for page in content:
        doc = nlp(page['data'])
        print("Entities in model_type 'Addresses' from document number: '%s'" % page['url'])
        for num, ent in enumerate(doc.ents):
            print(num + 1, ' - ', filter_text(ent.text))


def run_convert_documents_to_nlp_data(documents):
    processed_data = []

    for page in documents:
        p = page["data"]

        start_time = time.time()
        parsed = nlp(p)
        end_time = time.time()

        site = {
            "url": page["url"],
            "time_scraped": page["time"],
            "time_processed": end_time - start_time,
            "original": p,
            "parsed": parsed,
            "entities": []
        }
        for num, ent in enumerate(site["parsed"].ents):
            site["entities"].append({
                "id": num,
                "value": ent.text,
                "label": ent.label_
            })

        processed_data.append(site)

    return processed_data


def run_time_gathering_with_scrapers(name, parser, url_list):
    start_time = time.time()

    scraped = parser(url_list)
    scraper_data = {
        "name": name,
        "data": run_convert_documents_to_nlp_data(scraped),
        "duration": None
    }
    total_execution_time = time.time() - start_time

    scraper_data["duration"] = total_execution_time

    return scraper_data


def run_nlp_comparsion_with_scrapers():
    list = SV_LIST

    nr = run_time_gathering_with_scrapers("Network request", nr_parse, list)
    frame = run_time_gathering_with_scrapers("Scrapy", frame_parse, list)
    auto = run_time_gathering_with_scrapers("Selenium (Chrome)", auto_parse, list)

    # Future work, diffence between selenium Chrome / Firefox / Opera e.t.c
    # Classifier which decides if site is using react, if so use selenium otherwise use scrapy

    scraper_with_nlp_comparison_matrix([nr, frame, auto])


def run_nlp_test():
    for i, text in enumerate(ADDRESSES_TEST):
        doc = nlp(text)
        print("Entities in model_type 'Addresses' from document number: '%s'" % i)
        for num, ent in enumerate(doc.ents):
            print(num + 1, ' - ', ent.text, 'Label: ', ent.label_)


def run_displacy_ner():
    page = frame_parse(DISPLACY_LIST)[0]["data"]

    doc = nlp(page)
    displacy.serve(doc, style="ent", options={"colors": {
        "ADRESSER": "lightgreen",
        "FULL_ADRESSER": "lightblue"
    }})


# run_nlp_comparsion_with_scrapers()
# run_nlp_test()
run_displacy_ner()
