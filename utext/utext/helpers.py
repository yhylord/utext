import re

# remove newline characters and tabs and extra spaces in texts,
# also filter out empty texts


def filter_texts(texts):
    # anything that's not numbers, letters, or punctuations
    not_chars = r'[^\x20-\x7e]'
    filtered = []

    for text in selector_list.extract():
        # filter out non-characters, strip extra spaces and periods
        stripped = re.sub(not_chars, '', text).strip(' .')
        if stripped:
            filtered.append(stripped)
    return filtered


def get_page_name(url):
    url_levels = url.split('/')
    if url_levels[-1]:  # not empty string = not ended with '/' = html
        page_name = url_levels[-1].split('.')[0]
    elif '.' in url_levels[-2]:  # root domain
        page_name = url_levels[-2].split('.')[0]
    else:  # non-root domain ended with '/'
        page_name = url_levels[-2]
    return page_name
