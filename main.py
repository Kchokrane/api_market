
import xmltodict
import requests
import json




def outter(func):
    func = func

    def inner(self, *args, **kwargs):
        try:
            if func(self, *args, **kwargs) == 401:
                self.authentication()
                return func(self, *args, **kwargs)
        except:

            self.authentication()
            return func(self, *args, **kwargs)

    return inner


class MarketApi:
    def __init__(self):
        self.url = ' https://partners-test.mp.fnacdarty.com/api.php/'
        self.headers = {"Content-Type": "text/xml"}
        self.partner_id = '3196F628-84ED-BD50-9F5E-7CF7008354AB'
        self.shop_id = '990E00FC-E315-1583-A611-F1FE67835E74'
        self.key = '1D0141C6-68BA-1FB0-4450-056061D7CDD7'
        self.xmlns = 'http://www.fnac.com/schemas/mp-dialog.xsd'


    def authentication(self):
        url = self.url + '/auth'
        data_dict = {
            'auth': {'@xmlns': self.xmlns, 'shop_id': self.shop_id, 'partner_id': self.partner_id,
                     'key': self.key}}
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        content = self.xml_to_dict(response.text)
        self.token = content['auth_response']['token']
        return self.token

    def xml_to_dict(self, response):

        content = xmltodict.parse(response)
        content_str = json.dumps(content)
        new_dict = json.loads(content_str)
        return new_dict

    @outter
    def offers_update(self, l_dict, *args, **kwargs):

        self.authentication()

        data_dict = {
            'offers_update': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                              '@token': self.token}}
        list_dict = {"product_reference": {"@type": "Ean", "#text": l_dict['product_reference']},
                   "offer_reference": {"@type": "SellerSku", "#text": l_dict['offer_reference']},
                   "price": l_dict['price'],
                   "product_state": l_dict['product_state'],
                   "quantity": l_dict['quantity'], "description": l_dict['description'],
                   "showcase": l_dict['showcase'],



                   }
        for k in list(list_dict.keys()):
            if not list_dict[k]:
                del list_dict[k]
        data_dict['offers_update']['offer'] = list_dict
        xml = xmltodict.unparse(data_dict, encoding='utf-8')
        print(xml)
        response = requests.post(self.url + '/offers_update', headers=self.headers, data=xml.encode())
        print(response.text)
        if response.status_code == 200:
            batch_id = self.xml_to_dict(response.text)['offers_update_response']['batch_id']
            return batch_id
        return 400

    @outter
    def batch_status(self, batch_id):

        batch_dict = {
            'batch_status': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                             '@token': self.token, 'batch_id': batch_id}}
        batch_xml = xmltodict.unparse(batch_dict, encoding='utf-8')
        url = self.url + '/batch_status'
        response = requests.post(url, headers=self.headers, data=batch_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == [200]:
            response_dic = self.xml_to_dict(response.text)
            return response_dic

        return 400

    @outter
    def batch_query(self):

        # self.authentication()
        batch_dict = {
            'batch_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                            '@token': self.token}}
        batch_xml = xmltodict.unparse(batch_dict, encoding='utf-8')
        url = self.url + '/batch_query'
        response = requests.post(url, headers=self.headers, data=batch_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            response_dict = self.xml_to_dict(response.text)

            return response_dict
        return 400

    @outter
    def offers_query(self, paging=1):


        dict_data = {
            'offers_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                             '@token': self.token, '@results_count': 50,
                             'paging': paging}}


        dict_xml = xmltodict.unparse(dict_data, encoding='utf-8')
        url = self.url + '/offers_query'
        response = requests.post(url, data=dict_xml.encode('utf-8'), headers=self.headers)
        print(response.text)
        if response.status_code == 200:
            of_dict = self.xml_to_dict(response.text)
            return of_dict
        return 400

    @outter
    def offers_query_id(self, data):

        dict_data = {
            'offers_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                             '@token': self.token,
                             'offer_seller_id': data}
        }
        dict_xml = xmltodict.unparse(dict_data, encoding='utf-8')
        print(dict_xml)
        url = self.url + '/offers_query'
        response = requests.post(url, data=dict_xml.encode('utf-8'), headers=self.headers)
        print(response.text)
        if response.status_code == 200:
            of_dict = self.xml_to_dict(response.text)
            return of_dict
        return 400

    @outter
    def update_offer_price(self, update_dict):

        dic = {
            'offer_reference': {'@type': 'SellerSku', '#text': update_dict['offer_reference']},
            'price': update_dict['price'],
            'quantity': update_dict['quantity']
        }
        for k in list(dic.keys()):
            if not dic[k]:
                del dic[k]
        print(dic)
        data_dict = {
            'offers_update': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                              '@token': self.token,
                              'offer': dic
                              }
        }
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        response = requests.post(self.url + '/offers_update', headers=self.headers, data=data_xml.encode())
        print(response.text)
        if response.status_code == 200:
            batch_id = self.xml_to_dict(response.text)['offers_update_response']['batch_id']
            return batch_id
        return 400

    @outter
    def delete_offer(self, dicts):

        data_dict = {
            'offers_update': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                              '@token': self.token,
                              'offer': {
                                  'offer_reference': {'@type': 'SellerSku', '#text': dicts['offer_reference']},
                                  'treatment': 'delete'
                              }
                              }
        }
        data_xml = xmltodict.unparse(data_dict, encoding='utf-8')
        response = requests.post(self.url + '/offers_update', headers=self.headers, data=data_xml.encode())
        print(response.text)
        if response.status_code == 200:
            batch_id = self.xml_to_dict(response.text)['offers_update_response']['batch_id']
            return batch_id
            print(batch_id)
        return 400


