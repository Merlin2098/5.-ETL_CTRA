# gui/tabs/tab_certificates.py
"""
Tab de Generación de Certificados
Interfaz gráfica para generación de certificados desde datos limpios
Versión 2.1 - Distribución optimizada horizontal
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QLabel, QPushButton, QProgressBar, QComboBox,
    QLineEdit, QCheckBox, QFileDialog, QMessageBox,
    QTextEdit, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

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


class TabCertificates(QWidget):
    """Tab para generación de certificados"""
    
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
        
        # [2] Panel: Filtros de Datos (MEJORADO)
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
        """Crea el panel de filtros de datos MEJORADO"""
        group = QGroupBox("🔍 Filtros de Datos")
        group.setObjectName("etlGroup")
        layout = QVBoxLayout(group)
        layout.setSpacing(15)
        
        # Grid para filtros con mejor distribución
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        grid_layout.setColumnMinimumWidth(1, 200)  # Ancho mínimo para combos
        grid_layout.setColumnMinimumWidth(3, 200)
        
        # Labels
        label_dni = QLabel("DNI:")
        label_dni.setMinimumWidth(60)
        label_cliente = QLabel("Cliente:")
        label_cliente.setMinimumWidth(60)
        label_mes = QLabel("Mes:")
        label_mes.setMinimumWidth(60)
        
        # Combos con mejor tamaño
        self.combo_dni = QComboBox()
        self.combo_dni.addItem("TODOS")
        self.combo_dni.setEnabled(False)
        self.combo_dni.setMinimumWidth(180)
        self.combo_dni.currentTextChanged.connect(self._on_dni_changed)
        
        self.combo_cliente = QComboBox()
        self.combo_cliente.addItem("TODOS")
        self.combo_cliente.setEnabled(False)
        self.combo_cliente.setMinimumWidth(180)
        self.combo_cliente.currentTextChanged.connect(self._on_cliente_changed)
        
        self.combo_mes = QComboBox()
        self.combo_mes.addItem("TODOS")
        self.combo_mes.setEnabled(False)
        self.combo_mes.setMinimumWidth(180)
        self.combo_mes.currentTextChanged.connect(self._on_mes_changed)
        
        # Agregar al grid
        grid_layout.addWidget(label_dni, 0, 0)
        grid_layout.addWidget(self.combo_dni, 0, 1)
        grid_layout.addWidget(label_cliente, 0, 2)
        grid_layout.addWidget(self.combo_cliente, 0, 3)
        
        grid_layout.addWidget(label_mes, 1, 0)
        grid_layout.addWidget(self.combo_mes, 1, 1)
        
        layout.addLayout(grid_layout)
        
        # Fila de botón aplicar y resultado
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        self.btn_apply_filter = QPushButton("🎯 Aplicar Filtros")
        self.btn_apply_filter.setObjectName("secondaryButton")
        self.btn_apply_filter.setEnabled(False)
        self.btn_apply_filter.setMinimumWidth(150)
        self.btn_apply_filter.clicked.connect(self._on_apply_filter)
        
        self.label_filtered = QLabel("")
        self.label_filtered.setObjectName("outputLabel")
        self.label_filtered.setMinimumWidth(200)
        
        action_layout.addWidget(self.btn_apply_filter)
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
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMinimumHeight(30)
        layout.addWidget(self.progress_bar)
        
        # Label con paso actual
        self.label_paso = QLabel("")
        self.label_paso.setObjectName("stepLabel")
        layout.addWidget(self.label_paso)
        
        return group
    
    def _create_generate_button(self) -> QPushButton:
        """Crea el botón principal de generación"""
        self.btn_generate = QPushButton("🚀 GENERAR CERTIFICADOS")
        self.btn_generate.setObjectName("successButton")
        self.btn_generate.setMinimumHeight(50)
        self.btn_generate.setEnabled(False)
        self.btn_generate.clicked.connect(self._on_generate_clicked)
        
        return self.btn_generate
    
    def _connect_signals(self):
        """Conecta signals del controller con slots del UI"""
        # Signals de combos
        self.controller.combo_dni_updated.connect(self._on_combo_dni_updated)
        self.controller.combo_cliente_updated.connect(self._on_combo_cliente_updated)
        self.controller.combo_mes_updated.connect(self._on_combo_mes_updated)
        
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
            if self.controller.set_template_path(file_path):
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
            
            # Establecer carpeta en el controller (sin validación prematura)
            self.controller.set_output_folder(folder_path)
            self._update_generate_button_state()
    
    def _on_dni_changed(self, dni: str):
        """DNI seleccionado cambió"""
        if self.controller.df_original is None:
            return
        
        # Actualizar controller
        self.controller.on_dni_changed(dni)
    
    def _on_cliente_changed(self, cliente: str):
        """Cliente seleccionado cambió"""
        if self.controller.df_original is None:
            return
        
        dni = self.combo_dni.currentText()
        
        # Actualizar controller
        self.controller.on_cliente_changed(dni, cliente)
    
    def _on_mes_changed(self, mes: str):
        """Mes seleccionado cambió"""
        # No hace nada por ahora, pero está listo para futuras funcionalidades
        pass
    
    def _on_apply_filter(self):
        """Aplicar filtros seleccionados"""
        dni = self.combo_dni.currentText()
        cliente = self.combo_cliente.currentText()
        mes = self.combo_mes.currentText()
        
        # Aplicar filtro en el controller
        self.controller.apply_filter(dni, cliente, mes)
    
    def _on_generate_clicked(self):
        """Iniciar generación de certificados"""
        # Validar que todos los campos estén configurados
        if not self.controller.template_path:
            msg_box = QMessageBox(self)
            msg_box.setStyleSheet(MESSAGEBOX_LIGHT_STYLE)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Configuración Incompleta")
            msg_box.setText("⚠️ Debe seleccionar una plantilla Word antes de generar")
            msg_box.exec_()
            return
        
        if not self.controller.output_folder:
            msg_box = QMessageBox(self)
            msg_box.setStyleSheet(MESSAGEBOX_LIGHT_STYLE)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Configuración Incompleta")
            msg_box.setText("⚠️ Debe seleccionar una carpeta de salida antes de generar")
            msg_box.exec_()
            return
        
        if self.controller.df_original is None:
            msg_box = QMessageBox(self)
            msg_box.setStyleSheet(MESSAGEBOX_LIGHT_STYLE)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Configuración Incompleta")
            msg_box.setText("⚠️ Debe cargar un archivo Excel antes de generar")
            msg_box.exec_()
            return
        
        # Validar que no esté procesando
        if self.is_processing:
            msg_box = QMessageBox(self)
            msg_box.setStyleSheet(MESSAGEBOX_LIGHT_STYLE)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Procesamiento en Curso")
            msg_box.setText("Ya hay un proceso de generación en curso.\nPor favor espera a que termine.")
            msg_box.exec_()
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
    
    def _on_combo_dni_updated(self, dnis: list):
        """Actualizar combo DNI"""
        self.combo_dni.clear()
        self.combo_dni.addItems(dnis)
        self.combo_dni.setEnabled(True)
        
        # Habilitar botón de aplicar filtro
        self.btn_apply_filter.setEnabled(True)
    
    def _on_combo_cliente_updated(self, clientes: list):
        """Actualizar combo Cliente"""
        self.combo_cliente.clear()
        self.combo_cliente.addItems(clientes)
        self.combo_cliente.setEnabled(True)
    
    def _on_combo_mes_updated(self, meses: list):
        """Actualizar combo Mes"""
        self.combo_mes.clear()
        self.combo_mes.addItems(meses)
        self.combo_mes.setEnabled(True)
    
    def _on_file_loaded(self, record_count: int, file_path: str):
        """Archivo cargado exitosamente"""
        self.label_records.setText(f"📊 {record_count:,} registros cargados")
        self.label_estado.setText("Estado: ✅ Archivo cargado - Listo para configurar")
        
        # Rehabilitar botón
        self.btn_browse_file.setEnabled(True)
        
        # Actualizar botón de generar

    def _on_filter_applied(self, filtered_count: int):
        """Filtro aplicado"""
        self.label_filtered.setText(f"✅ {filtered_count:,} registros después del filtro")
        
        # Actualizar botón de generar
        self._update_generate_button_state()
    
    def _on_progress_updated(self, percent: int, message: str):
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
    
    def _on_error_occurred(self, error_msg: str):
        """Error ocurrido"""
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet(MESSAGEBOX_LIGHT_STYLE)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(f"Ha ocurrido un error:\n\n{error_msg}")
        msg_box.exec_()
        
        # Si estaba procesando, resetear estado
        if self.is_processing:
            self._set_processing_state(False)
            self.progress_bar.setValue(0)
            self.label_estado.setText("❌ Error en el proceso")
            self.label_paso.setText("")
            
            # Rehabilitar botón de archivo si fue un error de carga
            self.btn_browse_file.setEnabled(True)
    
    # ========================================
    # MÉTODOS AUXILIARES
    # ========================================
    
    def _update_generate_button_state(self):
        """Actualiza el estado del botón de generar"""
        state = self.controller.get_current_state()
        
        # Habilitar solo si todo está configurado
        can_generate = (
            state['has_data'] and
            state['has_template'] and
            state['has_output_folder'] and
            not self.is_processing
        )
        
        self.btn_generate.setEnabled(can_generate)
        
        # Actualizar estado
        if can_generate:
            records_to_process = state['filtered_records'] if state['has_filter'] else state['total_records']
            self.label_estado.setText(f"Estado: ✅ Listo para generar {records_to_process:,} certificados")
    
    def _set_processing_state(self, processing: bool):
        """Establece el estado de procesamiento"""
        self.is_processing = processing
        
        # Deshabilitar controles durante procesamiento
        self.btn_browse_file.setEnabled(not processing)
        self.btn_browse_template.setEnabled(not processing)
        self.btn_browse_output.setEnabled(not processing)
        self.combo_dni.setEnabled(not processing)
        self.combo_cliente.setEnabled(not processing)
        self.combo_mes.setEnabled(not processing)
        self.btn_apply_filter.setEnabled(not processing)
        self.check_generate_word.setEnabled(not processing)
        self.check_convert_pdf.setEnabled(not processing)
        self.btn_generate.setEnabled(not processing)
        
        # Emitir signal
        if processing:
            self.processing_started.emit()
        
        # Actualizar estado en app_controller
        if self.app_controller:
            self.app_controller.set_processing(processing)
    
    def _show_results_dialog(self, results: dict):
        """Muestra diálogo con resultados"""
        msg = "=" * 50 + "\n"
        msg += "RESULTADOS DE GENERACIÓN\n"
        msg += "=" * 50 + "\n\n"
        
        if results['success']:
            msg += "✅ Proceso completado exitosamente\n\n"
        else:
            msg += "⚠️ Proceso completado con errores\n\n"
        
        msg += f"📊 Registros procesados: {results['input_records']}\n"
        
        # FORMATAR EL TIEMPO (AGREGAR ESTAS LÍNEAS)
        total_time = results['total_time']
        if total_time >= 3600:
            horas = int(total_time // 3600)
            minutos = int((total_time % 3600) // 60)
            segundos = int(total_time % 60)
            tiempo_formateado = f"{horas:02d}:{minutos:02d}:{segundos:02d} (hh:mm:ss)"
        elif total_time >= 60:
            minutos = int(total_time // 60)
            segundos = int(total_time % 60)
            tiempo_formateado = f"{minutos:02d}:{segundos:02d} (mm:ss)"
        else:
            tiempo_formateado = f"{total_time:.2f} segundos"
        
        msg += f"⏱️ Tiempo total: {tiempo_formateado}\n\n"
        
        # Resultados Word
        if results['word_results']:
            word = results['word_results']
            msg += "📄 GENERACIÓN WORD:\n"
            msg += f"  • Total: {word['total']}\n"
            msg += f"  • Exitosos: {word['exitosos']}\n"
            msg += f"  • Fallidos: {word['fallidos']}\n\n"
        
        # Resultados PDF
        if results['pdf_results']:
            pdf = results['pdf_results']
            msg += "📕 CONVERSIÓN PDF:\n"
            msg += f"  • Total: {pdf['total']}\n"
            msg += f"  • Exitosos: {pdf['exitosos']}\n"
            msg += f"  • Fallidos: {pdf['fallidos']}\n\n"
        
        # Carpetas de salida
        msg += "📁 CARPETAS DE SALIDA:\n"
        msg += f"  • Principal: {results['output_folder']}\n"
        msg += f"  • Word: {results['word_folder']}\n"
        msg += f"  • PDF: {results['pdf_folder']}\n\n"
        
        # Errores
        if results['errors']:
            msg += "⚠️ ERRORES:\n"
            for error in results['errors']:
                msg += f"  • {error}\n"
        
        # Crear diálogo personalizado
        dialog = QMessageBox(self)
        dialog.setStyleSheet(MESSAGEBOX_LIGHT_STYLE)
        dialog.setWindowTitle("Resultados de Generación")
        dialog.setText("Proceso de generación finalizado")
        dialog.setDetailedText(msg)
        
        if results['success']:
            dialog.setIcon(QMessageBox.Information)
        else:
            dialog.setIcon(QMessageBox.Warning)
        
        # Botón para abrir carpeta
        btn_open_folder = dialog.addButton("Abrir Carpeta", QMessageBox.ActionRole)
        dialog.addButton(QMessageBox.Ok)
        
        dialog.exec_()
        
        # Si presionó "Abrir Carpeta"
        if dialog.clickedButton() == btn_open_folder:
            self._open_output_folder(results['output_folder'])
    
    def _open_output_folder(self, folder_path: str):
        """Abre la carpeta de salida en el explorador"""
        import platform
        import subprocess
        import os
        
        # Verificar que la carpeta existe
        if not os.path.exists(folder_path):
            msg_box = QMessageBox(self)
            msg_box.setStyleSheet(MESSAGEBOX_LIGHT_STYLE)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Error")
            msg_box.setText(f"La carpeta no existe:\n{folder_path}")
            msg_box.exec_()
            return
        
        try:
            sistema = platform.system()
            
            if sistema == "Windows":
                os.startfile(folder_path)
            elif sistema == "Darwin":  # macOS
                subprocess.Popen(["open", folder_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", folder_path])
        except Exception as e:
            msg_box = QMessageBox(self)
            msg_box.setStyleSheet(MESSAGEBOX_LIGHT_STYLE)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Error")
            msg_box.setText(f"No se pudo abrir la carpeta:\n{str(e)}")
            msg_box.exec_()
    
    # ========================================
    # MÉTODOS PÚBLICOS
    # ========================================
    
    def apply_theme(self, theme_data: dict):
        """Aplica el tema actual al tab"""
        # El tema se aplica automáticamente a través de los objectName
        # y los estilos definidos en MainWindow
        pass
    
    def reset_state(self):
        """Resetea el estado del tab"""
        self.clean_file_path = None
        self.template_path = None
        self.output_folder = None
        self.is_processing = False
        
        # Limpiar labels
        self.label_file.setText("Ningún archivo seleccionado")
        self.label_template.setText("Ninguna plantilla seleccionada")
        self.label_output.setText("Ninguna carpeta seleccionada")
        self.label_records.setText("📊 Esperando archivo...")
        self.label_filtered.setText("")
        
        # Resetear combos
        self.combo_dni.clear()
        self.combo_dni.addItem("TODOS")
        self.combo_dni.setEnabled(False)
        
        self.combo_cliente.clear()
        self.combo_cliente.addItem("TODOS")
        self.combo_cliente.setEnabled(False)
        
        self.combo_mes.clear()
        self.combo_mes.addItem("TODOS")
        self.combo_mes.setEnabled(False)
        
        # Resetear progreso
        self.progress_bar.setValue(0)
        self.label_estado.setText("Estado: ⏸️ Esperando configuración...")
        self.label_paso.setText("")
        
        # Deshabilitar botones
        self.btn_apply_filter.setEnabled(False)
        self.btn_generate.setEnabled(False)
        
        # Rehabilitar botones de selección
        self.btn_browse_file.setEnabled(True)
        self.btn_browse_template.setEnabled(True)
        self.btn_browse_output.setEnabled(True)