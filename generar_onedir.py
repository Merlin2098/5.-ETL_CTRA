"""
Script de Generación de Ejecutable Onedir
Proyecto: ETL + Certificados
Genera un ejecutable Windows con carpeta distribuible

Autor: Richi
Fecha: 2025
"""

import os
import sys
import pkg_resources
import subprocess
import shutil
from pathlib import Path

# ==========================================================
# CONFIGURACIÓN
# ==========================================================
NOMBRE_EXE = "ETL_Certificados.exe"
MAIN_SCRIPT = "app.py"

DIST_PATH = "dist"
BUILD_PATH = "build"
SPEC_PATH = "spec"

EXCLUSIONES = [
    "pip", "wheel", "setuptools", "pkg_resources",
    "distutils", "ensurepip", "test", "tkinter.test",
    "pytest", "pytest_cov", "coverage", "notebook",
    "IPython", "jupyter"
]

# ==========================================================
# VALIDAR ENTORNO VIRTUAL
# ==========================================================
def validar_entorno_virtual():
    """Verifica que se esté ejecutando dentro de un entorno virtual"""
    print("=" * 60)
    print("🔍 VALIDACIÓN DE ENTORNO VIRTUAL")
    print("=" * 60)

    if sys.prefix == sys.base_prefix:
        print("❌ ERROR: No estás dentro de un entorno virtual (venv).")
        print("   Activa uno antes de continuar.")
        print("   Ejemplo Windows: venv\\Scripts\\activate")
        print("   Ejemplo Linux/Mac: source venv/bin/activate")
        sys.exit(1)

    print(f"✅ Entorno virtual detectado: {sys.prefix}\n")

    paquetes = sorted([(pkg.key, pkg.version) for pkg in pkg_resources.working_set])
    print(f"📦 Librerías instaladas ({len(paquetes)}):")
    for nombre, version in paquetes:
        flag = "🧹 (excluir)" if nombre in EXCLUSIONES else "✅"
        print(f"   {flag} {nombre:<25} {version}")
    print("\n")

# ==========================================================
# CONFIRMACIÓN MANUAL
# ==========================================================
def confirmar_ejecucion():
    """Solicita confirmación del usuario antes de continuar"""
    print("=" * 60)
    print("⚠️  CONFIRMACIÓN DE EJECUCIÓN")
    print("=" * 60)
    print("Este proceso generará un ejecutable Windows onedir.")
    print("La carpeta 'data' estará visible para que los usuarios")
    print("puedan acceder a sus archivos raw, clean, output y templates.\n")
    
    respuesta = input("¿Deseas generar el ejecutable ahora? (S/N): ").strip().lower()

    if respuesta not in ("s", "si", "sí"):
        print("\n🛑 Proceso cancelado por el usuario.")
        sys.exit(0)

    print("\n✅ Confirmado. Continuando con la generación...\n")

# ==========================================================
# LIMPIAR BUILDS ANTERIORES
# ==========================================================
def limpiar_builds():
    """Elimina carpetas de builds anteriores"""
    print("🧹 Limpiando builds anteriores...")
    for carpeta in [DIST_PATH, BUILD_PATH, SPEC_PATH]:
        if os.path.exists(carpeta):
            try:
                shutil.rmtree(carpeta)
                print(f"   ✅ Eliminado: {carpeta}")
            except Exception as e:
                print(f"   ⚠️  No se pudo eliminar {carpeta}: {e}")
    print()

