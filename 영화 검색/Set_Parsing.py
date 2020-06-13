import xml.etree.ElementTree as ET
import urllib.request
from bs4 import BeautifulSoup
import requests

class Set_Parsing:
    def __init__(self):
        self.client_id = "tbnHeHUwtbVgWtr91vX5"
        self.client_secret = "rFSWzcfijB"

        self.daily_movie_url = "http://www.kobis.or.kr//kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key=0f7d6638c03ecc9885350d92093d8f8b"
        self.weekly_movie_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.xml?key=0f7d6638c03ecc9885350d92093d8f8b&weekGb=0"
        self.actor_movie_url = "http://www.kobis.or.kr//kobisopenapi/webservice/rest/people/searchPeopleList.xml?key=0f7d6638c03ecc9885350d92093d8f8b"
        self.actorinfo_movie_url = "http://www.kobis.or.kr//kobisopenapi/webservice/rest/people/searchPeopleinfo.xml?key=0f7d6638c03ecc9885350d92093d8f8b&peopleCd="
        self.Naver_url = "https://openapi.naver.com/v1/search/movie.xml?query="
        self.Naver_url_option = "&display=50"

    def Movie_xml_request(self, year, date, value):  # 영화진흥위원회 api 호출
        if value == 1:  # 일/주간 구분
            params = {'targetDt': year+date}
            response = requests.get(self.daily_movie_url, params=params)
        else:
            params = {'targetDt': year + date}
            response = requests.get(self.weekly_movie_url, params=params)
        self.xml_status = response.status_code
        self.xml_text = response.text

    def Naver_xml_request(self, name):  # 네이버영화 api 호출
        request = ''
        request = urllib.request.Request(self.Naver_url + urllib.parse.quote(name)+self.Naver_url_option)
        request.add_header("X-Naver-Client-Id", self.client_id)
        request.add_header("X-Naver-Client-Secret", self.client_secret)

        self.response = urllib.request.urlopen(request)
        self.Nxml_status =  self.response.getcode()
        self.response_text =  self.response.read()
        self.Nxml_text =  self.response_text.decode('utf-8')


    def Naver_HTML_request(self,url): #오직 영화 줄거리 가져오기 위한 함수 와!!
        req = urllib.request.Request(url)
        res= urllib.request.urlopen(req)
        Nhtml_text = res.read().decode('utf-8')
        soup = BeautifulSoup(Nhtml_text,'html.parser')

        return soup.head.find("meta",{"property":"og:description"}).get('content')

    def actorInfo_HTML_request(self,name):

        self.actor_info = []
        self.actor_info_tag = []
        del self.actor_info[:]
        del self.actor_info_tag[:]

        url = "https://search.naver.com/search.naver"
        params = {'query':"배우 "+name}
        response = requests.get(url,params=params)
        self.actorInfo_url = response.url
        html_text = response.text
        soup = BeautifulSoup(html_text, 'html.parser')

        root1 = soup.body.find("div",{"id":"wrap"}).find("div",{"id":"container"}) \
            .find("div", {"id": "content"}).find("div",{"id":"main_pack"}) \
            .find("div", {"id": "people_info_z"})

        root2 = root1.find("div", {"class": "cont_noline"}) \
            .find("div", {"class": "profile_wrap"})

        root3 = root1.find("div",{"class":"people_type"}).find("div",{"id":"tx_ca_people_movie_content"})\
            .find("ul")

        info_text = root2.find("dl")
        try:
            image_url = root2.find("div", {"class": "big_thumb"}).find("img")
            self.actor_image_url = image_url['src']
        except:
            pass

        info_list = info_text.select('dd')
        info_tag = info_text.select('dt')
        movie_list = root3.select('li')

        self.movie_img_list=[]
        self.movie_name_list = []
        del self.movie_img_list[:]
        del self.movie_name_list[:]

        for tag in movie_list:
            movieimage_url = tag.find("div", {"class": "big_thumb"}).find("img")
            self.movie_img_list.append(movieimage_url['src'])
            self.movie_name_list.append(movieimage_url['alt'])

        for tag in info_list:
            self.actor_info.append(tag.text)
        for tag in info_tag:
            self.actor_info_tag.append(tag.text)

    def actor_xml_request(self, name):
        params = {'peopleNm':name}
        self.response = requests.get(self.actor_movie_url,params=params)
        self.actor_xml_code = self.response.status_code
        self.actor_xml_text = self.response.text











