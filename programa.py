

import MySQLdb

"""Ao invés de usar desconectar() no fim de cada função optei por fazer elas voltarem ao meno a partir de menu() e movi
a opção de desconectar para o menu principal"""


def conectar():

    try:
        conn = MySQLdb.connect(
            db='financas',
            host='localhost',
            user='root',
            passwd='root'
        )
        return conn
    except MySQLdb.Error as e:
        print(f'Não foi possível se conectar a planilha, devido ao erro: {e}')


def desconectar():

    print('Finalizado...')
    conn = conectar()
    if conn:
        conn.close()


def listar_tudo():

    conn = conectar()
    cursor = conn.cursor()

    """Aqui coloquei um ORDER BY para que os meses e dias fiquem organizados em ordem crescente"""
    cursor.execute('SELECT c.id, c.descricao, c.dia, c.mes, c.custo, d.nome FROM gastos AS c, categorias AS d WHERE c.categoria = d.id ORDER BY c.mes, c.dia ASC')

    registros = cursor.fetchall()

    """Cabeçalho que criei, os {:<4} é a quantidade de espaços que a coluna ocupa, devo repetir no print para fical 
    organizado"""
    print(45 * '=')

    if len(registros) > 0:
        print("{:<4} {:<15} {:<4} {:<4} {:<10} {:<10}".format('id', 'Descrição', 'Dia', 'Mês', 'Custo', 'Categoria'))
        for registro in registros:
            print("{:<4} {:<15} {:<4} {:<4} {:<10} {:<10}".format(registro[0], registro[1], registro[2], registro[3],
                                                           registro[4], registro[5]))
    else:
        print('Não há registros na tabela.')
    print(45 * '=')

    menu()


def listar_mes():

    conn = conectar()
    cursor = conn.cursor()
    mes_selecionado = int(input('Escolha o mês desejado para ver as finanças (Escolha entre 01 e 12): '))
    if mes_selecionado in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        cursor.execute(f'SELECT c.id, c.descricao, c.dia, c.custo, d.nome FROM gastos AS c, categorias AS d WHERE c.categoria = d.id AND mes = {mes_selecionado} ORDER BY c.dia ASC')
        registros = cursor.fetchall()
        cursor.execute(f'SELECT SUM(custo) FROM gastos WHERE mes= {mes_selecionado}')

        """Esse codigo abaixo usei por que o fetchall retorna uma tupla com DECIMAL e o valor, e isso não tem como ser 
        usado no print adiante para mostrar o somatorio de valores, então eu decompus o cursor, primeir peguei apenas o 
        valor e joguei na variavel valor e depois transformei ela em float, então usei a variavel valorfinal que 
        funcionou"""
        row = cursor.fetchone()
        valor = row[0]
        valorfinal = (valor)

        print(45 * '=')
        print("{:<4} {:<15} {:<4} {:<10} {:<10}".format('id', 'Descrição', 'Dia', 'Custo', 'Categoria'))

        if len(registros) > 0:
            for registro in registros:
                print("{:<4} {:<15} {:<4} {:<10} {:<10}".format(registro[0], registro[1], registro[2], registro[3], registro[4]))
            print("\n{:<4} {:<15} {:<3} {:<10} {:<10}".format('Total', ' ', ' ', ' ', valorfinal))
        else:
            print('Não há registros para o mês selecionado.')
        print(45 * '=')
        continuar = input('Deseja verificar outro mês? [Digite Y para SIM]')
        while continuar == 'y':
            listar_mes()

        menu()
    else:
        print('Não identificado, tente novamente')
        listar_mes()


def listar_categoria():

    conn = conectar()
    cursor = conn.cursor()
    mes_selecionado = int(input('Escolha o mês desejado para ver as finanças por categoria (Escolha entre 01 e 12): '))
    if mes_selecionado in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        cursor.execute(f'SELECT d.id, d.nome, SUM(c.custo) FROM gastos AS c, categorias AS d WHERE mes={mes_selecionado} AND c.categoria = d.id  GROUP BY d.id, d.nome')
        registros = cursor.fetchall()
        cursor.execute(f'SELECT SUM(custo) FROM gastos WHERE mes= {mes_selecionado}')
        row = cursor.fetchone()
        valor = row[0]
        valorfinal = float(valor)

        print(45 * '=')
        print("{:<8} {:<10} {:<17}".format('id', 'Categoria', 'Gastos'))

        if len(registros) > 0:
            for registro in registros:
                print("{:<8} {:<10} {:<17}".format(registro[0], registro[1], registro[2]))
            print("\n{:<8} {:<10} {:<17}".format('Total', ' ', valorfinal))
        else:
            print('Não há registros para o mês selecionado.')
        print(45 * '=')

        continuar = input('Deseja verificar outro mês? [Digite Y para SIM]')
        while continuar == 'y':
            listar_categoria()
        menu()
    else:
        print('Não identificado, tente novamente')
        listar_categoria()


