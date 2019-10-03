from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from produtos.views import produto_detalhe
from mixer.backend.django import mixer
import pytest

@pytest.mark.django_db
class TestViews:

	def test_produto_detalhe_autenticado(self):
		produto = mixer.blend(
			'produtos.Produto',
			nome='Livro'
		)
		path = reverse('detalhe', kwargs={'pk' : 1})
		request = RequestFactory().get(path)
		request.user = mixer.blend(User)

		response = produto_detalhe(
			request, pk=produto.id
		)

		assert response.status_code == 200