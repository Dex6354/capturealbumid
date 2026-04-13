import streamlit as st
from ytmusicapi import YTMusic

# Configuração da página
st.set_page_config(page_title="Buscador de Album ID", layout="centered")

st.title("🎵 Buscar Album ID (YouTube Music)")
st.write("Extrai o `browseId` a partir do Song ID.")

# Campo de entrada
song_id = st.text_input("Digite o Song ID:", value="ikFFVfObwss")

if st.button("Buscar", type="primary"):
    if song_id:
        with st.spinner("Consultando a API..."):
            try:
                ytmusic = YTMusic()
                
                # Obtém os dados do endpoint /next
                playlist = ytmusic.get_watch_playlist(videoId=song_id)
                
                # Verifica se há faixas e se a chave 'album' existe
                if playlist.get('tracks'):
                    track = playlist['tracks'][0]
                    album_info = track.get('album')
                    
                    if album_info:
                        album_id = album_info.get('id')
                        st.success("Album ID encontrado!")
                        st.code(album_id, language="text")
                    else:
                        st.warning("Esta música não possui um Album ID associado (pode ser um single ou upload de usuário).")
                else:
                    st.error("Nenhuma informação de faixa encontrada.")
                    
            except Exception as e:
                st.error(f"Erro técnico: {str(e)}")
    else:
        st.warning("Por favor, insira um Song ID.")
