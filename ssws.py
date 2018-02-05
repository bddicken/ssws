import requests

ignore_url_ends = ['.pdf', 'mp3', 'gif', 'jpg', 'jpeg', 'png', 'zip', 'wav', 'ppm']
base_url = input('Enter URL to begin scraping at: ')
word_counts = {}

###
### Given the contents of an html page as text (html_page_text) and the associated url of that page,
### Return a list of all URLS on the same domain that this page links to.
###
def get_url_links_from_page(html_page_text, url):
    hrefs = []
    lines = html_page_text.split('\n')
    # Find all of the <a> links, get the href's
    for l in lines:
        if '<a' in l:
            i1 = l.index('<a')
            while i1 < len(l):
                if l[i1:].startswith('href="'):
                    i2 = i1 + 6
                    i3 = i1 + 6
                    while l[i3] != '"' and i3 < len(l):
                        i3 += 1
                    hrefs.append(l[i2:i3])
                i1+=1
    if url.endswith('index.html'):
        url = url[:-10]
    urls = []
    # Convert the hrefs to valid URLs
    for p in hrefs:
        if p.startswith('./'):
            urls.append(url + '/' + p[2:])
        elif p.startswith('/'):
            urls.append(base_url + p)
    # Return a list of valid URLs to caller
    return urls

###
### The proess function.
### Called for each scraped page.
### Gathers word counts for the entire scrape.
###
def do_word_count(page_data):
    sp = page_data.split(' ')
    for s in sp:
        if s not in word_counts:
            word_counts[s] = 0
        word_counts[s]+=1

###
### Called to summarize the findings of the scrape.
###
def summarize():
    sorted_word_counts = [(k, word_counts[k]) for k in sorted(word_counts, key=word_counts.get, reverse=True)]
    for k,v in sorted_word_counts:
        if (v > 10):
            print(k + " -> " + str(v))

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
        if ok:
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
main()

