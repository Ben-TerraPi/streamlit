import streamlit as st


#>>>>>>>>>>>>>>>>>>>>> Streamlit page


st.set_page_config(
    page_title="About us",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded",
)

#>>>>>>>>>>>>>>>>>>>>>> Streamlit sidebar


with st.sidebar:
    st.logo("images/The_Phryges.svg.png")
    st.image("./images/logo-paris-2024.png")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>HOME page


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Title & intro

st.title('🏅 Paris JO 2024 - Data Visualization Project'
            )

st.markdown("""
**The Paris 2024 Olympic Games data visualization dashboard**
is a project developed as part of *Le Wagon* bootcamp @Rennes,
it showcases data from the 
**Paris 2024 Olympic games**.
""")

with st.container():

    col1, col2 = st.columns(2)

    with col1:
        st.caption("""
        Autors : 

        Benoît Dourdet ([GitHub](https://github.com/Ben-TerraPi))
            
        Maxime Mobailly ([GitHub](https://github.com/maxmob35))
            
        Matteo Cherief ([GitHub](https://github.com/Matteo-chf))
            
        Gautier Martin ([GitHub](https://github.com/Gautier35400)) 
            
        · December 2024
        
        Version 1.0
        """)
            
    
    with col2:
        st.image("images/Untitled (1) (1).png",use_container_width=False, width=300)

