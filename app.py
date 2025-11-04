import streamlit as st
import requests

# -------------------------------
# 🎨 Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Hyeongwol's Art Explorer",
    page_icon="🖼️",
    layout="wide",
)

st.title("🖼️ Hyeongwol's Global Art Explorer")
st.markdown("Explore masterpieces from **MET**, **Harvard**, and **Rijksmuseum** using public Open APIs.")

# -------------------------------
# 🔍 Search Input
# -------------------------------
query = st.text_input("Enter a keyword to search artworks:", "flower")

if not query:
    st.info("Please enter a keyword to start searching.")
    st.stop()

# -------------------------------
# 🎨 Display helper
# -------------------------------
def show_artwork_card(title, artist, year, image, museum_name):
    with st.container():
        st.markdown(f"### {title}")
        if image:
            st.image(image, use_container_width=True)
        else:
            st.info("No image available for this artwork.")
        st.markdown(f"**Artist:** {artist or 'Unknown'}")
        st.markdown(f"**Year:** {year or 'Unknown'}")
        st.caption(f"🏛️ Source: {museum_name}")
        st.divider()

# -------------------------------
# 🏛️ MET Museum API
# -------------------------------
st.header("🏙️ The Metropolitan Museum of Art (MET)")
met_url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={query}"

try:
    met_data = requests.get(met_url, timeout=10).json()
    object_ids = met_data.get("objectIDs") or []

    if not object_ids:
        st.warning("No artworks found in MET Museum.")
    else:
        for obj_id in object_ids[:3]:
            data = requests.get(
                f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}",
                timeout=10
            ).json()
            show_artwork_card(
                data.get("title"),
                data.get("artistDisplayName"),
                data.get("objectDate"),
                data.get("primaryImageSmall"),
                "MET Museum"
            )
except Exception as e:
    st.error(f"⚠️ MET API error: {e}")

# -------------------------------
# 🏛️ Harvard Art Museums API
# -------------------------------
st.header("🎓 Harvard Art Museums")
harvard_api_key = "apikey=DEMO_KEY"  # You can replace this with your own key
harvard_url = f"https://api.harvardartmuseums.org/object?{harvard_api_key}&title={query}&size=3"

try:
    harvard_data = requests.get(harvard_url, timeout=10).json()
    records = harvard_data.get("records", [])
    if not records:
        st.warning("No artworks found in Harvard Museum.")
    else:
        for record in records:
            show_artwork_card(
                record.get("title"),
                record.get("people", [{}])[0].get("name") if record.get("people") else "Unknown",
                record.get("dated"),
                record.get("primaryimageurl"),
                "Harvard Art Museums"
            )
except Exception as e:
    st.error(f"⚠️ Harvard API error: {e}")

# -------------------------------
# 🏛️ Rijksmuseum API (Netherlands)
# -------------------------------
st.header("🇳🇱 Rijksmuseum")
rijks_api_key = "0fiuZFh4"  # Replace with your key if needed
rijks_url = f"https://www.rijksmuseum.nl/api/en/collection?key={rijks_api_key}&q={query}&imgonly=True"

try:
    rijks_data = requests.get(rijks_url, timeout=10).json()
    artworks = rijks_data.get("artObjects", [])
    if not artworks:
        st.warning("No artworks found in Rijksmuseum.")
    else:
        for art in artworks[:3]:
            show_artwork_card(
                art.get("title"),
                art.get("principalOrFirstMaker"),
                art.get("longTitle"),
                art.get("webImage", {}).get("url"),
                "Rijksmuseum"
            )
except Exception as e:
    st.error(f"⚠️ Rijksmuseum API error: {e}")

st.success("✅ Search completed. Enjoy exploring art around the world!")