# ==========================================================
# CONSTRUIR COMANDO PYINSTALLER
# ==========================================================
def construir_comando():
    """Construye el comando completo de PyInstaller"""
    base_dir = Path.cwd()

    comando = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",              # Modo directorio (no onefile)
        "--windowed",            # Sin consola (GUI)
        "--clean",               # Limpiar cache
        "--log-level", "WARN",   # Solo warnings y errores
        "--distpath", DIST_PATH,
        "--workpath", BUILD_PATH,
        "--specpath", SPEC_PATH,
        "--name", NOMBRE_EXE.replace(".exe", ""),
    ]

    # ======================================================
    # PATHS: Agregar rutas para imports
    # ======================================================
    # Directorio raíz (para encontrar config, controllers, core, gui)
    comando += ["--paths", str(base_dir)]

    # ======================================================
    # HIDDEN IMPORTS: Dependencias no detectadas automáticamente
    # ======================================================
    hidden_imports = [
    # PyQt5 core
    "PyQt5.QtCore",
    "PyQt5.QtGui", 
    "PyQt5.QtWidgets",
    
    # Pandas y sus dependencias
    "pandas",
    "openpyxl",
    
    # python-docx para Word
    "docx",
    "lxml",
    
    # win32com para conversión PDF (CRÍTICO)
    "win32com",
    "win32com.client",
    "pythoncom",
    "pywintypes",
    
    # Utilidades
    "pathlib",
    "json",
    ]
    
    for imp in hidden_imports:
        comando += ["--hidden-import", imp]

    # ======================================================
    # EXCLUSIONES: Módulos innecesarios
    # ======================================================
    for excl in EXCLUSIONES:
        comando += ["--exclude-module", excl]

    # ======================================================
    # ICONO DE LA APLICACIÓN
    # ======================================================
    ico_path = base_dir / "gui" / "resources" / "app.ico"
    if ico_path.exists():
        comando += ["--icon", str(ico_path)]
        print(f"   ✅ Icono encontrado: {ico_path}")
    else:
        print(f"   ⚠️  Advertencia: No se encontró el icono en {ico_path}")

    # ======================================================
    # ARCHIVOS Y CARPETAS DE DATOS (--add-data)
    # ======================================================
    print("\n📁 Agregando archivos y carpetas de datos...")
    
    # 1. CONFIG: settings.json
    config_settings = base_dir / "config" / "settings.json"
    if config_settings.exists():
        comando += ["--add-data", f"{config_settings};config"]
        print(f"   ✅ settings.json")
    else:
        print(f"   ⚠️  No se encontró config/settings.json")

    # 2. GUI THEMES: archivos JSON de temas
    themes_dir = base_dir / "gui" / "themes"
    if themes_dir.exists():
        for theme_file in themes_dir.glob("*.json"):
            comando += ["--add-data", f"{theme_file};gui/themes"]
            print(f"   ✅ {theme_file.name}")
    else:
        print(f"   ⚠️  No se encontró carpeta gui/themes")

    # 3. GUI RESOURCES: icono (ya incluido como --icon, pero también en bundle)
    if ico_path.exists():
        comando += ["--add-data", f"{ico_path};gui/resources"]

    # 4. DATA: Carpeta completa con estructura (raw, clean, output, templates)
    # Esta es la carpeta que queremos visible para el usuario
    data_dir = base_dir / "data"
    if data_dir.exists():
        # Incluir solo las subcarpetas necesarias con .gitkeep
        for subdir in ["raw", "clean", "output", "templates"]:
            subdir_path = data_dir / subdir
            if subdir_path.exists():
                # Buscar .gitkeep para mantener estructura
                gitkeep = subdir_path / ".gitkeep"
                if gitkeep.exists():
                    comando += ["--add-data", f"{gitkeep};data/{subdir}"]
                    print(f"   ✅ data/{subdir}/ (estructura)")
                
                # Si hay archivos importantes (como templates), incluirlos
                if subdir == "templates":
                    for template in subdir_path.glob("*.docx"):
                        comando += ["--add-data", f"{template};data/templates"]
                        print(f"   ✅ {template.name}")
    else:
        print(f"   ⚠️  No se encontró carpeta data/")

    # ======================================================
    # SCRIPT PRINCIPAL
    # ======================================================
    main_path = base_dir / MAIN_SCRIPT
    comando.append(str(main_path))
    
    return comando

