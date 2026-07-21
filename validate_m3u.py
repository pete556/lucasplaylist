#!/usr/bin/env python3
"""
Validador de M3U y generador de playlists para VLC
Autor: pete556
"""

import os
import sys
import requests
from urllib.parse import urlparse
from pathlib import Path


class M3UValidator:
    def __init__(self):
        self.timeout = 5
        self.valid_channels = []
        self.invalid_channels = []
        
    def load_playlists(self, filename='playlists.txt'):
        """
        Carga los enlaces M3U desde un archivo
        """
        if not os.path.exists(filename):
            print(f"❌ Error: No existe '{filename}'")
            print(f"\n📝 Crea un archivo '{filename}' con tus enlaces M3U, por ejemplo:")
            print("https://ejemplo.com/playlist1.m3u")
            print("https://ejemplo.com/playlist2.m3u")
            return []
        
        with open(filename, 'r') as f:
            links = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        return links
    
    def validate_url(self, url):
        """
        Valida que una URL sea accesible
        """
        try:
            response = requests.head(url, timeout=self.timeout, allow_redirects=True)
            return response.status_code == 200
        except:
            try:
                response = requests.get(url, timeout=self.timeout, stream=True)
                return response.status_code == 200
            except:
                return False
    
    def parse_m3u_content(self, url):
        """
        Descarga y parsea el contenido de un M3U
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            if response.status_code != 200:
                return []
            
            lines = response.text.split('\n')
            channels = []
            current_info = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('#EXTINF:'):
                    current_info = line
                elif line.startswith('http') and current_info:
                    channels.append({
                        'info': current_info,
                        'url': line,
                        'name': self._extract_channel_name(current_info)
                    })
                    current_info = None
            
            return channels
        except Exception as e:
            print(f"⚠️  Error descargando {url}: {str(e)}")
            return []
    
    def _extract_channel_name(self, extinf_line):
        """
        Extrae el nombre del canal de una línea EXTINF
        """
        try:
            # Formato: #EXTINF:-1,Nombre del Canal
            parts = extinf_line.split(',')
            if len(parts) > 1:
                return parts[-1].strip()
            return "Canal Desconocido"
        except:
            return "Canal Desconocido"
    
    def validate_channels(self, channels):
        """
        Valida cada canal de la lista
        """
        valid = []
        invalid = []
        
        for i, channel in enumerate(channels, 1):
            sys.stdout.write(f"\r🔍 Validando... {i}/{len(channels)}")
            sys.stdout.flush()
            
            if self.validate_url(channel['url']):
                valid.append(channel)
            else:
                invalid.append(channel)
        
        print()  # Nueva línea después del progreso
        return valid, invalid
    
    def generate_vlc_playlist(self, channels, output_file='vlc_playlist.m3u'):
        """
        Genera un archivo M3U compatible con VLC
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n')
            for channel in channels:
                f.write(f"{channel['info']}\n")
                f.write(f"{channel['url']}\n")
        
        return output_file
    
    def run(self):
        """
        Ejecuta el flujo completo de validación
        """
        print("\n" + "="*50)
        print("🎬 Validador de M3U - LucasPlaylist")
        print("="*50 + "\n")
        
        # 1. Cargar playlists
        print("📥 Cargando enlaces M3U...")
        playlist_urls = self.load_playlists()
        
        if not playlist_urls:
            return
        
        print(f"✅ Se encontraron {len(playlist_urls)} enlace(s)\n")
        
        # 2. Descargar y parsear canales
        print("📡 Descargando playlists...")
        all_channels = []
        for url in playlist_urls:
            print(f"  • {url}")
            channels = self.parse_m3u_content(url)
            all_channels.extend(channels)
            print(f"    → {len(channels)} canales encontrados")
        
        if not all_channels:
            print("\n❌ No se encontraron canales para validar")
            return
        
        print(f"\n📊 Total de canales: {len(all_channels)}\n")
        
        # 3. Validar canales
        print("🔗 Validando disponibilidad de canales...")
        valid, invalid = self.validate_channels(all_channels)
        
        # 4. Resultados
        print(f"\n✅ Canales válidos: {len(valid)}")
        print(f"❌ Canales no disponibles: {len(invalid)}")
        
        if valid:
            print(f"\n📋 Canales validados:")
            for channel in valid:
                print(f"  ✓ {channel['name']}")
        
        if invalid:
            print(f"\n⚠️  Canales no disponibles:")
            for channel in invalid:
                print(f"  ✗ {channel['name']}")
        
        # 5. Generar playlist para VLC
        if valid:
            output_file = self.generate_vlc_playlist(valid)
            print(f"\n✨ Playlist generada: {output_file}")
            print(f"\n🎬 Abre con VLC usando:")
            print(f"   vlc {output_file}")
            print(f"\n   O simplemente abre el archivo con VLC directamente\n")
        
        print("="*50 + "\n")


if __name__ == '__main__':
    validator = M3UValidator()
    validator.run()
