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


def extract_data_penduduk(value):
    # ada beberapa yang valuenya -, kembalikan None
    if value == '-':
        return None

    # hapus spasi di value
    return value.replace(' ', '')


def get_bps():
    soup = crawl_data(
        'https://www.bps.go.id/statictable/2009/02/20/1267/'
        'penduduk-indonesia-menurut-provinsi-1971-1980-1990-1995-2000-dan-2010.html'
    )

    bps = pd.DataFrame(columns=['wilayah', '1971', '1980', '1990', '1995', '2000', '2010'])

    # find results within table
    for r in soup.find_all('table')[2].find_all('tr', {'class': 'xl6310505'})[1:-3]:
        value = r.find_all('td', {'class', 'xl7610505'})

        bps = bps.append({
            'wilayah': r.find('td', {'class', 'xl6810505'}).get_text().replace('\n', '').replace('  ', ' ').lower(),
            '1971': extract_data_penduduk(value[0].get_text()),
            '1980': extract_data_penduduk(value[1].get_text()),
            '1990': extract_data_penduduk(value[2].get_text()),
            '1995': extract_data_penduduk(value[3].get_text()),
            '2000': extract_data_penduduk(value[4].get_text()),
            '2010': extract_data_penduduk(value[5].get_text())
        }, ignore_index=True)

    return bps


data_bps = get_bps()

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
def calculate_pemilih(bps, kawal2014, kawal2019):
    provinsi = ['aceh', 'sumatera utara', 'sumatera barat', 'riau',
                'jambi', 'sumatera selatan', 'bengkulu', 'lampung']

    # ambil data bps yang ada di provinsi sumatra
    # bps = bps[bps['wilayah'].isin(provinsi)]

    # ambil 2010
    penduduk = pd.DataFrame({
        'wilayah': bps['wilayah'],
        'penduduk': bps['2010'].astype('int')
    })

    # ambil data kawal2014 pemilu dari provinsi sumatra
    # kawal2014 = kawal2014[kawal2014['wilayah'].isin(provinsi)]

    # jumlahkan pemilih2014
    jumlah_pemilih = kawal2014['jokowi'] + kawal2014['prabowo']
    golput = penduduk['penduduk'] - jumlah_pemilih

    pemilih2014 = pd.DataFrame({
        'wilayah': kawal2014['wilayah'],
        'Golput 2014': golput.fillna(0).astype('int')
    })

    # ambil data kawal2019 pemilu dari provinsi sumatra
    # kawal2019 = kawal2019[kawal2019['wilayah'].isin(provinsi)]

    # jumlahkan pemilih
    jumlah_pemilih2 = kawal2019['jokowi'] + kawal2019['prabowo']
    golput2 = penduduk['penduduk'] - jumlah_pemilih2

    pemilih2019 = pd.DataFrame({
        'wilayah': kawal2019['wilayah'],
        'Golput 2019': golput2.fillna(0).astype('int')
    })

    m = pd.merge(penduduk, pemilih2014, on='wilayah')
    return pd.merge(m, pemilih2019, on='wilayah')



df = calculate_pemilih(data_bps, data_kawal2014, data_kawal)

# %%
# plot golput
df.plot.bar(x='wilayah', y=['penduduk', 'Golput 2014','Golput 2019'])
plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
plt.show()