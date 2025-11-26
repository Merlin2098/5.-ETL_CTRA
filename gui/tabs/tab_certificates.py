# gui/tabs/tab_certificates.py
"""
Tab de Generación de Certificados
Interfaz gráfica para generación de certificados desde datos limpios
Versión 3.1 - Filtros múltiples con ComboBox checkeable (estilo Excel)
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QLabel, QPushButton, QProgressBar, QComboBox,
    QLineEdit, QCheckBox, QFileDialog, QMessageBox,
    QTextEdit, QFrame, QGridLayout, QStyledItemDelegate,
    QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem

from pathlib import Path
from controllers.certificates_controller import CertificatesController
from config.paths import AppPaths


# ============================================================================
# CONSTANTE: Estilo fijo para QMessageBox (tema claro)
# ============================================================================
MESSAGEBOX_LIGHT_STYLE = """
    QMessageBox {
        background-color: #FFFFFF;
        color: #1E293B;
    }
    QMessageBox QLabel {
        color: #1E293B;
    }
    QMessageBox QPushButton {
        background-color: #0284C7;
        color: #FFFFFF;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
        min-width: 80px;
    }
    QMessageBox QPushButton:hover {
        background-color: #0369A1;
    }
    QMessageBox QPushButton:pressed {
        background-color: #075985;
    }
