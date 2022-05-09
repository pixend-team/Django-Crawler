from argparse import ONE_OR_MORE
import scrapy
import re
from bato_scraper.bato_scraper.items import TheodoTeamItem
import random

class TheodoSpider(scrapy.Spider):

    custom_settings = {
        "DOWNLOAD_DELAY": (random.randrange(3, 8)),
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }

    name = "theodo"
    def parse(self, response):

#whole body ------------------------------------------------------------------------------------------------

            body = response.css("body").get()

#product name ----------------------------------------------------------------------------------------------

            product_name = response.css("#productTitle::text").get().strip()

#seller name and link --------------------------------------------------------------------------------------

            seller = response.css("#bylineInfo::text").get().strip()
            seller_link = "https://www.amazon.ae"+response.css("#bylineInfo::attr(href)").get()

#orginal price ---------------------------------------------------------------------------------------------

            price_box = response.css("#olpLinkWidget_feature_div").get()
            on_time_price_1 = re.search(r"AED(.*?)\d+.\d+",price_box)
            if on_time_price_1 != None:
                on_time_price = on_time_price_1.group().replace("AED","").strip()
            else:
                on_time_price = "Not Found"
            price_for_24h = response.css("span.a-offscreen::text").get().replace("AED","")

#delivery price --------------------------------------------------------------------------------------------
            
            delivery_price_apex = response.css("#apex_desktop").get()
            delivery_price_box = response.css("#deliveryBlockContainer").get()

            # print(delivery_price_box)
            free_delivery = re.search(r'FREE delivery',delivery_price_box)
            import_fee_included = re.search(r'Estimated Import Fees Deposit',delivery_price_apex)
            delivery_on_time_price_fee = re.search(r'\d+.\d+ delivery',delivery_price_box)
            delivery_price_fee_24h_1 = re.search((r'\+ (.*?)\d+.\d+ \D+\<'),delivery_price_apex)
            if delivery_price_fee_24h_1 != None:
                delivery_price_fee_24h = delivery_price_fee_24h_1.group()
            else:
                delivery_price_fee_24h = "Not Found"
            if free_delivery == None:
                if delivery_on_time_price_fee != None:
                    delivery_price = delivery_on_time_price_fee.group()
                else:
                    delivery_price = import_fee_included.group()
            else:
                delivery_price = free_delivery.group()
     
#delivery time ---------------------------------------------------------------------------------------------

            delivery_date_unclean = response.css("#deliveryBlockContainer").get()
            try:
                delivery_date = re.search(r'\w+ \d+ - \d+', delivery_date_unclean).group()
            except AttributeError:
                delivery_date_0 = re.search(r'\w+, \w+ \d+', delivery_date_unclean)
                if delivery_date_0 != None:
                    delivery_date = delivery_date_0.group()
                else:
                    delivery_date = "From outside of UAE"

#customer review count and score ----------------------------------------------------------------------------

            customer_review_count = response.css("#acrCustomerReviewText::text").get("data")
            customer_review_score = body.split('\"a-icon-alt\">')[1].split("<")[0]
            
            if customer_review_count == "data":
                customer_review_count = "Not rated yet"
                customer_review_score = "Not rated yet"

#table of datas --------------------------------------------------------------------------------------------

            product_details_keys = []
            product_details_values = []
            try:
                product_details_keys_unclean = response.css("th.prodDetSectionEntry::text").getall()
                product_details_values_unclean = response.css("td.prodDetAttrValue::text").getall()
                for unclean_keys in product_details_keys_unclean:
                    product_details_keys.append(unclean_keys.strip())
                for unclean_values in product_details_values_unclean:
                    product_details_values.append(unclean_values.replace("\u200e","").replace("/n","").strip())
                asin_index = product_details_keys.index("ASIN")
                product_details = dict(zip(product_details_keys[:asin_index], product_details_values))
            except:
                product_details = "no table found"

#product datas --------------------------------------------------------------------------------------------

            list_unclean2 = []
            key_list = []
            value_list = []
            try:
                product_datas_div = response.css("#detailBullets_feature_div").get()
                list_unclean1 = product_datas_div.split("</span>")[:-1]
                for i in range(len(list_unclean1)):
                    list_unclean2.append(list_unclean1[i][::-1].split(">",1)[0][::-1].replace(":","").replace("\n","").replace("\u200f","").replace("\u200e","").strip())
                list_unclean2 = list(filter(None,list_unclean2))
                for i in range(len(list_unclean2)):
                    if i%2 == 0:
                        key_list.append(list_unclean2[i])
                    else:
                        value_list.append(list_unclean2[i])
                product_datas = dict(zip(key_list,value_list))
            except:
                product_datas = "No datas Found"
                
#product images href links --------------------------------------------------------------------------------

            images_list = []
            images_list_smallsize = []
            images_div = response.css('#altImages').get()
            images_html = images_div.split("src=")[1:-1]
            for i in range(len(images_html)):
                images_list_smallsize.append(images_html[i].split('"',2)[1][::-1])
            for i in range(len(images_list_smallsize)):
                images_list.append(images_list_smallsize[i].split(".",2)[2][::-1]+"._AC_LS1500_.jpg")

#add to database ------------------------------------------------------------------------------------------           

            item = TheodoTeamItem()
            # item["name"] = response.xpath("//div[@class='quote']").get()
            item.save()

#test prints ----------------------------------------------------------------------------------------------

            print("\n    y\n   y\n  y\ny\n y\n  y\n   y\n   y\n")
            print("product_name: "+product_name)
            print("on_time_price: "+on_time_price)
            print("price_for_24h: "+price_for_24h)
            print("delivery_date: "+delivery_date)
            print("delivery_price: "+delivery_price)
            print("delivery_price_fee_24h: "+delivery_price_fee_24h)
            print("seller: "+seller)
            print("seller_link: "+seller_link)
            print("customer_review_count: "+customer_review_count)
            print("customer_review_score: "+customer_review_score)
            print("product_details:")
            print(product_details)
            print("product_datas:")
            print(product_datas)
            print("images_list:")
            print(images_list)
            print("\n    y\n   y\n  y\ny\n y\n  y\n   y\n   y\n")
            # print(delivery_price_apex)
            print("\n    y\n   y\n  y\ny\n y\n  y\n   y\n   y\n")

            yield item