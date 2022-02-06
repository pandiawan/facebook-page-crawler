Facebook Page Crawler
=================
Scraping post from Facebook Page with BeautifulSoup

## Configuration and Installation

##### Prerequisites:

* Python 3.8.x

##### Install:
```bash
git clone https://github.com/pandiawan/facebook-page-crawler.git
cd facebook-page-crawler
pip3 install . -r requirements.txt
```

##### Example:
```python
import fb_crawler

fb = fb_crawler.FacebookPage()
fb.page_url = 'https://www.facebook.com/detikcom'
fb.until_date = '2022-02-06'
data = fb.crawl()
for row in data:
    print(row)
```

##### Result:
```bash
2022-02-06 18:16:11,966 - Crawling data..
2022-02-06 18:16:52,225 - Get 238 posts
{'id': '10161201584967079', 'author': 'detikcom', 'date': datetime.datetime(2022, 2, 6, 18, 6, 1), 'text': 'Polisi telah mengamankan pelaku pembunuh pria di Nganjuk. Pelaku adalah MYS (28) yang merupakan pegawai korban di toko spring bed.', 'link': 'https://www.facebook.com/374777242078/posts/10161201584967079/', 'comment_count': 1, 'share_count': 0, 'reactions': {'like': 26, 'love': 0, 'haha': 0, 'wow': 1, 'sad': 0, 'angry': 0, 'thankful': 0, 'pride': 0}}
{'id': '10161201579162079', 'author': 'detikcom', 'date': datetime.datetime(2022, 2, 6, 18, 2, 34), 'text': 'Sebuah mobil Suzuki Ertiga ditabrak dump truk di Porong, Sidoarjo. Kecelakaan itu membuat Ertiga itu nyangkut di pohon. Begini pengakuan sopirnya.', 'link': 'https://www.facebook.com/374777242078/posts/10161201579162079/', 'comment_count': 0, 'share_count': 0, 'reactions': {'like': 11, 'love': 0, 'haha': 0, 'wow': 1, 'sad': 0, 'angry': 0, 'thankful': 0, 'pride': 0}}
{'id': '10161201578942079', 'author': 'detikcom', 'date': datetime.datetime(2022, 2, 6, 18, 2, 24), 'text': 'Relawan Joko Widodo (Jokowi) se-Cirebon Raya pamer hasil kerja Presiden Jokowi. Mulai dari jalan tol sepanjang 1.666 KM hingga 27 bendungan', 'link': 'https://www.facebook.com/374777242078/posts/10161201578942079/', 'comment_count': 11, 'share_count': 0, 'reactions': {'like': 19, 'love': 2, 'haha': 9, 'wow': 0, 'sad': 0, 'angry': 0, 'thankful': 0, 'pride': 0}}
...
```