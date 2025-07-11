import streamlit as st
from search_dense import search_dense
from search_hybrid import search_hybrid



st.set_page_config(page_title="PGVector Hybrid Search", layout="wide")

st.title("PGVector Hybrid Search App")
st.markdown("Search across Annual Reports and Earnings Calls using Dense or Hybrid Search")

query = st.text_input("Enter your search query")

search_type = st.radio("Search Method", ["Dense", "Hybrid"], horizontal=True)

if st.button("Search") and query.strip():
    with st.spinner("Searching..."):
        if search_type == "Dense":
            results = search_dense(query)
        else:
            results = search_hybrid(query)

    st.success(f"Top {len(results)} results for: `{query}`")

    for r in results:
        st.write(f"** Document:** `{r['doc_name']}`")
        st.write(f"**Score:** `{r.get('hybrid', r.get('score', 0)):.4f}`")
        st.markdown(f"> {r['chunk'][:500]}...")
        st.markdown("---")


