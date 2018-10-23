title = 'tedt'
description = 'tedt'
price = 'tedt'
quantity = 'tedt'
minimum = 5
image_url = 'tedt'
my_id = 5


details = {
        "title": '"' + 'book3' + '"',
        "description": '"' + "Another awesome read" + '"',
        "price": 110,
        "quantity": 50,
        "minimum": 4,
        "image_url": '"' + "new_url" + '"',
        "created_by": 0,
        "updated_by":0
        }
for key,value in details.items():
    updatesql = f"""UPDATE users SET {key} = {value} WHERE id = {0};"""
    print(updatesql)