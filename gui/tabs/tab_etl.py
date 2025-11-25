"""
Tab ETL - Interfaz de Procesamiento ETL
Pestaña para cargar, procesar y exportar datasets
Versión 2.0 - Integrado con AppController
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFileDialog, QProgressBar, QGroupBox,
    QTextEdit, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import os
from pathlib import Path
import sys

# Importar el controlador ETL
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class FileLoadThread(QThread):
    """Thread para cargar archivo Excel sin bloquear UI"""
    
    # Señales
    load_started = pyqtSignal()
    load_progress = pyqtSignal(str)  # mensaje de estado
    load_finished = pyqtSignal(bool, str, int)  # éxito, mensaje, num_registros
    
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        """Ejecuta la carga del archivo"""
        try:
            self.load_progress.emit("📂 Leyendo archivo Excel...")
            
            import pandas as pd
            
            # Leer Excel (solo para contar registros)
            df = pd.read_excel(self.file_path, dtype={'DNI': str})
            num_registros = len(df)
            
            # Limpiar memoria
            del df
            
            self.load_progress.emit("✅ Archivo cargado correctamente")
            self.load_finished.emit(True, "Archivo cargado", num_registros)
            
        except Exception as e:
            self.load_finished.emit(False, f"Error al leer archivo: {str(e)}", 0)


class ETLProcessThread(QThread):
    """Thread para ejecutar el procesamiento ETL sin bloquear la UI"""
    
    # Señales para comunicación con la UI
    progress_updated = pyqtSignal(int, str)
    process_finished = pyqtSignal(bool, str, dict)
    
    def __init__(self, ruta_archivo: str, etl_controller=None):
        super().__init__()
        self.ruta_archivo = ruta_archivo
        
        # Usar el controlador proporcionado o crear uno nuevo
        if etl_controller:
            self.controller = etl_controller
            print("✅ ETLProcessThread usando controlador proporcionado")
        else:
            from controllers.etl_controller import ETLController
            self.controller = ETLController()
            print("⚠️  ETLProcessThread creando nuevo controlador (fallback)")
        
        # Conectar callback de progreso
        self.controller.set_progress_callback(self._progress_callback)
    
    def _progress_callback(self, porcentaje: int, mensaje: str):
        """Callback para reportar progreso"""
        self.progress_updated.emit(porcentaje, mensaje)
    
    def run(self):
        """Ejecuta el procesamiento ETL"""
        # Procesar con el archivo especificado
        exito, mensaje, estadisticas = self.controller.procesar_completo(self.ruta_archivo)
        self.process_finished.emit(exito, mensaje, estadisticas)


class TabETL(QWidget):
    """Tab de procesamiento ETL"""
    
    def __init__(self, etl_controller=None):
        super().__init__()
        
        # Usar el controlador proporcionado o crear uno nuevo
        if etl_controller:
            self.etl_controller = etl_controller
            print("✅ Tab ETL usando controlador proporcionado")
        else:
            from controllers.etl_controller import ETLController
            self.etl_controller = ETLController()
            print("⚠️  Tab ETL creando nuevo controlador (fallback)")
        
        # Variables de estado
        self.ruta_archivo_raw = None
        self.estadisticas = {}
        self.process_thread = None
        self.load_thread = None
        
        # Configurar UI
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Panel de carga de archivo
        panel_archivo = self.create_panel_archivo()
        main_layout.addWidget(panel_archivo)
        
        # Panel de procesamiento
        panel_proceso = self.create_panel_procesamiento()
        main_layout.addWidget(panel_proceso)
        
        # Panel de salida
        panel_salida = self.create_panel_salida()
        main_layout.addWidget(panel_salida)
        
        main_layout.addStretch()
    
    def create_panel_archivo(self) -> QGroupBox:
        """Crea el panel de carga de archivo"""
        group = QGroupBox("📂 Archivo de Entrada (RAW)")
        group.setObjectName("etlGroup")
        layout = QVBoxLayout(group)
        layout.setSpacing(10)
        
        # Botón para seleccionar archivo
        btn_layout = QHBoxLayout()
        
        self.btn_seleccionar = QPushButton("📁 Seleccionar Archivo Excel")
        self.btn_seleccionar.setObjectName("primaryButton")
        self.btn_seleccionar.clicked.connect(self.seleccionar_archivo)
        self.btn_seleccionar.setMinimumHeight(40)
        
        btn_layout.addWidget(self.btn_seleccionar)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # Label con nombre del archivo
        self.label_archivo = QLabel("📄 Ningún archivo seleccionado")
        self.label_archivo.setObjectName("fileLabel")
        layout.addWidget(self.label_archivo)
        
        # Label con cantidad de registros
        self.label_registros = QLabel("")
        self.label_registros.setObjectName("statsLabel")
        layout.addWidget(self.label_registros)
        
        # Información de carpeta de salida
        info_salida = QLabel("📤 <b>Salida:</b> data/clean (formato: clean_dd.mm.yyyy_hh.mm.ss.xlsx)")
        info_salida.setObjectName("statsLabel")
        layout.addWidget(info_salida)
        
        return group
    
    def create_panel_procesamiento(self) -> QGroupBox:
        """Crea el panel de procesamiento"""
        group = QGroupBox("⚙️ Procesamiento ETL")
        group.setObjectName("etlGroup")
        layout = QVBoxLayout(group)
        layout.setSpacing(15)
        
        # Botón de inicio
        btn_layout = QHBoxLayout()
        
        self.btn_procesar = QPushButton("🚀 Iniciar Procesamiento")
        self.btn_procesar.setObjectName("successButton")
        self.btn_procesar.setEnabled(False)
        self.btn_procesar.clicked.connect(self.iniciar_procesamiento)
        self.btn_procesar.setMinimumHeight(45)
        
        btn_layout.addWidget(self.btn_procesar)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # Label de estado
        self.label_estado = QLabel("Estado: ⏸️ Esperando archivo...")
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
    
    def create_panel_salida(self) -> QGroupBox:
        """Crea el panel de archivo de salida"""
        group = QGroupBox("💾 Archivo de Salida (CLEAN)")
        group.setObjectName("etlGroup")
        layout = QVBoxLayout(group)
        layout.setSpacing(10)
        
        # Label con nombre del archivo
        self.label_salida = QLabel("⏳ Esperando procesamiento...")
        self.label_salida.setObjectName("outputLabel")
        self.label_salida.setWordWrap(True)
        layout.addWidget(self.label_salida)
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        
        self.btn_abrir_carpeta = QPushButton("📂 Abrir Carpeta")
        self.btn_abrir_carpeta.setObjectName("secondaryButton")
        self.btn_abrir_carpeta.setEnabled(False)
        self.btn_abrir_carpeta.clicked.connect(self.abrir_carpeta_salida)
        
        btn_layout.addWidget(self.btn_abrir_carpeta)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        return group
    
    def seleccionar_archivo(self):
        """Abre diálogo para seleccionar archivo Excel"""
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Archivo Excel RAW",
            "data/raw",
            "Archivos Excel (*.xlsx *.xls)"
        )
        
        if ruta:
            # Actualizar UI inmediatamente
            nombre_archivo = os.path.basename(ruta)
            self.label_archivo.setText(f"📄 {nombre_archivo}")
            self.label_registros.setText("⏳ Analizando archivo...")
            self.label_estado.setText("Estado: 🔄 Cargando archivo...")
            
            # Deshabilitar botones durante carga
            self.btn_seleccionar.setEnabled(False)
            self.btn_procesar.setEnabled(False)
            
            # Crear y ejecutar thread de carga
            self.load_thread = FileLoadThread(ruta)
            self.load_thread.load_progress.connect(self._on_load_progress)
            self.load_thread.load_finished.connect(self._on_load_finished)
            self.load_thread.start()
    
    def _on_load_progress(self, mensaje: str):
        """Actualiza el mensaje durante la carga"""
        self.label_registros.setText(mensaje)
    
    def _on_load_finished(self, exito: bool, mensaje: str, num_registros: int):
        """Maneja la finalización de la carga del archivo"""
        # Rehabilitar botón de selección
        self.btn_seleccionar.setEnabled(True)
        
        if exito:
            # Guardar ruta
            self.ruta_archivo_raw = self.load_thread.file_path
            
            # Actualizar UI con éxito
            self.label_registros.setText(f"📊 {num_registros:,} registros detectados")
            self.label_estado.setText("Estado: ✅ Archivo cargado - Listo para procesar")
            
            # Habilitar botón de procesar
            self.btn_procesar.setEnabled(True)
        else:
            # Mostrar error
            self.label_registros.setText("❌ Error al cargar archivo")
            self.label_estado.setText("Estado: ⏸️ Esperando archivo...")
            
            QMessageBox.critical(
                self,
                "Error de Carga",
                f"No se pudo cargar el archivo:\n\n{mensaje}"
            )
    
    def iniciar_procesamiento(self):
        """Inicia el procesamiento ETL en un thread separado"""
        # Verificar que se haya seleccionado un archivo
        if not self.ruta_archivo_raw:
            QMessageBox.warning(
                self,
                "Error",
                "Por favor, selecciona un archivo Excel antes de iniciar el procesamiento."
            )
            return
        
        # Verificar que el archivo existe
        if not os.path.exists(self.ruta_archivo_raw):
            QMessageBox.warning(
                self,
                "Error",
                f"El archivo seleccionado no existe:\n{self.ruta_archivo_raw}"
            )
            return
        
        # Deshabilitar botones durante procesamiento
        self.btn_seleccionar.setEnabled(False)
        self.btn_procesar.setEnabled(False)
        self.btn_abrir_carpeta.setEnabled(False)
        
        # Resetear UI
        self.progress_bar.setValue(0)
        self.label_salida.setText("⏳ Procesando...")
        
        # Crear y ejecutar thread con el controlador proporcionado
        self.process_thread = ETLProcessThread(
            self.ruta_archivo_raw, 
            self.etl_controller  # Pasar el controlador al thread
        )
        
        # Conectar señales
        self.process_thread.progress_updated.connect(self.actualizar_progreso)
        self.process_thread.process_finished.connect(self.procesamiento_finalizado)
        
        # Iniciar thread
        self.process_thread.start()
    
    def actualizar_progreso(self, porcentaje: int, mensaje: str):
        """Actualiza la barra de progreso y mensajes"""
        self.progress_bar.setValue(porcentaje)
        self.label_paso.setText(mensaje)
        
        if porcentaje < 100:
            self.label_estado.setText(f"Estado: ⚙️ Procesando... ({porcentaje}%)")
    
    def procesamiento_finalizado(self, exito: bool, mensaje: str, estadisticas: dict):
        """Maneja la finalización del procesamiento"""
        # Rehabilitar botones
        self.btn_seleccionar.setEnabled(True)
        self.btn_procesar.setEnabled(True)
        
        if exito:
            # Procesamiento exitoso
            self.estadisticas = estadisticas
            self.label_estado.setText("Estado: ✅ Procesamiento completado exitosamente")
            
            # Actualizar panel de salida
            archivo_salida = estadisticas.get('archivo_salida', '')
            if archivo_salida:
                nombre = os.path.basename(archivo_salida)
                self.label_salida.setText(f"✅ {nombre}\n📁 {archivo_salida}")
                self.btn_abrir_carpeta.setEnabled(True)
                            
        else:
            # Error en procesamiento
            self.label_estado.setText("Estado: ❌ Error en procesamiento")
            
            QMessageBox.critical(
                self,
                "Error",
                f"Error durante el procesamiento:\n\n{mensaje}"
            )
    
    def _mostrar_resumen_estilizado(self, resumen: str):
        """Muestra el resumen en un QMessageBox estilizado para ambos temas"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("✅ Procesamiento Completado")
        msg_box.setText(resumen)
        msg_box.setIcon(QMessageBox.Information)
        
        # Estilo forzado para que sea legible en cualquier tema
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
            }
            QMessageBox QLabel {
                color: #1E293B;
                font-size: 13px;
                font-family: 'Consolas', 'Courier New', monospace;
                min-width: 500px;
            }
            QMessageBox QPushButton {
                background-color: #06B6D4;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 13px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #0891B2;
            }
            QMessageBox QPushButton:pressed {
                background-color: #0E7490;
            }
        """)
        
        msg_box.exec_()
    
    def generar_resumen_estadisticas(self, stats: dict) -> str:
        """Genera el texto de resumen de estadísticas"""
        texto = "═══════════════════════════════════════\n"
        texto += "         RESUMEN DE PROCESAMIENTO         \n"
        texto += "═══════════════════════════════════════\n\n"
        
        # Registros
        if 'registros_originales' in stats:
            texto += f"📊 Registros originales:      {stats['registros_originales']:,}\n"
        
        if 'columnas_eliminadas' in stats:
            texto += f"🗑️ Columnas eliminadas:       {stats['columnas_eliminadas']:,}\n"
        
        if 'filas_nulas_eliminadas' in stats:
            texto += f"❌ Filas nulas eliminadas:    {stats['filas_nulas_eliminadas']:,}\n"
        
        if 'registros_anulados' in stats:
            texto += f"🚫 Registros anulados:        {stats['registros_anulados']:,}\n"
        
        if 'fechas_invalidas' in stats:
            texto += f"⚠️  Fechas inválidas:          {stats['fechas_invalidas']:,}\n"
        
        if 'duplicados_eliminados' in stats:
            texto += f"♻️  Duplicados eliminados:     {stats['duplicados_eliminados']:,}\n"
        
        if 'contratos_divididos' in stats:
            texto += f"📅 Contratos divididos:       {stats['contratos_divididos']:,}\n"
        
        texto += "\n───────────────────────────────────────\n"
        
        if 'certificados_generados' in stats:
            texto += f"📋 Certificados generados:    {stats['certificados_generados']:,}\n"
        
        if 'registros_finales' in stats:
            texto += f"✅ Registros finales:         {stats['registros_finales']:,}\n"
        
        if 'tiempo_formateado' in stats:
            texto += f"⏱️  Tiempo de procesamiento:   {stats['tiempo_formateado']}\n"
        
        texto += "\n═══════════════════════════════════════\n"
        
        if 'archivo_salida' in stats:
            nombre = os.path.basename(stats['archivo_salida'])
            texto += f"\n💾 Archivo generado:\n{nombre}"
        
        return texto
    
    def abrir_carpeta_salida(self):
        """Abre la carpeta data/clean donde se guardó el archivo de salida"""
        directorio_salida = os.path.join("data", "clean")
        
        if not os.path.exists(directorio_salida):
            QMessageBox.warning(
                self,
                "Error",
                "La carpeta data/clean no existe"
            )
            return
        
        # Abrir carpeta según el sistema operativo
        import subprocess
        import platform
        
        sistema = platform.system()
        
        try:
            if sistema == "Windows":
                os.startfile(directorio_salida)
            elif sistema == "Darwin":  # macOS
                subprocess.Popen(["open", directorio_salida])
            else:  # Linux
                subprocess.Popen(["xdg-open", directorio_salida])
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"No se pudo abrir la carpeta:\n{str(e)}"
            )