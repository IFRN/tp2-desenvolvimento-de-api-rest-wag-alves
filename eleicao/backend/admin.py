from django.contrib import admin
from .models import *

@admin.register(Eleitor)
class Eleitor(admin.ModelAdmin):
    list_display = ('nome', 'email', 'ativo')
    list_filter = ('nome', 'data_cadastro')
    search_fields = ('nome',)


@admin.register(Eleicao)
class Eleicao(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'tipo', 'status')
    search_fields = ('titulo', 'descricao', 'tipo')


@admin.register(Candidato)
class Candidato(admin.ModelAdmin):
    list_display = ('eleicao', 'nome', 'numero', 'partido_ou_chapa')
    search_fields = ('nome', 'numero', 'eleicao')


@admin.register(AptidaoEleitor)
class AptidaoEleitor(admin.ModelAdmin):
    list_display = ('eleitor', 'eleicao', 'data_inclusao')
    list_filter = ('eleitor', 'eleicao')


@admin.register(RegistroVotacao)
class RegistroVotacao(admin.ModelAdmin):
    list_display = ('eleitor', 'data_hora')
    list_filter = ('eleitor', )
    search_fields = ('eleitor',)


@admin.register(Voto)
class Voto(admin.ModelAdmin):
    list_display = ('eleicao', 'candidato', 'data_hora')
    list_filter = ('eleicao',)
    search_fields = ('eleicao', 'candidato')
