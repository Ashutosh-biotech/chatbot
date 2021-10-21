from django.shortcuts import render
from django.http import JsonResponse
import wolframalpha
import wikipedia
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch


# Create your views here.
def home(request):
    return render(request, 'index.html')


def bot_search(request, query):
    null = "null"
    false = "false"
    if ('who are you' in query.lower()) or ('what is your name' in query.lower()) or ('your\'s name' in query.lower()) or ('your name' in query.lower()) or ('chatbot name' in query.lower()):
        return JsonResponse({'output': 'Christopher'})
    if ('who am i' in query.lower()) or ('what is my name' in query.lower()) or ('my name' in query.lower()) or ('chatbot friend name' in query.lower()) or ('chatbot friend\'s name' in query.lower()):
        return JsonResponse({'output': '😱 You don\'t know your name | 😅'})
    if ('who invented you' in query.lower()) or ('who made you' in query.lower()) or ('who discover you' in query.lower()):
        return JsonResponse({'output': 'Ashutosh (Head Boy) and Dhruv'})
    if ('what is your date of birth' in query.lower()) or ('when you born' in query.lower()) or ('when was you born' in query.lower()) or ('what is your dob' in query.lower()):
        return JsonResponse({'output': 'Actually I don\'t know'})
    if 'news' in query.lower():
        try:
            url = f"https://google-search3.p.rapidapi.com/api/v1/news/q={query}"
            headers = {
                'x-user-agent': "desktop",
                'x-rapidapi-host': "google-search3.p.rapidapi.com",
                'x-rapidapi-key': "your-api-key-from-radiapi"
            }

            response = requests.request("GET", url, headers=headers)
            response = eval(response.text)
            return JsonResponse({'output': f"{response['entries'][0]['title']}<br><br>{response['entries'][0]['summary']}"})
        except:
            query = query.replace('news', '')
            reqUrl = f"https://newsapi.org/v2/everything?q={query}&apiKey=your-api-key-from-news-api"
            headersList = {}
            payload = ""
            response = requests.request(
                "GET", reqUrl, data=payload,  headers=headersList)
            response = response.text
            response = eval(response)
            return JsonResponse({'output': f"{response['articles'][0]['title']}<br>{response['articles'][0]['discription']}<br><br><img src = '{response['articles'][0]['urlToImage']}'>"})

    if ('photo' in query.lower()) or ('pic' in query.lower()) or ('pics' in query.lower()) or ('picture' in query.lower()) or ('pictures' in query.lower()) or ('image' in query.lower()) or ('images' in query.lower()) or ('photos' in query.lower()):
        params = {
            "api_key": "your-api-key-from-serpapi",
            "engine": "google",
            "ijn": "0",
            "q": f"{query}",
            "google_domain": "google.com",
            "tbm": "isch"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        results = results['images_results'][0]['original']
        return JsonResponse({'output': f"<a href='{results}' target='newtab'><img src='{results}' alt='{query}' draggable='false'></a>"})

    try:
        URL = "https://www.google.co.in/search?q=" + query
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
        }
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        result = soup.find(class_='Z0LcW XcVN5d').get_text()
        return JsonResponse({'output': result})
    except:
        try:
            result = soup.find(class_='kno-rdesc')
            result = result.findChildren("span", recursive=False)[0].get_text()
            return JsonResponse({'output': result})
        except:
            try:
                client = wolframalpha.Client("your client key")
                res = client.query(query)
                ans = next(res.results).text
                if (ans == "(no data available)") or (ans == "(data not available)"):
                    sys.exit()
                ans = ans.replace('==', '<br>')
                return JsonResponse({'output': f'{ans}'})

            except:
                try:
                    url = f"https://google-search3.p.rapidapi.com/api/v1/search/q={query}"

                    headers = {
                        'x-user-agent': "desktop",
                        'x-rapidapi-host': "google-search3.p.rapidapi.com",
                        'x-rapidapi-key': "your-api-key-from-radiapi"
                    }

                    response = requests.request("GET", url, headers=headers)
                    response = eval(response.text)
                    return JsonResponse({'output': f"<a href='{response['results'][0]['link']}' target='newtab'>{response['results'][0]['title']}</a><br><br>{response['results'][0]['description']}"})

                except:
                    try:
                        ans = wikipedia.summary(query, sentences=10)
                        ans = ans.replace('==', '<br><br>')
                        return JsonResponse({'output': f'{ans}'})
                    except:
                        ans = "Sorry, I didn't get it"
                        return JsonResponse({'output': ans})
