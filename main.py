from ytmusicapi import YTMusic

def get_album_id(song_id):
    ytmusic = YTMusic()
    
    try:
        # Pega as informações da música/player queue
        playlist = ytmusic.get_watch_playlist(videoId=song_id)
        
        # O albumId fica dentro dos metadados da primeira faixa
        album_id = playlist['tracks'][0]['album']['id']
        
        print(f"Song ID: {song_id}")
        print(f"Album ID: {album_id}")
        return album_id
        
    except Exception as e:
        print(f"Erro ao buscar o álbum: {e}")
        return None

# Execução
get_album_id("ikFFVfObwss")
