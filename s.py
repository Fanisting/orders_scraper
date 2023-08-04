import playwright

def crawl_taobao(page):
    orders = []
    # Find elements
    createDateList = page.query_selector_all('//div/table/tbody/tr/td/label/span[2]')
    orderNoList = page.query_selector_all('//div/table/tbody/tr/td/span/span[3]')
    seller = page.query_selector_all('//div/table/tbody/tr/td[2]/span/a')
    orderSuccess = page.query_selector_all('//div/table/tbody[2]/tr/td[6]/div/p/span')
    goodsDetail = page.query_selector_all('//div/table/tbody[2]')
    goodsNum = page.query_selector_all('//div/table/tbody[2]/tr/td[3]/div/p')
    totalPay = page.query_selector_all('//div/table/tbody[2]/tr/td[5]/div/div/p')

    
    for i in range(len(createDateList)):
        tr = goodsDetail[i].query_selector_all('tr')
        goods = []
        for item in tr:
            name_element = item.query_selector('td > div > div:nth-child(2) > p > a > span:nth-child(2)')
            name = name_element.inner_text() if name_element else ''
            
            if name == '保险服务':
                break
            
            links_element = item.query_selector('td > div > div:nth-child(2) > p > a')
            links = links_element.get_attribute('href') if links_element else ''

            p = item.query_selector_all('td > div > div:nth-child(2) p')
            deliveryTime = ''
            if len(p) == 4:
                delivery_time_element = p[3].query_selector('span:nth-child(2)')
                deliveryTime = delivery_time_element.inner_text() if delivery_time_element else ''
            
            goods.append({"links": links, "name": name, "deliveryTime": deliveryTime})
        
        order = {
            "createDate": createDateList[i].inner_text(),
            "orderNo": orderNoList[i].inner_text(),
            "totalPay": totalPay[i].inner_text(),
            "goods": goods,
            "goodsNum": goodsNum[i].inner_text()
        }
        orders.append(order)
    return orders