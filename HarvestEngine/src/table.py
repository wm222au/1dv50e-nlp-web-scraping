from tabulate import tabulate


def get_full_address_entities(data, label):
    labels = []

    for page in data:
        for entity in page["entities"]:
            if entity["label"] == label:
                labels.append(entity)

    return labels


def get_address_length(data):
    return len(get_full_address_entities(data, "Adresser"))


def get_full_address_length(data):
    return len(get_full_address_entities(data, "FULL_Adresser"))


def get_avg_url_processing(data):
    time = 0

    for page in data:
        time += (page["time_scraped"] + page["time_processed"])

    return time / len(data)


def print_page(data):
    for page in data:
        print(f'Data for URL -> {page["url"]}')
        for entity in page["entities"]:
            print(f'Value: {entity["value"]}, Label: {entity["label"]}')


def scraper_with_nlp_comparison_matrix(scrapers):
    headers = ["Scraper", "Address", "Full address", "Address (%)", "Full address (%)", "False (%)",
               f'Avg. URL processing ({len(scrapers[0]["data"])})', "Total time"]

    table_data = []

    for scraper in scrapers:
        print(scraper["name"])
        data = scraper["data"]
        print_page(data)
        table_data.append([scraper["name"], get_address_length(data), get_full_address_length(data), "0%", "0%", "0%", get_avg_url_processing(data), scraper["duration"]])

    table = tabulate(table_data, headers=headers)

    print(table)
