from mixer.backend.django import mixer
import pytest
from django.test import TestCase

@pytest.mark.django_db
class TestModels:

		def test_tem_no_estoque(self):
			produto = mixer.blend(
				'produtos.Produto',
				quantidade=1
			)
			assert produto.tem_no_estoque == True


		def test_nao_tem_no_estoque(self):
			produto = mixer.blend(
				'produtos.Produto',
				quantidade=0
			)
			assert produto.tem_no_estoque == False


		def test_valor_nao_pode_ser_negativo(self):
			produto = mixer.blend(
				'produtos.Produto',
				preco=-10
			)
			assert produto.valor_negativo == True





















