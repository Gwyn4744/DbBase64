from db_base64 import DbBase64
        

def main():

    data_set = [
        'Man',
        'Ma',
        'M',
        'Nowa praca ',
        'ąćę',
        5
    ]

    db_base64 = DbBase64()
    db_base64.debug = True

    
    for ascii_string in data_set:
        try:
            print(db_base64.ascii_to_base64(ascii_string))
            print('---------------------------------')
        except TypeError as e:
            print('Błąd TypeError:', str(e))

main()
