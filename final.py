from msilib.schema import tables
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

#store the lottery number
lottoList=[]

browser=webdriver.Chrome('./chromedriver.exe')
browser.get('https://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx')

#click the options of searching by year/month
browser.find_element_by_id('Lotto649Control_history_radYM').click()
#find "year"
selectYear= Select(browser.find_element_by_id('Lotto649Control_history_dropYear'))
selectYear.select_by_value('110')

for i in range(12):
    #find "month"
    selectMonth=Select(browser.find_element_by_id('Lotto649Control_history_dropMonth'))
    selectMonth.select_by_value(str(i+1))
    #find "search"
    browser.find_element_by_id('Lotto649Control_history_btnSubmit').click()

    #fetch info. from the website
    html=browser.page_source
    soup=bs(html,'html.parser')

    #count the number of tables
    tableCount=len(soup.findAll('table',{'class':'td_hm'}))
    #fetch the lottery number of each table
    for i in range(tableCount):
        for j in range(1,7):
            tmp=soup.find('span',{'id':'Lotto649Control_history_dlQuery_No'+str(j)+'_'+str(i)})
            lottoList.append(int(tmp.text))
print(lottoList)

#count the frequency
lottoCnt=[0]*50
for i in lottoList:
    lottoCnt[i]+=1
print(lottoCnt)

dataSet={'Frequency':lottoCnt[1:]}
df=pd.DataFrame(data=dataSet,index=list(range(1,50)))

#plot
ax=df.plot(kind='bar',figsize=[15,10])
ax.set_yticks(np.arange(1,max(lottoCnt)+1))
ax.set_xlabel('Numbers',size=22)
ax.set_ylabel('Frequency',size=22)
plt.show()