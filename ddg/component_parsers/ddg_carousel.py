def parse_top_image_carousel(cmpt):
    parsed = {'type': 'top_image_carousel'}
    title = cmpt.find_all('a', {'class': 'module--carousel__body__title js-carousel-item-title'})

    if title:
        parsed['title'] = title.text
        parsed['url'] = title['href'].text

    return parsed
