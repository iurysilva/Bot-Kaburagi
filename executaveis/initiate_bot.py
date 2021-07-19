import discord
from discord.ext import commands, tasks
from funcionalidades import Lembrete
from funcionalidades import Animes
from discord.embeds import Embed
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
import string
from servicos.informacoes_sobre_tempo import retorna_hora
from servicos.informacoes_sobre_tempo import retorna_dia_da_semana
from servicos.manipulacao_de_embed import adiciona_info


intents = discord.Intents().default()
intents.members = True
cliente = commands.Bot(command_prefix='?', intents=intents)
slash = SlashCommand(cliente, sync_commands=True)