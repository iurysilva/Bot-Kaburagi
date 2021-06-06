from funcionalidades.funcionalidade_lembretes import retorna_data_hora


def adiciona_info(embed, autor=None):
    embed.set_footer(text='Kaburagi', icon_url='https://i.imgur.com/sDhQT5O.png')
    embed.timestamp = retorna_data_hora()
    if autor:
        embed.set_author(name=autor.display_name, icon_url=autor.avatar_url)
    
    return embed