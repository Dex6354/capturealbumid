import streamlit as st
from ytmusicapi import YTMusic

st.set_page_config(page_title="YTMusic Deep Extractor", layout="centered")

st.title("🎵 Extração Direta de Album ID")
st.write("Acessando o endpoint `/next` de forma bruta (Raw JSON).")

song_id = st.text_input("Digite o Song ID:", value="ikFFVfObwss")

if st.button("Buscar no JSON Real", type="primary"):
    if song_id:
        with st.spinner("Simulando requisição do player..."):
            try:
                yt = YTMusic()
                
                # Fazendo a chamada manual para o endpoint 'next'
                # Isso retorna o JSON exatamente como você vê no F12
                body = {"videoId": song_id}
                endpoint = "next"
                response = yt._send_request(endpoint, body)
                
                # Navegando no JSON para encontrar o browseId do Álbum
                # O caminho costuma ser: contents -> singleColumnMusicWatchNextResultsRenderer 
                # -> tabbedRenderer -> watchNextTabbedResultsRenderer -> tabs...
                
                album_id = None
                
                # Tentativa de busca recursiva simples para achar o MPREb_
                def find_browse_id(obj):
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            if k == "browseId" and isinstance(v, str) and v.startswith("MPREb_"):
                                return v
                            result = find_browse_id(v)
                            if result: return result
                    elif isinstance(obj, list):
                        for item in obj:
                            result = find_browse_id(item)
                            if result: return result
                    return None

                album_id = find_browse_id(response)

                if album_id:
                    st.success("BrowseId (Album ID) encontrado!")
                    st.code(album_id, language="text")
                    st.markdown(f"**Link:** [Ver no YT Music](https://music.youtube.com/browse/{album_id})")
                else:
                    st.error("Não foi possível localizar 'MPREb_' no JSON retornado.")
                    with st.expander("Inspecionar JSON completo (F12 style)"):
                        st.json(response)
                        
            except Exception as e:
                st.error(f"Erro na requisição: {e}")
