import textwrap
import re

class ContaBancaria:
    def __init__(self):
        self.saldo = 0
        self.limite = 800
        self.extrato = ""
        self.numero_saques = 0
        self.LIMITE_SAQUES = 4

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Valor inválido. @@@")

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.LIMITE_SAQUES

        if excedeu_saldo:
            print("\n@@@ Saldo insuficiente. @@@")
        elif excedeu_limite:
            print("\n@@@ Valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Número máximo de saques excedido. @@@")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Valor inválido. @@@")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Sem movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")

class Conta:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario

def menu(usuarios):
    if not usuarios:
        menu = """\n
        ================ MENU ================
        [nu]\tNovo usuário
        [q]\tSair
        => """
    else:
        menu = """\n
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """
    return input(textwrap.dedent(menu))

def criar_usuario(usuarios):
    while True:
        cpf = input("Informe o CPF (somente número): ")
        if validar_cpf(cpf):
            break
        else:
            print("\n@@@ CPF inválido, tente novamente. @@@")

    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n@@@ CPF informado já está em uso! @@@")
        return
    nome = input("Informe o nome completo: ")

    while True:
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        if validar_data(data_nascimento):
            break
        else:
            print("\n@@@ Data de nascimento inválida! Tente novamente. @@@")
    
    while True:
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        if validar_endereco(endereco):
            break
        else:
            print("\n@@@ Endereço inválido! Tente novamente. @@@")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

def validar_cpf(cpf):
    return cpf.isdigit() and len(cpf) == 11

def validar_data(data):
    pattern = re.compile(r"^([1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$")
    return bool(pattern.match(data))

def validar_endereco(endereco):
    return len(endereco) > 10 and " - " in endereco

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return Conta(agencia, numero_conta, usuario)
    print("\n@@@ Usuário não encontrado, falha ao criar conta! @@@")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero_conta}
            Titular:\t{conta.usuario['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    AGENCIA = "0001"
    usuarios = []
    contas = []
    conta_bancaria = ContaBancaria()

    while True:
        opcao = menu(usuarios)
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            conta_bancaria.depositar(valor)
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            conta_bancaria.sacar(valor)
        elif opcao == "e":
            conta_bancaria.exibir_extrato()
        elif opcao == "nu":
            criar_usuario(usuarios)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
