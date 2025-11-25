"""
splash_screen.py - Pantalla de Carga Inicial
Ventana de splash con diseño profesional y animación de progreso
Versión 3.0 - Inicialización real en background
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon
from config.paths import AppPaths


class SplashScreen(QWidget):
    """Ventana de splash screen con barra de progreso"""
    
    # Señal emitida cuando la carga está completa
    loading_complete = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(500, 350)
        
        # Centrar en pantalla
        self.center_on_screen()
        
        # Crear UI
        self.setup_ui()
        
        # Variables para inicialización real
        self.initialization_tasks = []
        self.current_task = 0
        self.progress_value = 0
        
    def setup_ui(self):
        """Configura la interfaz del splash screen"""
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Contenedor principal con estilo
        container = QWidget()
        container.setObjectName("splashContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)
        
        # Logo/Icono (opcional - puedes agregar una imagen aquí)
        try:
            icon_label = QLabel()
            icon_path = AppPaths.get_icon_path()
            pixmap = QPixmap(str(icon_path))
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label.setPixmap(scaled_pixmap)
                icon_label.setAlignment(Qt.AlignCenter)
                container_layout.addWidget(icon_label)
        except Exception:
            pass  # Si no hay icono, continuar sin él
        
        # Título
        title = QLabel("ETL + Certificados")
        title.setObjectName("splashTitle")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        container_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Sistema de Procesamiento y Generación")
        subtitle.setObjectName("splashSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        subtitle.setFont(subtitle_font)
        container_layout.addWidget(subtitle)
        
        # Espaciador
        container_layout.addSpacing(30)
        
        # Mensaje de estado
        self.status_label = QLabel("Iniciando aplicación...")
        self.status_label.setObjectName("splashStatus")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_font = QFont()
        status_font.setPointSize(10)
        self.status_label.setFont(status_font)
        container_layout.addWidget(self.status_label)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("splashProgress")
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(8)
        container_layout.addWidget(self.progress_bar)
        
        # Versión/Footer
        footer = QLabel("v1.0 | Ricardo Uculmana Quispe")
        footer.setObjectName("splashFooter")
        footer.setAlignment(Qt.AlignCenter)
        footer_font = QFont()
        footer_font.setPointSize(8)
        footer.setFont(footer_font)
        container_layout.addWidget(footer)
        
        layout.addWidget(container)
        
        # Aplicar estilos
        self.apply_styles()
    
    def apply_styles(self):
        """Aplica los estilos CSS al splash screen"""
        self.setStyleSheet("""
            #splashContainer {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f172a,
                    stop:1 #1e293b
                );
                border-radius: 16px;
                border: 2px solid #334155;
            }
            
            #splashTitle {
                color: #ffffff;
                font-weight: bold;
            }
            
            #splashSubtitle {
                color: #94a3b8;
            }
            
            #splashStatus {
                color: #cbd5e1;
                font-style: italic;
            }
            
            #splashProgress {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 4px;
            }
            
            #splashProgress::chunk {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0ea5e9,
                    stop:0.5 #06b6d4,
                    stop:1 #14b8a6
                );
                border-radius: 3px;
            }
            
            #splashFooter {
                color: #64748b;
            }
        """)
    
    def center_on_screen(self):
        """Centra la ventana en la pantalla"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def start_loading(self):
        """Inicia la carga real de la aplicación"""
        # Definir tareas de inicialización
        self.initialization_tasks = [
            ("Verificando estructura de directorios...", self.task_ensure_directories),
            ("Cargando configuración del sistema...", self.task_load_configuration),
            ("Inicializando componentes de interfaz...", self.task_init_components),
            ("Preparando módulos ETL...", self.task_prepare_etl),
            ("Configurando módulo de certificados...", self.task_prepare_certificates),
            ("Finalizando carga...", self.task_finalize)
        ]
        
        # Iniciar primera tarea
        self.current_task = 0
        QTimer.singleShot(100, self.execute_next_task)
    
    def execute_next_task(self):
        """Ejecuta la siguiente tarea de inicialización"""
        if self.current_task >= len(self.initialization_tasks):
            # Todas las tareas completadas
            self.finish_loading()
            return
        
        # Obtener tarea actual
        message, task_function = self.initialization_tasks[self.current_task]
        
        # Actualizar UI
        self.status_label.setText(message)
        progress = int((self.current_task / len(self.initialization_tasks)) * 100)
        self.progress_bar.setValue(progress)
        
        # Ejecutar tarea
        try:
            task_function()
        except Exception as e:
            print(f"Error en tarea de inicialización: {e}")
        
        # Avanzar a siguiente tarea
        self.current_task += 1
        
        # Programar siguiente tarea con delay para suavidad visual
        QTimer.singleShot(150, self.execute_next_task)
    
    def task_ensure_directories(self):
        """Tarea: Asegurar que existan los directorios necesarios"""
        AppPaths.ensure_data_dirs()
    
    def task_load_configuration(self):
        """Tarea: Cargar configuración (placeholder para futuras configs)"""
        pass
    
    def task_init_components(self):
        """Tarea: Inicializar componentes (placeholder)"""
        pass
    
    def task_prepare_etl(self):
        """Tarea: Preparar módulo ETL (placeholder)"""
        pass
    
    def task_prepare_certificates(self):
        """Tarea: Preparar módulo de certificados (placeholder)"""
        pass
    
    def task_finalize(self):
        """Tarea: Finalizar carga"""
        self.progress_bar.setValue(100)
    
    def finish_loading(self):
        """Finaliza la carga y emite la señal"""
        QTimer.singleShot(200, self._emit_complete)
    
    def _emit_complete(self):
        """Emite señal de carga completa y cierra splash"""
        self.loading_complete.emit()
        self.close()