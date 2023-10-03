from telebot import TeleBot
from model import Model
from keyboards import create_keyboard, create_markup_max_length, create_markup_num_beams, create_markup_top_k, \
    create_markup_top_p, create_markup_setting, create_markup_temperature

token = "6690241129:AAExSBXT5Co7dIZpGeNe-1mVITKfpk7ZpNQ"
bot: TeleBot = TeleBot(token)
model: Model = Model()

keyboard = create_keyboard()
markup_settings = create_markup_setting()
markup_num_beams, num_beams_value = create_markup_num_beams()
markup_top_p, top_p_value = create_markup_top_p()
markup_top_k, top_k_value = create_markup_top_k()
markup_temperature, temperature_value = create_markup_temperature()
markup_max_length, max_length_value = create_markup_max_length()


@bot.message_handler(commands=['start'])
def send_start_message(message):
    bot.send_message(message.chat.id, 'Чат бот\n'
                                      'Справка - /help\n'
                                      'Настройки - /settings\n'
                                      'Включить генерацию - /activate\n'
                                      'Отключить генерацию - /deactivate',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def send_help_message(message):
    bot.send_message(message.chat.id, 'Сообщение о справке.\n')


@bot.message_handler(commands=['activate'])
def send_activate_bot(message):
    model.enable()
    bot.send_message(message.chat.id, 'Генерация включена')


@bot.message_handler(commands=['deactivate'])
def send_deactivate_bot(message):
    model.disable()
    bot.send_message(message.chat.id, 'Генерация выключена')


@bot.message_handler(commands=['settings'])
def send_setting_message(message):
    bot.send_message(message.chat.id, 'Меню для настройки генерации ответов на вопросы\n',
                     reply_markup=markup_settings)


@bot.callback_query_handler(func=lambda call: call.data.startswith('param_'))
def callback_param(call):
    if call.data == 'param_num_beams':
        bot.edit_message_text('Изменение числа путей генерации текста для каждого шага', call.message.chat.id,
                              call.message.message_id, reply_markup=markup_num_beams)
    if call.data == 'param_top_k':
        bot.edit_message_text('Изменение числа наиболее вероятных следующих слов', call.message.chat.id,
                              call.message.message_id, reply_markup=markup_top_k)
    elif call.data == 'param_top_p':
        bot.edit_message_text('Изменение совокупной вероятности для следующих слов', call.message.chat.id,
                              call.message.message_id, reply_markup=markup_top_p)
    elif call.data == 'param_temperature':
        bot.edit_message_text('Изменение вероятности появления слов с большой вероятностью', call.message.chat.id,
                              call.message.message_id, reply_markup=markup_temperature)
    elif call.data == 'param_max_length':
        bot.edit_message_text('Изменение максимальной длины текста', call.message.chat.id,
                              call.message.message_id, reply_markup=markup_max_length)
    elif call.data == 'param_info':
        bot.send_message(call.message.chat.id, model.info())
    elif call.data == 'param_default':
        model.set_default()
        bot.send_message(call.message.chat.id, 'Параметры по умолчанию установлены')


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_num_beams'))
def callback_change_num_beams(call):
    for n in num_beams_value:
        if call.data == f'change_num_beams_{n}':
            model.set_num_beams(n)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=markup_settings)

@bot.callback_query_handler(func=lambda call: call.data.startswith('change_top_k'))
def callback_change_top_k(call):
    for k in top_k_value:
        if call.data == f'change_top_k_{k}':
            model.set_top_k(k)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=markup_settings)


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_top_p'))
def callback_change_top_p(call):
    for p in top_p_value:
        if call.data == f'change_top_p_{p}':
            model.set_top_p(p)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=markup_settings)


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_temperature'))
def callback_change_temperature(call):
    for temp in temperature_value:
        if call.data == f'change_temperature_{temp}':
            model.set_temperature(temp)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=markup_settings)


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_max_length_'))
def callback_change_max_length(call):
    for length in max_length_value:
        if call.data == f'change_max_length_{length}':
            model.set_max_length(length)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                          reply_markup=markup_settings)


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_back'))
def callback_change_back(call):
    if call.data == f'change_back':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=markup_settings)


@bot.message_handler(content_types=['text'])
def send_message(message):
    if model.active():
        bot.send_chat_action(message.chat.id, action='typing')
        message.text = 'Вопрос: ' + message.text + '\nОтвет:'
        result_generation = model.generate_text(message.text)
        bot.send_message(message.chat.id, result_generation)


if __name__ == '__main__':
    # bot.remove_webhook()
    bot.polling()
