from bs4 import BeautifulSoup
import requests
import re
import urllib.request, urllib.error, urllib.parse
import os
import argparse
import sys
import json
# adapted from http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search


def get_soup(url, header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')


def main(args):
    parser = argparse.ArgumentParser(description='Scrape Google images')
    parser.add_argument('-s', '--search', default='bananas', type=str, help='search term')
    parser.add_argument('-n', '--num_images', default=10, type=int, help='num images to save')
    parser.add_argument('-d', '--directory', default='utilities/downimages', type=str, help='save directory')
    parser.add_argument('-f', '--filter', default='isz:m,itp:photo,ic:trans,ift:png', type=str,
                        help='filter string from google advanced search tbs param')
    args = parser.parse_args()
    # query = args.search     #raw_input(args.search)
    filters = args.filter
    max_images = args.num_images
    save_directory = args.directory
    # query = query.split()
    # query = '+'.join(query)
    # url = "https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch&tbs="+filters
    categories = ["abdominal-wounds", "burns", "epidermolysis-bullosa", "extravasation-wound-images",
                  "foot-ulcers", "haemangioma", "leg-ulcer-images", "leg-ulcer-images-2", "malignant-wound-images",
                  "meningitis", "orthopaedic%20wounds", "miscellaneous", "pressure-ulcer-images-a",
                  "pressure-ulcer-images-b", "pilonidal-sinus", "toes"]
    base = "http://www.medetec.co.uk/slide%20scans/"

    # header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)
    # Chrome/43.0.2357.134 Safari/537.36"}
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/43.0.2357.134 Safari/537.36", 'Accept': 'text/html,application/xhtml+xml,'
                                                                            'application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive'}

    for c, cate in enumerate(categories):
        index = base + cate + "/index.html"
        indexPage = get_soup(index, header)
        hrefs = indexPage.find_all('a', href=True)
        mx = 0
        for h in hrefs:
            if 'target' in h['href']:
                for n in re.findall(r'\d+', h['href']):
                    mx = max(int(n), mx);
        print(mx)

        for t in range(mx):
            url = base + cate + "/target" + str(t) + ".html"
            soup = get_soup(url, header)
            ActualImages = []  # contains the link for Large original images, type of image
            for a in soup.find_all('img'):
                link = base + cate + "/" + a.get('src')
                ActualImages.append(link)
            for i, img in enumerate(ActualImages):
                try:
                    req = urllib.request.Request(img, headers=header)
                    raw_img = urllib.request.urlopen(req).read()

                    f = open(os.path.join(save_directory, cate + "_img_" + str(t) + ".jpg"), 'wb')
                    f.write(raw_img)
                    f.close()
                except Exception as e:
                    print(("could not load : " + img))
                    print(e)


if __name__ == '__main__':
    from sys import argv

    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()
