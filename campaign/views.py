from django.shortcuts import render
from .models import Campaign
from bs4 import BeautifulSoup
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CampaignSerializer

@api_view(['GET'])
def CampaignList(request):
    sales = Campaign.objects.all()
    serializer = CampaignSerializer(sales, many=True)
    return Response(serializer.data)

def camphome(request):
    Campaign.objects.all().delete()

    #Part to read all the campaigns data
    kampaaniad = [
        {"Rimi": 'scraper/rimi_kamp.html'},
        {"Maxima": 'scraper/maxima_kamp.html'}
        ]
    for item in kampaaniad:
        with open(list(item.values())[0], 'rb') as html_file:
            soup = BeautifulSoup(html_file, 'lxml')
            
            if list(item.keys())[0] == "Rimi":
                for article in soup.find_all('a', class_='gtm lottery-card js-slick-slide lottery-card--loyalty'):
                    if article is not None:  
                        url = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",str (article))
                        kmp_url = url[0]
                        bg_image = url[1]
                        description = article.find('div', class_='title')
                        period_date = article.find('div', class_='date')
                        if description and period_date is not None:
                            desc = description.text.strip()
                            date = period_date.text.strip()
                            wholedesc = desc + " " + date
                    
                    campaigns_data = Campaign(
                    kmp_url = kmp_url,
                    kmp_bg_image = bg_image,
                    kmp_desc = wholedesc,)
                    
                    campaigns_data.save()

            

    context = {
        'campaigns': Campaign.objects.all()
    }

    return render(request, 'sales/home.html', context)
