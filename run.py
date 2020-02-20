# Name: TAFA Web Version
# Author: SalisM3
# Github: https://github.com/salismazaya

from flask import Flask, request, render_template, make_response, redirect, url_for, flash
# kuki = "datr=PD78XeA_1Q56YYZ_VAGNaOFB; sb=PD78XRrUMAL3wRlVVzFLjoQC; locale=id_ID; m_pixel_ratio=2; wd=360x531; x-referer=eyJyIjoiL2hvbWUucGhwIiwiaCI6Ii9ob21lLnBocCIsInMiOiJtIn0%3D; c_user=100041106940465; xs=36%3A07c8hoSGTJSjfQ%3A2%3A1577024099%3A20352%3A10751; fr=01j67Pr46WWB535S6.AWVUxrgIqIXuS5OniPRb_Wx8Ds8.Bd9kOE.dr.F4A.0.0.Bd_3pj.; spin=r.1001566983_b.trunk_t.1577065874_s.1_v.2_"
from bs4 import BeautifulSoup as parser
import module, time, requests as r
mo = module.Model()
app = Flask(__name__)
app.secret_key = "salismazayagansSangaddd"
ua = "Mozilla/5.0 (Linux; Android 8.1.0; Redmi 5A Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36"



def get_kuki(url=""):
	kuki = request.cookies.get("cookie") 
	if mo.set_kuki(kuki, url=url):
		return kuki
	else:
		return None

@app.errorhandler(404)
def not_found(e):
	return render_template("error.html", err="404", text="Halaman Tidak Ditemukan"), 404

@app.errorhandler(500)
def internal_sever_error(e):
	return render_template("error.html", err="500", text="Terjadi Error Di Server Dalam Mohon Hubungi Author"), 500

# @app.route("/", methods=["GET", "POST"])
# def index():
# 	method = request.method
# 	if method == "GET":
# 		kuki = get_kuki()
# 		if kuki != None: return redirect("/home")
# 		return render_template("index.html") 
# 	else:
# 		u = request.form.get("username")
# 		p = request.form.get("password")
# 		ses = r.Session()
# 		data = ses.post("https://mbasic.facebook.com/login", data={'email':u, 'pass':p, 'login':'submit'}).url
# 		if "save-device" in data or "m_sess" in data or "home.php" in data:
# 			kuki = ";".join([str(x).split(" ")[1] for x in ses.cookies])
# 			return kuki_login(esteh=kuki)
# 		elif "checkpoint" in data:
# 			flash(True)
# 			return render_template("index.html", msg_error="Akun Checkpoint!") 
# 		else:
# 			flash(True)
# 			return render_template("index.html", msg_error="Username/Password Salah!") 

@app.route("/", methods=["GET", "POST"])
def kuki_login():
	method = request.method
	if method == "GET":
		kuki = get_kuki()
		if kuki != None: return redirect("/home")
		return render_template("index.html") 
	elif method == "POST" and request.form.get("kuki") != None: 
		kuki = request.form.get("kuki")
		if mo.cek_kuki(kuki):
			if not "Keluar (" in mo.html and not "Beranda" in mo.html and not "Cari Facebook" in mo.html:
				flash("Use Indonesian Language in Your Facebook")
				return render_template("index.html")
			respon = make_response(redirect(url_for('home')))
			respon.set_cookie('cookie', kuki)
			data = mo.get_name(kuki)
			respon.set_cookie('nama', data[0])
			respon.set_cookie('img', data[1])
			respon.set_cookie('id', data[2])
			return respon
		else:
			flash("Cookies Not Valid")
			return render_template("index.html")

@app.route("/home")
def home():
	kuki = get_kuki(url="me")
	if kuki == None: return redirect("/")
	return render_template("home.html", data=mo)

@app.route("/about")
def about():
	return render_template("about.html", data=mo)

@app.route("/logout")
def logout():
	respon = make_response(redirect("/"))
	respon.set_cookie("cookie", "", expires=0)
	respon.set_cookie("nama", "", expires=0)
	respon.set_cookie("id", "", expires=0)
	return respon

@app.route('/my_grup')
def my_grup():
	kuki = get_kuki(url="groups/?seemore")
	if kuki == None: return redirect("/")
	return render_template("my_grup.html", data=mo)

@app.route("/like")
def like():
	kuki = get_kuki()
	if kuki == None: return redirect("/")
	return render_template("like.html", data=mo)

@app.route("/get_sts", methods=["POST"])
def get_sts():
	url = request.form.get("url")
	limit = int(request.form.get("limit"))
	str1 = request.form.get("str1")
	str2 = request.form.get("str2")
	kondisi = request.form.get("kondisi")
	kuki = get_kuki()
	mo.dump_sts(url, str1, str2, limit, kondisi)
	return "|".join(mo.id)

@app.route("/url", methods=["POST"])
def url():
	try:
		url = request.form.get("url")
		kuki = request.cookies.get("cookie")
		mo.updateHeader = [("user-agent", ua), ("cookie", kuki)]
		return mo.buka(url)
	except:
		return ""

@app.route("/submit_url", methods=["POST"])
def submit_url():
	try:
		url = request.form.get("url")
		komen = request.form.get("komen")
		kunci = request.form.get("kunci")
		kuki = request.cookies.get("cookie")
		mo.updateHeader = [("user-agent", ua), ("cookie", kuki)]
		mo.br.open(url)
		mo.br.select_form(nr=0)
		mo.br[kunci] = str(komen)
		return mo.br.submit().read().decode()
	except:
		return ""

@app.route("/syarat")
def syarat():
	return render_template("syarat.html")

@app.route("/find_id_f")
def id_f():
	nama = request.args.get("nama")
	if nama != None:
		return "|".join(mo.find_id(nama))
	kuki = get_kuki()
	if kuki == None: return redirect("/")
	return render_template("find_id_f.html", data=mo)

@app.route("/spamkomen_f")
def spamkomen():
	kuki = get_kuki()
	if kuki == None: return redirect("/")
	return render_template("spamkomen_f.html", data=mo)

@app.route("/unfriends", methods=["GET", "POST"])
def unfren():
	kuki = get_kuki()
	if kuki == None: return redirect("/")
	if request.method == "POST":
		link = request.form.get("url")
		try:
			data = parser(mo.br.open(link).read(), "html.parser").find("a", string="Lainnya").get("href").split("=")[1].split("&")[0]
			# print(data)
			mo.br.open("https://mbasic.facebook.com/removefriend.php?friend_id=" + data + "&unref=profile_gear").read()
			mo.br.select_form(nr=1)
			# print(mo.br.form)
			return mo.br.submit().read().decode()
		except:
			return ""
	return render_template("unfriends.html", data=mo)

@app.route("/response_f_requests")
def rfp():
	kuki = get_kuki()
	if kuki == None: return redirect("/")
	return render_template("response_f_request.html", data=mo)

if __name__ == '__main__':
	app.run(debug=True)
