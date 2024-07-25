from time import sleep


class Simple:
    @staticmethod
    def send_text(telefones, wp):
        mensagem = "Olá, mensagem de teste."

        for telefone in telefones:
            try:
                if not wp.search_contact(telefone):
                    print(f"Contato {telefone} não encontrado no WhatsApp.")
                    continue  # Pular para o próximo número
                sleep(2)
            except Exception as e:
                print(f"Erro ao procurar o contato {telefone}: {e}")
                continue  # Pular para o próximo número

            try:
                wp.write_message(mensagem)
                sleep(3)
            except Exception as e:
                print(f"Erro ao enviar mensagem para {telefone}: {e}")
                continue  # Pular para o próximo número