"""
Gestión centralizada de rutas para desarrollo y distribución
Versión 2.0 - Compatible con PyInstaller
"""
import sys
from pathlib import Path


class AppPaths:
    """Gestión de rutas compatible con PyInstaller"""
    
    @staticmethod
    def get_base_path() -> Path:
        """
        Devuelve la ruta base del proyecto.
        
        Returns:
            Path: Ruta base (sys._MEIPASS en bundle, directorio raíz en desarrollo)
        """
        if getattr(sys, 'frozen', False):
            # Ejecutando como bundle de PyInstaller
            return Path(sys._MEIPASS)
        else:
            # Ejecutando en desarrollo
            return Path(__file__).parent.parent
    
    @staticmethod
    def get_data_dir() -> Path:
        """
        Carpeta data/ en el directorio del ejecutable.
        
        Returns:
            Path: Ruta a data/ (junto al .exe en producción, en proyecto en dev)
        """
        if getattr(sys, 'frozen', False):
            # En producción: junto al .exe
            return Path(sys.executable).parent / "data"
        else:
            # En desarrollo
            return AppPaths.get_base_path() / "data"
    
    @staticmethod
    def get_raw_dir() -> Path:
        """Carpeta data/raw/ para datasets sin procesar"""
        return AppPaths.get_data_dir() / "raw"
    
    @staticmethod
    def get_clean_dir() -> Path:
        """Carpeta data/clean/ para datasets limpios"""
        return AppPaths.get_data_dir() / "clean"
    
    @staticmethod
    def get_output_dir() -> Path:
        """Carpeta data/output/ para certificados generados"""
        return AppPaths.get_data_dir() / "output"
    
    @staticmethod
    def get_templates_dir() -> Path:
        """Carpeta data/templates/ para plantillas .docx"""
        return AppPaths.get_data_dir() / "templates"
    
    @staticmethod
    def get_icons_dir() -> Path:
        """Carpeta gui/resources/ dentro del bundle"""
        return AppPaths.get_base_path() / "gui" / "resources"
    
    @staticmethod
    def get_themes_dir() -> Path:
        """Carpeta gui/themes/ dentro del bundle"""
        return AppPaths.get_base_path() / "gui" / "themes"
    
    @staticmethod
    def get_config_file() -> Path:
        """Archivo config/settings.json"""
        return AppPaths.get_base_path() / "config" / "settings.json"
    
    # ============================================
    # MÉTODO GENÉRICO PARA RECURSOS
    # ============================================
    @staticmethod
    def get_resource(relative_path: str) -> Path:
        """
        Obtiene ruta absoluta a cualquier recurso interno.
        Compatible con PyInstaller.
        
        Args:
            relative_path: Ruta relativa desde la raíz del proyecto
                          Ejemplo: "gui/resources/app.ico"
        
        Returns:
            Path: Ruta absoluta al recurso
        
        Example:
            >>> icon = AppPaths.get_resource("gui/resources/app.ico")
            >>> theme = AppPaths.get_resource("gui/themes/theme_dark.json")
        
        Note:
            Este método reemplaza a resource_path() para mantener
            un único sistema de gestión de rutas.
        """
        return AppPaths.get_base_path() / relative_path
    
    # ============================================
    # MÉTODOS DE UTILIDAD
    # ============================================
    @staticmethod
    def ensure_data_dirs():
        """
        Crea las carpetas de datos si no existen.
        Útil para primera ejecución o distribución limpia.
        """
        dirs_to_create = [
            AppPaths.get_raw_dir(),
            AppPaths.get_clean_dir(),
            AppPaths.get_output_dir(),
            AppPaths.get_templates_dir()
        ]
        
        for directory in dirs_to_create:
            directory.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def get_icon_path() -> Path:
        """
        Atajo para obtener el ícono de la aplicación.
        
        Returns:
            Path: Ruta al archivo app.ico
        """
        return AppPaths.get_icons_dir() / "app.ico"