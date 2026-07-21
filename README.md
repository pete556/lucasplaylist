# LucasPlaylist

Script para validar enlaces M3U y generar links para abrir en VLC.

## Características
- ✅ Valida enlaces M3U
- ✅ Verifica disponibilidad de canales
- ✅ Genera links para VLC
- ✅ Soporte para múltiples playlists

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### 1. Agregar tus enlaces M3U

Crea un archivo `playlists.txt` con tus enlaces:

```
https://ejemplo.com/playlist1.m3u
https://ejemplo.com/playlist2.m3u
https://ejemplo.com/playlist3.m3u
```

### 2. Ejecutar el validador

```bash
python validate_m3u.py
```

### 3. Resultado

Generará un archivo `vlc_playlist.m3u` con los canales validados.

Para abrir en VLC:

```bash
vlc vlc_playlist.m3u
```

## Estructura

- `validate_m3u.py` - Script principal de validación
- `playlists.txt` - Archivo con tus enlaces M3U (crear manualmente)
- `vlc_playlist.m3u` - Playlist generada (se crea automáticamente)
- `requirements.txt` - Dependencias
