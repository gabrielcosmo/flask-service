def ckeck_url_params(query: dict, params: list) -> list:
    """
    :query: Represent the query string informed by url
    :params: The require paramemeters
    """
    absent: list = []
    list_query: list = []

    for q in enumerate(query):
        list_query.append(q[1])
    
    for p in params:

        if p not in list_query:
            absent.append(p)

    return absent
