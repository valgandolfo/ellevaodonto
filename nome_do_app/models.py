from django.db import models

class TbTabelaAtendimento(models.Model):
    ATE_ID = models.AutoField(primary_key=True)
    ATE_NOME = models.CharField(max_length=250)
    ATE_TELEFONE = models.CharField(max_length=20)
    ATE_INTERESSE = models.CharField(max_length=10)
    ATE_MENSSAGEM = models.CharField(max_length=250)
    ATE_DATCADASTRO = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'TBTABELA_ATENDIMENTO'

    def __str__(self):
        return f"{self.ATE_NOME} - {self.ATE_TELEFONE}"
