import pygame
import numpy as np
import sys
import os
from dig_simulator import simular_universo_dig

class DIGPygameUI:
    def __init__(self, width=1000, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("DIG Simulator - Pygame UI")
        
        # Fuentes modernas y limpias
        self.font_small = pygame.font.SysFont('Segoe UI', 13)
        self.font = pygame.font.SysFont('Segoe UI', 17)
        self.font_large = pygame.font.SysFont('Segoe UI', 22, bold=True)
        
        # Tamaños de los paneles
        self.sim_width = int(self.width * 0.7)
        self.metrics_width = self.width - self.sim_width
        
        # Parámetros de la simulación
        self.resolution = 100  # Tamaño de la cuadrícula
        self.rho_c = 1.0      # Densidad central
        self.Rs = 20.0        # Radio característico
        self.k_c2 = 1.0       # Constante de proporcionalidad
        self.delta_q = 0.1    # Parámetro cuántico
        self.num_frames = 120  # Número de frames
        
        # Estado de la simulación
        self.simulation_data = None
        self.is_playing = True  # Reproducir automáticamente
        self.current_frame = 0
        self.fps = 30
        self.clock = pygame.time.Clock()
        self.last_update = 0  # Para controlar la velocidad de actualización
        
        # Tema oscuro moderno
        self.BG_COLOR = (28, 32, 38)    # Fondo principal oscuro
        self.TEXT_COLOR = (230, 230, 235)  # Texto claro
        self.ACCENT_COLOR = (0, 200, 140)  # Verde acento
        self.SECONDARY_COLOR = (100, 180, 255)  # Azul claro
        self.PANEL_BG = (36, 41, 48)    # Fondo panel oscuro
        self.PANEL_BORDER = (44, 50, 60) # Borde panel
        self.PROGRESS_BG = (44, 50, 60) # Fondo barra progreso
        self.PROGRESS_FG = (0, 200, 140)  # Verde acento
        self.CARD_BG = (38, 43, 52)     # Fondo tarjetas
        self.CARD_BORDER = (52, 58, 70)  # Borde tarjetas
        self.BUTTON_COLOR = (44, 50, 60) # Botón normal
        self.BUTTON_HOVER = (0, 200, 140) # Botón hover (acento)
        self.BUTTON_TEXT = (230, 230, 235)
        self.SHADOW_COLOR = (20, 22, 26, 120) # Sombra sutil

        # Iniciar la simulación
        self.run_simulation()
    
    def run_simulation(self):
        print(f"Ejecutando simulación DIG con {self.num_frames} frames...")
        # Generar la simulación con múltiples frames
        simulation = simular_universo_dig(
            resolucion=self.resolution,
            rho_c=self.rho_c,
            Rs=self.Rs,
            k_c2=self.k_c2,
            delta_q=self.delta_q,
            num_frames=220
        )
        
        # Normalizar cada frame individualmente
        normalized_frames = []
        for i in range(simulation.shape[0]):
            frame = simulation[i]
            if np.max(frame) > np.min(frame):
                frame = (frame - np.min(frame)) / (np.max(frame) - np.min(frame))
            else:
                frame = np.zeros_like(frame)
            normalized_frames.append(frame)
        
        self.simulation_data = np.array(normalized_frames)
        self.current_frame = 0
        print(f"Simulación completada. Forma de los datos: {self.simulation_data.shape}")
        print(f"Duración: {len(self.simulation_data)/self.fps:.2f} segundos")
    
    def draw_metrics_panel(self):
        """Dibuja el panel lateral con las métricas de la simulación"""
        # Fondo del panel con sombra suave
        panel_rect = pygame.Rect(self.sim_width, 0, self.metrics_width, self.height)
        pygame.draw.rect(self.screen, self.PANEL_BG, panel_rect, border_radius=18)
        # Sombra lateral
        shadow_rect = pygame.Rect(self.sim_width-8, 0, 16, self.height)
        shadow = pygame.Surface((16, self.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow, self.SHADOW_COLOR, shadow.get_rect())
        self.screen.blit(shadow, (self.sim_width-8, 0))

        # Encabezado del panel
        header_rect = pygame.Rect(self.sim_width, 0, self.metrics_width, 70)
        pygame.draw.rect(self.screen, self.CARD_BG, header_rect, border_radius=18)
        pygame.draw.rect(self.screen, self.ACCENT_COLOR, 
                        (self.sim_width, 0, self.metrics_width, 5), border_radius=3)
        
        # Título del panel con icono
        title = self.font_large.render("📊 Métricas de Simulación", True, self.TEXT_COLOR)
        title_rect = title.get_rect(topleft=(self.sim_width + 24, 22))
        self.screen.blit(title, title_rect)
        
        if self.simulation_data is None or len(self.simulation_data) == 0:
            return
            
        frame = self.simulation_data[min(self.current_frame, len(self.simulation_data) - 1)]
        
        # Calcular métricas
        metrics = [
            ("Frame Actual", f"{self.current_frame + 1}/{len(self.simulation_data)}"),
            ("Tiempo", f"{self.current_frame/self.fps:.2f}s / {len(self.simulation_data)/self.fps:.2f}s"),
            ("FPS", f"{int(self.clock.get_fps())}"),
            ("Resolución", f"{frame.shape[1]}x{frame.shape[0]} píxeles"),
            ("Valor Mínimo", f"{np.min(frame):.4f}"),
            ("Valor Máximo", f"{np.max(frame):.4f}"),
            ("Valor Medio", f"{np.mean(frame):.4f}"),
            ("Desv. Estándar", f"{np.std(frame):.4f}" if frame.size > 1 else "N/A")
        ]
        
        # Dibujar métricas en tarjetas modernas
        y_offset = 90
        card_width = self.metrics_width - 44
        for label, value in metrics:
            card_rect = pygame.Rect(self.sim_width + 22, y_offset, card_width, 48)
            # Sombra sutil
            shadow_rect = card_rect.move(2, 3)
            shadow = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(shadow, self.SHADOW_COLOR, shadow.get_rect(), border_radius=12)
            self.screen.blit(shadow, shadow_rect.topleft)
            # Tarjeta
            pygame.draw.rect(self.screen, self.CARD_BG, card_rect, border_radius=12)
            pygame.draw.rect(self.screen, self.CARD_BORDER, card_rect, 1, border_radius=12)
            # Etiqueta
            label_surface = self.font_small.render(label.upper(), True, (140, 160, 200))
            self.screen.blit(label_surface, (card_rect.x + 18, card_rect.y + 7))
            # Valor
            value_surface = self.font.render(str(value), True, self.SECONDARY_COLOR)
            value_rect = value_surface.get_rect(
                bottomright=(card_rect.right - 18, card_rect.bottom - 8)
            )
            self.screen.blit(value_surface, value_rect)
            y_offset += 58

        # Parámetros de la simulación
        params_title = self.font_large.render("⚙️ Parámetros", True, self.TEXT_COLOR)
        self.screen.blit(params_title, (self.sim_width + 24, y_offset + 18))
        params = [
            ("Resolución", self.resolution),
            ("Densidad Central", self.rho_c),
            ("Radio Característico", self.Rs),
            ("Constante k_c2", self.k_c2),
            ("Delta Cuántico", self.delta_q),
            ("Núm. Frames", self.num_frames)
        ]
        y_offset += 54
        for label, value in params:
            param_text = f"{label}: {value}"
            param_surface = self.font_small.render(param_text, True, self.TEXT_COLOR)
            self.screen.blit(param_surface, (self.sim_width + 24, y_offset))
            y_offset += 24

    def save_frame(self):
        """Guarda el frame actual como una imagen PNG"""
        if self.simulation_data is not None:
            try:
                frame = self.simulation_data[min(self.current_frame, len(self.simulation_data) - 1)]
                os.makedirs("exports", exist_ok=True)
                import matplotlib.pyplot as plt
                
                # Crear una figura con fondo blanco
                plt.figure(figsize=(8, 8), facecolor='white')
                plt.imshow(frame, cmap='viridis')
                plt.axis('off')
                
                # Añadir información de metadatos
                plt.title(f"DIG Simulation - Frame {self.current_frame}", color='black')
                
                # Guardar con alta calidad
                filename = f"exports/dig_frame_{self.current_frame:04d}.png"
                plt.savefig(filename, bbox_inches='tight', pad_inches=0.1, dpi=150, facecolor='white')
                plt.close()
                
                print(f"Frame {self.current_frame} guardado como {filename}")
                
            except Exception as e:
                print(f"Error al guardar el frame: {e}")
    
    def export_animation(self, output_dir="exports/animation_frames", format="png"):
        """
        Exporta la animación como una secuencia de imágenes o un video MP4.
        
        Args:
            output_dir (str): Directorio de salida para los frames
            format (str): Formato de salida ('png', 'jpg' o 'mp4')
            
        Returns:
            str: Ruta al archivo o directorio exportado
        """
        if self.simulation_data is None:
            print("No hay datos de simulación para exportar.")
            return
            
        import os
        import numpy as np
        from PIL import Image
        
        os.makedirs(output_dir, exist_ok=True)
        total_frames = len(self.simulation_data)
        
        # Si es MP4, usamos OpenCV
        if format.lower() == 'mp4':
            try:
                import cv2
                
                # Configuración del video
                fps = self.fps
                frame_size = (self.simulation_data[0].shape[1], self.simulation_data[0].shape[0])
                output_file = os.path.join(output_dir, "animacion_dig.mp4")
                
                # Crear el objeto VideoWriter
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_file, fourcc, fps, frame_size, isColor=True)
                
                print(f"Exportando video MP4 a {output_file}...")
                
                for i, frame in enumerate(self.simulation_data):
                    # Normalizar a 0-255 y convertir a BGR para OpenCV
                    normalized = ((frame - frame.min()) * (1/(frame.max() - frame.min()) * 255)).astype('uint8')
                    color_frame = cv2.applyColorMap(normalized, cv2.COLORMAP_VIRIDIS)
                    
                    # Escribir frame en el video
                    out.write(color_frame)
                    
                    # Mostrar progreso
                    if (i + 1) % 10 == 0 or (i + 1) == total_frames:
                        print(f"  Frame {i+1}/{total_frames} procesado")
                
                out.release()
                print(f"¡Exportación completada! Video guardado en {output_file}")
                return output_file
                
            except ImportError:
                print("OpenCV no está instalado. Exportando como secuencia de imágenes...")
                format = 'png'  # Revertir a PNG si no hay OpenCV
        
        # Exportar como secuencia de imágenes
        print(f"Exportando {total_frames} frames a {output_dir}/...")
        
        for i, frame in enumerate(self.simulation_data):
            # Normalizar a 0-255
            normalized = ((frame - frame.min()) * (1/(frame.max() - frame.min()) * 255)).astype('uint8')
            img = Image.fromarray(normalized)
            
            # Aplicar mapa de colores personalizado
            if format.lower() == 'png':
                img = img.convert('L').convert('P')
                # Paleta de colores: negro, azul, cian, verde, amarillo, rojo
                img.putpalette([
                    0, 0, 0,    0, 0, 255,    0, 255, 255,
                    0, 255, 0,  255, 255, 0,   255, 0, 0
                ] * 42)
            
            # Guardar frame
            filename = os.path.join(output_dir, f"frame_{i:04d}.{format}")
            img.save(filename)
            
            # Mostrar progreso
            if (i + 1) % 10 == 0 or (i + 1) == total_frames:
                print(f"  Frame {i+1}/{total_frames} exportado")
                
        print(f"¡Exportación completada! {total_frames} frames guardados en {output_dir}")
        return os.path.abspath(output_dir)
    
    def draw_simulation(self):
        # Fondo principal
        self.screen.fill(self.BG_COLOR)
        
        if self.simulation_data is None or len(self.simulation_data) == 0:
            # Mostrar un mensaje si no hay datos
            text = self.font.render("No hay datos de simulación", True, self.TEXT_COLOR)
            self.screen.blit(text, (self.sim_width//2 - 100, self.height//2 - 10))
            return
            
        # Asegurarnos de que el frame actual sea válido
        frame_idx = min(self.current_frame, len(self.simulation_data) - 1)
        frame = self.simulation_data[frame_idx]
        
        # Asegurarnos de que el frame sea 2D
        if len(frame.shape) > 2:
            frame = frame[..., 0]
            
        # Calcular el tamaño de celda y las compensaciones para centrar
        height, width = frame.shape
        cell_size = min(self.sim_width // width, self.height // height)
        offset_x = (self.sim_width - width * cell_size) // 2
        offset_y = (self.height - height * cell_size) // 2 - 20  # Ajuste para el texto
        
        # Dibujar la simulación
        for y in range(height):
            for x in range(width):
                value = int(frame[y, x] * 255)
                # Usar un gradiente de azul a blanco para mejor visibilidad
                color = (value//2, value//2, 255)  # Azul a blanco
                rect = pygame.Rect(offset_x + x * cell_size, 
                                 offset_y + y * cell_size, 
                                 cell_size, cell_size)
                pygame.draw.rect(self.screen, color, rect, border_radius=2)
        
        # Barra de progreso moderna
        progress = (frame_idx + 1) / len(self.simulation_data)
        progress_bar_rect = pygame.Rect(50, self.height - 50, self.sim_width - 100, 18)
        pygame.draw.rect(self.screen, self.PROGRESS_BG, progress_bar_rect, border_radius=9)
        if progress > 0:
            filled_rect = pygame.Rect(50, self.height - 50, 
                                    int((self.sim_width - 100) * progress), 18)
            pygame.draw.rect(self.screen, self.PROGRESS_FG, filled_rect, border_radius=9)
        pygame.draw.rect(self.screen, self.PANEL_BORDER, progress_bar_rect, 1, border_radius=9)
        
        # Indicador de tiempo
        time_text = f"⏱ {frame_idx/self.fps:.1f}s / {len(self.simulation_data)/self.fps:.1f}s"
        time_surface = self.font_small.render(time_text, True, self.TEXT_COLOR)
        time_rect = time_surface.get_rect(center=(self.sim_width // 2, self.height - 41))
        self.screen.blit(time_surface, time_rect)
        
        # Barra de información superior moderna
        info_bg_rect = pygame.Rect(0, 0, self.sim_width, 44)
        pygame.draw.rect(self.screen, self.PANEL_BG, info_bg_rect, border_radius=0)
        pygame.draw.line(self.screen, self.PANEL_BORDER, (0, 44), (self.sim_width, 44), 1)
        info_items = [
            (f"🖼 Frame: {frame_idx+1}/{len(self.simulation_data)}", (16, 12)),
            (f"⏲ Tiempo: {frame_idx/self.fps:.1f}s", (180, 12)),
            (f"🎞 FPS: {int(self.clock.get_fps())}", (340, 12)),
            (f"📐 Resolución: {width}x{height}", (480, 12))
        ]
        for text, pos in info_items:
            text_surface = self.font.render(text, True, self.TEXT_COLOR)
            bg_rect = pygame.Rect(pos[0]-4, pos[1], text_surface.get_width()+8, 24)
            pygame.draw.rect(self.screen, self.CARD_BG, bg_rect, border_radius=6)
            pygame.draw.rect(self.screen, self.CARD_BORDER, bg_rect, 1, border_radius=6)
            self.screen.blit(text_surface, pos)
        
        # Barra de controles inferiores moderna
        controls_bg_rect = pygame.Rect(0, self.height - 80, self.sim_width, 80)
        pygame.draw.rect(self.screen, self.PANEL_BG, controls_bg_rect, border_radius=0)
        pygame.draw.line(self.screen, self.PANEL_BORDER, 
                        (0, self.height - 80), (self.sim_width, self.height - 80), 1)
        controls = [
            ("⏯ [ESPACIO]", "Play/Pause"),
            ("⬅ [←] [→] ➡", "Navegar"),
            ("🔄 [R]", "Reiniciar"),
            ("💾 [S]", "Guardar Frame"),
            ("⏹ [ESC]", "Salir")
        ]
        start_x = 24
        for key, desc in controls:
            key_bg = pygame.Rect(start_x, self.height - 70, 90, 26)
            pygame.draw.rect(self.screen, self.CARD_BG, key_bg, border_radius=7)
            pygame.draw.rect(self.screen, self.ACCENT_COLOR, key_bg, 1, border_radius=7)
            key_surface = self.font.render(key, True, self.ACCENT_COLOR)
            key_rect = key_surface.get_rect(center=key_bg.center)
            self.screen.blit(key_surface, key_rect)
            desc_surface = self.font_small.render(desc, True, self.TEXT_COLOR)
            self.screen.blit(desc_surface, (start_x, self.height - 40))
            start_x += 130

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Manejo de teclado
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.is_playing = not self.is_playing
                    elif event.key == pygame.K_r:
                        self.run_simulation()
                    elif event.key == pygame.K_s:
                        self.save_frame()
                    # Navegación con flechas
                    elif event.key == pygame.K_LEFT:
                        self.current_frame = max(0, self.current_frame - 1)
                        self.is_playing = False
                    elif event.key == pygame.K_RIGHT and self.simulation_data is not None:
                        self.current_frame = min(len(self.simulation_data) - 1, self.current_frame + 1)
                        self.is_playing = False
                
                # Manejo de clics del ratón
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    
                    # Verificar si se hizo clic en la barra de progreso
                    if (50 <= mouse_y <= 70 and 
                        50 <= mouse_x <= self.sim_width - 50 and
                        self.simulation_data is not None):
                        progress = (mouse_x - 50) / (self.sim_width - 100)
                        self.current_frame = int(progress * (len(self.simulation_data) - 1))
                        self.is_playing = False
                    
                    # Verificar si se hizo clic en el botón de exportar
                    export_rect = pygame.Rect(self.sim_width - 170, self.height - 54, 150, 36)
                    if export_rect.collidepoint(mouse_x, mouse_y):
                        print("\n=== Iniciando exportación de la animación ===")
                        export_path = self.export_animation(format='mp4')
                        if export_path:
                            print(f"=== Exportación completada exitosamente ===\n")
                            print(f"Archivo guardado en: {export_path}")
                        else:
                            print("=== Error durante la exportación ===\n")
            
            # Actualizar lógica de la simulación
            if self.is_playing and self.simulation_data is not None:
                if current_time - self.last_update > 1000 / self.fps:
                    self.current_frame = (self.current_frame + 1) % len(self.simulation_data)
                    self.last_update = current_time
            
            # Dibujar
            self.screen.fill(self.BG_COLOR)  # Limpiar pantalla con color de fondo
            self.draw_simulation()
            self.draw_metrics_panel()  # Dibujar el panel de métricas
            
            # Barra de estado en la parte inferior
            if self.simulation_data is not None:
                # Fondo de la barra de estado
                pygame.draw.rect(self.screen, self.PROGRESS_BG, 
                              (0, self.height - 60, self.sim_width, 60), border_radius=0)
                # Botón de exportar moderno
                export_rect = pygame.Rect(self.sim_width - 170, self.height - 54, 150, 36)
                mouse_pos = pygame.mouse.get_pos()
                is_hovered = export_rect.collidepoint(mouse_pos)
                pygame.draw.rect(self.screen, 
                              self.BUTTON_HOVER if is_hovered else self.BUTTON_COLOR, 
                              export_rect, 
                              border_radius=8)
                pygame.draw.rect(self.screen, self.ACCENT_COLOR, export_rect, 2, border_radius=8)
                # Icono y texto del botón
                export_text = self.font.render("⬇ Exportar Animación", True, self.BUTTON_TEXT if not is_hovered else self.BG_COLOR)
                text_rect = export_text.get_rect(center=export_rect.center)
                self.screen.blit(export_text, text_rect)
                # Barra de progreso
                progress = (self.current_frame + 1) / len(self.simulation_data)
                pygame.draw.rect(self.screen, (60, 70, 80), 
                              (50, self.height - 38, self.sim_width - 100, 12), 1, border_radius=6)
                pygame.draw.rect(self.screen, self.PROGRESS_FG, 
                              (50, self.height - 38, int((self.sim_width - 100) * progress), 12), border_radius=6)
                # Estado de reproducción
                status = "⏸ PAUSA" if not self.is_playing else "▶ REPRODUCIENDO"
                status_surface = self.font.render(status, True, self.TEXT_COLOR)
                status_rect = status_surface.get_rect(topleft=(24, self.height - 53))
                pygame.draw.rect(self.screen, (38, 43, 52), 
                              (status_rect.x - 10, status_rect.y - 5, 
                               status_rect.width + 20, status_rect.height + 10), 
                              border_radius=7)
                pygame.draw.rect(self.screen, self.ACCENT_COLOR, 
                              (status_rect.x - 10, status_rect.y - 5, 
                               status_rect.width + 20, status_rect.height + 10), 
                              2, border_radius=7)
                self.screen.blit(status_surface, (status_rect.x, status_rect.y))
                # Tiempo actual/total
                time_text = f"⏱ {self.current_frame/self.fps:.1f}s / {len(self.simulation_data)/self.fps:.1f}s"
                time_surface = self.font.render(time_text, True, self.TEXT_COLOR)
                time_rect = time_surface.get_rect(topright=(self.sim_width - 24, self.height - 53))
                self.screen.blit(time_surface, time_rect)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    app = DIGPygameUI()
    app.run()

