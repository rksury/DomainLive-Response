import csv
import openpyxl
import xlrd
from concurrent.futures import ThreadPoolExecutor
import requests
pool = ThreadPoolExecutor(max_workers=2)


def get_list(filename):
    if filename.endswith('csv'):
        with open(filename) as csv_file:
            url_from_csv = csv.reader(csv_file)
            print(url_from_csv)
            return [url[0] for url in url_from_csv if url]

    # if filename.endswith('xlrd'):
    #     wb = xlrd.open_workbook(filename, 'r')
    #     url_from_xlsx = wb.sheet_by_index(1:1)
    #     print(url_from_xlsx)
    #     return [url[0] for url in url_from_xlsx if url]

    if filename.endswith('txt'):
        text_file = open(filename, 'r')
        url_from_text = text_file.read()
        print(url_from_text)
        return [url[0] for url in url_from_text if url]


def get_status(url):
    # if url is not valid, error
    # if not starting with http/https
    try:
        res = requests.get(url)
        if res.status_code == 200:
            status = 'Success'
        elif res.status_code == 302:
            status = 'Redirected'
        elif res.status_code == 404:
            status = 'Not Found'
        else:
            print(res.status_code)
        # output_text = open('output.txt', 'a+')
        # for i in range(20):
        #     output_text.write([url, res.status_code, status])
        #     output_text.close()
        with open('output.csv', 'a') as csv_output:
            fields = ['Domain Name', 'Status Code', 'Status']
            output_writer = csv.writer(csv_output)
            output_writer.writerow(fields)
            output_writer.writerow([url, res.status_code, status])
    except Exception as e:
        status = str(e)

def get_status_of_all_csvurls(csvurls):
    for url in csvurls:
        future = pool.submit(get_status, (url))

def get_status_of_all_txturls(txturls):
    for url in txturls:
        future = pool.submit(get_status, (url))

def get_status_of_all_xlsxurls(xlsxurls):
    for url in xlsxurls:
        future = pool.submit(get_status, (url))

csvurls = get_list('urls.csv')
get_status_of_all_csvurls(csvurls)

txturls = get_list('urls.txt')
get_status_of_all_txturls(txturls)

# xlsxurls = get_list('urls.xlsx')
# get_status_of_all_xlsxurls(xlsxurls)