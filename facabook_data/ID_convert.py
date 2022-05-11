import sys
import urllib.request
import json

if __name__ == '__main__':
    id = "1967010696819714"
    app_id = "691248618653688"
    app_secret = "13cc37b482f8fdcea1522b84539c86fe"
    access_token = app_id + "|" + app_secret

    base = "https://graph.facebook.com/"
    url = base + "/" + id + "?access_token=" + access_token

    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            data = json.loads(response.read().decode('utf-8'))
            page_id = data['id']
            print("Facebook Numeric ID: %s" %page_id)
    except Exception as e:
        print(e)