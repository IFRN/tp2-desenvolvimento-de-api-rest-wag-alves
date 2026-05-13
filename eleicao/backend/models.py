from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Eleitor(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    validador_cpf = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        message='CPF deve estar no formato 000.000.000-00'
    )

    cpf = models.CharField(max_length=14, unique=True, validators=[validador_cpf])
    data_nascimento = models.DateField()
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'eleitores'
        verbose_name = 'Eleitor'
        verbose_name_plural = 'Eleitores'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.cpf})"
    


class Eleicao(models.Model):
    CHOICES_TIPO = [
        ('estudantil','Estudantil'),
        ('sindical','Sindical'),
        ('associacao','Associação'),
        ('condominio','Condomínio'),
        ('conselho','Conselho'),
        ('outra','Outra'),
    ]
    CHOICES_STATUS = [
        ('rascunho','Rascunho'),
        ('aberta','Aberta'),
        ('encerrada','Encerrada'),
        ('apurada','Apurada'),
    ]
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(choices=CHOICES_TIPO)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    status = models.CharField(choices=CHOICES_STATUS, default='rascunho')
    permite_branco = models.BooleanField(default=True)
    criada_por = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='eleicoes_criadas')

    class Meta:
        db_table = 'eleicao'
        verbose_name = 'Eleição'
        verbose_name_plural = 'Eleições'
        ordering = ['titulo']

    def __str__(self):
        return f"{self.titulo} ({self.data_inicio})"



class Candidato(models.Model):
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE, related_name='candidatos')
    numero = models.PositiveIntegerField()
    nome = models.CharField(max_length=150)
    nome_urna = models.CharField(max_length=50)
    partido_ou_chapa = models.CharField(max_length=100, blank=True)
    proposta = models.TextField(blank=True)
    foto_url = models.URLField(blank=True)


    class Meta:
        db_table = 'candidato'
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'
        ordering = ['nome']
        unique_together = [('eleicao', 'numero')]

    def __str__(self):
        return f"{self.eleicao} ({self.nome})"
    


class AptidaoEleitor(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='aptidoes')
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE, related_name='aptos')
    data_inclusao = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'aptidao_eleitor'
        ordering = ['eleicao']
        unique_together = [('eleitor', 'eleicao')]

    def __str__(self):
        return f"{self.eleicao} ({self.eleitor})"



class RegistroVotacao(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='registros_votacao')
    eleicao = models.ForeignKey(Eleicao, on_delete=models.PROTECT, related_name='registros_votacao')
    data_hora = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'registro_votacao'
        ordering = ['-data_hora']
        unique_together = [('eleitor', 'eleicao')]

    def __str__(self):
        return f"{self.eleicao} ({self.eleitor})"



class Voto(models.Model):
    eleicao = models.ForeignKey(Eleicao, on_delete=models.PROTECT, related_name='votos')
    candidato = models.ForeignKey(Candidato, on_delete=models.PROTECT, related_name='votos', null=True, blank=True)
    em_branco = models.BooleanField(default=False)
    data_hora = models.DateTimeField(auto_now_add=True)
    comprovante_hash = models.CharField(max_length=64, unique=True)