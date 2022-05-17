import sys
import urllib.request
import json

if __name__ == '__main__':
    page_name = 'jtbcnews'
    page_id = '240263402699918'
    app_id = "691248618653688"
    app_secret = "13cc37b482f8fdcea1522b84539c86fe"

    from_date = '2017-01-01'
    to_date = '2017-01-31'
    num_statues = '10'
    access_token = app_id + "|" + app_secret

    base = "https://graph.facebook.com/v13.0"
    node = "/%s/posts" % page_id
    fields = "/?fields=id,message,link.name,type,shares,reactions," + \
            "created_time,comments,limit(0).summary(true)" + \
            ".limit(0).summary(true)"
    duration = "&since=%s&until=%s" % (from_date, to_date)
    parameters = "&limit=%s&access_token=%s" % (num_statues, access_token)
    url = base + node + fields + duration + parameters

    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            data = json.loads(response.read().decode('utf-8'))
            print(data)
    except Exception as e:
        print(e)