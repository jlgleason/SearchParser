def parse_top_image_carousel(cmpt):
    """
    Parse shopping carousel titles and urls
    b_slidesContainer component
    :param cmpt: carousel component
    :return: parsed dictionary
    """
    parsed = {'type': 'top_image_carousel'}
    title = cmpt.find_all('span', {'class': 'b_adsTrunTx'})
    url = cmpt.find_all('a', {'id': 'rine'})

    if title:
        parsed['title'] = '|'.join([t.text for t in title])
    if url:
        parsed['url'] = url['href'].text

    return parsed
