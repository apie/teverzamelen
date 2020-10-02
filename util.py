# By Apie 2020-10-02
# License: MIT
def make_dict(item, header, fields):
    return {header[i]: field for i, field in enumerate(item) if header[i].strip() in fields}