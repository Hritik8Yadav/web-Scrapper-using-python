from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
import pymongo

logging.basicConfig(filename='scrapper.log',level=logging.INFO)


app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review",methods=['GET','POST'])
def final_page():
    if request.method=='POST':
        try:
            Search_name=request.form['content'].replace("  ","")
            # Search_name="creatine"
            Search_url="https://www.flipkart.com/search?q=" + Search_name
            print(Search_url)
            product_data=uReq(Search_url)
            product_page=product_data.read()
            # print(product_page)
            product_data.close()
            rearranged_page=bs(product_page,'html.parser')
            # print(rearranged_page)
            bigboxes=rearranged_page.findAll("div",{'class':'_1AtVbE col-12-12'})
            del bigboxes[0:3]
            # print(bigboxes)
            product_urls=bigboxes[0].div.div.div.a['href']
            final_product_urls='https://www.flipkart.com'+product_urls
            print(final_product_urls)
            page_data=requests.get(final_product_urls)
            page_data.encoding='utf-8'
            arranged_page_data=bs(page_data.text,'html.parser')
            all_data=arranged_page_data.findAll('div',{'class':'_1YokD2 _3Mn1Gg col-8-12'})
            # print(all_data)
            print(len(all_data))
            # print(all_data[0].findAll('div',{'class':'t-ZTKy'}))
            file_name=Search_name+'.csv'
            fle=open(file_name,'w')
            columns="PRODUCT, CUSTOMER NAME, RATING, HEADING, COMMENT \n"
            fle.write(columns)
            all_items=[]

            # for data in all_data:
                # try:
            product_name=all_data[0].div.div.div.p.text
            # print(product_name)
                # except:
                    # print("error in name")
            # print(product_name)
            # customer_name=all_data[0].div.findAll('p',{'class': "row _3n8db9"})
                # try:
            customer_name=all_data[0].findAll('p',{'class': '_2sc7ZR _2V5EHH'})
            # customer_name=all_data[0].div.div.div.div
            # print(customer_name)
            # print(len(customer_name))
                # except:
                    # print("error in cst_name")
            # cst_name=all_data[]
            # print(customer_name)
                # try:
            rating=all_data[0].findAll('div',{'class':'_3LWZlK _1BLPMq'})
            # print(rating)
            # print(len(rating))
                # except:
                    # print("error in rating")
            # print(rating)
                # try:
            heading=all_data[0].findAll('p',{'class':'_2-N8zT'})
            # print(heading)
            # print(len(heading))
                # except
                    # print("error in heading")
            # # print(heading)
                # try:
            full_review=all_data[0].findAll('div',{'class':'t-ZTKy'})
            # print(full_review)
            # print(len(full_review))
                # except:
                    # print("error in review")
            # print(full_review)
            for i in range(len(customer_name)):
                try:
                    Product=product_name
                except:
                    Product=" "
                try:
                    Name=customer_name[i].text
                except:
                    Name=" "
                try:
                    Rating=rating[i].text
                except:
                    Rating=" "
                try:
                    CommentHead=heading[i].text
                except:
                    CommentHead=" "
                try:
                    Comment=full_review[i].text
                except:
                    Comment=" "
                my_dict={"Product": Product,"Name": Name,"Rating": Rating,"CommentHead":CommentHead,"Comment":Comment}
                all_items.append(my_dict)
                
            # print(all_items)
            
            client = pymongo.MongoClient("mongodb+srv://hritik:hritik@cluster0.3w8072c.mongodb.net/?retryWrites=true&w=majority")
            db=client['project']
            col=db['col']
            col.insert_many(all_items)

            logging.info("log my final result {}".format(all_items))
            return render_template('result.html', reviews=all_items[0:(len(all_items)-1)])
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

            

if __name__=="__main__":
    app.run(host="0.0.0.0",port=3000)
