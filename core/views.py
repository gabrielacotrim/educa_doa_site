from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Usuario, Escola, Doador, Necessidade, Doacao
from .forms import CustomUserCreationForm, NecessidadeForm, DoacaoForm, LoginForm

def home(request):
    escolas_destaque = Escola.objects.all()[:3]
    return render(request, 'home.html', {'escolas': escolas_destaque})

def escolas(request):
    todas_escolas = Escola.objects.all()
    return render(request, 'escolas_list.html', {'escolas': todas_escolas})

def escola_detalhe(request, pk):
    escola = get_object_or_404(Escola, pk=pk)
    return render(request, 'escola_detalhe.html', {'escola': escola})

def cadastro_doador(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        if user_form.is_valid() and nome and cpf:
            try:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['senha'])
                    user.first_name = nome
                    user.is_doador = True
                    user.save()
                    Doador.objects.create(usuario=user, cpf=cpf)
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('login_doador')
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar: {e}')
        else:
            messages.error(request, 'Erro(s) no formulário. Verifique os dados inseridos (ex: nome de usuário já existe).')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'cadastro-doador.html', {'form': user_form})

def cadastro_escola(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        cidade = "Maceió" # Exemplo simplificado
        estado = "AL"
        if user_form.is_valid() and nome and cnpj:
            try:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    user.set_password(user_form.cleaned_data['senha'])
                    user.is_escola = True
                    user.save()
                    Escola.objects.create(usuario=user, cnpj=cnpj, nome_escola=nome, cidade=cidade, estado=estado)
                messages.success(request, 'Escola cadastrada com sucesso!')
                return redirect('login_escola')
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar: {e}')
        else:
            messages.error(request, 'Erro(s) no formulário. Verifique os dados inseridos (ex: nome de usuário ou CNPJ já existem).')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'cadastro-escola.html', {'form': user_form})

def login_doador(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email_ou_identificador']
            senha = form.cleaned_data['senha']
            user = authenticate(request, username=username, password=senha)
            if user is not None and user.is_doador:
                login(request, user)
                return redirect('dashboard_doador')
            else:
                messages.error(request, 'Credenciais inválidas.')
    else:
        form = LoginForm()
    return render(request, 'index.html', {'form': form})

def login_escola(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email_ou_identificador']
            senha = form.cleaned_data['senha']
            user = authenticate(request, username=username, password=senha)
            if user is not None and user.is_escola:
                login(request, user)
                return redirect('dashboard_escola')
            else:
                messages.error(request, 'Credenciais inválidas.')
    else:
        form = LoginForm()
    return render(request, 'escola-login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_doador(request):
    if getattr(request.user, 'is_doador', False):
        doacoes = Doacao.objects.filter(doador=request.user.doador)
        return render(request, 'dashboard_doador.html', {'doacoes': doacoes})
    return redirect('home')

@login_required
def dashboard_escola(request):
    if getattr(request.user, 'is_escola', False):
        necessidades = Necessidade.objects.filter(escola=request.user.escola)
        return render(request, 'dashboard_escola.html', {'necessidades': necessidades})
    return redirect('home')

@login_required
def nova_necessidade(request):
    if not getattr(request.user, 'is_escola', False):
        return redirect('home')
    if request.method == 'POST':
        form = NecessidadeForm(request.POST, request.FILES)
        if form.is_valid():
            nec = form.save(commit=False)
            nec.escola = request.user.escola
            nec.save()
            messages.success(request, 'Necessidade adicionada com sucesso!')
            return redirect('dashboard_escola')
    else:
        form = NecessidadeForm()
    return render(request, 'form_necessidade.html', {'form': form})

@login_required
def editar_necessidade(request, pk):
    if not getattr(request.user, 'is_escola', False):
        return redirect('home')
    nec = get_object_or_404(Necessidade, pk=pk, escola=request.user.escola)
    if request.method == 'POST':
        form = NecessidadeForm(request.POST, request.FILES, instance=nec)
        if form.is_valid():
            form.save()
            messages.success(request, 'Necessidade atualizada!')
            return redirect('dashboard_escola')
    else:
        form = NecessidadeForm(instance=nec)
    return render(request, 'form_necessidade.html', {'form': form})

@login_required
def realizar_doacao(request, necessidade_pk):
    if not getattr(request.user, 'is_doador', False):
        return redirect('login_doador')
    nec = get_object_or_404(Necessidade, pk=necessidade_pk)
    if request.method == 'POST':
        form = DoacaoForm(request.POST)
        if form.is_valid():
            valor = form.cleaned_data['valor']
            Doacao.objects.create(doador=request.user.doador, necessidade=nec, valor=valor)
            nec.valor_arrecadado += valor
            nec.save()
            messages.success(request, f'Doação de R$ {valor} realizada com sucesso!')
            return redirect('escola_detalhe', pk=nec.escola.pk)
    else:
        form = DoacaoForm()
    return render(request, 'form_doacao.html', {'form': form, 'necessidade': nec})
