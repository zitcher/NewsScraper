import requests as requests


def get(url, jsondata):
    return requests.get(url, params=jsondata)


class Gaurdian(object):
    def __init__(self,
                 api_key="",
                 search_endpoint="https://content.guardianapis.com/search"):
        self.api_key = api_key
        self.search_endpoint = search_endpoint

    '''
    string q: the query
    string from_date: year-month-day
    string to_date: year-month-day
    '''
    def guardian_get(self,
                     q,
                     from_date,
                     to_date,
                     page,
                     url=None,
                     api_key=None,
                     page_size=50):
        # default
        if url is None:
            url = self.search_endpoint
        if api_key is None:
            api_key = self.api_key

        # create jsondata
        jsondata = {}
        if q is None or q == "":
            jsondata = {
                "api-key": api_key,
                "q": q,
                "from-date": from_date,
                "to-date": to_date,
                "page": page,
                "page-size": page_size
            }
        else:
            jsondata = {
                "api-key": api_key,
                "from-date": from_date,
                "to-date": to_date,
                "page": page,
                "page-size": page_size
            }
        # request
        return get(url, jsondata).json()

    '''
    input
    date: %Y-%m-%d

    output:
    [(article_url, article_date) ....]
    '''
    def get_day_web_links_times(self, date):
        responses = []
        intial_get = self.guardian_get(None, date, date, 1)
        responses.append(intial_get)
        num_pages = intial_get["response"]["pages"]

        for i in range(2, num_pages+1):
            responses.append(self.guardian_get(None, date, date, i))

        article_urls_dates = []
        for page in responses:
            for article in page["response"]["results"]:
                article_urls_dates.append((article["webUrl"], article["webPublicationDate"]))

        return article_urls_dates


class Alphavantage(object):
    def __init__(self, api_key="", search_endpoint="https://www.alphavantage.co/query"):
        self.api_key = api_key
        self.search_endpoint = search_endpoint

    def alpha_vantage_get(self,
                          company_symbol,
                          url=None,
                          api_key=None,
                          function="TIME_SERIES_DAILY",
                          outputsize="full",
                          datatype="json"):
        if url is None:
            url = self.search_endpoint
        if api_key is None:
            api_key = self.api_key

        jsondata = {
            "apikey": api_key,
            "function": function,
            "symbol": company_symbol,
            "datatype": datatype,
            "outputsize": outputsize
        }
        print(jsondata)
        ret = get(url, jsondata).json()
        print(ret)
        return ret

    '''
    input: alpha_vantage_get data
    output: list of tuples:
    (
        'yr-month-day',
        {
        '1. open': 'val',
        '2. high': 'val',
        '3. low' : 'val',
        '4. close' : 'val',
        '5. volume' : 'val';'
        }
    )
    '''
    def stock_data_to_list(self, stock_data):
        stock_dic = stock_data['Time Series (Daily)']
        return tuple(stock_dic.items())

    '''
    input: stock_data_to_list data
    output: list of lists:
    [
        [
        string yr-month-day,
        float open,
        float high,
        float low,
        float close,
        float volume
        ]
    ]
    '''
    def parse_stock_list(self, stock_data):
        output = []
        for data in stock_data:
            element = []
            element.append(data[0])
            stock_data_vals = list(data[1].values())
            for value in stock_data_vals:
                element.append(float(value))
            output.append(element)
        return output
    '''
    input: alpha_vantage_get data
    output: list of lists:
    [
     [
     string yr-month-day,
     float open,
     float high,
     float low,
     float close,
     float volume
     ]
    ]
    '''
    def full_parse(self, stock_data):
        return self.parse_stock_list(self.stock_data_to_list(stock_data))


def percent_change(a, b):
    if (a + b == 0):
        return 0
    return (b - a)/midpoint(a, b)


def midpoint(a, b):
    return (a + b)/2


class NYT(object):
    def __init__(self,
                 archive_api_key="",
                 archive_endpoint="https://api.nytimes.com/svc/archive/v1/"):
        self.archive_api_key = archive_api_key
        self.archive_endpoint = archive_endpoint

    '''
    int year: > 1990
    int month: 1-12
    '''
    def archive_get(self,
                    year,
                    month,
                    api_key=None):
        # default
        if api_key is None:
            api_key = self.archive_api_key

        # create jsondata
        jsondata = {
            "api-key": api_key,
        }
        # request
        return get(self.archive_endpoint+str(year)+"/"+str(month)+".json", jsondata).json()

    '''
    input
    integer year: 2001
    integer month: 7

    output:
    [(article_url, article_date) ....]
    '''
    def get_month_links_date(self, year, month):
        article_urls_dates = []
        response = self.archive_get(year, month)

        article_urls_dates = []
        for doc in response['response']['docs']:
            article_urls_dates.append((doc["web_url"], doc['pub_date']))

        return article_urls_dates
