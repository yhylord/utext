# remove newline characters and tabs and extra spaces in texts,
# also filter out empty texts


def filter_texts(selector_list):
    # delete any \n, \t, \xa0, or \u2028
    # \xa0 and \u2028 are unicode space and separator
    translation_table = dict.fromkeys(map(ord, '\n\t\xa0\u2028'), None)
    filtered = []
    for text in selector_list.extract():
        # filter out extra periods
        stripped = text.translate(translation_table).strip(' .')
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
