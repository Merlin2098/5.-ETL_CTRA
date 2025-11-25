# app.py (actualizado)
"""
App.py - Punto de Entrada Principal
Sistema de Certificados y ETL
Versión 4.0 - Inicialización optimizada con splash screen
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path de Python
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui.main_window import MainWindow
from gui.splash_screen import SplashScreen
from config.paths import AppPaths
from controllers.app_controller import AppController


def main():
    """Función principal de la aplicación"""
    
    # Crear aplicación INMEDIATAMENTE (sin operaciones bloqueantes)
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Certificados y ETL")
    app.setOrganizationName("CertificadosApp")
    
    # Configurar estilo de aplicación
    app.setStyle("Fusion")
    
    # Configurar icono de la aplicación (para taskbar)
    try:
        icon_path = AppPaths.get_icon_path()
        app.setWindowIcon(QIcon(str(icon_path)))
    except Exception as e:
        print(f"Advertencia: No se pudo cargar el icono de la aplicación: {e}")
    
    # Mostrar splash screen INMEDIATAMENTE
    # (la validación de directorios se hace dentro del splash)
    splash = SplashScreen()
    splash.show()
    
    # Procesar eventos para mostrar el splash inmediatamente
    app.processEvents()
    
    # Variable para almacenar la ventana principal
    main_window = None
    
    def on_loading_complete():
        """Callback cuando el splash screen termina"""
        nonlocal main_window
        
        # Inicializar controlador principal después del splash
        app_controller = AppController()
        
        # Crear y mostrar ventana principal con AppController
        main_window = MainWindow(app_controller)
        main_window.show()
        
        # Traer ventana al frente
        main_window.raise_()
        main_window.activateWindow()
        
        # Cleanup cuando se cierre la aplicación
        app.aboutToQuit.connect(app_controller.cleanup)
    
    # Conectar señal de carga completa
    splash.loading_complete.connect(on_loading_complete)
    
    # Iniciar animación de carga (ejecuta tareas en background)
    splash.start_loading()
    
    # Ejecutar aplicación
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()