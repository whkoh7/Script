import xml.etree.ElementTree as ET
import urllib.request
from bs4 import BeautifulSoup
import requests

class Set_Parsing:
    def __init__(self):
        self.client_id = "tbnHeHUwtbVgWtr91vX5"
        self.client_secret = "rFSWzcfijB"

        self.daily_movie_url = "http://www.kobis.or.kr//kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key=0f7d6638c03ecc9885350d92093d8f8b&targetDt="
        self.weekly_movie_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.xml?key=0f7d6638c03ecc9885350d92093d8f8b&weekGb=0&targetDt="
        self.Naver_url = "https://openapi.naver.com/v1/search/movie.xml?query="
        self.Naver_url_option = "&display=50"

    def Movie_xml_request(self, year, date, value):  # 영화진흥위원회 api 호출
        if value == 1:  # 일/주간 구분
            self.request = urllib.request.Request(
                self.daily_movie_url + year + date)
        else:
            self.request = urllib.request.Request(
                self.weekly_movie_url + year + date)
        self.response = urllib.request.urlopen(self.request)
        self.xml_status = self.response.getcode()
        self.response_text = self.response.read()
        self.xml_text = self.response_text.decode('utf-8')

    def Naver_xml_request(self, name):  # 네이버영화 api 호출
        self.Nrequest = ''
        self.Nrequest = urllib.request.Request(self.Naver_url + urllib.parse.quote(name)+self.Naver_url_option)
        self.Nrequest.add_header("X-Naver-Client-Id", self.client_id)
        self.Nrequest.add_header("X-Naver-Client-Secret", self.client_secret)

        self.Nresponse = urllib.request.urlopen(self.Nrequest)
        self.Nxml_status = self.Nresponse.getcode()
        self.Nresponse_text = self.Nresponse.read()
        self.Nxml_text = self.Nresponse_text.decode('utf-8')


    def Naver_HTML_request(self,url): #오직 영화 줄거리 가져오기 위한 함수 와!!
        req = urllib.request.Request(url)
        res= urllib.request.urlopen(req)
        Nhtml_text = res.read().decode('utf-8')
        soup = BeautifulSoup(Nhtml_text,'html.parser')

        return soup.head.find("meta",{"property":"og:description"}).get('content')