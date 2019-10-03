## Brincando com TDD e DJANGO
### Alguns comandos e códigos úteis para o projeto

# Agora vamos instalar pytest e outras libs
```
pip install pytest --user
pip install pytest-django --user
pip install pytest-cov --user
pip install mixer --user
```

#### Criando o projeto
```
django-admin startproject testando_django
cd testando_django
```
#### Criando a APP
```
python manage.py startapp produtos
python manage.py migrate
```
#### Criar a classe Produto (produtos/models.py)
```
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    # preco = models.DecimalField(max_digits=5, decimal_places=2, min_value=0)
    quantidade = models.IntegerField()
    publicado_em = models.DateField()


    @property
    def tem_no_estoque(self):
        return self.quantidade > 0
```
#### Criar a view produto_detalhe (produtos/views.py)
```
from django.shortcuts import render, get_object_or_404
from .models import Produto

# Create your views here.
def produto_detalhe(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'produto_detalhe.html', {'produto': produto})
```
#### Importar a APP (urls.py)
```
from django.contrib import admin
from django.urls import path
from produtos import views

urlpatterns = [
    path('<int:pk>', views.produto_detalhe, name="detalhe"),
    path('admin/', admin.site.urls),
]
```

#### Criar a pasta templates (produtos/templates)
#### Criar a página html (produtos/templates/produto_detalhe.html)
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver (Page not found)
python manage.py shell

>>> from produtos.models import Produto
>>> from datetime import datetime
>>> produto = Produto.objects.create(nome='Livro', descricao = 'Introdução ao Python', preco=29.90, quantidade=50, publicado_em=datetime.now())
>>> produto.save()
>>> Produto.objects.all().values()
>>> Produto.objects.get(id=1)
>>> Produto.objects.get(nome='Livro')
```
#### Vamos adicionar uma anotação para obrigar o login ao ver o produto
#### Modificando a view produto_detalhe (produtos/views.py)
```
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produto

# Create your views here.

@login_required
def produto_detalhe(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 
        'produto_detalhe.html', 
        { 'produto' : produto }
    )
```
#### Agora os testes começam
#### Vamos criar o arquivo pytest.ini no diretório root do projeto, com o conteúdo abaixo:
```
[pytest]
DJANGO_SETTINGS_MODULE = testando_django.settings
```
#### Criar pasta e arquvo (produtos/test/test_urls.py)
```
from django.urls import reverse, resolve

class TestUrls:
    
    def test_detalhe_url(self):
        path = reverse('detalhe', kwargs={'pk': 1})
        assert resolve(path).view_name == 'detalhe'
```
## Rodando os testes
```
$ py.test
```
#### Testando models (produtos/tests/test_models.py)
```
from mixer.backend.django import mixer
import pytest

@pytest.mark.django_db
class TestModels:

    def test_produto_em_estoque(self):
        produto = mixer.blend('produtos.Produto', quantidade=1)
        assert produto.tem_no_estoque == True

    def test_produto_sem_estoque(self):
        produto = mixer.blend('produtos.Produto', quantidade=0)
        assert produto.tem_no_estoque == False
```
#### testando views (produtos/tests/test_views.py)
```
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from produtos.views import produto_detalhe
from mixer.backend.django import mixer
import pytest
import pdb

@pytest.mark.django_db
class TestViews:

    def test_produto_detalhe_autenticado(self):
        # pdb.set_trace()
        produto = mixer.blend('produtos.Produto') # gerar um produto randômico
        path = reverse('detalhe', kwargs={'pk': produto.id}) # ex: /1
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = produto_detalhe(request, pk=produto.id)
        assert response.status_code == 200

    def test_produto_detalhe_nao_autenticado(self):
        produto = mixer.blend('produtos.Produto') # gerar um produto randômico
        # print(produto.__dict__)
        path = reverse('detalhe', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        
        response = produto_detalhe(request, pk=produto.id)
        # assert response.status_code == 200
        assert 'accounts/login' in response.url
```

## verificando a cobertura de testes
```
pytest --cov=produtos
```
