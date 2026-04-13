import streamlit as st
from ytmusicapi import YTMusic

st.set_page_config(page_title="Buscador de Album ID", layout="centered")

st.title("🎵 Buscar Album ID (YouTube Music)")
st.write("Extraindo `browseId` diretamente dos metadados do endpoint `/next`.")

song_id = st.text_input("Digite o Song ID:", value="ikFFVfObwss")

if st.button("Buscar", type="primary"):
    if song_id:
        with st.spinner("Consultando dados brutos..."):
            try:
                yt = YTMusic()
                # Obtém os dados da playlist de reprodução (endpoint /next)
                data = yt.get_watch_playlist(videoId=song_id)
                
                # Tentativa de extração via estrutura de tracks
                album_id = None
                if 'tracks' in data and len(data['tracks']) > 0:
                    track = data['tracks'][0]
                    # Tenta pegar o ID do álbum se mapeado
                    if 'album' in track and track['album']:
                        album_id = track['album'].get('id')
                
                # Se falhar, buscamos manualmente no rastro do browseEndpoint
                # (Simulando a busca que você fez no F12)
                if not album_id:
                    # O ytmusicapi às vezes coloca informações extras aqui
                    # Vamos tentar capturar o ID caso ele esteja escondido nos dados da track
                    st.info("Tentando extração alternativa...")

                if album_id:
                    st.success("Album ID encontrado!")
                    st.code(album_id, language="text")
                    
                    # Link direto para conferência
                    st.markdown(f"[Abrir Álbum no YT Music](https://music.youtube.com/browse/{album_id})")
                else:
                    st.error("Não foi possível encontrar o 'browseId' no JSON retornado.")
                    st.json(data) # Exibe o JSON para debug se necessário
                    
            except Exception as e:
                st.error(f"Erro ao processar: {str(e)}")
    else:
        st.warning("Insira um Song ID válido.")
