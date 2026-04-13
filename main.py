import streamlit as st
from ytmusicapi import YTMusic

# Configuração da página
st.set_page_config(page_title="Buscador de Album ID", layout="centered")

st.title("🎵 Buscar Album ID (YouTube Music)")
st.write("Extrai o `browseId` (MPREb_...) a partir do endpoint `/next`.")

# Campo de entrada
song_id = st.text_input("Digite o Song ID (ex: ikFFVfObwss):", value="ikFFVfObwss")

if st.button("Buscar", type="primary"):
    if song_id:
        with st.spinner("Consultando a API..."):
            try:
                ytmusic = YTMusic()
                
                # A função get_watch_playlist consome o endpoint /next internamente
                playlist = ytmusic.get_watch_playlist(videoId=song_id)
                
                # Navega no JSON de resposta para pegar o ID do álbum
                album_id = playlist['tracks'][0]['album']['id']
                
                if album_id and album_id.startswith("MPREb_"):
                    st.success("Album ID encontrado com sucesso!")
                    st.code(album_id, language="text")
                else:
                    st.warning("Álbum não encontrado para este Song ID.")
                    
            except Exception as e:
                st.error(f"Erro ao consultar a API: {e}")
    else:
        st.warning("Por favor, preencha o Song ID.")
