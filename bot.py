import telebot;
import requests;
import cherrypy;
bot = telebot.TeleBot('5075374981:AAGjvJXnIEL8QaHMyb5yyL8zQR0Yvbqrx_U');
tokenf='5075374981:AAGjvJXnIEL8QaHMyb5yyL8zQR0Yvbqrx_U'
WEBHOOK_HOST="94.29.124.44"
WEBHOOK_PORT =80
WEBHOOK_PORTs ="80"
WEBHOOK_LISTEN='0.0.0.0'
WEBHOOK_SSL_CERT='C:/Users/user/AppData/Local/Programs/Python/Python310/webhook_cert.pem'
WEBHOOK_SSL_PRIV='C:/Users/user/AppData/Local/Programs/Python/Python310/webhook_pkey.pem'
WEBHOOK_URL_BASE = "https://"+WEBHOOK_HOST+":" +WEBHOOK_PORTs
WEBHOOK_URL_PATH = "/5075374981:AAGjvJXnIEL8QaHMyb5yyL8zQR0Yvbqrx_U/"
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and 'content-type' in cherrypy.request.headers and cherrypy.request.headers['content-type'] == 'application/json':
            
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

rownum=0;


@bot.message_handler(func=lambda message: True, content_types=['text'])
def get_text_messages(message):
    if message.text == "/close":
        bot.send_message(message.from_user.id, "Введите номер строки таблицы которую вы хотите отметить как выполнено")
        bot.register_next_step_handler(message,get_rownum)
    elif message.text == "/all":
        bot.send_message(message.from_user.id, "Поиск......")
        response2 = requests.get("https://script.google.com/macros/s/AKfycbwHL0ccv64F9i_5unLDEdkoSmEIw3Ozukze1esQfywRnnsPD0RJTpgImG1h4XCzEAuGzg/exec")
        json2=response2.json()
        if json2['result']=="":
            bot.send_message(message.from_user.id, "Активных заявок нет")
        else:
            i=0
            while i<=1000:
                try:
                    bot.send_message(message.from_user.id,"Номер заявки: "+str(json2['result'][i][8])+"; Адрес: "+str(json2['result'][i][1])+"; Обратившийся: "+str(json2['result'][i][2])+"; Номер помещения: "+str(json2['result'][i][3])+"; Номер телефона: "+str(json2['result'][i][5])+"; Описание проблемы: "+str(json2['result'][i][4]))
                    i=i+1;
                except Exception:
                    i=1001
    else:
        bot.send_message(message.from_user.id, "Список доступных команд /close (для закрытия заявки) и /all (для получения списка нне закрытых заявок)")
def get_rownum(message):
    global rownum
    if message.text=="/close":
        bot.send_message(message.from_user.id, "Введите номер строки таблицы которую вы хотите отметить как выполнено")
        bot.register_next_step_handler(message,get_rownum)
    elif message.text=="/all":
        bot.send_message(message.from_user.id, "Поиск......")
        response2 = requests.get("https://script.google.com/macros/s/AKfycbwHL0ccv64F9i_5unLDEdkoSmEIw3Ozukze1esQfywRnnsPD0RJTpgImG1h4XCzEAuGzg/exec")
        json2=response2.json()
        if json2['result']=="":
            bot.send_message(message.from_user.id, "Активных заявок нет")
        else:
            i=0
            while i<=1000:
                try:
                    bot.send_message(message.from_user.id,"Номер заявки: "+str(json2['result'][i][8])+"; Адрес: "+str(json2['result'][i][1])+"; Обратившийся: "+str(json2['result'][i][2])+"; Номер помещения: "+str(json2['result'][i][3])+"; Номер телефона: "+str(json2['result'][i][5])+"; Описание проблемы: "+str(json2['result'][i][4]))
                    i=i+1;
                except Exception:
                    i=1001
        bot.register_next_step_handler(message,get_text_messages)
    else:
        cheker=0
        try:
            rownum=int(message.text)
            response = requests.get("https://script.google.com/macros/s/AKfycbyDLPGpNQ5gP8qtIXy2AZUHzyzB0F9C3yl4ADXDEkwpZAC4Q4sHxlCqZxffAznlw8KSCg/exec?inp="+message.text)
            json=response.json()
            if json['result']=="Изменено":
                bot.send_message(message.from_user.id, "Изменено")
            else:
                bot.send_message(message.from_user.id, "Эта заявка уже выполнена или не существует")
        except Exception:
            bot.send_message(message.from_user.id, "Введите номер строки таблицы которую вы хотите отметить как выполнено")          
            bot.register_next_step_handler(message,get_rownum)
bot.remove_webhook()
bot.delete_webhook()
#bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,certificate=open(WEBHOOK_SSL_CERT, 'r'))
#cherrypy.config.update({
    #'server.socket_host': WEBHOOK_LISTEN,
    #'server.socket_port': WEBHOOK_PORT,
   # 'server.ssl_module': 'builtin',
  #  'server.ssl_certificate': WEBHOOK_SSL_CERT,
 #   'server.ssl_private_key': WEBHOOK_SSL_PRIV
#})
#cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
bot.polling(none_stop=True)
