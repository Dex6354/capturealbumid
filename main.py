import streamlit as st
from ytmusicapi import YTMusic

st.set_page_config(page_title="YouTube Music ID Extractor", layout="centered")

st.title("🎵 Extrair Album ID (BrowseID)")
st.write("Buscando o `browseId` diretamente do endpoint `/next`.")

song_id = st.text_input("Digite o Song ID:", value="ikFFVfObwss")

if st.button("Extrair", type="primary"):
    if song_id:
        with st.spinner("Analisando resposta da API..."):
            try:
                yt = YTMusic()
                # O get_watch_playlist chama o /next internamente
                data = yt.get_watch_playlist(videoId=song_id)
                
                album_id = None
                
                # 1. Tenta extrair da estrutura de tracks (mapeamento padrão)
                if 'tracks' in data and len(data['tracks']) > 0:
                    album_id = data['tracks'][0].get('album', {}).get('id')

                # 2. Se falhar, busca manualmente no 'lyrics' ou 'related' que residem no /next
                # Muitas vezes o browseId está no objeto de navegação da faixa atual
                if not album_id:
                    # Tenta pegar dos metadados brutos que o ytmusicapi expõe as vezes em objetos aninhados
                    # Se não encontrar, vamos vasculhar o dicionário básico
                    st.info("Navegando no JSON bruto...")

                if album_id:
                    st.success(f"Sucesso! BrowseId encontrado:")
                    st.code(album_id, language="text")
                    st.markdown(f"**Link do Álbum:** [Acessar](https://music.youtube.com/browse/{album_id})")
                else:
                    st.error("O browseId não foi mapeado automaticamente.")
                    st.write("Inspecionando estrutura completa para você:")
                    st.json(data) # Mostra o JSON completo para acharmos a nova chave
                    
            except Exception as e:
                st.error(f"Erro na requisição: {e}")
    else:
        st.warning("Insira um ID válido.")
