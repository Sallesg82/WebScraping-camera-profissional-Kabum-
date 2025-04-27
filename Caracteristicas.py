import pandas as pd

df = pd.read_excel('camera.xlsx')

def marca(nome):
    marcas = ['canon', 'sony', 'powershot', 'nikon', 'kodak', 'tomato', 'insta360', 'tomate', 'fujifilm', 'Panasonic', 'Conference', 'ptz', 'sjcam', ]
    veri_marca = nome.lower()
    for m in marcas:
        if m in veri_marca:
            return m
    return 'desconhecido'

def cor(nome):
    cores = ['preto', 'preta', 'black', 'amarelo', 'amarela', 'azul']
    veri_cor = nome.lower()
    for c in cores:
        if c in veri_cor:
            return c
    return 'desconhecido'

def tem_lente(nome):
    return 'lente' in nome.lower()

def eh_filmadora(nome):
    return 'filmadora' in nome.lower()

def tem_hd_sd(nome):
    termos = ['hd', 'sd']
    nome_min = nome.lower()
    return any(t in nome_min for t in termos)

def eh_kit(nome):
    return 'kit' in nome.lower()

# Aplicar funções
df['marca'] = df['nome'].apply(marca)
df['cor'] = df['nome'].apply(cor)
df['tem_lente'] = df['nome'].apply(tem_lente)
df['é_filmadora'] = df['nome'].apply(eh_filmadora)
df['tem_hd_sd'] = df['nome'].apply(tem_hd_sd)
df['é_kit'] = df['nome'].apply(eh_kit)


df = df[df['é_kit'] == False]

df.to_excel('testetratado.xlsx', index=False)

print('Arquivo salvo como testetratado.xlsx!')