# ==========================================================
# GENERAR EJECUTABLE
# ==========================================================
def generar_exe():
    """Ejecuta PyInstaller para generar el ejecutable"""
    print("=" * 60)
    print("🚀 INICIANDO GENERACIÓN DEL EJECUTABLE (MODO ONEDIR)")
    print("=" * 60)

    verificar_main()
    verificar_estructura()
    limpiar_builds()

    cmd = construir_comando()
    
    print("\n⚙️  Comando PyInstaller generado:")
    print("=" * 60)
    # Imprimir comando de forma legible
    for i, part in enumerate(cmd):
        if i == 0:
            print(f"{part} \\")
        elif part.startswith("--"):
            print(f"  {part} \\")
        else:
            print(f"    {part} \\")
    print("=" * 60)
    
    print("\n🔨 Compilando, por favor espera...\n")
    result = subprocess.run(cmd)

    print("\n" + "=" * 60)
    if result.returncode == 0:
        carpeta_exe = Path(DIST_PATH) / NOMBRE_EXE.replace(".exe", "")
        print(f"✅ GENERACIÓN COMPLETADA CORRECTAMENTE")
        print("=" * 60)
        print(f"\n📂 Carpeta de salida:")
        print(f"   {carpeta_exe.absolute()}")
        print(f"\n📦 Ejecutable principal:")
        print(f"   {(carpeta_exe / NOMBRE_EXE).absolute()}")
        print(f"\n💡 IMPORTANTE:")
        print(f"   - La carpeta 'data' estará visible en el bundle")
        print(f"   - Los usuarios pueden agregar/modificar archivos ahí")
        print(f"   - Distribuye toda la carpeta '{NOMBRE_EXE.replace('.exe', '')}/'")
    else:
        print("❌ ERROR EN LA GENERACIÓN")
        print("=" * 60)
        print("💡 Revisa los mensajes de error arriba.")
        print("   Posibles causas:")
        print("   - Faltan dependencias en el venv")
        print("   - Estructura de carpetas incorrecta")
        print("   - Imports problemáticos en el código")
    print("=" * 60)

# ==========================================================
# VERIFICAR SCRIPT PRINCIPAL
# ==========================================================
def verificar_main():
    """Verifica que exista el script principal"""
    ruta = Path.cwd() / MAIN_SCRIPT
    if not ruta.is_file():
        print(f"❌ ERROR: No se encontró '{MAIN_SCRIPT}' en el directorio actual.")
        print(f"   Asegúrate de ejecutar este script desde la raíz del proyecto.")
        sys.exit(1)
    else:
        print(f"✅ Archivo principal encontrado: {MAIN_SCRIPT}\n")

# ==========================================================
# VERIFICAR ESTRUCTURA DEL PROYECTO
# ==========================================================
def verificar_estructura():
    """Verifica que existan las carpetas y archivos necesarios"""
    print("🔍 Verificando estructura del proyecto:")
    print("=" * 60)
    
    base_dir = Path.cwd()
    
    # Carpetas críticas
    carpetas_requeridas = [
        "config",
        "controllers",
        "core",
        "core/etl",
        "core/certificates",
        "core/utils",
        "gui",
        "gui/tabs",
        "gui/themes",
        "gui/resources",
        "data",
        "data/raw",
        "data/clean",
        "data/output",
        "data/templates"
    ]
    
    # Archivos críticos
    archivos_requeridos = [
        "app.py",
        "config/paths.py",
        "config/settings.json",
        "gui/main_window.py",
        "gui/resources/app.ico",
        "gui/themes/theme_dark.json",
        "gui/themes/theme_light.json",
    ]
    
    todo_ok = True
    
    print("\n📁 Carpetas:")
    for carpeta in carpetas_requeridas:
        ruta = base_dir / carpeta
        if ruta.exists():
            print(f"   ✅ {carpeta}/")
        else:
            print(f"   ❌ {carpeta}/ NO ENCONTRADA")
            todo_ok = False
    
    print("\n📄 Archivos:")
    for archivo in archivos_requeridos:
        ruta = base_dir / archivo
        if ruta.exists():
            print(f"   ✅ {archivo}")
        else:
            print(f"   ⚠️  {archivo} no encontrado")
            # No marcamos como error crítico para algunos archivos
    
    if not todo_ok:
        print("\n❌ ERROR: Estructura del proyecto incompleta.")
        print("   Asegúrate de ejecutar este script desde la raíz del proyecto.")
        print("   Deben existir todas las carpetas core, config, gui, data, etc.")
        sys.exit(1)
    
    print("\n" + "=" * 60)

