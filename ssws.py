###
### SSWS stands for "Super Simple Web Scraper".
### This is a simple, single-file implementation of a web scraper.
### Presently, it just gathers word-counts for web-pages (or web-page trees)
###

import requests

ignore_url_ends = ['.pdf', 'mp3', 'gif', 'jpg', 'jpeg', 'png', 'zip', 'wav', 'ppm']
base_url = input('Enter URL to begin scraping at: ')
recurse = input('Should I follow pages linked from this page (y/n) ? ')
word_counts = {}

###
### Given the contents of an html page as text (html_page_text) and the associated url of that page,
### Return a list of all URLS on the same domain that this page links to.
###
def get_url_links_from_page(html_page_text, url):
    hrefs = []
    lines = html_page_text.split('\n')
    # Find all of the <a> links, get the href's
    for line in lines:
        if '<a' in line:
            i1 = line.index('<a')
            while i1 < len(line):
                if line[i1:].startswith('href="'):
                    i2 = i1 + 6
                    i3 = i1 + 6
                    while line[i3] != '"' and i3 < len(line):
                        i3 += 1
                    hrefs.append(line[i2:i3])
                i1+=1
    if url.endswith('index.html'):
        url = url[:-10]
    urls = []
    # Convert the hrefs to valid URLs
    for path in hrefs:
        if path.startswith('./'):
            urls.append(url + '/' + path[2:])
        elif path.startswith('/'):
            urls.append(base_url + path)
    # Return a list of valid URLs to caller
    return urls

###
### The proess function.
### Called for each scraped page.
### Gathers word counts for the entire scrape.
###
def do_word_count(page_data):
    words = page_data.split(' ')
    for word in words:
        word = word.strip('\n')
        if word not in word_counts:
            word_counts[word] = 0
        word_counts[word]+=1

###
### Called to summarize the findings of the scrape.
###
def summarize():
    sorted_word_counts = [(k, word_counts[k]) for k in sorted(word_counts, key=word_counts.get, reverse=True)]
    for k,v in sorted_word_counts:
        if (v > 10):
            print(k.rjust(15) + " -> " + str(v))

###
### Recursive helper function for scrape_url_tree.
### scrape_url is any valid web URL.
### depth is the current URL tree depth.
### process_function is a function that this function will call, and pass each pages content to, for further processing.
###
def scrape_url_tree_helper(scrape_url, depth, process_function):
    print('  ' * depth + 'SCRAPING URL: ' + scrape_url)
    page = requests.get(scrape_url)
    html = page.text
    # Call processing function
    process_function(html)
    urls = get_url_links_from_page(html, scrape_url)
    for u in urls:
        ok = True
        for end in ignore_url_ends:
            if u.endswith(end):
                ok = False
                break
        if ok and recurse == 'y':
            scrape_url_tree_helper(u, depth+1, process_function)

###
### Call this function to begin scrping the scrape_url, and all linked URLs on the same domain.
### scrape_url should be a valid web URL.
###
def scrape_url_tree(scrape_url):
    scrape_url_tree_helper(scrape_url, 0, do_word_count)

###
### Starting point!
###
def main():
    scrape_url_tree(base_url)
    summarize()

### :)
try:
    main()
except:
    print('SSWS experienced an issue. Please double-check your URL.')

