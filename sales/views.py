from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.serializers import Serializer
from .models import Sale
from campaign.models import Campaign
from django.views.generic import ListView, DetailView
from bs4 import BeautifulSoup
import requests
import re
from django.contrib.admin.utils import flatten
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SaleSerializer
import json


@api_view(['GET'])
def SalesList(request):
    sales = Sale.objects.order_by('?')
    serializer = SaleSerializer(sales, many=True)
    return Response(serializer.data)


def saleListDetail(request, pk):
    
    obj_cat = Sale.objects.get(id=pk)

    context = {
        'data' : Sale.objects.get(id=pk),
        'sales': Sale.objects.filter(category = obj_cat.category).order_by('?')[:3]
    }
    
    return render(request, "sales/sale_detail.html", context)
    

# Function to define categories of products
def check_category(headline):
    
    categories = {
        "Puuviljad ja marjad" : ['ananass', 'apelsin', 'arbuus', 'avokaado', 'banaan', 'dattel', 'füüsal', 'granaat', 'greip', 'jõhvika', 'kiivi', 'kumkvaat', 'kurkum', 'laim', 'maasika', 'mandariin', 'mango', 'melon', 'mustikas', 'papaia', 'passionfruit', 'pirn', 'pitahaia', 'ploom', 'puuviljamiks', 'puuviljasalat', 'sidrun', 'smuuti', 'sõstar', 'tamarind', 'vaarikas', 'viinamari', 'viinamarjad', 'õun'],
        "Piimatooted": ['jogurtijook','jogurt', 'kaerajook', 'kaeravahepala', 'keefir', 'kinder', 'kissell', 'kodujuust', 'kohuke', 'kohupiim', 'koor', 'muna', 'petimaius','pasha', 'pett', 'piim', 'puder', 'puding', 'rjazenka', 'tarretis', 'jäätis', 'või ','võie ', 'taluvõi', 'majonees'],
        "Juustud" : ['brie', 'camembert', 'gouda', 'hummus', 'juust', 'mozzarella', 'pizzariiv', 'toasty', 'toorjuust'],
        "Liha" : ['pardifilee','liharull','antrekoo', 'broiler', 'fuet', 'fuetec', 'hakkliha', 'hernesupikogu', 'kalkuni', 'kana', 'karbonaad', 'keele', 'klops', 'koib', 'konserv', 'koot', 'kotlet', 'liha', 'pasteet', 'part', 'peekon', 'pekk', 'pelmeenid' ,'pihv', 'pikkpoiss', 'pitsakate', 'poolkoivad', 'pooltii', 'praad', 'prae', 'prosciutto', 'põsk', 'raguu', 'ribad', 'ribi', 'romstee', 'rulaad', 'saiakate', 'salaami', 'sardell', 'sea', 'singi', 'sink', 'strooganov', 'suitsusin', 'sült', 'turistieine', 'veise', 'viiner', 'vorst', 'õllepärlid', 'õllemops', 'šašlõkk', 'šnitsel'],
        "Kala" : ['haug', 'ahven', 'heeringa', 'kala', 'karp', 'kilu', 'koger', 'koha', 'krabi', 'krevet', 'lesta', 'lõhe', 'pangaasiuse', 'paalia', 'rannakarp', 'räim', 'tuuni', 'tursa', 'viburhännak', 'vikerforell', 'mintafilee'],
        "Köögiviljad ja seened" : ['spargel','austerservik', 'baklažaan', 'basiilik', 'bataat', 'brokoli', 'frillis', 'hernes', 'idu', 'ingver', 'juurseller', 'kaalikas', 'kapsas', 'kartul', 'koriander', 'kukeseen', 'kurk', 'köögiviljad' ,'kõrvits', 'küüslau', 'lauk', 'mais', 'mustjuur', 'oregano', 'paksoi', 'paprika', 'partinaak', 'peet', 'petersell', 'pipar', 'porgand', 'puravik', 'redis', 'riisika', 'rosmariin', 'rukola', 'rukola', 'salat', 'seen', 'shiitake', 'sibul', 'till', 'tomat', 'tüümian', 'uba', 'varsseller', 'šampinjon'],
        "Leivad, saiad, kondiitritooted" : ['väike väänik','suhkrutigu','croissant', 'ekleer', 'keerd', 'kook', 'koogid', 'korp', 'krutoonid', 'kuivik', 'kulitš','kukkel', 'kringel', 'lavash', 'leib', 'leiv', 'leivuke', 'muhkel', 'pala', 'palmik', 'pehmik', 'pirukas', 'pitsa', 'pizza ', 'ruks', ' rull', 'rummipallid', 'moosipall', 'rääk', 'rõngas', 'röst', 'sai', 'sepik', 'struud', 'struudel', 'tasku', 'tort', 'tortilja', 'tortilla', 'vahvl'],
        "Kuumad ja karastusjoogid" : ['toonik', 'kakaokapslid', 'alkoholivaba','kohviuba',' tee', 'greenfield', 'jook', 'jäätee', 'kohv ', 'kohvioad', 'kohvikapslid', 'mahl ', 'siirup', 'vesi', 'nektar'],
        "Maiustused, kuivained ja kauasäilivad toidukaubad " : ['suhkur ','sool ', 'jahu ', 'heinz', 'helb', 'hommikueine', 'iirise', 'kaste', 'karamell', 'ketšup', 'kiirnuudlid', 'komm', 'kompv', 'kookospiim', 'konserv','krõps', 'küpsis', 'maiuspala','maiustus', 'makaron', 'müsl', 'moos ', 'mesi', 'nuudlid', 'oliiv', 'pasta', 'präänik', 'pähkl', 'põltsamaa', 'riis', 'rosin', 'salvest', 'snäk', 'seakamar', 'taigen' ,'tudengieine', 'šokolaad', 'õli', 'näkileib','sarapuupähkel'],
        "Lemmikloomakaubad ja kodukeemia" : ['värskendaja','ajax', 'nõudepesumasinageel', 'kalatoit', 'kassi', 'kiisueine', 'koer', 'koeravorst', 'konserv koertele', 'küülik', 'laadija', 'paber', 'pesuvahend', 'pesugeel', 'pesukapslid', 'puhastus', 'pulber', 'õhu'],
        "Alkohol" : ['jägermeister','alkohoolne jook', 'brändi', 'piiritusejook', 'ararat', 'cognac', 'konjak', 'liköör', 'martini', 'piiritusjook', 'rumm', 'siider', 'vana tallinn', 'vein', 'viin,', 'viin ', 'viski', 'whisky', 'õlu'],
        "Kodukaubad" : ['taskurätikud','aluspesu', 'küün', 'kleep', 'lõngad', 'pann', 'seemned', 'voodi', 'hooldus', 'pleedid', 'kaus', 'klaas', 'tass', 'hambapasta', 'tampoon', 'raseerija', 'hügieeniside', 'deodoran', 'jumestus', 'toidukonteiner', 'mähkmed', 'salvrätik'],
        "Teised tooted": ['mänguas', 'kampaania', 'kaunistus', 'grillkaubad']
    }
    match = []
    for key, values in categories.items():
        if(isinstance(values, list)):
            for value in values:
                if str(value) in headline.lower():
                    match.append(key)
                
    return (match[-1])