"""


class CheckableComboBox(QComboBox):
    """
    ComboBox con checkboxes estilo filtros de Excel.
    Permite selección múltiple mediante checkboxes.
    Incluye opción "Todos" dentro del dropdown y buscador integrado.
    """
    
    # Signal cuando cambia la selección
    selectionChanged = pyqtSignal()
    
    # Texto especial para el item "Todos"
    ALL_ITEMS_TEXT = "(Seleccionar Todos)"
    
    def __init__(self, parent=None, enable_search=False):
        super().__init__(parent)
        
        # Configurar modelo
        self.setModel(QStandardItemModel(self))
        
        # Flag para habilitar búsqueda
        self.enable_search = enable_search
        self.search_line = None
        
        # Mantener el dropdown abierto al hacer clic
        self.view().viewport().installEventFilter(self)
        
        # Conectar señal de cambio
        self.model().dataChanged.connect(self._on_item_changed)
        
        # Flag para evitar recursión
        self._updating = False
        
        # Actualizar texto al inicio
        self.update_display_text()
    
    def showPopup(self):
        """Override para agregar buscador al abrir el dropdown"""
        super().showPopup()
        
        if self.enable_search and self.search_line is None:
            # Obtener el frame del popup
            popup = self.view().window()
            
            if popup and not hasattr(popup, '_search_added'):
                # Crear el campo de búsqueda
                self.search_line = QLineEdit(popup)
                self.search_line.setPlaceholderText("🔍 Buscar...")
                self.search_line.setClearButtonEnabled(True)
                self.search_line.textChanged.connect(self._filter_items)
                
                # Posicionar el buscador encima de la lista
                self.search_line.setGeometry(2, 2, popup.width() - 4, 25)
                self.search_line.show()
                self.search_line.setFocus()
                
                # Ajustar posición de la vista
                view = self.view()
                current_geo = view.geometry()
                view.setGeometry(
                    current_geo.x(),
                    current_geo.y() + 27,
                    current_geo.width(),
                    current_geo.height() - 27
                )
                
                # Marcar que ya se agregó
                popup._search_added = True
    
    def hidePopup(self):
        """Override para limpiar el buscador al cerrar"""
        if self.search_line:
            self.search_line.clear()
            self.search_line = None
            
            # Quitar marca del popup
            popup = self.view().window()
            if popup and hasattr(popup, '_search_added'):
                delattr(popup, '_search_added')
        
        super().hidePopup()
    
    def _filter_items(self, search_text: str):
        """Filtra items según el texto de búsqueda"""
        search_text = search_text.lower().strip()
        
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item:
                item_text = item.text()
                
                # No ocultar el item "Todos" ni el separador
                if item_text == self.ALL_ITEMS_TEXT or item_text.startswith("─"):
                    self.view().setRowHidden(i, False)
                else:
                    # Mostrar/ocultar según coincidencia
                    matches = search_text in item_text.lower()
                    self.view().setRowHidden(i, not matches)
    
    def eventFilter(self, obj, event):
        """Evita que el dropdown se cierre al hacer clic en un item"""
        if event.type() == QEvent.MouseButtonRelease:
            if obj == self.view().viewport():
                index = self.view().indexAt(event.pos())
                item = self.model().itemFromIndex(index)
                
                if item and item.isCheckable():
                    # Detectar si es el item "Todos"
                    if item.text() == self.ALL_ITEMS_TEXT:
                        # Toggle entre marcar/desmarcar todos
                        if item.checkState() == Qt.Checked:
                            self._uncheck_all_items()
                        else:
                            self._check_all_items()
                    else:
                        # Toggle checkbox normal
                        if item.checkState() == Qt.Checked:
                            item.setCheckState(Qt.Unchecked)
                        else:
                            item.setCheckState(Qt.Checked)
                    
                    return True
        
        return super().eventFilter(obj, event)
    
    def add_item(self, text: str, checked: bool = False):
        """
        Agrega un item con checkbox.
        
        Args:
            text: Texto del item
            checked: Si inicia marcado
        """
        item = QStandardItem(text)
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setCheckState(Qt.Checked if checked else Qt.Unchecked)
        self.model().appendRow(item)
    
    def add_items(self, texts: list, all_checked: bool = False):
        """
        Agrega múltiples items con opción "Todos" al inicio.
        
        Args:
            texts: Lista de textos
            all_checked: Si todos inician marcados
        """
        # Agregar item "Todos" al inicio
        self.add_item(self.ALL_ITEMS_TEXT, all_checked)
        
        # Agregar separador visual (deshabilitado)
        separator = QStandardItem("─" * 30)
        separator.setFlags(Qt.NoItemFlags)
        separator.setEnabled(False)
        self.model().appendRow(separator)
        
        # Agregar items normales
        for text in texts:
            self.add_item(text, all_checked)
    
    def get_checked_items(self) -> list:
        """Retorna lista de textos de items marcados (excluyendo 'Todos')"""
        checked = []
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item and item.checkState() == Qt.Checked:
                text = item.text()
                # Excluir el item especial "Todos"
                if text != self.ALL_ITEMS_TEXT:
                    checked.append(text)
        return checked
    
    def _check_all_items(self):
        """Marca todos los items (incluido el item 'Todos')"""
        self._updating = True
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item and item.isCheckable():
                item.setCheckState(Qt.Checked)
        self._updating = False
        self._on_item_changed()
    
    def _uncheck_all_items(self):
        """Desmarca todos los items (incluido el item 'Todos')"""
        self._updating = True
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item and item.isCheckable():
                item.setCheckState(Qt.Unchecked)
        self._updating = False
        self._on_item_changed()
    
    def clear_items(self):
        """Limpia todos los items"""
        self.model().clear()
    
    def update_display_text(self):
        """Actualiza el texto mostrado en el combo"""
        checked = self.get_checked_items()
        total_items = self.model().rowCount() - 2  # Excluir "Todos" y separador
        
        if len(checked) == 0:
            self.setCurrentText("(Ninguno seleccionado)")
        elif len(checked) == total_items:
            self.setCurrentText(f"(Todos - {len(checked)} items)")
        else:
            self.setCurrentText(f"({len(checked)} seleccionados)")
    
    def _on_item_changed(self):
        """Callback cuando cambia un item"""
        if self._updating:
            return
        
        # Verificar si todos los items (excepto "Todos") están marcados
        checked_items = self.get_checked_items()
        total_items = self.model().rowCount() - 2  # Excluir "Todos" y separador
        
        # Actualizar estado del item "Todos" según los demás items
        all_item = self.model().item(0)
        if all_item and all_item.text() == self.ALL_ITEMS_TEXT:
            self._updating = True
            if len(checked_items) == total_items and total_items > 0:
                all_item.setCheckState(Qt.Checked)
            else:
                all_item.setCheckState(Qt.Unchecked)
            self._updating = False
        
        self.update_display_text()
        self.selectionChanged.emit()


class TabCertificates(QWidget):
    """Tab para generación de certificados con filtros múltiples estilo Excel"""
    
    # Signals
    processing_started = pyqtSignal()
    processing_finished = pyqtSignal(bool)  # True si exitoso, False si falló
    
    def __init__(self, app_controller, parent=None):
        super().__init__(parent)
        
        # Referencias
        self.app_controller = app_controller
        self.controller = CertificatesController()
        
        # Estado interno
        self.clean_file_path = None
        self.template_path = None
        self.output_folder = None
        self.is_processing = False
        
        # Configurar UI
        self.setup_ui()
        self._connect_signals()
        self._apply_initial_state()
    
    def setup_ui(self):
        """Configura la interfaz de usuario optimizada horizontal"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # [1] Panel: Configuración de Archivos (HORIZONTAL)
        panel_config = self.create_panel_configuracion()
        main_layout.addWidget(panel_config)
        
        # [2] Panel: Filtros de Datos con Selección Múltiple
        panel_filtros = self.create_panel_filtros()
        main_layout.addWidget(panel_filtros)
        
        # [3] Panel: Opciones de Generación (HORIZONTAL)
        panel_opciones = self.create_panel_opciones()
        main_layout.addWidget(panel_opciones)
        
        # [4] Panel: Progreso
        panel_progreso = self.create_panel_progreso()
        main_layout.addWidget(panel_progreso)
        
        # [5] Botón de Acción Principal
        btn_generate = self._create_generate_button()
        main_layout.addWidget(btn_generate)
        
        main_layout.addStretch()
    
    def create_panel_configuracion(self) -> QGroupBox:
        """Crea el panel de configuración de archivos en HORIZONTAL"""
        group = QGroupBox("📂 Configuración de Archivos")
        group.setObjectName("etlGroup")
        layout = QVBoxLayout(group)
        layout.setSpacing(10)
        
        # Fila 1: Botones en HORIZONTAL
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Botón Archivo Excel
        file_container = QVBoxLayout()
        self.btn_browse_file = QPushButton("📊 Seleccionar Excel")
        self.btn_browse_file.setObjectName("primaryButton")
        self.btn_browse_file.setMinimumHeight(40)
        self.btn_browse_file.setMinimumWidth(180)
        self.btn_browse_file.clicked.connect(self._on_browse_clean_file)
        file_container.addWidget(self.btn_browse_file)
        
        # Info archivo seleccionado
        self.label_file = QLabel("Ningún archivo seleccionado")
        self.label_file.setObjectName("fileLabel")
        self.label_file.setAlignment(Qt.AlignCenter)
        self.label_file.setWordWrap(True)
        self.label_file.setMaximumHeight(40)
        file_container.addWidget(self.label_file)
        
        # Botón Plantilla Word
        template_container = QVBoxLayout()
        self.btn_browse_template = QPushButton("📄 Seleccionar Plantilla")
        self.btn_browse_template.setObjectName("primaryButton")
        self.btn_browse_template.setMinimumHeight(40)
        self.btn_browse_template.setMinimumWidth(180)
        self.btn_browse_template.clicked.connect(self._on_browse_template)
        template_container.addWidget(self.btn_browse_template)
        
        # Info plantilla seleccionada
        self.label_template = QLabel("Ninguna plantilla seleccionada")
        self.label_template.setObjectName("fileLabel")
        self.label_template.setAlignment(Qt.AlignCenter)
        self.label_template.setWordWrap(True)
        self.label_template.setMaximumHeight(40)
        template_container.addWidget(self.label_template)
        
        # Botón Carpeta Salida
        output_container = QVBoxLayout()
        self.btn_browse_output = QPushButton("📂 Seleccionar Salida")
        self.btn_browse_output.setObjectName("primaryButton")
        self.btn_browse_output.setMinimumHeight(40)
        self.btn_browse_output.setMinimumWidth(180)
        self.btn_browse_output.clicked.connect(self._on_browse_output)
        output_container.addWidget(self.btn_browse_output)
        
        # Info carpeta seleccionada
        self.label_output = QLabel("Ninguna carpeta seleccionada")
        self.label_output.setObjectName("fileLabel")
        self.label_output.setAlignment(Qt.AlignCenter)
        self.label_output.setWordWrap(True)
        self.label_output.setMaximumHeight(40)
        output_container.addWidget(self.label_output)
        
        # Agregar contenedores al layout horizontal
        buttons_layout.addLayout(file_container)
        buttons_layout.addLayout(template_container)
        buttons_layout.addLayout(output_container)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        # Info registros (debajo de los botones)
        records_layout = QHBoxLayout()
        self.label_records = QLabel("📊 Esperando archivo...")
        self.label_records.setObjectName("statsLabel")
        records_layout.addWidget(self.label_records)
        records_layout.addStretch()
        
        layout.addLayout(records_layout)
        
        return group
    
    def create_panel_filtros(self) -> QGroupBox:
        """Crea el panel de filtros con ComboBox checkeable estilo Excel"""
        group = QGroupBox("🔍 Filtros de Datos (Selección Múltiple)")
        group.setObjectName("etlGroup")
        layout = QVBoxLayout(group)
        layout.setSpacing(15)
        
        # Grid para los filtros (sin botones externos)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        grid_layout.setColumnMinimumWidth(1, 250)
        grid_layout.setColumnMinimumWidth(3, 250)
        
        # ===== DNI (con buscador) =====
        label_dni = QLabel("DNI:")
        label_dni.setMinimumWidth(60)
        
        self.combo_dni = CheckableComboBox(enable_search=True)
        self.combo_dni.setEnabled(False)
        self.combo_dni.setMinimumWidth(220)
        self.combo_dni.selectionChanged.connect(self._on_dni_selection_changed)
        
        # Label contador DNI
        self.label_count_dni = QLabel("0 seleccionados")
        self.label_count_dni.setStyleSheet("color: #17C7CD; font-size: 12px; font-weight: bold;")
        
        # ===== CLIENTE (sin buscador) =====
        label_cliente = QLabel("Cliente:")
        label_cliente.setMinimumWidth(60)
        
        self.combo_cliente = CheckableComboBox(enable_search=False)
        self.combo_cliente.setEnabled(False)
        self.combo_cliente.setMinimumWidth(220)
        self.combo_cliente.selectionChanged.connect(self._on_cliente_selection_changed)
        
        # Label contador Cliente
        self.label_count_cliente = QLabel("0 seleccionados")
        self.label_count_cliente.setStyleSheet("color: #17C7CD; font-size: 12px; font-weight: bold;")
        
        # ===== MES (sin buscador) =====
        label_mes = QLabel("Mes:")
        label_mes.setMinimumWidth(60)
        
        self.combo_mes = CheckableComboBox(enable_search=False)
        self.combo_mes.setEnabled(False)
        self.combo_mes.setMinimumWidth(220)
        self.combo_mes.selectionChanged.connect(self._on_mes_selection_changed)
        
        # Label contador Mes
        self.label_count_mes = QLabel("0 seleccionados")
        self.label_count_mes.setStyleSheet("color: #17C7CD; font-size: 12px; font-weight: bold;")
        
        # Agregar al grid
        # Fila 0: DNI y Cliente
        grid_layout.addWidget(label_dni, 0, 0)
        grid_layout.addWidget(self.combo_dni, 0, 1)
        grid_layout.addWidget(self.label_count_dni, 0, 2, Qt.AlignLeft)
        
        grid_layout.addWidget(label_cliente, 0, 3)
        grid_layout.addWidget(self.combo_cliente, 0, 4)
        grid_layout.addWidget(self.label_count_cliente, 0, 5, Qt.AlignLeft)
        
        
        # Fila 1: Mes
        grid_layout.addWidget(label_mes, 1, 0)
        grid_layout.addWidget(self.combo_mes, 1, 1)
        grid_layout.addWidget(self.label_count_mes, 1, 2, Qt.AlignLeft)
        
        
        layout.addLayout(grid_layout)
        
        # ===== FILA DE BOTONES Y RESULTADO =====
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        self.btn_apply_filter = QPushButton("🎯 Aplicar Filtros")
        self.btn_apply_filter.setObjectName("secondaryButton")
        self.btn_apply_filter.setEnabled(False)
        self.btn_apply_filter.setMinimumWidth(150)
        self.btn_apply_filter.setMinimumHeight(35)
        self.btn_apply_filter.clicked.connect(self._on_apply_filter)
        
        self.btn_clear_filter = QPushButton("🗑️ Limpiar Filtros")
        self.btn_clear_filter.setObjectName("secondaryButton")
        self.btn_clear_filter.setEnabled(False)
        self.btn_clear_filter.setMinimumWidth(150)
        self.btn_clear_filter.setMinimumHeight(35)
        self.btn_clear_filter.clicked.connect(self._on_clear_filter)
        
        self.label_filtered = QLabel("")
        self.label_filtered.setObjectName("outputLabel")
        self.label_filtered.setMinimumWidth(250)
        
        action_layout.addWidget(self.btn_apply_filter)
        action_layout.addWidget(self.btn_clear_filter)
        action_layout.addWidget(self.label_filtered)
        action_layout.addStretch()
        
        layout.addLayout(action_layout)
        
        return group
    
    def create_panel_opciones(self) -> QGroupBox:
        """Crea el panel de opciones de generación en HORIZONTAL"""
        group = QGroupBox("⚙️ Opciones de Generación")
        group.setObjectName("etlGroup")
        layout = QHBoxLayout(group)
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Checkboxes en HORIZONTAL
        self.check_generate_word = QCheckBox("📄 Generar Word (.docx)")
        self.check_generate_word.setChecked(True)
        self.check_generate_word.setMinimumWidth(180)
        self.check_generate_word.setStyleSheet("color: #17C7CD;")
        
        self.check_convert_pdf = QCheckBox("📕 Convertir a PDF (.pdf)")
        self.check_convert_pdf.setChecked(True)
        self.check_convert_pdf.setMinimumWidth(180)
        self.check_convert_pdf.setStyleSheet("color: #17C7CD;")
        
        layout.addWidget(self.check_generate_word)
        layout.addWidget(self.check_convert_pdf)
        layout.addStretch()
        
        return group
    
    def create_panel_progreso(self) -> QGroupBox:
        """Crea el panel de progreso"""
        group = QGroupBox("📊 Progreso de Generación")
        group.setObjectName("etlGroup")
        layout = QVBoxLayout(group)
        layout.setSpacing(15)
        
        # Label de estado
        self.label_estado = QLabel("Estado: ⏸️ Esperando configuración...")
        self.label_estado.setObjectName("statusLabel")
        estado_font = QFont()
        estado_font.setPointSize(10)
        self.label_estado.setFont(estado_font)
        layout.addWidget(self.label_estado)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("etlProgressBar")
        self.progress_bar.setMinimumHeight(30)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Label de paso actual
        self.label_paso = QLabel("")
        self.label_paso.setObjectName("stepLabel")
        layout.addWidget(self.label_paso)
        
        # Label tiempo restante
        
        return group
    
    def _create_generate_button(self) -> QPushButton:
        """Crea el botón de generación principal"""
        btn = QPushButton("🚀 Generar Certificados")
        btn.setObjectName("generateButton")
        btn.setMinimumHeight(50)
        btn.setEnabled(False)
        btn.clicked.connect(self._on_generate_clicked)
        
        # Establecer color cyan #17C7CD
        btn.setStyleSheet("""
            QPushButton#generateButton {
                background-color: #17C7CD;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton#generateButton:hover {
                background-color: #14B3BD;
            }
            QPushButton#generateButton:pressed {
                background-color: #119AA3;
            }
            QPushButton#generateButton:disabled {
                background-color: #64748B;
                color: #94A3B8;
            }
        """)
        
        # Guardar referencia
        self.btn_generate = btn
        
        return btn
    
    def _connect_signals(self):
        """Conecta signals del controller con slots de la UI"""
        # Signals de actualización de listas
        self.controller.list_dni_updated.connect(self._on_list_dni_updated)
        self.controller.list_cliente_updated.connect(self._on_list_cliente_updated)
        self.controller.list_mes_updated.connect(self._on_list_mes_updated)
        
        # Signals de habilitación/deshabilitación
        self.controller.cliente_section_enabled.connect(self._on_cliente_section_enabled)
        self.controller.mes_section_enabled.connect(self._on_mes_section_enabled)
        self.controller.apply_button_enabled.connect(self._on_apply_button_enabled)
        
        # Signals de estado
        self.controller.file_loaded.connect(self._on_file_loaded)
        self.controller.filter_applied.connect(self._on_filter_applied)
        
        # Signals de progreso
        self.controller.progress_updated.connect(self._on_progress_updated)
        self.controller.generation_completed.connect(self._on_generation_completed)
        
        # Signals de errores
        self.controller.error_occurred.connect(self._on_error_occurred)
    
    def _apply_initial_state(self):
        """Aplica el estado inicial del UI"""
        self.progress_bar.setValue(0)
        self.label_estado.setText("Estado: ⏸️ Esperando configuración...")
        self.label_paso.setText("")
        self.label_filtered.setText("")
        self.label_records.setText("📊 Esperando archivo...")
    
    # ========================================
    # SLOTS - ACCIONES DE USUARIO
    # ========================================
    
    def _on_browse_clean_file(self):
        """Examinar archivo limpio"""
        default_dir = str(AppPaths.get_clean_dir())
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Archivo Excel Limpio",
            default_dir,
            "Excel Files (*.xlsx *.xls)"
        )
        
        if file_path:
            # Actualizar UI inmediatamente
            nombre_archivo = Path(file_path).name
            self.label_file.setText(nombre_archivo)
            self.label_records.setText("⏳ Cargando archivo...")
            self.label_estado.setText("Estado: 🔄 Cargando archivo...")
            
            # Deshabilitar botones durante carga
            self.btn_browse_file.setEnabled(False)
            
            # Cargar archivo en el controller
            self.controller.load_clean_file(file_path)
    
    def _on_browse_template(self):
        """Examinar plantilla Word"""
        default_dir = str(AppPaths.get_templates_dir())
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Plantilla Word",
            default_dir,
            "Word Files (*.docx)"
        )
        
        if file_path:
            self.template_path = file_path
            nombre_plantilla = Path(file_path).name
            self.label_template.setText(nombre_plantilla)
            
            # Establecer plantilla en el controller
            if self.controller.set_template(file_path):
                self._update_generate_button_state()
    
    def _on_browse_output(self):
        """Examinar carpeta de salida"""
        default_dir = str(AppPaths.get_output_dir())
        
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar Carpeta de Salida",
            default_dir
        )
        
        if folder_path:
            self.output_folder = folder_path
            # Mostrar solo el nombre de la carpeta, no la ruta completa
            folder_name = Path(folder_path).name
            self.label_output.setText(folder_name)
            
            # Establecer carpeta en el controller
            self.controller.set_output_folder(folder_path)
            self._update_generate_button_state()
    
    def _on_dni_selection_changed(self):
        """Detecta cambios en selección de DNIs y notifica al controller"""
        selected_dnis = self.combo_dni.get_checked_items()
        
        # Actualizar contador
        count = len(selected_dnis)
        self.label_count_dni.setText(f"{count} seleccionado{'s' if count != 1 else ''}")
        
        self.controller.on_dni_selection_changed(selected_dnis)
    
    def _on_cliente_selection_changed(self):
        """Detecta cambios en selección de Clientes y notifica al controller"""
        selected_clientes = self.combo_cliente.get_checked_items()
        
        # Actualizar contador
        count = len(selected_clientes)
        self.label_count_cliente.setText(f"{count} seleccionado{'s' if count != 1 else ''}")
        
        self.controller.on_cliente_selection_changed(selected_clientes)
    
    def _on_mes_selection_changed(self):
        """Detecta cambios en selección de Meses y notifica al controller"""
        selected_meses = self.combo_mes.get_checked_items()
        
        # Actualizar contador
        count = len(selected_meses)
        self.label_count_mes.setText(f"{count} seleccionado{'s' if count != 1 else ''}")
        
        self.controller.on_mes_selection_changed(selected_meses)
    
    def _on_apply_filter(self):
        """Aplicar filtros seleccionados y bloquear filtros anteriores"""
        self.controller.apply_filters()
        
        # BLOQUEAR filtros para evitar cambios sin limpiar
        # Usuario debe usar "Limpiar Filtros" para hacer nuevas combinaciones
        self.combo_dni.setEnabled(False)
        self.combo_cliente.setEnabled(False)
        self.combo_mes.setEnabled(False)
    
    def _on_clear_filter(self):
        """Limpiar todos los filtros y rehabilitar combos"""
        self.controller.clear_filters()
        
        # Resetear contadores
        self.label_count_dni.setText("0 seleccionados")
        self.label_count_cliente.setText("0 seleccionados")
        self.label_count_mes.setText("0 seleccionados")
        
        # REHABILITAR DNI para permitir nueva selección
        # Los demás se habilitarán según la cascada
        if self.controller.df_original is not None:
            dnis_count = self.combo_dni.model().rowCount()
            self.combo_dni.setEnabled(dnis_count > 0)
    
    def _on_generate_clicked(self):
        """Iniciar generación de certificados"""
        # Validar que todos los campos estén configurados
        if not self.controller.template_path:
            self._show_warning("Configuración Incompleta", 
                             "⚠️ Debe seleccionar una plantilla Word antes de generar")
            return
        
        if not self.controller.output_folder:
            self._show_warning("Configuración Incompleta",
                             "⚠️ Debe seleccionar una carpeta de salida antes de generar")
            return
        
        if self.controller.df_original is None:
            self._show_warning("Configuración Incompleta",
                             "⚠️ Debe cargar un archivo Excel antes de generar")
            return
        
        # Validar que no esté procesando
        if self.is_processing:
            self._show_warning("Procesamiento en Curso",
                             "Ya hay un proceso de generación en curso.\nPor favor espera a que termine.")
            return
        
        # Confirmar con el usuario
        state = self.controller.get_current_state()
        records_to_process = state['filtered_records'] if state['has_filter'] else state['total_records']
        
        msg = f"¿Deseas generar {records_to_process} certificados?\n\n"
        msg += f"Plantilla: {Path(self.template_path).name}\n"
        msg += f"Salida: {self.output_folder}\n\n"
        
        if self.check_generate_word.isChecked():
            msg += "✅ Se generarán archivos Word\n"
        if self.check_convert_pdf.isChecked():
            msg += "✅ Se convertirán a PDF\n"
        
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet(MESSAGEBOX_LIGHT_STYLE)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Confirmar Generación")
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        reply = msg_box.exec_()
        
        if reply == QMessageBox.No:
            return
        
        # Preparar opciones
        options = {
            'generate_word': self.check_generate_word.isChecked(),
            'convert_pdf': self.check_convert_pdf.isChecked(),
            'batch_size': 100
        }
        
        # Cambiar estado
        self._set_processing_state(True)
        
        # Iniciar generación
        self.controller.start_generation(options)
    
    # ========================================
    # SLOTS - SIGNALS DEL CONTROLLER
    # ========================================
    
    def _on_list_dni_updated(self, dnis: list):
        """Actualizar ComboBox DNI con items disponibles"""
        self.combo_dni.clear_items()
        self.combo_dni.add_items(dnis, all_checked=False)
        self.combo_dni.setEnabled(len(dnis) > 0)
        
        # Habilitar botón limpiar si hay datos
        self.btn_clear_filter.setEnabled(len(dnis) > 0)
    
    def _on_list_cliente_updated(self, clientes: list):
        """Actualizar ComboBox Cliente con items disponibles"""
        self.combo_cliente.clear_items()
        self.combo_cliente.add_items(clientes, all_checked=False)
    
    def _on_list_mes_updated(self, meses: list):
        """Actualizar ComboBox Mes con items disponibles"""
        self.combo_mes.clear_items()
        self.combo_mes.add_items(meses, all_checked=False)
    
    def _on_cliente_section_enabled(self, enabled: bool):
        """Habilita/deshabilita la sección de Cliente"""
        self.combo_cliente.setEnabled(enabled)
    
    def _on_mes_section_enabled(self, enabled: bool):
        """Habilita/deshabilita la sección de Mes"""
        self.combo_mes.setEnabled(enabled)
    
    def _on_apply_button_enabled(self, enabled: bool):
        """Habilita/deshabilita el botón Aplicar Filtros"""
        self.btn_apply_filter.setEnabled(enabled)
        
        if not enabled:
            self.label_filtered.setText("⚠️ Debe seleccionar al menos un valor en cada filtro")
        else:
            self.label_filtered.setText("")
    
    def _on_file_loaded(self, record_count: int, file_path: str):
        """Archivo cargado exitosamente"""
        self.label_records.setText(f"📊 {record_count:,} registros cargados")
        self.label_estado.setText("Estado: ✅ Archivo cargado - Seleccione filtros")
        
        # Rehabilitar botón
        self.btn_browse_file.setEnabled(True)
    
    def _on_filter_applied(self, filtered_count: int):
        """Filtro aplicado - Mantener combos bloqueados"""
        self.label_filtered.setText(f"✅ {filtered_count:,} certificados listos para generar")
        self.label_filtered.setStyleSheet("color: #17C7CD; font-weight: bold;")
        
        # MANTENER BLOQUEADOS los combos después de aplicar filtros
        # Solo "Limpiar Filtros" los desbloqueará
        self.combo_dni.setEnabled(False)
        self.combo_cliente.setEnabled(False)
        self.combo_mes.setEnabled(False)
        
        # Actualizar botón de generar
        self._update_generate_button_state()
    
    def _on_progress_updated(self, percent: int, message: str, tiempo_restante: float):
        """Actualizar progreso"""
        self.progress_bar.setValue(percent)
        self.label_paso.setText(message)
        
        if percent < 100:
            self.label_estado.setText(f"Estado: ⚙️ Generando certificados... ({percent}%)")
    
    def _on_generation_completed(self, results: dict):
        """Generación completada"""
        self._set_processing_state(False)
        
        # Resetear progreso
        self.progress_bar.setValue(100)
        self.label_estado.setText("Estado: ✅ Generación completada")
        self.label_paso.setText("Proceso finalizado exitosamente")
        
        # Mostrar resultados
        self._show_results_dialog(results)
        
        # Emitir signal
        self.processing_finished.emit(results['success'])
    
    def _on_error_occurred(self, title: str, error_msg: str):
        """Error ocurrido"""
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet(MESSAGEBOX_LIGHT_STYLE)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(f"Ha ocurrido un error:\n\n{error_msg}")
        msg_box.exec_()
        
        # Resetear estado si estaba procesando
        if self.is_processing:
            self._set_processing_state(False)
        
        # Rehabilitar botón de archivo
        self.btn_browse_file.setEnabled(True)
    
    # ========================================
    # MÉTODOS AUXILIARES
    # ========================================
    
    def _update_generate_button_state(self):
        """Actualiza el estado del botón Generar según la configuración"""
        can_generate = (
            self.controller.df_original is not None and
            self.controller.template_path is not None and
            self.controller.output_folder is not None
        )
        
        self.btn_generate.setEnabled(can_generate and not self.is_processing)
    
    def _set_processing_state(self, is_processing: bool):
        """Cambia el estado de procesamiento"""
        self.is_processing = is_processing
        
        # Deshabilitar/habilitar controles
        self.btn_browse_file.setEnabled(not is_processing)
        self.btn_browse_template.setEnabled(not is_processing)
        self.btn_browse_output.setEnabled(not is_processing)
        self.btn_apply_filter.setEnabled(not is_processing)
        self.btn_clear_filter.setEnabled(not is_processing)
        self.btn_generate.setEnabled(not is_processing)
        
        # Combos
        self.combo_dni.setEnabled(not is_processing)
        self.combo_cliente.setEnabled(not is_processing)
        self.combo_mes.setEnabled(not is_processing)
        
        # Emitir signal
        if is_processing:
            self.processing_started.emit()
    
    def _show_warning(self, title: str, message: str):
        """Muestra un diálogo de advertencia"""
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet(MESSAGEBOX_LIGHT_STYLE)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
    
    def _show_results_dialog(self, results: dict):
        """Muestra diálogo con resultados de la generación"""
        success = results.get('success', False)
        tiempo_total = results.get('total_time_formatted', '00:00')
        
        # Construir mensaje
        if success:
            icon = QMessageBox.Information
            title = "✅ Generación Completada"
            msg = "🎉 Los certificados se generaron exitosamente!\n\n"
        else:
            icon = QMessageBox.Warning
            title = "⚠️ Generación Completada con Errores"
            msg = "⚠️ La generación finalizó pero hubo algunos errores:\n\n"
        
        # Resultados Word
        if results.get('word_results'):
            word = results['word_results']
            msg += f"📄 Word:\n"
            msg += f"   ✅ Exitosos: {word.get('exitosos', 0)}\n"
            msg += f"   ❌ Fallidos: {word.get('fallidos', 0)}\n\n"
        
        # Resultados PDF
        if results.get('pdf_results'):
            pdf = results['pdf_results']
            msg += f"📕 PDF:\n"
            msg += f"   ✅ Exitosos: {pdf.get('exitosos', 0)}\n"
            msg += f"   ❌ Fallidos: {pdf.get('fallidos', 0)}\n\n"
        
        msg += f"⏱️ Tiempo total: {tiempo_total}\n"
        msg += f"📂 Ubicación: {self.output_folder}"
        
        # Mostrar diálogo
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet(MESSAGEBOX_LIGHT_STYLE)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.exec_()
    
    def apply_theme(self, theme_data: dict):
        """
        Aplica tema a este tab.
        
        Args:
            theme_data: Diccionario con colores del tema
        """
        # El tema se aplica automáticamente a través del stylesheet global
        # Este método existe por compatibilidad con la arquitectura actual
        pass