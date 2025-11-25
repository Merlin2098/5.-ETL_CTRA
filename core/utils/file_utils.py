# core/utils/file_utils.py
"""
Utilidades para manejo seguro de archivos y directorios
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Optional, Tuple
import tempfile


class FileUtils:
    """
    Utilidades para operaciones seguras con archivos
    """
    
    @staticmethod
    def safe_delete(file_path: str) -> bool:
        """
        Elimina archivo de forma segura (con verificación)
        
        Args:
            file_path: Ruta del archivo a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                path.unlink()
                return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def safe_delete_dir(dir_path: str) -> bool:
        """
        Elimina directorio de forma segura
        
        Args:
            dir_path: Ruta del directorio a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            path = Path(dir_path)
            if path.exists() and path.is_dir():
                shutil.rmtree(path)
                return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Obtiene tamaño de archivo en bytes
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            int: Tamaño en bytes, 0 si no existe
        """
        try:
            return os.path.getsize(file_path) if os.path.exists(file_path) else 0
        except Exception:
            return 0
    
    @staticmethod
    def get_file_size_readable(file_path: str) -> str:
        """
        Obtiene tamaño de archivo en formato legible
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            str: Tamaño formateado (ej: "1.5 MB")
        """
        size_bytes = FileUtils.get_file_size(file_path)
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    @staticmethod
    def ensure_dir(directory: str) -> bool:
        """
        Asegura que un directorio exista (crea si no existe)
        
        Args:
            directory: Ruta del directorio
            
        Returns:
            bool: True si existe o se creó correctamente
        """
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> List[Path]:
        """
        Lista archivos en un directorio
        
        Args:
            directory: Directorio a listar
            pattern: Patrón para filtrar archivos
            
        Returns:
            List[Path]: Lista de rutas de archivos
        """
        try:
            path = Path(directory)
            if path.exists() and path.is_dir():
                return list(path.glob(pattern))
            return []
        except Exception:
            return []
    
    @staticmethod
    def copy_file_safe(source: str, destination: str) -> bool:
        """
        Copia archivo de forma segura
        
        Args:
            source: Archivo origen
            destination: Archivo destino
            
        Returns:
            bool: True si se copió correctamente
        """
        try:
            shutil.copy2(source, destination)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_file_hash(file_path: str, algorithm: str = "md5") -> Optional[str]:
        """
        Calcula hash de un archivo
        
        Args:
            file_path: Ruta del archivo
            algorithm: Algoritmo de hash (md5, sha1, sha256)
            
        Returns:
            str: Hash del archivo o None si hay error
        """
        try:
            hash_func = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception:
            return None
    
    @staticmethod
    def is_valid_excel_file(file_path: str) -> bool:
        """
        Verifica si un archivo es un Excel válido
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            bool: True si es un archivo Excel válido
        """
        try:
            path = Path(file_path)
            valid_extensions = {'.xlsx', '.xls'}
            return (path.exists() and 
                    path.is_file() and 
                    path.suffix.lower() in valid_extensions and
                    path.stat().st_size > 0)
        except Exception:
            return False
    
    @staticmethod
    def create_temp_file(prefix: str = "temp_", suffix: str = ".tmp") -> str:
        """
        Crea un archivo temporal
        
        Args:
            prefix: Prefijo del nombre
            suffix: Sufijo del nombre
            
        Returns:
            str: Ruta del archivo temporal creado
        """
        try:
            temp_file = tempfile.NamedTemporaryFile(
                prefix=prefix, 
                suffix=suffix, 
                delete=False
            )
            temp_file.close()
            return temp_file.name
        except Exception:
            return ""
    
    @staticmethod
    def get_file_creation_time(file_path: str) -> Optional[float]:
        """
        Obtiene tiempo de creación del archivo
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            float: Timestamp de creación o None
        """
        try:
            return os.path.getctime(file_path)
        except Exception:
            return None
    
    @staticmethod

    @staticmethod
    def open_file_explorer(folder_path: str) -> bool:
        """
        Abre el explorador de archivos en la carpeta especificada
        Compatible con Windows, macOS y Linux
        
        Args:
            folder_path: Ruta de la carpeta a abrir
            
        Returns:
            bool: True si se abrió correctamente
        """
        import platform
        import subprocess
        
        try:
            path = Path(folder_path)
            if not path.exists():
                return False
            
            system = platform.system()
            
            if system == "Windows":
                # Windows: usar os.startfile
                os.startfile(str(path))
            elif system == "Darwin":
                # macOS: usar comando open
                subprocess.run(["open", str(path)], check=True)
            elif system == "Linux":
                # Linux: usar xdg-open
                subprocess.run(["xdg-open", str(path)], check=True)
            else:
                return False
            
            return True
            
        except Exception:
            return False

    def get_file_modification_time(file_path: str) -> Optional[float]:
        """
        Obtiene tiempo de modificación del archivo
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            float: Timestamp de modificación o None
        """
        try:
            return os.path.getmtime(file_path)
        except Exception:
            return None