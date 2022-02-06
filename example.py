import fb_crawler

fb = fb_crawler.FacebookPage()
fb.page_url = 'https://www.facebook.com/detikcom'
fb.until_date = '2022-02-06'
data = fb.crawl()
for row in data:
    print(row)
