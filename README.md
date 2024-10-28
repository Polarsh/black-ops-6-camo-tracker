# Black Ops 6 Camo Tracker

Este proyecto en Python ayuda a los jugadores de *Call of Duty: Black Ops 6* a hacer seguimiento de los camuflajes de armas. Extrae datos de armas, categorías y requisitos de camuflaje desde una página web y los organiza en un archivo Excel.

## Requisitos

Instala las dependencias con:
```bash
pip install -r requirements.txt
```

## Uso

1. **Configura `categories.json`**: 
   Incluye las categorías y nombres de armas, con el formato:
   ```json
   [
     {
       "category": "Assault Rifles",
       "weapons": ["XM4", "AK-74"]
     }
   ]
   ```
2. **Ejecuta el script**:
   ```bash
   python camo_tracker
   ```

3. **Resultados**:
   - Los datos se guardarán en `camo_tracker.xlsx`, con columnas ordenadas por `"Category"` y `"Weapon"`.

## Estructura del Proyecto
```plaintext
.
├── categories.json         # Datos de categorías y armas
├── camo_tracker.py         # Script principal
├── requirements.txt        # Dependencias
└── README.md               # Documentación
```
