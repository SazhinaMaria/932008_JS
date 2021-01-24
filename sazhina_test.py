import requests
r = requests.get('https://Sazhinamain.mariyasazhina.repl.co?tz=Europe/Moscow')
#################################################
data1 = {'old_date':'{"date":"12.20.2021 22:21:05", "target_tz":"EST"}','new_tz':'ETC/GMT'}
r1 = requests.post('https://Sazhinamain.mariyasazhina.repl.co' , data = data1)
##############################################
data2 = {'data_diff' : '{"first_date":"12.20.2021 22:21:05", "first_tz": "EST", "second_date":"12.21.2021 10:15:20", "second_tz": "Europe/Moscow"}'}
r2 = requests.post('https://Sazhinamain.mariyasazhina.repl.co', data = data2)
###################################################