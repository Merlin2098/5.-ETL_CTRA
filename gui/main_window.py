# main_window.py (CORREGIDO)
"""
Ventana Principal de la Aplicación
Define la estructura base con tabs y sistema de temas
Versión 4.0 - Optimización de carga y lazy loading mejorado
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon

from gui.themes import ThemeManager
from config.paths import AppPaths


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación ETL + Certificados"""
    
    def __init__(self, app_controller=None):
        super().__init__()
        
        # Controlador principal de la aplicación
        self.app_controller = app_controller
        
        # Estado de lazy loading
        self.tab_etl = None
        self.tab_certificados = None
        self.tabs_cargados = {
            'etl': False,
            'certificados': False
        }
        
        # Configurar ventana
        self.setWindowTitle("ETL + Certificados")
        self.setMinimumSize(1000, 700)
        
        # Configurar icono usando AppPaths (compatible con PyInstaller)
        try:
            icon_path = AppPaths.get_icon_path()
            self.setWindowIcon(QIcon(str(icon_path)))
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el icono de la ventana: {e}")
        
        # Crear layout principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Crear contenedor superior con header
        top_container = QWidget()
        top_layout = QVBoxLayout(top_container)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        top_layout.addWidget(header)
        
        # Tab Widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("mainTabs")
        
        # Crear placeholders para ambos tabs (se cargan después)
        placeholder_etl = self._create_placeholder("⏳ Cargando interfaz ETL...")
        placeholder_certificados = self._create_placeholder("⏳ Cargando interfaz de Certificados...")
        
        # Agregar tabs (con placeholders inicialmente)
        self.tab_widget.addTab(placeholder_etl, "📊 ETL")
        self.tab_widget.addTab(placeholder_certificados, "📄 Certificados")
        
        # FORZAR TAB INICIAL COMO ETL (índice 0)
        self.tab_widget.setCurrentIndex(0)
        
        # Conectar señal de cambio de tab
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        
        top_layout.addWidget(self.tab_widget)
        
        main_layout.addWidget(top_container)
        
        # Footer
        footer = self.create_footer()
        main_layout.addWidget(footer)
        
        # Cargar temas (usar AppController si está disponible)
        if self.app_controller:
            self.theme_manager = self.app_controller.theme_manager
        else:
            self.theme_manager = ThemeManager()
            
        self.aplicar_tema()
        
        # LAZY LOADING: Inicializar controladores y cargar Tab ETL después de mostrar ventana
        QTimer.singleShot(100, self._initialize_after_show)
    
    def _create_placeholder(self, message: str) -> QWidget:
        """Crea un widget placeholder para lazy loading"""
        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)
        layout.addStretch()
        label_loading = QLabel(message)
        label_loading.setAlignment(Qt.AlignCenter)
        label_loading.setStyleSheet("font-size: 16px; color: #64748b;")
        layout.addWidget(label_loading)
        layout.addStretch()
        return placeholder
    
    def _initialize_after_show(self):
        """Inicializa controladores después de mostrar la ventana"""
        # Inicializar controladores si AppController está disponible
        if self.app_controller:
            self._initialize_controllers()
        
        # Cargar Tab ETL inicial
        self._cargar_tab_etl_inicial()
    
    def _initialize_controllers(self):
        """Inicializa y registra los controladores en AppController"""
        try:
            # Importar solo cuando sea necesario (lazy import)
            from controllers.etl_controller import ETLController
            
            # Inicializar ETL Controller
            etl_controller = ETLController()
            self.app_controller.register_etl_controller(etl_controller)
            
            print("✅ Controladores inicializados correctamente")
            
        except Exception as e:
            print(f"❌ Error inicializando controladores: {e}")
    
    def _cargar_tab_etl_inicial(self):
        """Carga el Tab ETL de forma progresiva después de mostrar la ventana"""
        if not self.tabs_cargados['etl']:
            print("🔧 Iniciando carga del Tab ETL...")
            
            # CRÍTICO: Desconectar temporalmente la señal para evitar recursión
            self.tab_widget.currentChanged.disconnect(self._on_tab_changed)
            
            try:
                # Crear Tab ETL real
                from gui.tabs.tab_etl import TabETL
                
                # Pasar el controlador ETL si está disponible
                etl_controller = None
                if self.app_controller:
                    etl_controller = self.app_controller.get_controller('etl')
                
                self.tab_etl = TabETL(etl_controller)
                
                # Reemplazar placeholder
                current_index = self.tab_widget.currentIndex()  # Guardar índice actual
                self.tab_widget.removeTab(0)
                self.tab_widget.insertTab(0, self.tab_etl, "📊 ETL")
                
                # Restaurar índice si no era 0
                if current_index != 0:
                    self.tab_widget.setCurrentIndex(current_index)
                else:
                    self.tab_widget.setCurrentIndex(0)  # Forzar tab ETL
                
                # Marcar como cargado
                self.tabs_cargados['etl'] = True
                
                print("✅ Tab ETL cargado correctamente")
                
            except Exception as e:
                print(f"❌ Error cargando Tab ETL: {e}")
            finally:
                # CRÍTICO: Reconectar la señal
                self.tab_widget.currentChanged.connect(self._on_tab_changed)
    
    def _cargar_tab_certificados(self):
        """Carga el Tab Certificados de forma progresiva"""
        if not self.tabs_cargados['certificados']:
            print("🔧 Iniciando carga del Tab Certificados...")
            
            # CRÍTICO: Desconectar temporalmente la señal para evitar recursión
            self.tab_widget.currentChanged.disconnect(self._on_tab_changed)
            
            try:
                # Crear Tab Certificados real
                from gui.tabs.tab_certificates import TabCertificates
                
                # Pasar el app_controller al tab de certificados
                self.tab_certificados = TabCertificates(self.app_controller)
                
                # Reemplazar placeholder
                current_index = self.tab_widget.currentIndex()  # Guardar índice actual
                self.tab_widget.removeTab(1)
                self.tab_widget.insertTab(1, self.tab_certificados, "📄 Certificados")
                
                # Restaurar índice original (debería ser 1, pero por seguridad)
                if current_index != 1:
                    self.tab_widget.setCurrentIndex(current_index)
                
                # Marcar como cargado
                self.tabs_cargados['certificados'] = True
                
                print("✅ Tab Certificados cargado correctamente")
                
            except Exception as e:
                print(f"❌ Error cargando Tab Certificados: {e}")
                # Mostrar placeholder de error
                error_placeholder = self._create_placeholder("❌ Error cargando interfaz de Certificados")
                self.tab_widget.removeTab(1)
                self.tab_widget.insertTab(1, error_placeholder, "📄 Certificados")
            finally:
                # CRÍTICO: Reconectar la señal
                self.tab_widget.currentChanged.connect(self._on_tab_changed)
    
    def _on_tab_changed(self, index: int):
        """Maneja el cambio de tab para lazy loading - VERSIÓN CORREGIDA"""
        print(f"🔍 Cambio de tab detectado: {index}")
        print(f"🔍 Estado tabs cargados: ETL={self.tabs_cargados['etl']}, Certificados={self.tabs_cargados['certificados']}")
        
        # Tab ETL (índice 0)
        if index == 0 and not self.tabs_cargados['etl']:
            print("🚀 Solicitando carga del Tab ETL...")
            self._cargar_tab_etl_inicial()
        
        # Tab Certificados (índice 1)
        elif index == 1 and not self.tabs_cargados['certificados']:
            print("🚀 Solicitando carga del Tab Certificados...")
            self._cargar_tab_certificados()
        
        # Si ambos están cargados, solo log para debugging
        elif self.tabs_cargados['etl'] and self.tabs_cargados['certificados']:
            print(f"✅ Ambos tabs cargados, navegando a índice: {index}")
    
    def create_header(self) -> QWidget:
        """Crea el header con título y controles"""
        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(80)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 0, 30, 0)
        
        # Título
        title_label = QLabel("ETL + Certificados")
        title_label.setObjectName("titleLabel")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        layout.addWidget(title_label)
        layout.addStretch()
        
        # Botón de cambio de tema
        self.btn_theme = QPushButton("🌙")
        self.btn_theme.setObjectName("themeButton")
        self.btn_theme.setFixedSize(40, 40)
        self.btn_theme.clicked.connect(self.cambiar_tema)
        self.btn_theme.setToolTip("Cambiar tema (Claro/Oscuro)")
        
        layout.addWidget(self.btn_theme)
        
        return header
    
    def create_footer(self) -> QWidget:
        """Crea el footer con información de copyright"""
        footer = QWidget()
        footer.setObjectName("footer")
        footer.setFixedHeight(40)
        
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(30, 0, 30, 0)
        
        footer_label = QLabel("© 2024 Sistema ETL + Certificados | Desarrollado por Ricardo Uculmana Quispe")
        footer_label.setObjectName("footerLabel")
        layout.addWidget(footer_label, alignment=Qt.AlignCenter)
        
        return footer
    
    def cambiar_tema(self):
        """Cambia entre tema claro y oscuro"""
        self.theme_manager.toggle_theme()
        self.aplicar_tema()
        
        # Propagar cambio de tema a tabs cargados
        if self.tabs_cargados['etl'] and self.tab_etl:
            if hasattr(self.tab_etl, 'apply_theme'):
                theme_data = self.app_controller.get_current_theme_data() if self.app_controller else self.theme_manager.theme_data
                self.tab_etl.apply_theme(theme_data)
        
        if self.tabs_cargados['certificados'] and self.tab_certificados:
            if hasattr(self.tab_certificados, 'apply_theme'):
                theme_data = self.app_controller.get_current_theme_data() if self.app_controller else self.theme_manager.theme_data
                self.tab_certificados.apply_theme(theme_data)
    
    def aplicar_tema(self):
        """Aplica el tema actual a la ventana"""
        if self.app_controller:
            tema_actual = self.app_controller.get_current_theme_name()
            theme_data = self.app_controller.get_current_theme_data()
        else:
            tema_actual = self.theme_manager.get_current_theme()
            theme_data = self.theme_manager.theme_data
        
        # Actualizar ícono del botón
        if tema_actual == 'dark':
            self.btn_theme.setText("☀️")
        else:
            self.btn_theme.setText("🌙")
        
        # Obtener estilos
        styles = self._get_styles(theme_data)
        
        # Aplicar stylesheet
        self.setStyleSheet(styles)
    
    def _get_styles(self, theme_data: dict) -> str:
        """Obtiene los estilos CSS según el tema actual"""
        # Colores base - Acceso correcto según estructura del JSON
        bg_primary = theme_data['colors']['background']
        bg_secondary = theme_data['colors']['surface']
        text_primary = theme_data['colors']['text']['primary']
        text_secondary = theme_data['colors']['text']['secondary']
        primary = theme_data['colors']['primary']
        success = theme_data['colors']['success']
        accent = theme_data['colors']['accent']
        border = theme_data['colors']['border']
        
        return f"""
        /* ===== ESTILOS GLOBALES ===== */
        QMainWindow {{
            background-color: {bg_primary};
        }}
        
        /* ===== HEADER ===== */
        #header {{
            background-color: {bg_secondary};
            border-bottom: 2px solid {border};
        }}
        
        #titleLabel {{
            color: {text_primary};
        }}
        
        #themeButton {{
            background-color: {bg_primary};
            border: 2px solid {border};
            border-radius: 20px;
            font-size: 18px;
        }}
        
        #themeButton:hover {{
            background-color: {primary};
            border-color: {primary};
        }}
        
        /* ===== TABS ===== */
        QTabWidget::pane {{
            border: none;
            background-color: {bg_primary};
        }}
        
        QTabBar::tab {{
            background-color: {bg_secondary};
            color: {text_secondary};
            padding: 12px 24px;
            margin-right: 4px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: bold;
            font-size: 16px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {primary};
            color: white;
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {border};
        }}
        
        /* ===== FOOTER ===== */
        #footer {{
            background-color: {bg_secondary};
            border-top: 2px solid {border};
        }}
        
        #footerLabel {{
            color: {text_secondary};
            font-size: 16px;
        }}
        
        /* ===== GROUPBOX (Paneles) ===== */
        QGroupBox {{
            background-color: {bg_secondary};
            border: 2px solid {border};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
            font-weight: bold;
            color: {text_primary};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 4px 8px;
            color: {primary};
            font-size: 16px;
        }}
        
        #etlGroup {{
            background-color: {bg_secondary};
        }}
        
        /* ===== BOTONES ===== */
        QPushButton {{
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 14px;
        }}
        
        #primaryButton {{
            background-color: {primary};
            color: white;
            border: none;
        }}
        
        #primaryButton:hover {{
            background-color: {accent};
        }}
        
        #primaryButton:disabled {{
            background-color: {border};
            color: {text_secondary};
        }}
        
        #successButton {{
            background-color: {success};
            color: white;
            border: none;
        }}
        
        #successButton:hover {{
            background-color: {primary};
        }}
        
        #successButton:disabled {{
            background-color: {border};
            color: {text_secondary};
        }}
        
        #secondaryButton {{
            background-color: transparent;
            color: {primary};
            border: 2px solid {primary};
        }}
        
        #secondaryButton:hover {{
            background-color: {primary};
            color: white;
        }}
        
        #secondaryButton:disabled {{
            border-color: {border};
            color: {text_secondary};
        }}
        
        /* ===== LABELS ===== */
        QLabel {{
            color: {text_primary};
        }}
        
        #fileLabel {{
            font-size: 15px;
            color: {text_primary};
            font-weight: bold;
        }}
        
        #statsLabel {{
            font-size: 14px;
            color: {text_secondary};
        }}
        
        #statusLabel {{
            font-size: 15px;
            color: {primary};
            font-weight: bold;
        }}
        
        #stepLabel {{
            font-size: 14px;
            color: {text_secondary};
            font-style: italic;
        }}
        
        #outputLabel {{
            font-size: 15px;
            color: {success};
            font-weight: bold;
        }}
        
        /* ===== PROGRESS BAR ===== */
        QProgressBar {{
            border: 2px solid {border};
            border-radius: 6px;
            text-align: center;
            background-color: {bg_primary};
            color: {text_primary};
            font-weight: bold;
        }}
        
        QProgressBar::chunk {{
            background-color: {primary};
            border-radius: 4px;
        }}
        
        #etlProgressBar::chunk {{
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {primary},
                stop:1 {accent}
            );
        }}
        
        /* ===== TEXT EDIT (Consola) ===== */
        QTextEdit {{
            background-color: {bg_primary};
            color: {text_primary};
            border: 2px solid {border};
            border-radius: 6px;
            padding: 8px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
        }}
        
        /* ===== SCROLLBAR ===== */
        QScrollBar:vertical {{
            border: none;
            background: {bg_primary};
            width: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {border};
            border-radius: 5px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {primary};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        """