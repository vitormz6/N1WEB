# N2 Programação WEB

![License](https://img.shields.io/badge/license-MIT-green)
![Flask](https://img.shields.io/badge/Flask-v2.0-blue)
![Python](https://img.shields.io/badge/Python-3.9-blue)

## 🎉 Bem-vindo ao Meu App!

Uma aplicação web simples e eficiente para gerenciamento de usuários. Criada usando **Flask**, esta aplicação permite criar, editar, bloquear e desbloquear usuários de forma amigável e segura.

## 📸 Demonstração

![image](https://github.com/user-attachments/assets/7c360042-ebbd-4ca4-be3a-a77828fc011a)

## 📖 Sobre

Este é um projeto de exemplo de um sistema de gerenciamento de usuários, onde administradores podem gerenciar o acesso de diversos usuários ao sistema. É possível cadastrar novos usuários, editá-los, bloquear contas e desbloquear quando necessário.

## ✨ Funcionalidades

- ✅ **Adicionar Usuários**: Crie contas com nome real, e-mail e senha.
- ✅ **Editar Usuários**: Atualize informações do usuário, incluindo e-mail e senha.
- ✅ **Bloquear/Desbloquear Usuários**: Impeça o acesso de usuários indesejados ou permita que eles acessem novamente.
- ✅ **Sistema de Login**: Controle o acesso ao sistema de forma segura.
- ✅ **Interface Amigável**: Uma interface web simples e funcional.
- ✅ **Recuperação de Senha**: Solicitação de redefinição de senha via email.
- ✅ **Recuperação de Senha**: Envio de link seguro para redefinição de senha.
- ✅ **Recuperação de Senha**: Redefinição de senha com validação de token.

## 🛠️ Instalação

Siga as etapas abaixo para rodar o projeto localmente:

### Pré-requisitos

Certifique-se de ter o **Python** (>= 3.9) instalado. Para verificar a versão, execute:

```bash
python --version
```

### Passos de Instalação
## Clone o Repositório
```git clone https://github.com/seu-usuario/seu-repositorio.git``` e depois ```cd seu-repositorio```

Vá até N2WEB

## Instale as Dependências
```
pip install Flask==2.3.2 Flask-Mail==0.9.1 Flask-WTF==1.1.1 Flask-SQLAlchemy==3.0.5 itsdangerous==2.1.2 email-validator==1.3.1
```
_**Nota:** _As versões especificadas são exemplos. Você pode ajustar as versões conforme a compatibilidade do seu projeto ou remover os números de versão para instalar as versões mais recentes.__

## Atualizar as Configurações do Flask-Mail no app.py
```# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Servidor SMTP do Gmail
app.config['MAIL_PORT'] = 587  # Porta para TLS
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "seuemail@gmail.com"  # Substitua pelo seu email
app.config['MAIL_PASSWORD'] = "suasenhagerada"      # Substitua pela sua senha de app
app.config['MAIL_DEFAULT_SENDER'] = ('N2 Programação WEB', app.config['MAIL_USERNAME'])
```

### Importante:
Substitua "seuemail@gmail.com" pelo seu endereço de email real do Gmail.
Substitua "suasenhagerada" pela senha de app de 16 caracteres que você gerou.

## Execute a Aplicação
```python app.py``` (ou opelo IDE)

## Acesse no Navegador
Abra seu navegador e vá para:
http://localhost:5000

# 🚀 Como Usar
- Página Inicial: Acesse a página inicial para ver a mensagem de boas-vindas.
- Gerenciamento de Usuários: Vá para a aba "Manage Users" para adicionar, editar, bloquear ou desbloquear usuários.
- Login: Faça login na aba "Login" para acessar o sistema com credenciais existentes.

# 🚀 Usando a Funcionalidade "Esqueci Minha Senha"
## 1. Solicitar a Redefinição de Senha
**Acesse a Página de Login**
  Abra o navegador e vá para http://localhost:5000/login.
  
**Clique em "Esqueci minha senha"**
  Na página de login, abaixo do formulário, clique no link "Esqueci minha senha".
  
**Insira seu Email**
  Você será redirecionado para a página "Esqueci Minha Senha".
  Insira o endereço de email que você usou para se registrar e clique em "Enviar".

## 2. Receber o Email de Redefinição
**Verifique sua Caixa de Entrada**
  Após solicitar a redefinição, verifique a caixa de entrada do email que você inseriu.

**Email de Redefinição**
  Você receberá um email com o assunto "Redefinir Sua Senha".
  O corpo do email conterá um link para redefinir sua senha.
  
## 3. Redefinir a Senha
**Clique no Link de Redefinição**
  Abra o email e clique no link fornecido.
  O link redirecionará você para a página de "Redefinir Senha" no aplicativo.
  
**Inserir Nova Senha**
  Na página de redefinição, insira sua nova senha e confirme a nova senha.
  Clique em "Redefinir Senha" para confirmar.
  
**Confirmação**
  Você verá uma mensagem confirmando que sua senha foi atualizada com sucesso.
  Agora, você pode retornar à página de login e entrar com sua nova senha.

# Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar o projeto.
