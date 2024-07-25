import pandas as pd
from config.store import Store
from config.simple import Simple
from config.send_image import Image
from whatsapp_api import WhatsApp

wp = WhatsApp()

input("Pressione enter após escanear o QR Code")

phone_list = 'data/phone_list.csv'
file_path = 'data/data_store.xlsx'
img_path = 'C:/Users/Rodrigo/Desktop/Helper Bot/img/img.png'


def carregar_telefones(file_path):
    df = pd.read_csv(file_path)
    return df['TELEFONE'].tolist()


telefones = carregar_telefones(phone_list)


def get_main_option():
    return input(f"Escolha uma das opções:\n"
                 f"01: Enviar mensagem de texto simples\n"
                 f"02: Enviar mensagem de texto da Super Visão\n"
                 f"03: Enviar imagem\n")


def get_sub_option():
    return input(f"Qual tipo de mensagem você gostaria de enviar?\n"
                 f"01: Confirmação de serviço\n"
                 f"02: Divulgação\n"
                 f"03: Voltar\n")


while True:
    top_option = get_main_option()
    if top_option == "01":
        Simple.send_text(telefones, wp)
    elif top_option == "02":
        while True:
            sec_option = get_sub_option()
            if sec_option == "01":
                Store.store_msgm("01", file_path, wp)
                break
            elif sec_option == "02":
                Store.store_msgm("02", file_path, wp)
                break
            elif sec_option == "03":
                break
            else:
                print("Opção errada, tente novamente")
    elif top_option == "03":
        Image.send_img(telefones, img_path, wp)
    else:
        print("Opção inválida. Escolha 01 para enviar mensagem de texto ou 02 para enviar imagem.")