from django.db import models

# Create your models here.

class Produto(models.Model):
	nome = models.CharField(max_length=100)
	descricao = models.TextField()
	preco = models.DecimalField(
		max_digits=5,
		decimal_places=2
	)
	quantidade = models.IntegerField()
	publicado_em = models.DateField()

	@property
	def tem_no_estoque(self):
		return self.quantidade > 0
	