class MarketOrderApi(MarketApi):
    @outter
    def orders_update(self, update_dict):

        ls = []

        if ',' in update_dict['order_id']:
            lis_id = update_dict['order_id'].split(',')
            for id in lis_id:
                ls.append({'@order_id': id, '@action': update_dict['action'],
                           'order_detail': {'action': update_dict['order_detail_action']}
                           })
        else:
            ls = {'@order_id': update_dict['order_id'], '@action': update_dict['action'],
                  'order_detail': {'action': update_dict['order_detail_action'],'order_detail_id': update_dict['order_detail_id']}
                  }
        dict_data = {
            'orders_update': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                              '@token': self.token,
                              'order': ls
                              }
        }
        data_xml = xmltodict.unparse(dict_data, encoding='utf-8')
        print(data_xml)
        url = self.url + '/orders_update'
        response = requests.post(url, headers=self.headers, data=data_xml.encode('utf-8'))
        (response.text)
        if response.status_code == 200:
            data = self.xml_to_dict(response.text)
            return data
        return response.status_code

    @outter
    def orders_query(self, query_dict):

        order_dict = {
            'orders_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                             '@token': self.token, '@results_count': 20}}
        order_dict['orders_query']['paging'] = query_dict['paging']
        order_xml = xmltodict.unparse(order_dict, encoding='utf-8')
        url = self.url + '/orders_query'
        response = requests.post(url, headers=self.headers, data=order_xml.encode('utf-8'))
        print(response.text)
        if response.status_code == 200:
            response_dict = self.xml_to_dict(response.text)
            return response_dict
        return 400

    @outter
    def orders_query_date(self, qu_dict):

        dict_data = {
            'orders_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                             '@token': self.token, '@results_count': 20,
                             'paging': qu_dict['paging'],
                             'states': {'state': qu_dict['state']},
                             'date': {'@type': qu_dict['date-type'], 'min': qu_dict['min'], 'max': qu_dict['max']}
                             }
        }
        if qu_dict['date-type'] == '':
            dict_data['orders_query'].pop('date')
        if qu_dict['state'] == 'ALL':
            dict_data['orders_query'].pop('states')
        dict_xml = xmltodict.unparse(dict_data, encoding='utf-8')
        url = self.url + '/orders_query'
        response = requests.post(url, data=dict_xml.encode('utf-8'), headers=self.headers)
        print(response.text)
        if response.status_code == 200:
            of_dict = self.xml_to_dict(response.text)
            return of_dict
        return 400


class MarketPricingApi(MarketApi):
        @outter
        def pricing_query(self, query_dict):


            pricing_dict = {
                'pricing_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                                  '@token': self.token, '@sellers': query_dict['sellers']}}
            pricing_dict['pricing_query']['product_reference '] = {'@type': 'Ean',
                                                                   '#text': query_dict['product_reference']}
            pricing_xml = xmltodict.unparse(pricing_dict, encoding='UTF-8')
            url = self.url + '/pricing_query'
            response = requests.post(url, headers=self.headers, data=pricing_xml)
            if response.status_code == 200:
                print(response.text)
                response_dict = self.xml_to_dict(response.text)
                return response_dict
            print(response.text)
            return 400


        @outter
        def carriers_query(self):

            # self.authentication()
            pricing_dict = {
                'carriers_query': {'@xmlns': self.xmlns, '@shop_id': self.shop_id, '@partner_id': self.partner_id,
                                   '@token': self.token, 'query': 'all'}}
            pricing_xml = xmltodict.unparse(pricing_dict, encoding='UTF-8')
            url = self.url + '/carriers_query'
            response = requests.post(url, headers=self.headers, data=pricing_xml)
            print(response.text)
            if response.status_code == 200:
                response_dict = self.xml_to_dict(response.text)
                return response_dict
                print(response_dict)
            return 400


if __name__ == '__main__':

    mark = MarketApi()
    print(mark)
    mark.authentication()
    print(mark.authentication())

    # id = mark.offers_update({'product_reference': '5030917077418', 'offer_reference': 'B067-F0D-75E', 'price': '20', 'product_state': '11',
    #                           'quantity': '20', 'description': 'new item', 'showcase': '2'})
    # print(id)


    # mark.offers_query()
    mark.batch_query()
    # mark.delete_offer({'offer_reference': 'B76A-CD5-153'})
    # mark.batch_status('6A994213-CD41-42CF-DBC2-43E03A3E7E4A')
    # mark.offers_query_id('B76A-CD5-153')
    # id = mark.update_offer_price({'offer_reference': 'B067-F0D-75E','price': '33','quantity': '33',})

    # marks = MarketOrderApi()
    # marks.authentication()

    # id = marks.orders_query({'paging': 1})
    # id = marks.orders_update({'order_id': '622A7874A4665', 'action': 'accept_order',
    #  'order_detail_action': 'Accepted','order_detail_id':1
    #  })

    # order = MarketPricingApi()
    # order.authentication()
    # id = order.carriers_query()
    # print(id)
    # id = order.pricing_query({'sellers': 'all', 'product_reference': '0711719247159'})
    # print(id)

    # id = mark.offers_query(
    #     {'results_count': '3', 'paging': '1', 'min': '2019-11-04T14:15:38+01:00', 'max': '2019-12-04T14:15:38+01:00'})
    # print(id)