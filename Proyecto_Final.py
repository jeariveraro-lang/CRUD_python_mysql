import tkinter as tk
from tkinter import ttk, messagebox
from Dolls import CDolls
from Clientes import CClientes
from cartas import CCartas, ESTADOS

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Final - Auto Memory Dolls")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Tabs
        self.tab_dolls = ttk.Frame(self.notebook)
        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_cartas = ttk.Frame(self.notebook)
        self.tab_reportes = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_dolls, text="Dolls")
        self.notebook.add(self.tab_clientes, text="Clientes")
        self.notebook.add(self.tab_cartas, text="Cartas")
        self.notebook.add(self.tab_reportes, text="Reportes")

        self.build_dolls_tab()
        self.build_clientes_tab()
        self.build_cartas_tab()
        self.build_reportes_tab()

    #Comandos Dolls
    def build_dolls_tab(self):
        frame = self.tab_dolls

        # Formulario
        tk.Label(frame, text="Nombre").grid(row=0, column=0)
        self.doll_nombre = tk.Entry(frame); self.doll_nombre.grid(row=0, column=1)

        tk.Label(frame, text="Edad").grid(row=1, column=0)
        self.doll_edad = tk.Entry(frame); self.doll_edad.grid(row=1, column=1)

        self.doll_activo = tk.BooleanVar()
        tk.Checkbutton(frame, text="Activo", variable=self.doll_activo).grid(row=2, column=1)

        tk.Button(frame, text="Agregar", command=self.add_doll).grid(row=3, column=0)
        tk.Button(frame, text="Actualizar", command=self.update_doll).grid(row=3, column=1)
        tk.Button(frame, text="Eliminar", command=self.delete_doll).grid(row=3, column=2)

        # Tabla
        cols = ("id", "nombre", "edad", "activo", "cartas_en_proceso")
        self.tree_dolls = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            self.tree_dolls.heading(c, text=c)
        self.tree_dolls.grid(row=4, column=0, columnspan=3)
        self.load_dolls()

    def load_dolls(self):
        for row in self.tree_dolls.get_children():
            self.tree_dolls.delete(row)
        for d in CDolls.listar():
            self.tree_dolls.insert("", "end", values=(d["id"], d["nombre"], d["edad"], d["activo"], d["cartas_en_proceso"]))

    def add_doll(self):
        try:
            CDolls.crear(self.doll_nombre.get(), int(self.doll_edad.get()), self.doll_activo.get())
            self.load_dolls()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_doll(self):
        selected = self.tree_dolls.selection()
        if not selected: return
        item = self.tree_dolls.item(selected[0])["values"]
        try:
            CDolls.actualizar(item[0], self.doll_nombre.get(), int(self.doll_edad.get()), self.doll_activo.get())
            self.load_dolls()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_doll(self):
        selected = self.tree_dolls.selection()
        if not selected: return
        item = self.tree_dolls.item(selected[0])["values"]
        try:
            CDolls.eliminar(item[0])
            self.load_dolls()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    #Comandos_Clientes
    def build_clientes_tab(self):
        frame = self.tab_clientes

        tk.Label(frame, text="Nombre").grid(row=0, column=0)
        self.cliente_nombre = tk.Entry(frame); self.cliente_nombre.grid(row=0, column=1)

        tk.Label(frame, text="Ciudad").grid(row=1, column=0)
        self.cliente_ciudad = tk.Entry(frame); self.cliente_ciudad.grid(row=1, column=1)

        tk.Label(frame, text="Motivo").grid(row=2, column=0)
        self.cliente_motivo = tk.Entry(frame); self.cliente_motivo.grid(row=2, column=1)

        tk.Label(frame, text="Contacto").grid(row=3, column=0)
        self.cliente_contacto = tk.Entry(frame); self.cliente_contacto.grid(row=3, column=1)

        tk.Button(frame, text="Agregar", command=self.add_cliente).grid(row=4, column=0)
        tk.Button(frame, text="Actualizar", command=self.update_cliente).grid(row=4, column=1)
        tk.Button(frame, text="Eliminar", command=self.delete_cliente).grid(row=4, column=2)

        # Búsqueda
        tk.Label(frame, text="Buscar por nombre").grid(row=5, column=0)
        self.search_cliente = tk.Entry(frame); self.search_cliente.grid(row=5, column=1)
        tk.Button(frame, text="Buscar", command=self.search_clientes).grid(row=5, column=2)

        # Tabla
        cols = ("id", "nombre", "ciudad", "motivo", "contacto")
        self.tree_clientes = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            self.tree_clientes.heading(c, text=c)
        self.tree_clientes.grid(row=6, column=0, columnspan=3)
        self.load_clientes()

    def load_clientes(self, busqueda=None):
        for row in self.tree_clientes.get_children():
            self.tree_clientes.delete(row)
        for c in CClientes.listar(busqueda=busqueda):
            self.tree_clientes.insert("", "end", values=(c["id"], c["nombre"], c["ciudad"], c["motivo"], c["contacto"]))

    def add_cliente(self):
        try:
            CClientes.crear(self.cliente_nombre.get(), self.cliente_ciudad.get(), self.cliente_motivo.get(), self.cliente_contacto.get())
            self.load_clientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_cliente(self):
        selected = self.tree_clientes.selection()
        if not selected: return
        item = self.tree_clientes.item(selected[0])["values"]
        try:
            CClientes.actualizar(item[0], self.cliente_nombre.get(), self.cliente_ciudad.get(),
                                 self.cliente_motivo.get(), self.cliente_contacto.get())
            self.load_clientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_cliente(self):
        selected = self.tree_clientes.selection()
        if not selected: return
        item = self.tree_clientes.item(selected[0])["values"]
        try:
            CClientes.eliminar(item[0])
            self.load_clientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_clientes(self):
        self.load_clientes(busqueda=self.search_cliente.get())

    #Comandos_Cartas
    def build_cartas_tab(self):
        frame = self.tab_cartas

        tk.Label(frame, text="Cliente ID").grid(row=0, column=0)
        self.carta_cliente = tk.Entry(frame); self.carta_cliente.grid(row=0, column=1)

        tk.Label(frame, text="Doll ID").grid(row=1, column=0)
        self.carta_doll = tk.Entry(frame); self.carta_doll.grid(row=1, column=1)

        tk.Label(frame, text="Fecha (YYYY-MM-DD)").grid(row=2, column=0)
        self.carta_fecha = tk.Entry(frame); self.carta_fecha.grid(row=2, column=1)

        tk.Label(frame, text="Estado").grid(row=3, column=0)
        self.carta_estado = ttk.Combobox(frame, values=ESTADOS); self.carta_estado.grid(row=3, column=1)

        tk.Label(frame, text="Contenido").grid(row=4, column=0)
        self.carta_contenido = tk.Entry(frame, width=50); self.carta_contenido.grid(row=4, column=1)

        tk.Button(frame, text="Sugerir Doll", command=self.sugerir_doll).grid(row=1, column=2)

        tk.Button(frame, text="Agregar", command=self.add_carta).grid(row=5, column=0)
        tk.Button(frame, text="Actualizar", command=self.update_carta).grid(row=5, column=1)
        tk.Button(frame, text="Eliminar", command=self.delete_carta).grid(row=5, column=2)

        # Tabla
        cols = ("id","cliente","ciudad","doll","fecha","estado","contenido","cliente_id","doll_id")
        self.tree_cartas = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            self.tree_cartas.heading(c, text=c)
        self.tree_cartas.grid(row=6, column=0, columnspan=3)
        self.load_cartas()

    def load_cartas(self):
        for row in self.tree_cartas.get_children():
            self.tree_cartas.delete(row)
        for c in CCartas.listar():
            self.tree_cartas.insert("", "end", values=(c["id"], c["cliente"], c["ciudad"], c["doll"],
                                                       c["fecha"], c["estado"], c["contenido"],
                                                       c["cliente_id"], c["doll_id"]))

    def add_carta(self):
        try:
            CCartas.crear(int(self.carta_cliente.get()), int(self.carta_doll.get()),
                          self.carta_fecha.get(), self.carta_contenido.get(),
                          self.carta_estado.get() or "borrador")
            self.load_cartas()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_carta(self):
        selected = self.tree_cartas.selection()
        if not selected: return
        item = self.tree_cartas.item(selected[0])["values"]
        try:
            CCartas.actualizar(item[0], int(self.carta_cliente.get()), int(self.carta_doll.get()),
                               self.carta_fecha.get(), self.carta_estado.get(), self.carta_contenido.get())
            self.load_cartas()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_carta(self):
        selected = self.tree_cartas.selection()
        if not selected: return
        item = self.tree_cartas.item(selected[0])["values"]
        try:
            CCartas.eliminar(item[0])
            self.load_cartas()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def sugerir_doll(self):
        sugerida = CCartas.sugerir_doll()
        if sugerida:
            self.carta_doll.delete(0, tk.END)
            self.carta_doll.insert(0, sugerida[0])
            messagebox.showinfo("Sugerencia", f"Doll sugerida: {sugerida[1]} (ID {sugerida[0]})")
        else:
            messagebox.showwarning("Sugerencia", "No hay Dolls disponibles")

    #Comandos_Reportes
    def build_reportes_tab(self):
        frame = self.tab_reportes

        tk.Label(frame, text="ID Doll").grid(row=0, column=0)
        self.rep_doll_id = tk.Entry(frame); self.rep_doll_id.grid(row=0, column=1)
        tk.Button(frame, text="Generar", command=self.generar_reporte).grid(row=0, column=2)

        self.rep_resultado = tk.Text(frame, width=60, height=15)
        self.rep_resultado.grid(row=1, column=0, columnspan=3)

    def generar_reporte(self):
        try:
            id_doll = int(self.rep_doll_id.get())
            datos = CCartas.listar()
            total_cartas = sum(1 for c in datos if c["doll_id"] == id_doll)
            clientes_distintos = len(set(c["cliente_id"] for c in datos if c["doll_id"] == id_doll))

            self.rep_resultado.delete("1.0", tk.END)
            self.rep_resultado.insert(tk.END, f"Reporte para Doll ID {id_doll}\n")
            self.rep_resultado.insert(tk.END, f"Total de cartas escritas: {total_cartas}\n")
            self.rep_resultado.insert(tk.END, f"Clientes distintos atendidos: {clientes_distintos}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
