import tkinter as tk

from telas.tela_principal import TelaNotas

if __name__ == "__main__":
    # Cria a janela principal
    janela = tk.Tk()
    janela.title("Sistema de Cadastro Escolar")
    janela.geometry("720x340") # Largura x Altura

    # Cria a instância da tela de cadastro
    principal = TelaNotas(janela)

    # Inicia o loop da aplicação
    janela.mainloop()

