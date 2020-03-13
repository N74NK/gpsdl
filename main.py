# -*- coding: utf-8 -*-


import sys, os
from nyvt1 import progress
from urllib.parse import quote_plus


'''

[  Code by Njank Yuti  ]
[  I'am not pro coder  ]

Find me:
    https://github.com/N74NK
    https://facebook.com/njnk.xnxx
    https://instagram.com/n74nk.420
    https://solozstring.blogspot.com

Note:
    Remame author, kontolnya pecah!
    
'''


W = '\033[0m'
D = '\033[90m'
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
P = '\033[95m'
C = '\033[96m'


try:
	import requests
	from bs4 import BeautifulSoup
except:
	os.system('pip install requests bs4')


def ny_cari(query):
    ny_res = requests.get('https://apkpure.com/search?q={}&region='.format(quote_plus(query)),
             headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) '
                      'Version/9.1.2 Safari/601.7.5 '}).text
    ny_sop = BeautifulSoup(ny_res, "html.parser")
    ny_sr = ny_sop.find('div', {'id': 'search-res'}).find('dl', {'class': 'search-dl'})
    app_tag = ny_sr.find('p', {'class': 'search-title'}).find('a')
    download_link = 'https://apkpure.com' + app_tag['href']
    return download_link


'''

[  Code by Njank Yuti  ]
[  I'am not pro coder  ]

Find me:
    https://github.com/N74NK
    https://facebook.com/njnk.xnxx
    https://instagram.com/n74nk.420
    https://solozstring.blogspot.com

Note:
    Remame author, kontolnya pecah!
    
'''


def download(link):
    ny_res2 = requests.get(link + '/download?from=details', headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) '
                      'Version/9.1.2 Safari/601.7.5 '
    }).text
    soup = BeautifulSoup(ny_res2, "html.parser").find('a', {'id': 'download_link'})
    if soup['href']:
        r = requests.get(soup['href'], stream=True, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) '
                          'Version/9.1.2 Safari/601.7.5 '
        })
        with open(link.split('/')[-1] + '.apk', 'wb') as file:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), label='downloading', expected_size=(total_length/1024) + 1):
                if chunk:
                    file.write(chunk)
                    # sys.stdout.write('\rProses: ')
                    file.flush()


def download_apk(app_id):
    download_link = ny_cari(app_id)
    '''
    
    [  Code by Njank Yuti  ]
    [  I'am not pro coder  ]
    
    Find me:
        https://github.com/N74NK
        https://facebook.com/njnk.xnxx
        https://instagram.com/n74nk.420
        https://solozstring.blogspot.com
    
    Note:
        Remame author, kontolnya pecah!
        
    '''
    if download_link is not None:
        ny_res = requests.get(download_link + '/').text
        ny_size = BeautifulSoup(ny_res, "html.parser").find('span',{'class':'ver-item-s'}).text
        print(f'  name: {download_link}'.replace('https://apkpure.com/','').replace('/','').replace(f'{ny_pkg}','').replace('-',' ').title())
        print(f'  size: {ny_size}')
        download(download_link)
        print(f'  download completed! {ny_pkg}.apk\n'.replace('https://play.google.com/store/apps/details?id=',''))
    else:
        print('  no results\n')


print(f''' \n
      .
       .
   . ;.
    .;
     ;;.  
   ;.;;    
   ;;;;.  [ Play Store Apk Downloader ]
   ;;;;;   
   ;;;;;     - Author: Njank Yuti
 ..;;;;;..   - Codename: N.yvt1
  ':::::'    - Facebook: njnk.xnxx
    ':`   
''')


if len(sys.argv) < 2:
	print(f'''Usage: python {sys.argv[0]} <play-store-url>
Example: python {sys.argv[0]} https://play.google.com/store/apps/details?id=com.termux
	''')
else:
	ny_pkg=sys.argv[1].replace('https://play.google.com/store/apps/details?id=','')
	download_apk(ny_pkg)
