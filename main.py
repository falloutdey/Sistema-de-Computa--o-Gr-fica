# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import math
import re

import globals
from grid import Grid
from interface import *
from Sistemas.bresenham import Bresenham
from Sistemas.polilinha import Polilinha
from Sistemas.circulo import Circulo
from Sistemas.elipse import Elipse
from Sistemas.curvas import Curvas
from Sistemas.preenchimentoRecursivo import PreenchimentoRecursivo
from Sistemas.varredura import Varredura
from Sistemas.recorteLinha import RecorteLinha
from Sistemas.recortePoligono import RecortePoligono
from Sistemas.transformacao import Transformacao
from Sistemas.projecoes import Projetor3D

class App:
    """
    Classe principal que gerencia a interface gráfica e a lógica do sistema de computação gráfica.
    """
    def __init__(self, root):
        """
        Inicializa a aplicação principal.

        Args:
            root (tk.Tk): A janela raiz da aplicação.
        """
        globals.init()
        self.root = root
        self.root.title("Sistema de Computação Gráfica")

        # Cria a grade de desenho (canvas)
        self.tela = Grid(self.root, 550)
        self.tela.tela.pack(side=tk.LEFT, padx=10, pady=10)
        self.tela.tela.bind("<Button-1>", self.handle_grid_click)

        # Variável de controle para o modo de desenho atual
        self.current_mode = tk.StringVar(value="linha")

        # Container principal para todos os controles
        self.main_controls_container = tk.Frame(self.root)
        self.main_controls_container.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        # Container superior para os painéis de modo e controles dinâmicos
        top_panel_container = tk.Frame(self.main_controls_container)
        top_panel_container.pack(fill='x', anchor='n')

        # Painel estático para seleção de modo
        static_controls_frame = tk.Frame(top_panel_container)
        static_controls_frame.pack(side=tk.LEFT, anchor='n')

        # Painel dinâmico que exibe os controles do modo selecionado
        self.dynamic_controls_frame = tk.Frame(top_panel_container)
        self.dynamic_controls_frame.pack(side=tk.RIGHT, anchor='n', padx=(10, 0))

        # Cria os frames da UI
        self.create_mode_selection_frame(static_controls_frame)
        self.create_all_control_frames()

        # Botão para limpar a tela
        ttk.Button(self.main_controls_container, text="Limpar Tudo", command=lambda: self.limpar_tudo(manter_desenho=False)).pack(pady=20, padx=10, ipady=10, fill='x')

        # Frame com os nomes dos desenvolvedores
        dev_frame = tk.Frame(self.main_controls_container)
        dev_frame.pack(side=tk.BOTTOM, pady=10)
        tk.Label(dev_frame, text="Desenvolvido por:", font=("Helvetica", 8, "bold")).pack()
        tk.Label(dev_frame, text="Deydson Assunção da Costa", font=("Helvetica", 8)).pack()
        tk.Label(dev_frame, text="Dionísio Fares da Silva", font=("Helvetica", 8)).pack()
        
        # Inicializa o modo e a visibilidade dos widgets
        self.switch_mode()
        self.toggle_distancia_camera()

    def create_mode_selection_frame(self, parent):
        """
        Cria o frame com os botões de rádio para selecionar o modo de desenho.

        Args:
            parent (tk.Widget): O widget pai onde este frame será inserido.
        """
        mode_frame = ttk.LabelFrame(parent, text="Modo de Desenho")
        mode_frame.pack(pady=10, padx=10)
        
        modos = {
            "Linha": "linha", "Polilinha": "polilinha", "Círculo": "circulo", 
            "Elipse": "elipse", "Curva": "curva", "Preenchimento": "preenchimento", 
            "Varredura": "varredura", "Recorte de Linha": "recorte_linha", 
            "Recorte de Polígono": "recorte_poligono", "Transformação": "transformacao", 
            "Projeção 3D": "projecao"
        }

        for text, value in modos.items():
            ttk.Radiobutton(mode_frame, text=text, variable=self.current_mode, 
                            value=value, command=self.switch_mode).pack(anchor="w")

    def create_all_control_frames(self):
        """
        Usa as funções do `ui_frames.py` para criar todos os painéis de controle
        e armazena-os em dicionários para fácil acesso.
        """
        self.frames = {}
        self.widgets = {}

        # Mapeia cada modo a uma função de criação de frame
        frame_factories = {
            "linha": create_linha_frame,
            "polilinha": create_polilinha_frame,
            "circulo": create_circulo_frame,
            "elipse": create_elipse_frame,
            "curva": create_curva_frame,
            "preenchimento": create_preenchimento_frame,
            "varredura": create_varredura_frame,
            "recorte_linha": create_recorte_linha_frame,
            "recorte_poligono": create_recorte_poligono_frame,
            "transformacao": create_transformacao_frame,
            "projecao": create_projecao_frame,
        }

        # Cria cada frame e armazena seus widgets
        for mode, factory in frame_factories.items():
            frame, widgets = factory(self.dynamic_controls_frame, self)
            self.frames[mode] = frame
            self.widgets[mode] = widgets

    def get_widget(self, mode, widget_name):
        """
        Retorna um widget específico de um frame de controle.

        Args:
            mode (str): A chave do modo (ex: 'linha', 'circulo').
            widget_name (str): O nome do widget a ser recuperado.

        Returns:
            tk.Widget: O widget solicitado.
        """
        return self.widgets[mode][widget_name]

    def handle_grid_click(self, event):
        """
        Manipula o evento de clique do mouse na grade de desenho.

        Args:
            event (tk.Event): O objeto de evento do clique.
        """
        grid_x, grid_y = self.tela.converter_para_coordenadas_grid(event.x, event.y)
        modo = self.current_mode.get()

        # Limpa a tela se for o primeiro ponto de um novo desenho
        if not globals.pontos_selecionados and modo not in ["preenchimento", "recorte_linha", "recorte_poligono", "projecao"]:
            self.tela.limpar_tela()

        # Limita o número de pontos para formas simples
        max_points = {"linha": 2, "circulo": 2, "elipse": 3}
        if modo in max_points and len(globals.pontos_selecionados) >= max_points[modo]:
            self.limpar_tudo(manter_desenho=False)

        # Lógica de clique específica para cada modo
        if modo == "transformacao":
            if globals.estado_transformacao == "definindo_poligono":
                globals.pontos_selecionados.append((grid_x, grid_y))
                self.atualizar_texto_pontos()
                self.desenhar_poligono_para_transformacao()
        elif modo == "projecao":
            return
        elif modo == "recorte_linha":
            if globals.estado_recorte == "definindo_janela":
                if len(globals.pontos_selecionados) >= 2: self.limpar_tudo(manter_desenho=False)
                globals.pontos_selecionados.append((grid_x, grid_y)); self.tela.desenhar_pixel(grid_x, grid_y, "red")
                if len(globals.pontos_selecionados) == 1:
                    self.get_widget('recorte_linha', 'entry_xmin').delete(0, tk.END); self.get_widget('recorte_linha', 'entry_xmin').insert(0, str(grid_x)); self.get_widget('recorte_linha', 'entry_ymin').delete(0, tk.END); self.get_widget('recorte_linha', 'entry_ymin').insert(0, str(grid_y))
                elif len(globals.pontos_selecionados) == 2:
                    self.get_widget('recorte_linha', 'entry_xmax').delete(0, tk.END); self.get_widget('recorte_linha', 'entry_xmax').insert(0, str(grid_x)); self.get_widget('recorte_linha', 'entry_ymax').delete(0, tk.END); self.get_widget('recorte_linha', 'entry_ymax').insert(0, str(grid_y))
            elif globals.estado_recorte == "definindo_linha":
                if len(globals.pontos_selecionados) >= 2:
                    self.limpar_tudo(manter_desenho=True, limpar_apenas_pontos=True); self.tela.destacar_janela(**globals.janela_de_recorte)
                globals.pontos_selecionados.append((grid_x, grid_y)); self.tela.desenhar_pixel(grid_x, grid_y, "blue")
                if len(globals.pontos_selecionados) == 1:
                    self.get_widget('recorte_linha', 'entry_x0_recorte').delete(0, tk.END); self.get_widget('recorte_linha', 'entry_x0_recorte').insert(0, str(grid_x)); self.get_widget('recorte_linha', 'entry_y0_recorte').delete(0, tk.END); self.get_widget('recorte_linha', 'entry_y0_recorte').insert(0, str(grid_y))
                elif len(globals.pontos_selecionados) == 2:
                    self.get_widget('recorte_linha', 'entry_x1_recorte').delete(0, tk.END); self.get_widget('recorte_linha', 'entry_x1_recorte').insert(0, str(grid_x)); self.get_widget('recorte_linha', 'entry_y1_recorte').delete(0, tk.END); self.get_widget('recorte_linha', 'entry_y1_recorte').insert(0, str(grid_y))
                    self.desenhar_linha_original_para_recorte()
        elif modo == "recorte_poligono":
            if globals.estado_recorte == "definindo_janela":
                if len(globals.pontos_selecionados) >= 2: self.limpar_tudo(manter_desenho=False)
                globals.pontos_selecionados.append((grid_x, grid_y)); self.tela.desenhar_pixel(grid_x, grid_y, "red")
                if len(globals.pontos_selecionados) == 1:
                    self.get_widget('recorte_poligono', 'entry_xmin_p').delete(0, tk.END); self.get_widget('recorte_poligono', 'entry_xmin_p').insert(0, str(grid_x)); self.get_widget('recorte_poligono', 'entry_ymin_p').delete(0, tk.END); self.get_widget('recorte_poligono', 'entry_ymin_p').insert(0, str(grid_y))
                elif len(globals.pontos_selecionados) == 2:
                    self.get_widget('recorte_poligono', 'entry_xmax_p').delete(0, tk.END); self.get_widget('recorte_poligono', 'entry_xmax_p').insert(0, str(grid_x)); self.get_widget('recorte_poligono', 'entry_ymax_p').delete(0, tk.END); self.get_widget('recorte_poligono', 'entry_ymax_p').insert(0, str(grid_y))
            elif globals.estado_recorte == "definindo_poligono":
                globals.pontos_selecionados.append((grid_x, grid_y));
                self.atualizar_texto_pontos()
                self.desenhar_poligono_original_para_recorte()
        elif modo == "preenchimento":
            if globals.estado_preenchimento == "escolhendo_semente":
                if not self.ponto_esta_dentro((grid_x, grid_y), globals.poligono_para_preencher): messagebox.showwarning("Ponto Inválido", "O ponto de semente deve estar DENTRO do polígono."); return
                if self.tela.checar_matriz(grid_x, grid_y) == '#000000': messagebox.showwarning("Ponto Inválido", "O ponto de semente não pode estar sobre uma borda."); return
                self.tela.limpar_marcadores(); globals.pontos_selecionados = [(grid_x, grid_y)]; self.tela.desenhar_marcador_temporario(grid_x, grid_y, "cyan")
                self.get_widget('preenchimento', 'entry_p_x_fill').delete(0, tk.END); self.get_widget('preenchimento', 'entry_p_x_fill').insert(0, str(grid_x)); self.get_widget('preenchimento', 'entry_p_y_fill').delete(0, tk.END); self.get_widget('preenchimento', 'entry_p_y_fill').insert(0, str(grid_y))
            else: globals.pontos_selecionados.append((grid_x, grid_y)); self.tela.desenhar_pixel(grid_x, grid_y, "blue"); self.atualizar_texto_pontos()
        elif modo in ["polilinha", "varredura", "curva"]:
            globals.pontos_selecionados.append((grid_x, grid_y)); cor = "blue"
            if modo == "varredura": cor = "magenta"
            elif modo == "curva":
                if len(globals.pontos_selecionados) == 1: cor = "green"
                else:
                    if len(globals.pontos_selecionados) > 2: self.tela.desenhar_pixel(globals.pontos_selecionados[-2][0], globals.pontos_selecionados[-2][1], "orange")
                    cor = "red"
            self.tela.desenhar_pixel(grid_x, grid_y, cor); self.atualizar_texto_pontos()
        elif modo in ["linha", "circulo", "elipse"]:
            globals.pontos_selecionados.append((grid_x, grid_y))
            cor_ponto = {"linha": "blue", "circulo": "green", "elipse": "purple"}
            self.tela.desenhar_pixel(grid_x, grid_y, cor_ponto[modo])
            if modo == "linha":
                if len(globals.pontos_selecionados) == 1: self.get_widget('linha', 'entry_x0').delete(0, tk.END); self.get_widget('linha', 'entry_x0').insert(0, str(grid_x)); self.get_widget('linha', 'entry_y0').delete(0, tk.END); self.get_widget('linha', 'entry_y0').insert(0, str(grid_y))
                elif len(globals.pontos_selecionados) == 2: self.get_widget('linha', 'entry_x1').delete(0, tk.END); self.get_widget('linha', 'entry_x1').insert(0, str(grid_x)); self.get_widget('linha', 'entry_y1').delete(0, tk.END); self.get_widget('linha', 'entry_y1').insert(0, str(grid_y))
            elif modo == "circulo":
                if len(globals.pontos_selecionados) == 1: self.get_widget('circulo', 'entry_cx').delete(0, tk.END); self.get_widget('circulo', 'entry_cx').insert(0, str(grid_x)); self.get_widget('circulo', 'entry_cy').delete(0, tk.END); self.get_widget('circulo', 'entry_cy').insert(0, str(grid_y))
                elif len(globals.pontos_selecionados) == 2: p1,p2=globals.pontos_selecionados; raio=math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2); self.get_widget('circulo', 'entry_raio').delete(0,tk.END); self.get_widget('circulo', 'entry_raio').insert(0,f"{raio:.2f}"); self.desenhar_circulo()
            elif modo == "elipse":
                if len(globals.pontos_selecionados) == 1: self.get_widget('elipse', 'entry_ex').delete(0, tk.END); self.get_widget('elipse', 'entry_ex').insert(0, str(grid_x)); self.get_widget('elipse', 'entry_ey').delete(0, tk.END); self.get_widget('elipse', 'entry_ey').insert(0, str(grid_y))
                elif len(globals.pontos_selecionados) == 2: raio_x=abs(globals.pontos_selecionados[1][0]-globals.pontos_selecionados[0][0]); self.get_widget('elipse', 'entry_rx').delete(0,tk.END); self.get_widget('elipse', 'entry_rx').insert(0,str(raio_x))
                elif len(globals.pontos_selecionados) == 3: raio_y=abs(globals.pontos_selecionados[2][1]-globals.pontos_selecionados[0][1]); self.get_widget('elipse', 'entry_ry').delete(0,tk.END); self.get_widget('elipse', 'entry_ry').insert(0,str(raio_y)); self.desenhar_elipse()

    def ponto_esta_dentro(self, ponto, poligono):
        """
        Verifica se um ponto está dentro de um polígono usando o algoritmo Ray Casting.

        Args:
            ponto (tuple): As coordenadas (x, y) do ponto a ser verificado.
            poligono (list): Uma lista de tuplas com os vértices do polígono.

        Returns:
            bool: True se o ponto está dentro, False caso contrário.
        """
        x, y = ponto; n = len(poligono); dentro = False; p1x, p1y = poligono[0]
        for i in range(n + 1):
            p2x, p2y = poligono[i % n]
            if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y: xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= xinters: dentro = not dentro
            p1x, p1y = p2x, p2y
        return dentro

    def add_point_from_entry(self):
        """
        Adiciona um ponto à lista de pontos selecionados a partir dos valores
        inseridos nos campos de entrada (Entry widgets).
        """
        modo = self.current_mode.get()
        entry_map={"polilinha":('entry_p_x_pv','entry_p_y_pv'),"varredura":('entry_p_x_varredura','entry_p_y_varredura'),"curva":('entry_p_x_curva','entry_p_y_curva'),"preenchimento":('entry_p_x_preenchimento','entry_p_y_preenchimento'),"recorte_poligono":('entry_p_x_recorte_p','entry_p_y_recorte_p'), "transformacao":('entry_p_x_transf', 'entry_p_y_transf')}
        if modo not in entry_map: return
        entry_x_name, entry_y_name = entry_map[modo]
        entry_x = self.get_widget(modo, entry_x_name)
        entry_y = self.get_widget(modo, entry_y_name)
        
        try: x=int(entry_x.get()); y=int(entry_y.get())
        except ValueError: messagebox.showerror("Entrada Inválida", "As coordenadas do ponto devem ser números inteiros."); return
        if not globals.pontos_selecionados and modo not in ["preenchimento", "recorte_linha", "recorte_poligono"]: self.tela.limpar_tela()

        globals.pontos_selecionados.append((x, y))

        if modo == "recorte_poligono":
            if globals.estado_recorte == "definindo_poligono":
                self.atualizar_texto_pontos()
                self.desenhar_poligono_original_para_recorte()
        elif modo == "transformacao":
            self.desenhar_poligono_para_transformacao()
        else:
            cor = "blue"
            if modo=="varredura": cor="magenta"
            elif modo=="curva":
                if len(globals.pontos_selecionados)==1: cor="green"
                else: cor="red"
            self.tela.desenhar_pixel(x,y,cor)
            if modo=="curva" and len(globals.pontos_selecionados)>2: p_anterior=globals.pontos_selecionados[-2]; self.tela.desenhar_pixel(p_anterior[0],p_anterior[1],"orange")

        self.atualizar_texto_pontos(); entry_x.delete(0,tk.END); entry_y.delete(0,tk.END)


    def desenhar_poligono_para_transformacao(self, cor='blue'):
        """
        Desenha o polígono que será transformado na tela.

        Args:
            cor (str): A cor do polígono.
        """
        self.tela.limpar_tela()
        pontos = globals.pontos_selecionados if globals.estado_transformacao == "definindo_poligono" else globals.poligono_para_transformar
        if len(pontos) >= 2:
            polilinha = Polilinha(pontos, fechar=True)
            self.tela.desenhar(polilinha.saida, cor)
        elif pontos:
            for ponto in pontos:
                self.tela.desenhar_pixel(ponto[0], ponto[1], cor)

    def finalizar_poligono_para_transformacao(self):
        """
        Finaliza a definição do polígono para transformação, mudando o estado da aplicação.
        """
        if len(globals.pontos_selecionados) < 3:
            messagebox.showerror("Polígono Inválido", "São necessários pelo menos 3 pontos para formar um polígono.")
            return
        globals.poligono_para_transformar = list(globals.pontos_selecionados)
        globals.estado_transformacao = "aplicando_transformacao"
        self.switch_transform_state()
        self.atualizar_texto_pontos()

    def aplicar_translacao(self):
        """
        Aplica a transformação de translação ao polígono.
        """
        if not globals.poligono_para_transformar: messagebox.showwarning("Nenhum Polígono", "Finalize um polígono primeiro."); return
        try:
            dx = int(self.get_widget('transformacao', 'entry_dx_transf').get())
            dy = int(self.get_widget('transformacao', 'entry_dy_transf').get())
        except ValueError: messagebox.showerror("Entrada Inválida", "Os valores de translação devem ser inteiros."); return

        transformador = Transformacao(globals.poligono_para_transformar)
        globals.poligono_para_transformar = transformador.translacao(dx, dy)
        self.desenhar_poligono_para_transformacao(cor='green')
        self.atualizar_texto_pontos()

    def get_pivo_from_combobox(self, combobox):
        """
        Obtém e valida as coordenadas do ponto pivô selecionado em um Combobox.

        Args:
            combobox (ttk.Combobox): O widget combobox.

        Returns:
            list or None: Uma lista com as coordenadas [x, y] do pivô ou None se a entrada for inválida.
        """
        pivo_str = combobox.get()
        if not pivo_str:
            messagebox.showerror("Pivô Inválido", "Por favor, selecione um ponto pivô da lista.")
            return None
        try:
            numeros = re.findall(r'-?\d+\.?\d*', pivo_str)
            return [float(numeros[0]), float(numeros[1])]
        except (IndexError, ValueError):
            messagebox.showerror("Pivô Inválido", f"Não foi possível ler as coordenadas do pivô: {pivo_str}")
            return None

    def aplicar_escalonamento(self):
        """
        Aplica a transformação de escalonamento ao polígono.
        """
        if not globals.poligono_para_transformar: messagebox.showwarning("Nenhum Polígono", "Finalize um polígono primeiro."); return

        pivo = self.get_pivo_from_combobox(self.get_widget('transformacao', 'combo_pivo_escalonamento'))
        if pivo is None: return

        try:
            sx = float(self.get_widget('transformacao', 'entry_sx_transf').get())
            sy = float(self.get_widget('transformacao', 'entry_sy_transf').get())
        except ValueError: messagebox.showerror("Entrada Inválida", "Fatores de escala devem ser números."); return

        transformador = Transformacao(globals.poligono_para_transformar)
        pontos_transformados_rasterizados = transformador.escalonamento(sx, sy, pivo=pivo)

        self.tela.limpar_tela()
        self.tela.desenhar(pontos_transformados_rasterizados, 'green')

        globals.poligono_para_transformar = transformador.entrada
        self.atualizar_texto_pontos()

    def aplicar_rotacao(self):
        """
        Aplica a transformação de rotação ao polígono.
        """
        if not globals.poligono_para_transformar: messagebox.showwarning("Nenhum Polígono", "Finalize um polígono primeiro."); return

        pivo = self.get_pivo_from_combobox(self.get_widget('transformacao', 'combo_pivo_rotacao'))
        if pivo is None: return

        try:
            angulo = float(self.get_widget('transformacao', 'entry_angulo_transf').get())
        except ValueError: messagebox.showerror("Entrada Inválida", "O ângulo deve ser um número."); return

        transformador = Transformacao(globals.poligono_para_transformar)
        pontos_transformados_rasterizados = transformador.rotacao(angulo, pivo=pivo)

        self.tela.limpar_tela()
        self.tela.desenhar(pontos_transformados_rasterizados, 'green')

        globals.poligono_para_transformar = transformador.entrada
        self.atualizar_texto_pontos()

    def desenhar_linha(self):
        """
        Desenha uma linha na tela usando o algoritmo de Bresenham.
        """
        try: p1=(int(self.get_widget('linha', 'entry_x0').get()),int(self.get_widget('linha', 'entry_y0').get())); p2=(int(self.get_widget('linha', 'entry_x1').get()),int(self.get_widget('linha', 'entry_y1').get()))
        except ValueError: messagebox.showerror("Entrada Inválida", "As coordenadas devem ser números inteiros."); self.limpar_tudo(manter_desenho=True); return
        self.tela.limpar_tela(); linha=Bresenham(p1, p2); self.tela.desenhar(linha.saida,'#000000'); self.tela.desenhar_pixel(p1[0],p1[1],"blue"); self.tela.desenhar_pixel(p2[0],p2[1],"blue")

    def desenhar_polilinha(self):
        """
        Desenha uma polilinha (aberta) na tela.
        """
        if len(globals.pontos_selecionados)<2: messagebox.showwarning("Pontos Insuficientes", "São necessários pelo menos 2 pontos para desenhar uma polilinha."); return
        pontos_para_desenhar = list(globals.pontos_selecionados); self.tela.limpar_tela()
        polilinha=Polilinha(pontos_para_desenhar, fechar=False); self.tela.desenhar(polilinha.saida,'#000000')
        for ponto in pontos_para_desenhar: self.tela.desenhar_pixel(ponto[0],ponto[1],"blue")

    def desenhar_circulo(self):
        """
        Desenha um círculo na tela usando o algoritmo do ponto médio.
        """
        try: centro=(int(self.get_widget('circulo', 'entry_cx').get()),int(self.get_widget('circulo', 'entry_cy').get())); raio=float(self.get_widget('circulo', 'entry_raio').get())
        except ValueError: messagebox.showerror("Entrada Inválida", "O centro deve ter coordenadas inteiras e o raio um número."); self.limpar_tudo(manter_desenho=True); return
        if raio <= 0: messagebox.showwarning("Raio Inválido", "O raio do círculo deve ser maior que zero."); self.limpar_tudo(manter_desenho=True); return
        self.tela.limpar_tela(); circulo=Circulo(centro, raio); self.tela.desenhar(circulo.saida,'#000000'); self.tela.desenhar_pixel(centro[0],centro[1],"green")

    def desenhar_elipse(self):
        """
        Desenha uma elipse na tela usando o algoritmo do ponto médio.
        """
        try: centro=(int(self.get_widget('elipse', 'entry_ex').get()),int(self.get_widget('elipse', 'entry_ey').get())); rx=float(self.get_widget('elipse', 'entry_rx').get()); ry=float(self.get_widget('elipse', 'entry_ry').get())
        except ValueError: messagebox.showerror("Entrada Inválida", "O centro deve ter coordenadas inteiras e os raios números."); self.limpar_tudo(manter_desenho=True); return
        if rx <= 0 or ry <= 0: messagebox.showwarning("Raios Inválidos", "Os raios X e Y devem ser maiores que zero."); self.limpar_tudo(manter_desenho=True); return
        self.tela.limpar_tela(); elipse=Elipse(centro, rx, ry); self.tela.desenhar(elipse.saida,'#000000'); self.tela.desenhar_pixel(centro[0],centro[1],"purple")

    def desenhar_curva(self):
        """
        Desenha uma curva de Bézier na tela.
        """
        if len(globals.pontos_selecionados) < 3: messagebox.showwarning("Pontos Insuficientes", "São necessários pelo menos 3 pontos de controle para uma curva."); return
        pontos_para_desenhar = list(globals.pontos_selecionados); self.tela.limpar_tela()
        curva = Curvas(pontos_para_desenhar); self.tela.desenhar(curva.saida, '#000000')
        for i, ponto in enumerate(pontos_para_desenhar):
            if i == 0: cor = "green"
            elif i == len(pontos_para_desenhar) - 1: cor = "red"
            else: cor = "orange"
            self.tela.desenhar_pixel(ponto[0], ponto[1], cor)

    def finalizar_poligono_para_preenchimento(self):
        """
        Finaliza a definição do polígono para preenchimento e avança para a etapa de seleção da semente.
        """
        if len(globals.pontos_selecionados) < 3: messagebox.showerror("Polígono Inválido", "São necessários pelo menos 3 pontos para formar um polígono."); return
        self.tela.limpar_tela(); globals.poligono_para_preencher = list(globals.pontos_selecionados)
        poligono_fechado = Polilinha(globals.poligono_para_preencher, fechar=True); self.tela.desenhar(poligono_fechado.saida, '#000000')
        globals.estado_preenchimento = "escolhendo_semente"; globals.pontos_selecionados.clear(); self.atualizar_texto_pontos(); self.switch_fill_state()

    def executar_preenchimento(self):
        """
        Executa o algoritmo de preenchimento recursivo (Flood Fill).
        """
        try: ponto_semente = (int(self.get_widget('preenchimento', 'entry_p_x_fill').get()), int(self.get_widget('preenchimento', 'entry_p_y_fill').get())); cor = self.get_widget('preenchimento', 'entry_cor_preenchimento').get()
        except ValueError: messagebox.showerror("Entrada Inválida", "As coordenadas do ponto de semente devem ser números inteiros."); return
        if not (cor.startswith('#') and len(cor) == 7): messagebox.showerror("Cor Inválida", "A cor deve estar no formato #RRGGBB."); return
        if not globals.poligono_para_preencher: messagebox.showwarning("Nenhum Polígono", "Primeiro, finalize um polígono para depois o preencher."); return
        if not self.ponto_esta_dentro(ponto_semente, globals.poligono_para_preencher): messagebox.showwarning("Ponto Inválido", "O ponto de semente deve estar DENTRO do polígono."); return
        self.tela.limpar_marcadores(); PreenchimentoRecursivo(ponto_semente, cor, self.tela); self.limpar_tudo(manter_desenho=True, limpar_apenas_pontos=True)

    def executar_varredura(self):
        """
        Executa o algoritmo de preenchimento por varredura (Scanline).
        """
        if len(globals.pontos_selecionados) < 3: messagebox.showwarning("Pontos Insuficientes", "São necessários pelo menos 3 pontos para preencher com varredura."); return
        pontos_para_desenhar = list(globals.pontos_selecionados); self.tela.limpar_tela()
        preenchimento = Varredura(pontos_para_desenhar); self.tela.desenhar(preenchimento.saida, "#FFA500")
        borda = Polilinha(pontos_para_desenhar, fechar=True); self.tela.desenhar(borda.saida, '#000000')

    def finalizar_janela_de_recorte(self):
        """
        Finaliza a definição da janela de recorte para o recorte de linha.
        """
        try: x_coords = [int(self.get_widget('recorte_linha', 'entry_xmin').get()), int(self.get_widget('recorte_linha', 'entry_xmax').get())]; y_coords = [int(self.get_widget('recorte_linha', 'entry_ymin').get()), int(self.get_widget('recorte_linha', 'entry_ymax').get())]
        except ValueError: messagebox.showerror("Entrada Inválida", "As coordenadas da janela devem ser números inteiros."); return
        xmin, xmax = min(x_coords), max(x_coords); ymin, ymax = min(y_coords), max(y_coords)
        globals.janela_de_recorte = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        self.tela.limpar_tela(); self.tela.destacar_janela(**globals.janela_de_recorte)
        globals.estado_recorte = "definindo_linha"; globals.pontos_selecionados.clear(); self.switch_clip_state()

    def desenhar_linha_original_para_recorte(self):
        """
        Desenha a linha original (antes do recorte) em tom de cinza para referência.
        """
        try: p1 = (int(self.get_widget('recorte_linha', 'entry_x0_recorte').get()), int(self.get_widget('recorte_linha', 'entry_y0_recorte').get())); p2 = (int(self.get_widget('recorte_linha', 'entry_x1_recorte').get()), int(self.get_widget('recorte_linha', 'entry_y1_recorte').get()))
        except ValueError: return
        linha_original = Bresenham(p1, p2); self.tela.desenhar(linha_original.saida, 'lightgrey')

    def executar_recorte_linha(self):
        """
        Executa o algoritmo de recorte de linha de Cohen-Sutherland.
        """
        if not globals.janela_de_recorte: messagebox.showwarning("Janela não Definida", "Primeiro, defina uma janela de recorte."); return
        try: p1 = (int(self.get_widget('recorte_linha', 'entry_x0_recorte').get()), int(self.get_widget('recorte_linha', 'entry_y0_recorte').get())); p2 = (int(self.get_widget('recorte_linha', 'entry_x1_recorte').get()), int(self.get_widget('recorte_linha', 'entry_y1_recorte').get()))
        except ValueError: messagebox.showerror("Entrada Inválida", "As coordenadas da linha devem ser números inteiros."); return
        self.tela.limpar_tela(); self.tela.destacar_janela(**globals.janela_de_recorte)
        recorte = RecorteLinha(p1, p2, **globals.janela_de_recorte); self.tela.desenhar(recorte.saida, '#000000')

    def finalizar_janela_para_recorte_poligono(self):
        """
        Finaliza a definição da janela de recorte para o recorte de polígono.
        """
        try:
            x_coords = [int(self.get_widget('recorte_poligono', 'entry_xmin_p').get()), int(self.get_widget('recorte_poligono', 'entry_xmax_p').get())]; y_coords = [int(self.get_widget('recorte_poligono', 'entry_ymin_p').get()), int(self.get_widget('recorte_poligono', 'entry_ymax_p').get())]
        except ValueError: messagebox.showerror("Entrada Inválida", "As coordenadas da janela devem ser números inteiros."); return
        xmin, xmax = min(x_coords), max(x_coords); ymin, ymax = min(y_coords), max(y_coords)
        globals.janela_de_recorte = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        self.tela.limpar_tela(); self.tela.destacar_janela(**globals.janela_de_recorte)
        globals.estado_recorte = "definindo_poligono"; globals.pontos_selecionados.clear(); self.atualizar_texto_pontos(); self.switch_clip_state()

    def desenhar_poligono_original_para_recorte(self):
        """
        Desenha o polígono original (antes do recorte) em tom de cinza.
        """
        self.tela.limpar_tela()
        self.tela.destacar_janela(**globals.janela_de_recorte)
        if len(globals.pontos_selecionados) >= 2:
            polilinha_original = Polilinha(globals.pontos_selecionados, fechar=True)
            self.tela.desenhar(polilinha_original.saida, 'lightgrey')
        for ponto in globals.pontos_selecionados:
            self.tela.desenhar_pixel(ponto[0], ponto[1], "blue")

    def executar_recorte_poligono(self):
        """
        Executa o algoritmo de recorte de polígono de Sutherland-Hodgman.
        """
        if not globals.janela_de_recorte: messagebox.showwarning("Janela não Definida", "Primeiro, defina uma janela de recorte."); return
        if len(globals.pontos_selecionados) < 3: messagebox.showwarning("Pontos Insuficientes", "São necessários pelo menos 3 pontos para um polígono."); return
        self.tela.limpar_tela(); self.tela.destacar_janela(**globals.janela_de_recorte)
        recorte = RecortePoligono(globals.pontos_selecionados, **globals.janela_de_recorte); self.tela.desenhar(recorte.saida, '#000000')

    def limpar_tudo(self, manter_desenho=False, limpar_apenas_pontos=False):
        """
        Limpa a tela, os campos de entrada e reinicializa as variáveis de estado.

        Args:
            manter_desenho (bool): Se True, não limpa o conteúdo do canvas.
            limpar_apenas_pontos (bool): Se True, limpa apenas a lista de pontos selecionados.
        """
        self.tela.limpar_marcadores()
        if not limpar_apenas_pontos:
            for mode_widgets in self.widgets.values():
                for widget in mode_widgets.values():
                    if isinstance(widget, tk.Entry):
                        widget.delete(0, tk.END)
                    elif isinstance(widget, tk.Text):
                        widget.config(state=tk.NORMAL)
                        widget.delete('1.0', tk.END)
                        widget.config(state=tk.DISABLED)
                    elif isinstance(widget, ttk.Combobox):
                        widget.set('')
                        widget['values'] = []
        
        globals.init()

        if self.current_mode.get() == "transformacao": self.switch_transform_state()
        if self.current_mode.get() == "projecao": self.switch_projection_state()

        if not manter_desenho:
            self.tela.limpar_tela()

    def atualizar_texto_pontos(self):
        """
        Atualiza a caixa de texto que exibe os pontos selecionados para o modo atual.
        """
        modo = self.current_mode.get()
        widgets_map = {
            "polilinha": "texto_pontos_polilinha", "curva": "texto_pontos_curva",
            "varredura": "texto_pontos_varredura", "preenchimento": "texto_pontos_preenchimento",
            "recorte_poligono": "texto_pontos_recorte_p", "transformacao": "texto_pontos_transformacao"
        }
        if modo in widgets_map:
            widget = self.get_widget(modo, widgets_map[modo])
            widget.config(state=tk.NORMAL)
            widget.delete('1.0', tk.END)

            pontos_a_exibir = globals.pontos_selecionados if modo != "transformacao" or globals.estado_transformacao == "definindo_poligono" else globals.poligono_para_transformar
            pontos_formatados = [[round(p[0]), round(p[1])] for p in pontos_a_exibir]

            for ponto in pontos_formatados:
                widget.insert(tk.END, f"({ponto[0]}, {ponto[1]})\n")
            widget.config(state=tk.DISABLED)

        if modo == "transformacao":
            combo_pivo_escalonamento = self.get_widget('transformacao', 'combo_pivo_escalonamento')
            combo_pivo_rotacao = self.get_widget('transformacao', 'combo_pivo_rotacao')

            formatted_points = [f"({int(p[0])}, {int(p[1])})" for p in globals.poligono_para_transformar]
            combo_pivo_escalonamento['values'] = formatted_points
            combo_pivo_rotacao['values'] = formatted_points
            if formatted_points:
                combo_pivo_escalonamento.current(0)
                combo_pivo_rotacao.current(0)
            else:
                combo_pivo_escalonamento.set('')
                combo_pivo_rotacao.set('')

    def switch_mode(self):
        """
        Alterna entre os diferentes modos de desenho, exibindo o painel de controle correto.
        """
        globals.init()
        self.limpar_tudo(manter_desenho=False)
        modo = self.current_mode.get()

        for frame in self.frames.values():
            frame.pack_forget()

        if modo in self.frames:
            frame_ativo = self.frames[modo]
            frame_ativo.pack(pady=10, padx=10, fill="x", anchor='n')

            if modo == "preenchimento": self.switch_fill_state()
            elif modo in ["recorte_linha", "recorte_poligono"]: self.switch_clip_state()
            elif modo == "transformacao": self.switch_transform_state()
            elif modo == "projecao": self.switch_projection_state()

    def switch_fill_state(self):
        """
        Alterna a visibilidade dos sub-frames no modo de preenchimento.
        """
        if globals.estado_preenchimento == "desenhando_poligono":
            self.get_widget('preenchimento', 'frame_desenho_poligono').pack(fill="x")
            self.get_widget('preenchimento', 'frame_escolha_semente').pack_forget()
        else:
            self.get_widget('preenchimento', 'frame_desenho_poligono').pack_forget()
            self.get_widget('preenchimento', 'frame_escolha_semente').pack(fill="x")

    def switch_clip_state(self):
        """
        Alterna a visibilidade dos sub-frames nos modos de recorte.
        """
        modo = self.current_mode.get()
        if modo == "recorte_linha":
            if globals.estado_recorte == "definindo_janela":
                self.get_widget('recorte_linha', 'frame_definir_janela').pack(fill="x")
                self.get_widget('recorte_linha', 'frame_definir_linha').pack_forget()
            else:
                self.get_widget('recorte_linha', 'frame_definir_janela').pack_forget()
                self.get_widget('recorte_linha', 'frame_definir_linha').pack(fill="x")
        elif modo == "recorte_poligono":
            if globals.estado_recorte == "definindo_janela":
                self.get_widget('recorte_poligono', 'frame_definir_janela_p').pack(fill="x")
                self.get_widget('recorte_poligono', 'frame_definir_poligono').pack_forget()
            else:
                self.get_widget('recorte_poligono', 'frame_definir_janela_p').pack_forget()
                self.get_widget('recorte_poligono', 'frame_definir_poligono').pack(fill="x")

    def switch_transform_state(self):
        """
        Alterna a visibilidade dos sub-frames no modo de transformação.
        """
        if globals.estado_transformacao == "definindo_poligono":
            self.get_widget('transformacao', 'frame_add_ponto_transf').pack(fill="x")
            self.get_widget('transformacao', 'frame_opcoes_transf').pack_forget()
        else:
            self.get_widget('transformacao', 'frame_add_ponto_transf').pack_forget()
            self.get_widget('transformacao', 'frame_opcoes_transf').pack(fill="x")

    def switch_projection_state(self):
        """
        Alterna a visibilidade dos sub-frames no modo de projeção 3D.
        """
        if globals.estado_projecao == "definindo_vertices":
            self.get_widget('projecao', 'frame_definir_vertices_3d').pack(fill='x')
            self.get_widget('projecao', 'frame_definir_arestas_3d').pack_forget()
        else:
            self.get_widget('projecao', 'frame_definir_vertices_3d').pack_forget()
            self.get_widget('projecao', 'frame_definir_arestas_3d').pack(fill='x')

    def add_vertice_3d(self):
        """
        Adiciona um vértice 3D à lista de vértices.
        """
        try:
            x = int(self.get_widget('projecao', 'entry_vertice_x').get())
            y = int(self.get_widget('projecao', 'entry_vertice_y').get())
            z = int(self.get_widget('projecao', 'entry_vertice_z').get())
            globals.vertices_3d_selecionados.append([x, y, z])

            texto_vertices_3d = self.get_widget('projecao', 'texto_vertices_3d')
            texto_vertices_3d.config(state=tk.NORMAL)
            texto_vertices_3d.delete('1.0', tk.END)
            for i, v in enumerate(globals.vertices_3d_selecionados):
                texto_vertices_3d.insert(tk.END, f"V{i}: ({v[0]}, {v[1]}, {v[2]})\n")
            texto_vertices_3d.config(state=tk.DISABLED)

            self.get_widget('projecao', 'entry_vertice_x').delete(0, tk.END)
            self.get_widget('projecao', 'entry_vertice_y').delete(0, tk.END)
            self.get_widget('projecao', 'entry_vertice_z').delete(0, tk.END)
            self.get_widget('projecao', 'entry_vertice_x').focus_set()

        except ValueError:
            messagebox.showerror("Entrada Inválida", "Coordenadas X, Y e Z devem ser inteiras.")

    def finalizar_vertices_3d(self):
        """
        Finaliza a definição de vértices e avança para a definição de arestas.
        """
        if len(globals.vertices_3d_selecionados) < 2:
            messagebox.showwarning("Vértices Insuficientes", "Adicione pelo menos 2 vértices.")
            return
        globals.estado_projecao = "definindo_arestas"

        opcoes_vertices = [f"V{i}: ({v[0]}, {v[1]}, {v[2]})" for i, v in enumerate(globals.vertices_3d_selecionados)]
        combo_aresta_de = self.get_widget('projecao', 'combo_aresta_de')
        combo_aresta_para = self.get_widget('projecao', 'combo_aresta_para')
        combo_aresta_de['values'] = opcoes_vertices
        combo_aresta_para['values'] = opcoes_vertices
        combo_aresta_de.current(0)
        combo_aresta_para.current(1 if len(opcoes_vertices) > 1 else 0)

        self.switch_projection_state()

    def add_aresta_3d(self):
        """
        Adiciona uma aresta entre dois vértices 3D selecionados.
        """
        de_str = self.get_widget('projecao', 'combo_aresta_de').get()
        para_str = self.get_widget('projecao', 'combo_aresta_para').get()

        if not de_str or not para_str:
            messagebox.showerror("Seleção Inválida", "Selecione um vértice de origem e um de destino.")
            return

        try:
            idx_de = int(de_str.split(':')[0].replace('V', ''))
            idx_para = int(para_str.split(':')[0].replace('V', ''))

            if idx_de == idx_para:
                messagebox.showwarning("Aresta Inválida", "Uma aresta não pode conectar um vértice a ele mesmo.")
                return

            aresta = sorted([idx_de, idx_para])
            if aresta not in globals.arestas_3d_selecionadas:
                globals.arestas_3d_selecionadas.append(aresta)
                
                texto_arestas_3d = self.get_widget('projecao', 'texto_arestas_3d')
                texto_arestas_3d.config(state=tk.NORMAL)
                texto_arestas_3d.delete('1.0', tk.END)
                for a in globals.arestas_3d_selecionadas:
                    texto_arestas_3d.insert(tk.END, f"Aresta: (V{a[0]} -- V{a[1]})\n")
                texto_arestas_3d.config(state=tk.DISABLED)
            else:
                messagebox.showinfo("Aresta Duplicada", "Essa aresta já foi adicionada.")

        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Não foi possível adicionar a aresta.")

    def executar_projecao(self):
        """
        Executa a projeção 3D selecionada e desenha o resultado na tela.
        """
        tipo_projecao = self.get_widget('projecao', 'combo_tipo_projecao').get()
        if not tipo_projecao:
            messagebox.showerror("Seleção Inválida", "Por favor, selecione um tipo de projeção.")
            return

        projetor = Projetor3D(globals.vertices_3d_selecionados, globals.arestas_3d_selecionadas)

        if tipo_projecao == "Ortogonal":
            vertices_2d = projetor.projetar_ortogonal()
        elif tipo_projecao == "Cavalier":
            vertices_2d = projetor.projetar_cavalier()
        elif tipo_projecao == "Cabinet":
            vertices_2d = projetor.projetar_cabinet()
        elif tipo_projecao == "Perspectiva":
            try:
                distancia = float(self.get_widget('projecao', 'entry_distancia_proj').get())
                if distancia <= 0:
                    messagebox.showerror("Valor Inválido", "A distância da câmera deve ser maior que zero.")
                    return
                vertices_2d = projetor.projetar_perspectiva(distancia)
            except ValueError:
                messagebox.showerror("Entrada Inválida", "A distância da câmera deve ser um número.")
                return

        projetor.rasterizar_arestas(vertices_2d)
        self.tela.limpar_tela()
        self.tela.desenhar(projetor.saida, 'black')

    def toggle_distancia_camera(self, event=None):
        """
        Mostra ou esconde o campo de entrada para a distância da câmera,
        dependendo se a projeção perspectiva está selecionada.
        """
        label_distancia_proj = self.get_widget('projecao', 'label_distancia_proj')
        entry_distancia_proj = self.get_widget('projecao', 'entry_distancia_proj')
        btn_projetar_objeto = self.get_widget('projecao', 'btn_projetar_objeto')
        
        label_distancia_proj.pack_forget()
        entry_distancia_proj.pack_forget()
        btn_projetar_objeto.pack_forget()

        if self.get_widget('projecao', 'combo_tipo_projecao').get() == "Perspectiva":
            label_distancia_proj.pack()
            entry_distancia_proj.pack(pady=5)

        btn_projetar_objeto.pack(pady=10, fill="x", ipady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()