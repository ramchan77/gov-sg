import re
import pandas as pd
import time
import glob
import string
import json
import requests
import justext
from bs4 import BeautifulSoup

count=0
fd = open('gov_sg_output_mm.csv','a')
fd.write('"Main Title";"Title";"Website";"Comapny Mail";"Telephone";"Fax";"Address 1";"Address 2";"Address 3";"Address 4";"Address 5";"Fullname";"Designation";"Email";"Phone"\r\n')
fd.close()
def get_page_data(url):
    try:
        r = requests.get(url)
    except:
        get_page_data(url)
    try:
        result=BeautifulSoup(r.content)
    except:
        fd = open('error_link.csv','a')
        fd.write(str(url)+'\r\n')
        fd.close()
        result=''
    return result
def get_staff_data(result):
    global count
    global main_title
    count+=1
    try:
    	contacts=result.findAll('ul',{'class':''})
    except Exception as e:
    	print(e)
    try:
        title=result.find('div',{'class':'agency-title'}).text.encode("utf-8")
    except:
        title=''
    print('Result Of Page : '+str(count)+' '+str(main_title)+' -- '+str(title))
    try:
        address=result.find('address')
        all_address=address.find('p',{'class':'street-address'}).text.split('\r\n')
    except:
        pass
    try:
        address_1=all_address[0]
    except:
        address_1=''
    try:
        address_2=all_address[1]
    except:
        address_2=''
    try:
        address_3=all_address[2]
    except:
        address_3=''
    try:
        address_4=all_address[3]
    except:
        address_4=''
    try:
        address_5=all_address[4]
    except:
        address_5=''
    try:
        tel_info=address.findAll('p',{'class':'tel-info'})
    except:
        pass
    try:
        tel=tel_info[0].text
    except:
        tel=''
    try:
        fax=tel_info[1].text
    except:
        fax=''
    try:
        web_email=address.find('p',{'class':'website'}).findAll('a')
    except:
        pass
    try:
        website=web_email[0].text
    except:
        website=''
    try:
        email=web_email[1].text
    except:
        email=''    
    for aa in contacts:
        li_tag=aa.findAll('li')
        for li_item in li_tag:
            Designation=''
            Name=''
            Email=''
            Telephone=''
            if li_item.has_attr('id'):
                Designation=li_item.find('div',{'class':'rank'}).text
                Name=li_item.find('div',{'class':'name'}).text
                Email=li_item.find('div',{'class':'email'}).text
                Telephone=li_item.find('div',{'class':'tel'}).text
                try:
                    fd = open('gov_sg_output_mm.csv','a')
                    fd.write('"'+str(main_title.encode("utf-8"))+'";"'+str(title.encode("utf-8"))+'";"'+str(website.encode("utf-8"))+'";"'+str(email.encode("utf-8"))+'";"'+str(tel.encode("utf-8"))+'";"'+str(fax.encode("utf-8"))+'";"'+str(address_1.encode("utf-8"))+'";"'+str(address_2.encode("utf-8"))+'";"'+str(address_3.encode("utf-8"))+'";"'+str(address_4.encode("utf-8"))+'";"'+str(address_5.encode("utf-8"))+'";"'+str(Name.encode("utf-8"))+'";"'+str(Designation.encode("utf-8"))+'";"'+str(Email.encode("utf-8"))+'";"'+str(Telephone.encode("utf-8"))+'"\r\n')
                    fd.close()
                except Exception as e:
                    print(e)
def get_subdirectories(result):
    sub_dir=[]
    next_list=result.findAll('ul',{'class':'section-listing'})
    next_list=list(set(next_list))
    for nl in next_list:
        aTag=nl.findAll('a')
        for att in aTag:
            sub_dir.append('https://www.gov.sg'+str(att.get('href')))
    return sub_dir
root_link=['https://www.gov.sg/sgdi/ministries/moe/statutory-boards/np/departments/olt','https://www.gov.sg/sgdi/ministries/mfa/departments/hq/departments/da/departments/tp','https://www.gov.sg/sgdi/ministries/moh/departments/aic/departments/ctd','https://www.gov.sg/sgdi/ministries/moh/departments/nhgp/departments/cs']
for link in root_link:
    page_data=get_page_data(link)
    try:
        main_title=page_data.find('div',{'class':'agency-title'}).text
    except Exception as e:
        print(e)
    print(main_title)
    staff_data=get_staff_data(page_data)
    sundirectories=get_subdirectories(page_data)
    nested_sub=[]
    #print('root',link)
    for sub_dir_link in sundirectories:
        #print('subdirectory',sub_dir_link)
        page_data=get_page_data(sub_dir_link)
        staff_data=get_staff_data(page_data)
        nes_sub=get_subdirectories(page_data)
        nested_sub+=nes_sub
    old_sub=nested_sub
    new_sub=[]
    #print('old sub',old_sub)
    #print('old sub count',len(old_sub))
    while len(old_sub)>1:
        for ns_link in old_sub:
            #print('ns sub',ns_link)
            page_data=get_page_data(ns_link)
            staff_data=get_staff_data(page_data)
            nes_sub=get_subdirectories(page_data)
            new_sub+=nes_sub
        old_sub=new_sub
        new_sub=[]
        #print('old sub',old_sub)
        #print('old sub count',len(old_sub))
            
    
