from time import sleep


class Image:
    @staticmethod
    def send_img(telefones, img, wp):
        for telefone in telefones:
            try:
                if not wp.search_contact(telefone):
                    print(f"Contato {telefone} não encontrado.")
                    continue
                sleep(2)
            except Exception as e:
                print(f"Erro ao procurar contato {telefone}: {e}")
                continue

            try:
                wp.enviar_imagem(img)
                sleep(2)
            except Exception as e:
                print(f"Erro ao enviar imagem para o telefone {telefone}: {e}")
                continue

