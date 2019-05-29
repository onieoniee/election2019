# %%
import time
import pandas as pd
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#define: membuat function
def crawl_data(url, second=5):
    # specify the url

    # The path to where you have your chrome webdriver stored:
    webdriver_path = '/Users/user/Downloads/chromedriver'

    # Add arguments telling Selenium to not actually open a window
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920x1080')

    # Fire up the headless browser
    browser = webdriver.Chrome(executable_path=webdriver_path,
                               options=chrome_options)

    # Load webpage
    browser.get(url)

    # It can be a good idea to wait for a few seconds before trying to parse the page
    # to ensure that the page has loaded completely.
    time.sleep(second)

    # Parse HTML, close browser
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.quit()

    return soup


def extract_data_pemilu(value):
    # ada beberapa yang valuenya -, kembalikan None
    if value == '-':
        return None

    # hapus spasi di value
    return value.replace(' ', '')


def get_kawal2014():
    soup = crawl_data(
        'https://2014.kawalpemilu.org/#0', second=10)

    results = soup.find('table', {'class': 'aggregate'})
    rows = results.find_all('tr', {'class': 'datarow'})

    kawal2014 = pd.DataFrame(columns=['wilayah', 'jokowi', 'prabowo'])

    # find results within table
    for r in rows:
        # find all columns per result
        data = r.find_all('td')
        # check that columns have data
        if len(data) == 0:
            continue

        satu = data[2].getText()
        dua = data[10].getText()
        # Remove decimal point
        satu = satu.replace('.', '')
        dua = dua.replace('.', '')
        # Cast Data Type Integer
        satu = int(satu)
        dua = int(dua)

        kawal2014 = kawal2014.append({
            'wilayah': data[1].find('a').getText().lower(),
            'jokowi': satu,
            'prabowo': dua
        }, ignore_index=True)

    return kawal2014


data_kawal2014 = get_kawal2014()


# %%
def get_kawal_pemilu():
    soup2 = crawl_data('https://kawalpemilu.org/#0', second=10)

    # find results within table
    results2 = soup2.find('table', {'class': 'table'})
    rows2 = results2.find_all('tr', {'class': 'row'})

    kawal = pd.DataFrame(columns=['wilayah', 'jokowi', 'prabowo'])

    for r in rows2:
        # find all columns per result
        data = r.find_all('td')
        # check that columns have data
        if len(data) == 0:
            continue

        satu = data[2].find('span', attrs={'class': 'abs'}).getText()
        dua = data[3].find('span', attrs={'class': 'abs'}).getText()
        # Remove decimal point
        satu = satu.replace('.', '')
        dua = dua.replace('.', '')
        # Cast Data Type Integer
        satu = int(satu)
        dua = int(dua)

        kawal = kawal.append({
            'wilayah': data[1].find('a').getText().lower(),
            'jokowi': satu,
            'prabowo': dua
        }, ignore_index=True)

    return kawal


data_kawal = get_kawal_pemilu()


# %%
def calculate_pemilih(kawal2014, kawal2019):
    provinsi = ['aceh', 'sumatera utara', 'sumatera barat', 'riau',
                'jambi', 'sumatera selatan', 'bengkulu', 'lampung']

    # ambil data bps yang ada di provinsi sumatra
    # kawal2014 = kawal2014[kawal2014['wilayah'].isin(provinsi)]

    # ambil 2010
    jumlah_pemilih1 = kawal2014['jokowi'] + kawal2014['prabowo']

    pemilih1 = pd.DataFrame({
        'wilayah': kawal2014['wilayah'],
        'Tahun 2014': jumlah_pemilih1.astype('int')
    })

    # ambil data kawal pemilu dari provinsi sumatra
    # kawal2019 = kawal2019[kawal2019['wilayah'].isin(provinsi)]

    # jumlahkan pemilih
    jumlah_pemilih = kawal2019['jokowi'] + kawal2019['prabowo']

    pemilih = pd.DataFrame({
        'wilayah': kawal2019['wilayah'],
        'Tahun 2019': jumlah_pemilih.astype('int')
    })

    return pd.merge(pemilih1, pemilih, on='wilayah')


df = calculate_pemilih(data_kawal2014, data_kawal)

# %%
# plot golput
df.plot.bar(x='wilayah', y=['Tahun 2014', 'Tahun 2019'])
plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
plt.title('Grafik Pemilih dari tahun 2014 ke 2019')
plt.xlabel('Provinsi')
plt.ylabel('Jumlah Penduduk')
plt.show()