# Main function to create data and add it to database from external resource
def home(request):
    Sale.objects.all().delete()


    #Part to read each offer 
    kauplused = [
    {"Rimi": 'scraper\mrimi.html', "article" : "offer-card__content offer-card__section", "headline":"offer-card__name", "discount" : 'badge_c', "price": "price-badge", "image" : 'offer-card__image-cloudinary'},
    {"Maxima": 'scraper\maxima.html', "article" : "col-third", "headline":"title", "discount" : 'discount percents', "price": "discount price", "image" : 'img'}
    ]
    def find_data(dict):
        
        with open(list(dict.values())[0], 'rb') as html_file:
            soup = BeautifulSoup(html_file, 'lxml')

        all_sales = []
        for article in soup.find_all('div', class_=list(dict.values())[1]):
            if article is not None:
                headline = article.find('div', class_=list(dict.values())[2]).text.strip()
                discount = article.find('div', class_=list(dict.values())[3])
                price = article.find("div", {"class" : list(dict.values())[4]})
                new_price = ''
                old_price = ''

                try:
                    category = check_category(headline)
                except:
                    category = 'Teised tooted'
                            
            if discount is not None:
                discount = discount.text.strip()
                if '%' not in discount:
                    discount = 0    
                    
            if price is not None:
                price = price.text.split()
                for key, value in dict.items():
                    if key == "Rimi":
                        for i in price:
                            if len(price) == 5:
                                new_price = price[0]+"."+price[1]+price[2] 
                                old_price = price[3] + price[4]
                            elif len(price) == 3:
                                new_price = price[0]+"."+price[1]+price[2]
                                old_price = 0
                            elif len(price) == 2:
                                new_price = price[0]+" "+price[1]
                                old_price = 0
                            else:
                                new_price=price[0]
                                old_price = 0
                    elif key == "Maxima":
                        for i in price:
                            if len(price) == 2:
                                new_price = price[0]
                                new_price = new_price[:-3]+"."+new_price[-3:]
                                old_price = price[1]
                            else: 
                                new_price = price[0]
                                new_price = new_price[:-3]+"."+new_price[-3:]
                                old_price = 0


            for key, value in dict.items():
                if key == "Maxima":
                    image = article.find('div', class_=list(dict.values())[5]).img['src']
                    url = f'http://www.maxima.ee{image}'
                elif key == "Rimi":
                    regex = re.compile(list(dict.values())[5])
                    image = article.find('div', class_= regex)
                    url = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",str(image))
                    url = str(url)
                    while True:
                        if url[-1].isalpha() == False:
                            url = url[:-1]
                        elif url[0].isalpha() == False:
                            url = url[1:]
                        else:
                            break

            sales_dict = {"category": category,"store": list(dict.keys())[0],"headline": headline, "image": url, "discount": discount, "new_price": new_price, "old_price" : old_price}
            all_sales.append(sales_dict)
        
        return all_sales

    new_list = []
    for i in kauplused:
        new_list.append(find_data(i))

    all_sales_list = flatten(new_list)

    
    for i in all_sales_list:
           sales_data = Sale(
           category = i["category"],
           store = i["store"],
           headline = i['headline'],
           image = i["image"],
           discount = i["discount"],
           new_price = i["new_price"],
           old_price = i["old_price"],
           
        )
           sales_data.save()


    context = {
        'sales': Sale.objects.order_by('?'),
        'campaigns' : Campaign.objects.all()
    }

    return render(request, 'sales/home.html', context)

