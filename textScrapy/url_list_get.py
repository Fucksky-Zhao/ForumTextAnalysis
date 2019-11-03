import urllib.request
from lxml import etree
from time import time
# import pandas as pd

start = time()

# url = "https://bbs.51credit.com/forum-8-5.html"

start_url = ["https://bbs.51credit.com/forum-13-" + str(a) + ".html" for a in range(1, 501)]

# df = pd.DataFrame(columns=('url', 'title'))
# i = 0

headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Host': 'bbs.51credit.com',
        # 'Cookie': 'Hm_lpvt_2368db03d58b3a9c27ac58870c989566=1565267908; Hm_lpvt_e1c4a75f7c338d0f46496d0e6fee84c4=1565267908; Hm_lpvt_ed2cce1d377593c5a0c03e66ded87152=1565267908; kcjY_2132_seccodeS00=19baLu7xXERqJHmCsfldmmFOvFXrdd2BUpnyug27%2BhqGCKMY71qcRDsGFkzhTS5PmEdxiKP%2FQE6I; Hm_lpvt_503aa9d07fdc15d3be8984abec3c64ed=1565267896; Hm_lpvt_eeb48e878a0e05acb294a0d8b0299dcb=1565267896; kcjY_2132_viewid=tid_5603691; Hm_lvt_eeb48e878a0e05acb294a0d8b0299dcb=1565267873; kcjY_2132_lastvisit=1565264219; kcjY_2132_sendmail=1; kcjY_2132_atarget=1; kcjY_2132_saltkey=aVrGRjmM; Hm_lvt_2368db03d58b3a9c27ac58870c989566=1565267822,1565267854; Hm_lvt_ed2cce1d377593c5a0c03e66ded87152=1565267822,1565267854; kcjY_2132_ulastactivity=1563086932%7C0; kcjY_2132_lastact=1565267906%09misc.php%09seccode; acw_tc=3ccdc15615652678198547021e2a0f492bb6b70ba40bdb1558579fcb53effe; kcjY_2132_smile=1D1; kcjY_2132_checkpm=1; Hm_lvt_503aa9d07fdc15d3be8984abec3c64ed=1565267873; kcjY_2132_visitedfid=8; kcjY_2132_forum_lastvisit=D_8_1565267869; kcjY_2132_auth=e0a3whiI8CcVgDRGj1qKdUUFZjVR%2BQ0kNRBPvC3XjtWW4l8dgEw4HYN2TGkKhz44mMTmPCqj%2BoK1E97k1OWbWPXsTlRV; Hm_lvt_e1c4a75f7c338d0f46496d0e6fee84c4=1565267822,1565267854; BAIDU_SSP_lcr=https://www.baidu.com/link?url=_rX7u5SeGczRs05yKF8Lrlw3EjIWF6oPYKcE7K--KPgqQQreqSWs4ito7nD4VLQl&wd=&eqid=b3e57a50000cac58000000055d4c1768; Hm_lpvt_e06f837c19a278d81816c90560e0d82d=1565267896; token=eyJhbGciOiJIUzUxMiJ9.eyJvcyI6MiwicGhvbmUiOiIxODIqKioqOTA2NSIsImJic1VJZCI6IjcyMTUxNDUiLCJleHAiOjE1Njc4NTk4NTEsInVzZXJJZCI6MTIzMTQxNTAwNCwiaWF0IjoxNTY1MjY3ODUxLCJ1c2VybmFtZSI6Imthc2hlbjkzNjY0MjYyIn0.efC2KCUw3Rxr5I1Ko1i7--mEHJ2JDhHkxSm1oHRIZYMORxTNYWSOczbZI5UEF1KTzoncXey3Uh7JG7qumI1JQQ; clientkey=739881BF1F270DD0451EB2A98DF9CF6B; Hm_lvt_e06f837c19a278d81816c90560e0d82d=1565267822; source_status=1; smidV2=20190808203703480af48525b9b5a356dd17266b8b744e00c24a04e4cff3570; sessionid=73BF51663DD54FADFDC2CA502E313CF8',
    }

url_list = []
title_list = []

for url in start_url:
    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req).read().decode("utf-8",'ignore')
    response = etree.HTML(response)

    temp = response.xpath('//a[@class="threadlist s xst"]')
    # title_temp = response.xpath('//a[@class="threadlist s xst"]/text()')

    url_list_temp = ["https://bbs.51credit.com/" + a.get('href') for a in temp]
    url_list += url_list_temp
    # title_list += title_list_temp

url_list = set(url_list)

file = open('data_spdb.txt', 'w')
for a in url_list:
    file.write(a+'\n')
file.close()

end = time()
print(str(end - start) + " s")

# print(real_url)
print(len(url_list))
