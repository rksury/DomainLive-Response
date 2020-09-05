import csv
import openpyxl
import xlrd
from concurrent.futures import ThreadPoolExecutor
import requests

pool = ThreadPoolExecutor(max_workers=2)


def get_list(filename):
    try:
        if filename.endswith('csv'):
            with open(filename) as csv_file:
                url_from_csv = csv.reader(csv_file)
                print(url_from_csv)
                return [url[0] for url in url_from_csv if url]

        elif filename.endswith('txt'):
            text_file = open(filename, 'r')
            url_from_text = text_file.readlines()
            return [url.replace('\n', '') for url in url_from_text if url]

        # elif filename.endswith('xlrd'):
        #     wb = xlrd.open_workbook(filename, 'r')
        #     url_from_xlrd = wb.sheet_by_index(0)
        #     print(url_from_xlrd.cell_value(0, 0))
        #     return [url.replace('\n', '') for url in url_from_xlrd if url]
        else:
            print(filename)
    except Exception as e:
        data = str(e)


def get_status(url):
    print(url)
    # fields = ['Domain Name', 'Status Code', 'Status']
    try:
        res = requests.get(url)
        if res.status_code == 200:
            status = 'Success'
        elif res.status_code == 302:
            status = 'Redirected'
        elif res.status_code == 404:
            status = 'Not Found'
        else:
            status =''
        with open('output.csv', 'a') as csv_output:
            output_writer = csv.writer(csv_output)
            output_writer.writerow([url, res.status_code, status])
    except Exception as e:
        status = str(e)


def get_status_of_all_urls(urls):
    for url in urls:
        future = pool.submit(get_status, url)


urls = get_list('urls.csv')
get_status_of_all_urls(urls)

urls = get_list('urls.txt')
get_status_of_all_urls(urls)

# urls = get_list('urls.xlsx')
# get_status_of_all_urls(urls)
