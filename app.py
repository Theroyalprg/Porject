import streamlit as st
from PIL import Image
import io
from src.database import init_db, save_inspection, list_inspections, update_review
from src.pdf_ingest import ingest_pdf_bytes, search_chunks

st.set_page_config(page_title="Railway Infrastructure Intelligence", page_icon="🚆", layout="wide")
init_db()
st.title("🚆 Railway Infrastructure Intelligence")
st.caption("Minor Project-I prototype · Academic demo only; not for operational safety decisions.")
a, b, c = st.tabs(["Inspect image", "Manual knowledge base", "Inspection history"])

with a:
    image_file = st.file_uploader("Upload railway infrastructure image", type=["jpg","jpeg","png","webp"])
    asset = st.text_input("Asset / track reference (optional)")
    location = st.text_input("Location / chainage (optional)")
    notes = st.text_area("Inspection notes")
    if image_file:
        img_bytes = image_file.getvalue()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        st.image(img, use_container_width=True)
        st.warning("Railway-specific model weights are not bundled. Do not treat generic pretrained detections as railway defect findings.")
        if st.button("Save image as inspection record", type="primary"):
            rid = save_inspection(image_file.name, img_bytes, asset, location, notes)
            st.success(f"Saved inspection record #{rid}.")

with b:
    pdf = st.file_uploader("Upload a permitted railway technical manual PDF", type=["pdf"])
    if pdf and st.button("Extract and chunk PDF"):
        try:
            st.session_state["chunks"] = ingest_pdf_bytes(pdf.getvalue(), pdf.name)
            st.success(f"Created {len(st.session_state['chunks'])} page-aware chunks.")
        except Exception as e:
            st.error(f"PDF extraction failed: {e}")
    query = st.text_input("Search manual passages")
    if st.button("Search") and query.strip():
        hits = search_chunks(query, st.session_state.get("chunks", []))
        if not hits:
            st.info("No matching passage found in the currently indexed PDF.")
        for hit in hits:
            with st.expander(f"{hit['source']} · pages {hit['page_start']}–{hit['page_end']} · {hit['section'] or 'Section not detected'}"):
                st.write(hit["text"])
                st.caption("Baseline keyword search. Semantic embeddings/FAISS are a later milestone.")

with c:
    records = list_inspections()
    if records:
        st.dataframe(records, use_container_width=True, hide_index=True)
        rid = st.number_input("Record ID", min_value=1, step=1)
        status = st.selectbox("Review status", ["Pending review", "Reviewed", "Follow-up required", "Closed"])
        if st.button("Update review status"):
            update_review(int(rid), status)
            st.success("Updated.")
            st.rerun()
    else:
        st.info("No inspection records saved yet.")
st.divider()
st.caption("Limitations: no trained defect model, no validated engineering risk score, and no safety-critical use. Manual text extraction must be checked against original pages.")
