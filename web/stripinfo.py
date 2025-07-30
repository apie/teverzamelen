from stripinfo_parser import Parser


def get_stripinfo_collection_data(collection_url):
    p = Parser(collection_url)
    name = p.title
    data = p.get_data()
    return dict(
        name=name,
        items=map(lambda x: " ".join((x["countcol"], x["firstcol"])), data),
    )
