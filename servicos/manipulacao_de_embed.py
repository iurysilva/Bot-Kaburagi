from servicos.informacoes_sobre_tempo import retorna_data_hora


def adiciona_info(embed, autor=None):
    embed.set_footer(text='Kaburagi', icon_url='https://i.ibb.co/1LB5zCv/5x38c88c1eb51.png')
    embed.timestamp = retorna_data_hora()
    if autor:
        embed.set_author(name=autor.display_name, icon_url=autor.avatar_url)
    return embed