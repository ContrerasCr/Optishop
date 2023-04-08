import requests
from bs4 import BeautifulSoup
from lxml import etree


def scrap_lider(url):
	try:
		response = requests.get(url)
	except requests.exceptions.MissingSchema:
		return "No item"
	
	soup = BeautifulSoup(response.text, 'html.parser')
	price = soup.find("p", {"itemprop": "lowPrice"})
	brand = soup.find("span", {"itemprop": "brand"})
	name = soup.find("span", {"itemprop": "name"})
	data = name.text, brand.text, price.text
	return data


def scrap_santaisabel(url):
	
	try:
		response = requests.get(url)
	except requests.exceptions.MissingSchema:
		return "No item"
	
	soup = BeautifulSoup(response.text, 'html.parser')
	value = soup.find_all("script")
	lis = [i.text for i in value if len(i.text) > 5]
	lis = [i for i in lis if '"Product","name"' in i]

	val = lis[0].replace("{", "").replace("}", "").replace('"', '').split(",")
	
	values = {}
	for a in val:
		k = a.split(":", 1)
		h, i = k[0], k[1]
		values[h] = i
	
	name = values['description']
	price = values['price']
	data = name.split("|")[0], price
	return data


def scrap_jumbo(url):
	try:
		response = requests.get(url)
	except requests.exceptions.MissingSchema:
		return "No item"
	
	soup = BeautifulSoup(response.text, 'html.parser')

	value = soup.find_all("div")
	val = [i for i in value if i.get("id") == "root"]
	val2 = val[0].find_all("div")
	sic = set()
	for i in val2:
		try:
			price = i.find("span", {"class": "product-sigle-price-wrapper"})
			name = i.find("h1", {"class": "product-name"})
			dat = (name.text, price.text)
			sic.add(dat)
		except:
			pass
	
	return sic


def scrap_unimarc(url):
	try:
		response = requests.get(url)
	except requests.exceptions.MissingSchema:
		return "No item"
	
	soup = BeautifulSoup(response.text, 'html.parser')
	value = soup.find_all("div")
	print(value)
	dom = etree.HTML(str(soup))
	print(dom.xpath('/html/body/div[1]/div'))


url_lider = 'https://www.lider.cl/supermercado/product/La-Crianza-Hamburguesa-Vacuno-Light/279677'
url_santa = "https://www.santaisabel.cl/habas-congeladas-500-g-cuisine-and-co-1763679/p"
url_jumbo = "https://www.jumbo.cl/naranja-granel-2/p"
url_unimarc = "https://www.unimarc.cl/product/shampoo-herbolaria-dpack-tio-nacho-400ml"

supermercados = {
	"colun_yogurt_mora": ["https://www.lider.cl/supermercado/product/Colun-Yoghurt--Batido-Sabor-Mora-Bolsa/5269",
			   			  "https://www.santaisabel.cl/yoghurt-batido-colun-mora-bolsa-1-kg/p"],
	"Loncoleche_sinlactosa": ["https://www.lider.cl/supermercado/product/Loncoleche-Leche-Descremada-Sin-Lactosa-Bolsa/291895",
							  "https://www.santaisabel.cl/leche-descremada-loncoleche-bolsa-800-g-sin-lactosa-instantanea/p"],
	"Svelty_sinlactosa": ["",
						  "https://www.santaisabel.cl/leche-sin-lactosa-svelty-softpack-polvo-descremada800-g/p"],
	"Quaker_avena": ["https://www.lider.cl/supermercado/product/Quaker-Avena-Integral-Instantanea/1015660",
					 "https://www.santaisabel.cl/avena-instantanea-quaker-900-g-2/p"],
	"Vivo_avena": ["https://www.lider.cl/supermercado/product/Vivo-Avena-Instananea/834061",
				   "https://www.santaisabel.cl/avena-instantanea-vivo-900-g/p"],
	"Lider_avena": ["https://www.lider.cl/supermercado/product/Lider-Avena-Instant%C3%A1nea/1089058",
	                ""],
	"Carozzy_fideos": ["https://www.lider.cl/supermercado/product/Carozzi-Pasta-Vitaminizada-Spaghetti-5-Bolsa/2713",
					   "https://www.santaisabel.cl/spaghetti-n-5-carozzi-bolsa-400-g-2/p"],
	"lucchetti_fideos": ["https://www.lider.cl/supermercado/product/Lucchetti-Fideos-Spaghetti-5-Bolsa/10703",
						 "https://www.santaisabel.cl/spaghetti-n-5-lucchetti-bolsa-400-g/p"],
	"Trattoria_fideos": ["https://www.lider.cl/supermercado/product/Trattoria-Trigos-Dorados-Spaghetti-5-con-Huevos-Frescos-Bolsa/270334",
				  "https://www.santaisabel.cl/spaghetti-n-5-trattoria-bolsa-400-g-con-huevos-frescos/p"],
	"Recetadelabuelo_hamburguesa": ["https://www.lider.cl/supermercado/product/Receta-del-Abuelo-Hamburguesa-Vacuno/736033",
									"https://www.santaisabel.cl/hamburguesa-receta-del-abuelo-100-g/p"],
	"Frac": ["https://www.lider.cl/supermercado/product/Costa-Galletas-Frac-Vainilla/2975,"
			 "https://www.santaisabel.cl/galletas-frac-costa-130-g-vainilla-2/p"]
	"Pomarola_salsa": ["https://www.lider.cl/supermercado/product/Pomarola-Salsa-de-Tomate-Italiana-Bolsa/7923",
					   "https://www.santaisabel.cl/salsa-de-tomate-pomarola-carozzi-doypack-200-g-italiana/p"]
	
	
}

prod_lider = []
prod_santa = []
for producto, link in supermercados.items():
	
	lider = link[0]
	santa = link[1]
	try:
		prod_lider.append((producto, scrap_lider(lider)))
	except IndexError:
		print(producto, link)
	
	try:
		prod_santa.append((producto, scrap_santaisabel(santa)))
	except IndexError:
		print(producto, link)

print(prod_lider)
print(prod_santa)
