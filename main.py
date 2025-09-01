import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
import tkinter as tk
from tkinter import messagebox
from tkinter.font import nametofont
class LojaFranciscoApp:
    def __init__(self):
        self.root = ttk.Window(themename="flatly")
        self.root.title("Loja do Francisco Edilberto")
        self.root.geometry("440x800")
        self.root.resizable(True, True)
        self.root.place_window_center()
        
        self.value_var = ttk.StringVar()
        self.quantity_var = ttk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        title_label = ttk.Label(
            main_frame,
            text="LOJA DO FRANCISCO EDILBERTO",
            font=("Arial", 15, "bold"),
        )
        title_label.pack(pady=(0,20))

        self.create_discount_table(main_frame)

        self.create_input_section(main_frame)

        self.create_button_section(main_frame)

        self.create_results_section(main_frame)

    def create_discount_table(self, parent):
        default_font = nametofont("TkDefaultFont")
        default_font.configure(size=10)
        table_title = ttk.Label(
            text="TABELA DE DESCONTOS",
            font=("Arial", 14, "bold"),
            bootstyle=INFO,
            justify=CENTER
        )
        table_title.pack(pady=(0, 10))

        column_headers = [
            {
                "text": "Faixa de Quantidade",
                "anchor": "center",
                "stretch": True,
                "width": 200
            },
            {
                "text": "Percentual de Desconto",
                "anchor": "center",
                "stretch": True,
                "width": 150
            }
        ]
        
        row_data = [
            ("Até 9 unidades", "0%"),
            ("Entre 10 e 99 unidades", "5%"),
            ("Entre 100 e 999 unidades", "10%"),
            ("Acima de 1000 unidades", "15%")
        ]

        colors = self.root.style.colors
        discount_table = Tableview(
            master=parent,
            coldata=column_headers,
            rowdata=row_data,
            pagesize=12,
            autofit=True,
            bootstyle=INFO,
            stripecolor=(colors.light, None),
            height=11,
            autoalign=True,
        )
        discount_table.pack(fill=X, pady=(0, 20))

    def create_input_section(self, parent):
        input_frame = ttk.LabelFrame(
            parent,
            text="Dados do Produto",
            padding=15,
            bootstyle=SUCCESS
        )
        input_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(input_frame, text="Valor do Produto (R$):").grid(
            row=0, column=0, sticky=W, pady=5, padx=(0, 10)
        )
        
        value_entry = ttk.Entry(
             input_frame,
             textvariable=self.value_var,
             font=("Arial", 11),
             width=20
        )
        value_entry.grid(row=0, column=1, sticky=EW, pady=5)
        value_entry.focus()

        ttk.Label(input_frame, text="Quantidade:").grid(
            row=1, sticky=EW, pady=5
        )   
        quanity_entry = ttk.Entry(
            input_frame,
            textvariable=self.quantity_var,
            font=("Arial", 11),
            width=20
        )
        quanity_entry.grid(row=1, column=1, sticky=EW, pady=5)

        input_frame.columnconfigure(1, weight=1)

    def create_button_section(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=X, pady=(0, 20))

        calc_button = ttk.Button(
            button_frame,
            text="Calcular Desconto",
            command=self.calculate_discount,
            bootstyle=SUCCESS,
            width=15
        )
        calc_button.pack(side=LEFT, padx=(0, 10))

        clear_button = ttk.Button(
            button_frame,
            text="Limpar",
            command=self.clear_fields,
            bootstyle=SECONDARY,
            width=15
        )
        clear_button.pack(side=LEFT)
        
        exit_button = ttk.Button(
            button_frame,
            text="Sair",
            command=self.root.quit,
            bootstyle=DANGER,
            width=12
        )
        exit_button.pack(side=RIGHT)

    def create_results_section(self, parent):
        self.results_frame = ttk.LabelFrame(
            parent,
            text="Resumo da Compra",
            padding=15,
            bootstyle=PRIMARY
        )
        self.results_frame.pack(fill=BOTH,expand=YES)

        self.results_text = ttk.Label(
            self.results_frame,
            text="Preencha todos os dados acima e clique em\n 'Calcular Desconto' para ver o resumo.",
            font=("Arial", 11),
            justify=CENTER
        )
        self.results_text.pack(fill=BOTH, expand=YES)

    def validate_inputs(self):
        try:
            value = float(self.value_var.get().replace(',','.'))
            if value <=0:
                messagebox.showerror("'Erro:", "O valor deve ser maior que zero.'")
                return None, None
        except ValueError:
            messagebox.showerror("Erro:","Digite um valor numérico válido.")
            return None, None

        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
               messagebox.showerror("Erro:", "A quantidade dever ser maior que zero.")
               return None, None
        except ValueError:
           messagebox.showerror("Erro", "A quantidade dever ser um número inteiro")
           return None, None
        return value, quantity
    
    def calculate_discount(self):
        """Calcula o desconto e exibe os resultados"""
        value, quantity = self.validate_inputs()

        if value is None or quantity is None:
            return
        
        total_value = value * quantity

        if quantity <=9:
            discount = 0
            faixa = 'Até 9 unidades.'

        elif quantity <= 99:
            discount = 0.05
            faixa = 'Entre 10 e 99 unidades.'
        elif quantity <= 999:
            discount = 0.10
            faixa = 'Entre 100 e 999 unidades.'
        else:
            discount = 0.15
            faixa = 'Acima de 1000 unidades.'

        discount_value = total_value * discount
        final_value = total_value - discount_value

        result_text = f"""RESUMO DA COMPRA
Quantidade: {quantity:,} unidades
Valor Unitário: R${value:.2f}
Faixa de desconto: {faixa}
Percentual de desconto: {discount*100:.0f}%
Valor sem desconto: R${total_value:,.2f}"""
        if discount > 0:
            result_text += f"""
Valor do desconto: R${discount_value:,.2f}
VALOR FINAL: R${final_value:,.2f}"""
        else:
            result_text += f"""
VALOR FINAL: R${final_value:,.2f}"""
            
        self.results_text.config(text=result_text)

        if discount > 0:
            self.results_frame.config(bootstyle=SUCCESS)
        else:
            self.results_frame.config(bootstyle=INFO)

    def clear_fields(self):
        """Limpa todos os campos"""
        self.value_var.set("")
        self.quantity_var.set("")
        self.results_text.config(text="Preencha todos os dados acima e clique em\n 'Calcular Desconto' para ver o resumo.", justify=CENTER)
        self.results_frame.config(bootstyle=PRIMARY)

    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LojaFranciscoApp()
    app.run()