# ==========================================================
# CREAR README PARA DISTRIBUCIÓN
# ==========================================================
def crear_readme_distribucion():
    """Crea un README.txt para el usuario final"""
    carpeta_exe = Path(DIST_PATH) / NOMBRE_EXE.replace(".exe", "")
    
    if not carpeta_exe.exists():
        return
    
    readme_content = """
===============================================
ETL + CERTIFICADOS - GUÍA DE USO
===============================================

📦 CONTENIDO DEL PAQUETE:
- ETL_Certificados.exe: Ejecutable principal
- _internal/: Librerías y dependencias (NO MODIFICAR)
- data/: Carpeta de trabajo (VISIBLE Y MODIFICABLE)
  ├── raw/: Coloca aquí tus archivos Excel originales
  ├── clean/: Aquí se guardarán los datos procesados
  ├── output/: Certificados generados (Word y PDF)
  └── templates/: Plantillas Word para certificados

🚀 INSTRUCCIONES DE USO:

1. EJECUTAR LA APLICACIÓN:
   - Haz doble clic en ETL_Certificados.exe
   - No muevas archivos de la carpeta _internal/

2. PREPARAR TUS DATOS:
   - Coloca tu archivo Excel en data/raw/
   - Asegúrate de que tenga el formato correcto
   - Columnas esperadas: DNI, nombres, fechas, etc.

3. AGREGAR PLANTILLAS:
   - Coloca tu plantilla Word en data/templates/
   - Usa variables como {{nombre}}, {{dni}}, etc.
   - Ver documentación para lista completa de variables

4. USAR LA APLICACIÓN:
   a) Pestaña ETL:
      - Selecciona archivo raw
      - Ejecuta proceso ETL
      - Revisa archivo clean generado
   
   b) Pestaña Certificados:
      - Selecciona archivo clean
      - Selecciona plantilla
      - Aplica filtros (opcional)
      - Genera certificados

⚠️ IMPORTANTE:
- NO elimines la carpeta _internal/
- NO muevas el .exe fuera de esta carpeta
- La carpeta data/ es tu área de trabajo
- Los archivos clean y output se generan automáticamente

📝 ESTRUCTURA DE DIRECTORIOS:
ETL_Certificados/
├── ETL_Certificados.exe
├── _internal/ (NO TOCAR)
└── data/ (TU ÁREA DE TRABAJO)
    ├── raw/
    ├── clean/
    ├── output/
    └── templates/

💡 CONSEJOS:
- Mantén backups de tus archivos raw
- Revisa los archivos clean antes de generar certificados
- Los certificados se organizan en carpetas con timestamp

🆘 SOPORTE:
Si encuentras problemas, contacta al desarrollador
con una descripción detallada del error.

Desarrollado por: Richi
Versión: 1.0
===============================================
"""
    
    readme_path = carpeta_exe / "README.txt"
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"\n📝 README creado: {readme_path}")
    except Exception as e:
        print(f"\n⚠️  No se pudo crear README: {e}")

# ==========================================================
# EJECUCIÓN PRINCIPAL
# ==========================================================
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   GENERADOR DE EJECUTABLE - ETL + CERTIFICADOS")
    print("   Modo: Onedir (carpeta distribuible)")
    print("=" * 60 + "\n")
    
    try:
        validar_entorno_virtual()
        confirmar_ejecucion()
        generar_exe()
        crear_readme_distribucion()
        
        print("\n" + "=" * 60)
        print("🎉 PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Prueba el ejecutable localmente")
        print("   2. Verifica que la carpeta data/ sea accesible")
        print("   3. Distribuye toda la carpeta del ejecutable")
        print("   4. Incluye el README.txt para los usuarios finales\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)