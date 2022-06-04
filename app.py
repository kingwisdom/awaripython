import flask
from flask import request, jsonify
import requests
from bs4 import BeautifulSoup

app = flask.Flask(__name__)
app.config["DEBUG"] = False

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]



# def getproduct(search):
    


# getproduct("Generator")

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."
    results = []

    for book in books:
        if book['id'] == id:
            results.append(book)
    return jsonify(results)


@app.route('/api/awari/items', methods=['GET'])
def api_search():
    if 'search' in request.args:
        search = request.args['search']
    else:
        return "Error: No id field provided. Please specify an id."
    results = []

    products = []
    for x in range(1, 4):
        baseurl = f"https://www.jumia.com.ng/catalog/?q={search}&page={x}#catalog-listing"

        r = requests.get(baseurl)

        soup = BeautifulSoup(r.content, 'lxml')

        myList = soup.find_all('article', class_='prd _fb col c-prd')

        for item in myList:
            name = item.find('h3', class_='name').text.strip()
            price = item.find('div', class_='prc').text.strip()
            imgUrl = item.find('img', class_='img').get('data-src')
            link = item.find('a', href=True)['href']

            my_dict = {'Product Name': name, 'Product Price': price, "link": link, "image": imgUrl}
            products.append(my_dict)


    return jsonify(products)
    
@app.route('/api/awari/konga', methods=['GET'])
def api_search_konga():
    if 'search' in request.args:
        search = request.args['search']
    else:
        return "Error: No id field provided. Please specify an id."
    results = []

    products = []

    baseurl = f"https://jiji.ng/search?query={search}"

    r = requests.get(baseurl)

    soup = BeautifulSoup(r.content, 'lxml')

    myList = soup.find_all('div', class_='b-list-advert__item-wrapper')
    print("list",myList)

    for item in myList:
        name = item.find('div', class_='b-advert-title-inner qa-advert-title b-advert-title-inner--h3').text.strip()
        price = item.find('div', class_='prc').text.strip()
        imgUrl = item.find('picture', class_='h-flex-center h-width-100p h-height-100p h-overflow-hidden').get('srcset')
        link = item.find('a', href=True)['href']

        my_dict = {'Product Name': name, 'Product Price': price, "link": link, "image": imgUrl}
        products.append(my_dict)


    return jsonify(products)
    


app.run()