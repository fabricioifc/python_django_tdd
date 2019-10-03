from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produto

# @login_required
def produto_detalhe(request, pk):
	produto = get_object_or_404(Produto, pk=pk)
	return render(
		request, 
		'produto_detalhe.html',
		{ 'produto' : produto}
	)