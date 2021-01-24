from wsgiref.simple_server import make_server
import sys
from urllib.parse import parse_qs
from datetime import datetime
import dateutil.parser
from pytz import timezone
import json


#Эта функция возвращает текущее время
def get_current_time(timez):
    time_tz = timezone(timez)
    dt = datetime.now().astimezone(time_tz)
    fmt = '%m.%d.%Y %H:%M:%S %Z' #Format for printing
    return 'Time of '+timez+' is now: '+dt.strftime(fmt)

#Эта функция принимает время из зоны пользователя в json формате и возвращает время из другой таймзоны
def convert_date(date_json , new_tz):
  old_date = ''
  old_tz = ''
  data_date = json.loads(date_json)
  for key, value in data_date.items():
    if(key == 'date'):
      old_date = value;
    if(key == 'target_tz'):
      old_tz = value
  fmt = '%m.%d.%Y %H:%M:%S'
  dt_old = timezone(old_tz).localize(datetime.strptime(old_date,fmt))
  dt_new = dt_old.astimezone(timezone(new_tz))
  return dt_new.strftime(fmt)

#Эта функция считает разницу между двумя различными зонами
def differ_time(dates_json):
    first_date = first_tz = second_date = second_tz =''
    data_date = json.loads(dates_json)
    for key, value in data_date.items():
      if(key == 'first_date'):
        first_date = value;
      if(key == 'second_date'):
        second_date = value
      if(key == 'first_tz'):
        first_tz = value;
      if(key == 'second_tz'):
        second_tz = value
    dt_first= timezone(first_tz).localize(dateutil.parser.parse(first_date))
    dt_second= timezone(second_tz).localize(dateutil.parser.parse(second_date))

    first_date_gmt = dt_first.astimezone(timezone('GMT'))
    second_date_gmt = dt_second.astimezone(timezone('GMT'))
    #Разница между datetime-значениями в секундах
    return (first_date_gmt-second_date_gmt).total_seconds()

def read_get_data(env, param):
    get_data = parse_qs(env['QUERY_STRING'])
    return get_data.get(param, [''])[0]


def read_post_data(request_body,param):
    post_data = parse_qs(request_body.decode())
    return post_data.get(param, [''])[0]
    
def app (env, start_response):
    response_body = "Result";
    get_data ='';
    get_data=read_get_data(env,'tz');
    try:
        request_body_size = int(env.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    if(request_body_size > 0):
      request_body = env['wsgi.input'].read(request_body_size)
      post_data1 = read_post_data(request_body , 'old_date')
      post_data2 = read_post_data(request_body , 'new_tz')
      post_data3 = read_post_data(request_body , 'data_diff')
    else:
      post_data1=''
      post_data2=''
      post_data3=''
    
    #Текущее Время
    ct = ''
    if(get_data != ''):
      ct = get_current_time(get_data)
    cnv = ''
    if(post_data1!='' and post_data2!=''):
      cnv = convert_date(post_data1 , post_data2)
    
    df=''
    if(post_data3 != ''):
      df = differ_time(post_data3)
    
    response_body = ""
    if(ct != ''):
      response_body += ct+ "|| "
    if(cnv != ''):
      response_body +="New Date is: " +cnv + "||"
    if(df != ''):
      response_body +="Differnce is: " +str(df) + " seconds||"
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    return [response_body.encode()]

with make_server('', 8081, app) as httpd:
  print("Serving on port 8081...")
  httpd.serve_forever()
  httpd.handle_request()