import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox
from data.context.postgre_sql_context import Postgre_Sql_Context

class TelaNotas:
    def __init__(self, win):
        """Inicializa a interface gráfica para gerenciamento de notas."""
        self.db_context = Postgre_Sql_Context()

        # Carrega alunos e disciplinas do banco de dados
        self.nomes_alunos, self.dicionario_alunos = self.buscar_alunos()
        self.nomes_disciplinas, self.dicionario_disciplinas = self.buscar_disciplinas()

        # Componentes da interface
        self.lblAluno = tk.Label(win, text='Aluno:')
        self.combobox_aluno = ttk.Combobox(win, values=self.nomes_alunos, width=30)
        self.lblDisciplina = tk.Label(win, text='Disciplina:')
        self.combobox_disciplina = ttk.Combobox(win, values=self.nomes_disciplinas, width=30)
        self.lblNota = tk.Label(win, text='Nota:')
        self.entrada_nota = tk.Entry(win, width=10)
        self.lblIdAluno = tk.Label(win, text='ID do Aluno:')
        self.entrada_id_aluno = tk.Entry(win, width=10)

        # Novos componentes para seleção por ID
        self.lblIdSelecao = tk.Label(win, text='ID para Seleção:')
        self.entrada_id_selecao = tk.Entry(win, width=10)
        self.btnSelecionarAluno = tk.Button(win, text='Selecionar Aluno', command=self.selecionar_aluno_por_id)

        self.btnVerificar = tk.Button(win, text='Verificar', command=self.verificar_nota)
        self.btnSalvar = tk.Button(win, text='Salvar', command=self.salvar_nota)
        self.btnExcluir = tk.Button(win, text='Excluir', command=self.excluir_nota)
        self.btnLimpar = tk.Button(win, text='Limpar', command=self.limpar_campos)
        self.btnCadastrarAluno = tk.Button(win, text='Cadastrar Aluno', command=self.cadastrar_aluno)
        self.btnVerNotas = tk.Button(win, text='Ver Notas por ID', command=self.ver_notas_por_id)

        # Posicionamento dos componentes
        self.lblAluno.place(x=50, y=30)
        self.combobox_aluno.place(x=150, y=30)
        self.lblDisciplina.place(x=50, y=60)
        self.combobox_disciplina.place(x=150, y=60)
        self.lblNota.place(x=50, y=90)
        self.entrada_nota.place(x=150, y=90)
        self.lblIdAluno.place(x=50, y=120)
        self.entrada_id_aluno.place(x=150, y=120)

        # Posicionamento dos novos componentes
        self.lblIdSelecao.place(x=350, y=30)
        self.entrada_id_selecao.place(x=450, y=30)
        self.btnSelecionarAluno.place(x=550, y=30)

        self.btnVerificar.place(x=50, y=160)
        self.btnSalvar.place(x=150, y=160)
        self.btnExcluir.place(x=250, y=160)
        self.btnLimpar.place(x=350, y=160)
        self.btnCadastrarAluno.place(x=450, y=160)
        self.btnVerNotas.place(x=250, y=120)

        # Variável para rastrear a nota atual
        self.current_id_nota = None

    def buscar_alunos(self):
        """Busca os nomes e IDs dos alunos no banco de dados."""
        query = "SELECT id_aluno, nome FROM alunos"
        try:
            self.db_context.conectar()
            results = self.db_context.executar_query_sql(query)
            self.db_context.desconectar()
            nomes_alunos = [row[1] for row in results]
            dicionario_alunos = {row[1]: row[0] for row in results}
            return nomes_alunos, dicionario_alunos
        except Exception as e:
            msgbox.showerror('Erro', f'Falha ao carregar alunos: {e}')
            return [], {}

    def buscar_disciplinas(self):
        """Busca os nomes e IDs das disciplinas no banco de dados."""
        query = "SELECT id_disciplina, nome_disciplina FROM disciplinas"
        try:
            self.db_context.conectar()
            results = self.db_context.executar_query_sql(query)
            self.db_context.desconectar()
            nomes_disciplinas = [row[1] for row in results]
            dicionario_disciplinas = {row[1]: row[0] for row in results}
            return nomes_disciplinas, dicionario_disciplinas
        except Exception as e:
            msgbox.showerror('Erro', f'Falha ao carregar disciplinas: {e}')
            return [], {}

    def selecionar_aluno_por_id(self):
        """Seleciona o aluno no combobox com base no ID fornecido."""
        id_aluno_str = self.entrada_id_selecao.get().strip()
        if not id_aluno_str:
            msgbox.showwarning('Aviso', 'Digite o ID do aluno.')
            return
        try:
            id_aluno = int(id_aluno_str)
        except ValueError:
            msgbox.showerror('Erro', 'ID do aluno deve ser um número válido.')
            return

        # Buscar o nome do aluno pelo ID
        query = f"SELECT nome FROM alunos WHERE id_aluno = {id_aluno}"
        try:
            self.db_context.conectar()
            result = self.db_context.executar_query_sql(query)
            self.db_context.desconectar()
            if result and result[0][0]:
                nome_aluno = result[0][0]
                if nome_aluno in self.nomes_alunos:
                    self.combobox_aluno.set(nome_aluno)
                    msgbox.showinfo('Sucesso', f'Aluno {nome_aluno} selecionado.')
                else:
                    msgbox.showerror('Erro', 'Aluno não encontrado na lista.')
            else:
                msgbox.showerror('Erro', 'Aluno não encontrado.')
        except Exception as e:
            msgbox.showerror('Erro', f'Falha ao buscar aluno: {str(e)}')

    def verificar_nota(self):
        """Verifica se existe uma nota para o aluno e disciplina selecionados."""
        nome_aluno = self.combobox_aluno.get()
        nome_disciplina = self.combobox_disciplina.get()
        if not nome_aluno or not nome_disciplina:
            msgbox.showwarning('Aviso', 'Selecione aluno e disciplina.')
            return
        try:
            id_aluno = self.dicionario_alunos[nome_aluno]
            id_disciplina = self.dicionario_disciplinas[nome_disciplina]
        except KeyError:
            msgbox.showerror('Erro', 'Aluno ou disciplina inválidos.')
            return

        query = f"SELECT id_nota, nota FROM notas WHERE id_aluno = {id_aluno} AND id_disciplina = {id_disciplina}"
        try:
            self.db_context.conectar()
            results = self.db_context.executar_query_sql(query)
            self.db_context.desconectar()
            if results:
                self.current_id_nota, nota = results[0]
                self.entrada_nota.delete(0, tk.END)
                self.entrada_nota.insert(0, str(nota))
                msgbox.showinfo('Info', 'Nota encontrada.')
            else:
                self.current_id_nota = None
                self.entrada_nota.delete(0, tk.END)
                msgbox.showinfo('Info', 'Nenhuma nota encontrada.')
        except Exception as e:
            msgbox.showerror('Erro', f'Falha ao verificar nota: {e}')

    def salvar_nota(self):
        """Salva (insere ou atualiza) a nota no banco de dados."""
        nome_aluno = self.combobox_aluno.get()
        nome_disciplina = self.combobox_disciplina.get()
        nota_str = self.entrada_nota.get()
        
        if not all([nome_aluno, nome_disciplina, nota_str]):
            msgbox.showwarning('Aviso', 'Todos os campos são obrigatórios.')
            return
        
        try:
            id_aluno = self.dicionario_alunos[nome_aluno]
            id_disciplina = self.dicionario_disciplinas[nome_disciplina]
            nota = float(nota_str)
        except KeyError:
            msgbox.showerror('Erro', 'Aluno ou disciplina inválidos.')
            return
        except ValueError:
            msgbox.showerror('Erro', 'Valor de nota inválido.')
            return

        if self.current_id_nota is None:
            # Inserção de nova nota
            query = f"SELECT MAX(id_nota) FROM notas"
            try:
                self.db_context.conectar()
                result = self.db_context.executar_query_sql(query)
                max_id = result[0][0] if result and result[0][0] is not None else 0
                novo_id_nota = max_id + 1
                query = f"INSERT INTO notas (id_nota, id_aluno, id_disciplina, nota) VALUES ({novo_id_nota}, {id_aluno}, {id_disciplina}, {nota})"
                self.db_context.executar_update_sql(query)
                self.db_context.desconectar()
                msgbox.showinfo('Sucesso', 'Nota salva com sucesso.')
                self.limpar_campos_parcial()
            except Exception as e:
                msgbox.showerror('Erro', f'Falha ao salvar nota: {e}')
        else:
            # Atualização de nota existente
            query = f"UPDATE notas SET nota = {nota} WHERE id_nota = {self.current_id_nota}"
            try:
                self.db_context.conectar()
                self.db_context.executar_update_sql(query)
                self.db_context.desconectar()
                msgbox.showinfo('Sucesso', 'Nota salva com sucesso.')
                self.limpar_campos_parcial()
            except Exception as e:
                msgbox.showerror('Erro', f'Falha ao salvar nota: {e}')

    def excluir_nota(self):
        """Exclui a nota atual do banco de dados."""
        if self.current_id_nota is None:
            msgbox.showwarning('Aviso', 'Nenhuma nota selecionada para excluir.')
            return
        query = f"DELETE FROM notas WHERE id_nota = {self.current_id_nota}"
        try:
            self.db_context.conectar()
            self.db_context.executar_update_sql(query)
            self.db_context.desconectar()
            msgbox.showinfo('Sucesso', 'Nota excluída com sucesso.')
            self.limpar_campos_parcial()
        except Exception as e:
            msgbox.showerror('Erro', f'Falha ao excluir nota: {e}')

    def limpar_campos(self):
        """Limpa todos os campos da interface."""
        self.combobox_aluno.set('')
        self.combobox_disciplina.set('')
        self.entrada_nota.delete(0, tk.END)
        self.entrada_id_aluno.delete(0, tk.END)
        self.current_id_nota = None

    def limpar_campos_parcial(self):
        """Limpa apenas os campos relacionados à nota, preservando o aluno."""
        self.combobox_disciplina.set('')
        self.entrada_nota.delete(0, tk.END)
        self.entrada_id_aluno.delete(0, tk.END)
        self.current_id_nota = None

    def cadastrar_aluno(self):
        """Abre uma janela para cadastrar um novo aluno."""
        janela_cadastro = tk.Toplevel()
        janela_cadastro.title("Cadastrar Aluno")
        janela_cadastro.geometry("300x200")

        lbl_nome = tk.Label(janela_cadastro, text="Nome do Aluno:")
        lbl_nome.pack(pady=5)
        entrada_nome = tk.Entry(janela_cadastro, width=30)
        entrada_nome.pack(pady=5)

        lbl_data_nascimento = tk.Label(janela_cadastro, text="Data de Nascimento (AAAA-MM-DD):")
        lbl_data_nascimento.pack(pady=5)
        entrada_data_nascimento = tk.Entry(janela_cadastro, width=30)
        entrada_data_nascimento.pack(pady=5)

        def salvar_novo_aluno():
            nome = entrada_nome.get().strip()
            data_nascimento = entrada_data_nascimento.get().strip()
            if not nome or not data_nascimento:
                msgbox.showwarning('Aviso', 'O nome e a data de nascimento são obrigatórios.')
                return
            
            try:
                from datetime import datetime
                datetime.strptime(data_nascimento, '%Y-%m-%d')
            except ValueError:
                msgbox.showerror('Erro', 'Data de nascimento inválida. Use o formato AAAA-MM-DD.')
                return

            query = "INSERT INTO alunos (nome, data_nascimento) VALUES (%s, %s)"
            params = (nome, data_nascimento)
            try:
                self.db_context.conectar()
                if not self.db_context.executar_update_sql(query, params):
                    raise Exception("Falha ao executar a inserção do aluno.")
                self.db_context.desconectar()

                self.nomes_alunos, self.dicionario_alunos = self.buscar_alunos()
                self.combobox_aluno['values'] = self.nomes_alunos
                msgbox.showinfo('Sucesso', 'Aluno cadastrado com sucesso.')
                janela_cadastro.destroy()
            except Exception as e:
                msgbox.showerror('Erro', f'Falha ao cadastrar aluno: {str(e)}')
                if self.db_context.conectar() is not None:
                    self.db_context.desconectar()

        btn_salvar = tk.Button(janela_cadastro, text="Salvar", command=salvar_novo_aluno)
        btn_salvar.pack(pady=10)

    def ver_notas_por_id(self):
        """Exibe todas as notas de um aluno com base no ID fornecido."""
        id_aluno = self.entrada_id_aluno.get().strip()
        if not id_aluno:
            msgbox.showwarning('Aviso', 'Digite o ID do aluno.')
            return
        
        try:
            id_aluno = int(id_aluno)
        except ValueError:
            msgbox.showerror('Erro', 'ID do aluno deve ser um número válido.')
            return

        # Buscar o nome do aluno
        query_nome = f"SELECT nome FROM alunos WHERE id_aluno = {id_aluno}"
        try:
            self.db_context.conectar()
            result = self.db_context.executar_query_sql(query_nome)
            self.db_context.desconectar()
            if result and result[0][0]:
                nome_aluno = result[0][0]
            else:
                nome_aluno = f"ID {id_aluno}"
        except Exception as e:
            msgbox.showerror('Erro', f'Falha ao buscar nome do aluno: {str(e)}')
            nome_aluno = f"ID {id_aluno}"

        query = f"SELECT d.nome_disciplina, n.nota FROM notas n JOIN disciplinas d ON n.id_disciplina = d.id_disciplina WHERE n.id_aluno = {id_aluno}"
        try:
            self.db_context.conectar()
            results = self.db_context.executar_query_sql(query)
            self.db_context.desconectar()

            if not results:
                msgbox.showinfo('Info', f'Nenhuma nota encontrada para o aluno com ID {id_aluno}.')
                return

            janela_notas = tk.Toplevel()
            janela_notas.title(f"Notas do(a) {nome_aluno}")
            janela_notas.geometry("300x200")

            lbl_titulo = tk.Label(janela_notas, text=f"Notas do(a) {nome_aluno}:")
            lbl_titulo.pack(pady=5)

            lista_notas = tk.Listbox(janela_notas, width=40, height=10)
            lista_notas.pack(pady=5)

            for disciplina, nota in results:
                lista_notas.insert(tk.END, f"{disciplina}: {nota}")

            btn_fechar = tk.Button(janela_notas, text="Fechar", command=janela_notas.destroy)
            btn_fechar.pack(pady=5)

        except Exception as e:
            msgbox.showerror('Erro', f'Falha ao buscar notas: {str(e)}')