def inserir():

    conn = conectar()
    cursor = conn.cursor()

    descricao = input('Informe o produto ou serviço: ')
    dia = int(input('Informe o dia: '))
    mes = int(input('Informe o mês: '))
    custo = float(input('Informe o custo: '))

    cursor.execute(f'SELECT * FROM categorias')
    categoria1 = cursor.fetchall()
    print(categoria1)

    categoria = int(input('Informe o id da categoria: '))

    cursor.execute(f"INSERT INTO gastos (descricao, dia, mes, custo, categoria) VALUES ('{descricao}',{dia}, {mes}, {custo}, {categoria})")
    conn.commit()

    if cursor.rowcount == 1:
        print('Dados inseridos com sucesso!')
    else:
        print('Os dados não puderam ser inseridos')

    continuar = input('Deseja inserir outro registro? [Digite Y para SIM]')
    while continuar == 'y':
        inserir()
    menu()


def atualizar():

    print('Voce pode usar esta função para atualizar ou substituir algum registo!...')

    conn = conectar()
    cursor = conn.cursor()
    substituto = int(input('Qual o id do produto / serviço a ser substituído? '))
    descricao = input('Qual o novo produto / serviço a ser inserido? ')
    dia = int(input('Insira o dia: '))
    mes = int(input('Insira o mês: '))
    custo = float(input('Insira o valor: R$ '))


    cursor.execute(f"UPDATE gastos SET descricao='{descricao}', dia={dia}, mes={mes}, custo={custo} WHERE id={substituto}")
    conn.commit()

    categoria = input('Qual a categoria do registro? ')
    cursor.execute(f'SELECT * FROM categorias')
    categoria1 = cursor.fetchall()
    print("{:<10} {:<15}".format(categoria1[0], categoria1[1]))
    numero = int(input('Esoclha o numero da categoria: '))
    cursor.execute(f"UPDATE categoria SET nome='{categoria}' WHERE id={numero}")

    if cursor.rowcount == 1:
        print('O registo foi atualizado')
    else:
        print('Não foi possível atualizar o registro')

    continuar = input('Deseja atualizar outro registro? [Digite Y para SIM]')
    if continuar == 'y':
        atualizar()
    elif continuar == 'n':
        print('Voltando ao menu...')
        menu()
    else:
        print('Comando inválido, voltando ao menu inicial')
        menu()


def deletar():

    conn = conectar()
    cursor = conn.cursor()
    delet = int(input('Informe o ID do item que deseja apagar da tabela: '))
    cursor.execute(f'DELETE FROM gastos WHERE id={delet}')
    conn.commit()

    if cursor.rowcount == 1:
        print('Registro deletado')
    else:
        print('Não foi possível apagar este registro, verifique se o ID está correto')

    continuar = input('Deseja deletar outro registo? [Digite Y para SIM]')
    while continuar == 'y':
        deletar()
    menu()


def menu():

    print('\n=========Gerenciamento de Gastos==============')
    print('Selecione uma opção: ')
    print('1 - Verificar todos os registros.')
    print('2 - Gastos do mês.')
    print('3 - Gastos por categoria.')
    print('4 - Inserir registros.')
    print('5 - Atualizar registros.')
    print('6 - Deletar registros.')
    print('7 - Inserir Categorias')
    print('8 - Deletar categorias')
    print('9 - Limpar banco')
    print('0 - Desconectar\n')

    opcao = int(input())
    if opcao in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
        if opcao == 1:
            listar_tudo()
        elif opcao == 2:
            listar_mes()
        elif opcao == 3:
            listar_categoria()
        elif opcao == 4:
            inserir()
        elif opcao == 5:
            atualizar()
        elif opcao == 6:
            deletar()
        elif opcao == 7:
            categoria()
        elif opcao == 8:
            deletar_categoria()
        elif opcao == 9:
            deletar_all()
        elif opcao == 0:
            desconectar()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')


def categoria():

    conn = conectar()
    cursor = conn.cursor()
    cat = input('Informe a categoria que deseja adicionar: ')
    cursor.execute(f"INSERT INTO categorias (nome) VALUES ('{cat}')")
    conn.commit()
    if cursor.rowcount == 1:
        print('Categoria Adicionada')
    else:
        print('Não foi possível adicionar esta categoria')

    continuar = input('Deseja Adicionar outra categoria? [Digite Y para SIM]')
    while continuar == 'y':
        categoria()
    menu()


def deletar_categoria():

    print('\nATENÇÃO: NÃO É POSSÍVEL APAGAR UMA CATEGORIA QUE JA TENHA REGISTROS, PARA ISSO APAGAR PRIMEIRO TODOS OS REGISTROS DA CATEGORIA DESEJADA\n\n')
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM categorias')
    cat = cursor.fetchall()
    print(cat)
    delet = int(input('Informe o ID da categoria que deseja apagar da tabela: '))

    try:
        cursor.execute(f'DELETE FROM categorias WHERE id={delet}')
        conn.commit()
        if cursor.rowcount == 1:
            print('Registro deletado')
        else:
            print('Não foi possível apagar este registro, verifique se o ID está correto')

        continuar = input('Deseja deletar outro registo? [Digite Y para SIM]')
        while continuar == 'y':
            deletar_categoria()
        menu()

    except MySQLdb.Error as e:
        print(f'Esta categoria possui registros. Erro: {e}')
        menu()


def deletar_all():

    conn = conectar()
    cursor = conn.cursor()
    a = input('Atenção, deseja deletar todos os registros do banco? (Digite y para SIM)')
    if a in 'yY':
        cursor.execute('DELETE FROM gastos')
        conn.commit()
        menu()
    else:
        menu()


if __name__ == '__main__':
    menu()
