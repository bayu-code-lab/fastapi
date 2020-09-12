from connection import DbMongoManager

async def check_phone_number_or_email(phone_number_or_email):
    with DbMongoManager("mst_customer") as my_coll:
        result={}
        is_exist = True
        data=my_coll.aggregate([
                    {'$project':
                        {
                            'id':'$id',
                            'email':{'$toLower':'$email'},
                            'phone_number':'$phone_number',
                            'full_name':'$full_name',
                            'time_otp_request':'$time_otp_request'
                        }},
                    {'$match':{'$or':[
                        {'email':phone_number_or_email.lower()},
                        {'phone_number':phone_number_or_email}
                        ]}},
                    {'$limit':1}
                ])
        for i in data:
            result['id']=i['id']
            result['email']=i['email']
            result['phone_number']=i['phone_number']
            result['full_name']=i['full_name']
            result['time_otp_request']=i['time_otp_request']

        if result == {}:
            is_exist = False

        return {'is_exist': is_exist, 'data': result}
