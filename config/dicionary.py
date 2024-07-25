import pandas as pd


def criar_lista_atendimentos(file_path):

    df = pd.read_excel(file_path, header=1)

    nomes = df['NOME'].tolist()
    placas = df['PLACA'].tolist()
    convenios = df['PART/CONV.'].tolist()
    laudos = df['L'].tolist()

    def format_telefone(telefone):
        if pd.isna(telefone):
            return None
        telefone_str = str(telefone)
        if telefone_str.endswith('.0'):
            telefone_str = telefone_str[:-2]
        return telefone_str

    telefones = df['TELEFONE'].apply(format_telefone).tolist()

    palavras_irrelevantes = {'CRÉDITO', 'DÉBITO', 'PIX', 'DINHEIRO', 'TOTAL', 'Depósito M', 'Depósito T', 'Retirada', 'Moeda'}

    resultado = []
    for nome, placa, convenio, telefone, laudo in zip(nomes, placas, convenios, telefones, laudos):

        if pd.notna(nome) and pd.notna(telefone) and pd.notna(convenio) and pd.notna(laudo):

            if all(isinstance(nome, str) and palavra not in nome.upper() for palavra in palavras_irrelevantes):
                resultado.append({'nome': nome, 'placa': placa, 'convenio': convenio, 'telefone': telefone, 'laudo': laudo})

    return resultado


if __name__ == "__main__":
    file_path = '/mnt/data/image.png'
    atendimentos = criar_lista_atendimentos(file_path)
    print(atendimentos)
