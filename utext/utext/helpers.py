import re
from urllib.parse import urlparse

# remove newline characters and tabs and extra spaces in texts,
# also filter out empty texts


def filter_texts(texts):
    # anything that's not numbers, letters, or punctuations
    not_chars = r'[^\x20-\x7e]'
    filtered = []

    for text in texts:
        # filter out non-characters, strip extra spaces and periods
        stripped = re.sub(not_chars, '', text).strip(' .')
        if stripped:
            filtered.append(stripped)
    return filtered


def get_page_name(url):
    path = urlparse(url).path
    page_name_with_file_extension = path.strip('/').replace('/', '_')
    return page_name_with_file_extension.split('.')[0]
