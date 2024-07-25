from time import sleep
from config.dicionary import criar_lista_atendimentos
import os


class Store:
    @staticmethod
    def store_msgm(option, file_path, wp):
        services = criar_lista_atendimentos(file_path)

        def log_error(nome, placa, telefone):
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            log_file_path = os.path.join(log_dir, "erros_de_contato.txt")

            with open(log_file_path, "a") as log_file:
                log_file.write(f"Nome: {nome}, Placa: {placa}, Telefone: {telefone}\n")

        for service in services:
            name = service['nome'].capitalize()
            plate = service['placa']
            phone = service['telefone']
            partner = service['convenio']
            report = service['laudo']

            if report == 'TR':
                report_modality = "Transferência"
            elif report == 'CT':
                report_modality = "Cautelar"
            elif report == 'CB':
                report_modality = "Combo"
            elif report == 'REV':
                report_modality = "Revistoria"
            elif report == 'PQ':
                report_modality = "Pesquisa"
            elif report == "DOC":
                report_modality = "CRLV"
            else:
                report_modality = "Desconhecido"

            try:
                if not wp.search_contact(phone):
                    print(f"Contato {phone} não encontrado no WhatsApp.")
                    continue
                sleep(2)
            except Exception as e:
                log_error(name, plate, phone)
                print(f"Erro ao procurar o contato {phone}: {e}")
                continue
            if partner == "":
                modality = "Poupa Tempo"
            else:
                if partner.capitalize() in ['Hebert', 'Angela', 'Rosi', 'Glauco']:
                    modality = partner
                elif partner.lower() == 'particular':
                    modality = "Poupa Tempo"
                else:
                    modality = "Convenio"

            if option == "01":
                mensagem = (f"Olá *{name}*.\n"
                            f"Esta é uma mensagem da *Super Visão Vistorias Automotivas*\n"
                            f"Segue alguns dados do seu atendimento:\n"
                            f"*Modalidade de vistoria:* {report_modality}\n"
                            f"*Placa do veículo:* {plate}\n"
                            f"*Detran/Despachante:* {modality}\n"
                            f"Agradecemos a sua preferência.\n"
                            f"Se puder nos avaliar, é só clicar no link abaixo.\n"
                            f"https://goo.gl/maps/7m3j36qF3pqBiFNXA\n")
                wp.write_message(mensagem)
                sleep(2)

            if option == "02":
                mensagem = (f"Olá, *{name}*.\n"
                            f"Obrigado por confiar em nossos serviços de vistoria.\n"
                            f"Saiba que estamos trabalhando sempre para prestar o melhor atendimento que você merece.\n"
                            f"Você sabia que a CAUTELAR e a CERTICAR são laudos ideais para você obter antes de comprar ou vender seu veículo?.\n"
                            f"Fale conosco para saber mais sobre esses serviços e como podemos ajudar em outras áreas.\n"
                            f"Caso queira conhecer mais, nos siga no instagram: https://www.instagram.com/supervisao.aparecida.sp/!\n"
                            f"Estamos anciosos pelo seu retorno!!.\n"
                            f"**Super Visão de Aparecida**."
                            )
                wp.write_message(mensagem)
                sleep(2)

