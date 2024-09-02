import streamlit as st
from langchain_helper import get_few_shot_db_chain

st.title("SVAM T-Shirts: Database Q&A 👕")

@st.cache_data
def fetch_response(question):
    chain = get_few_shot_db_chain(question)
    return chain.run(question)

question = st.text_input("Question: ",placeholder="Ex: What are different brands available in the store")
st.write("")

if question:
    try:
        response = fetch_response(question)
        st.write("")
        st.header("Answer")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.write("")
st.write("")
st.write("")
st.subheader("Sample Questions: ")
st.write(
    """
    - what is the costliest tshirt you have in your store and what is price of it along with its brand ?
    - what is stock_quantity of white nike tshirts availalbe ?
    - what will be the total revenue if all the blue adidas tshirts with discount has been sold ?
    - which brand has more number of xl tshirts?

   """
)

st.write("")
st.write("")
st.write("")
st.write("")
st.markdown(
    "[View this project on GitHub](https://github.com/viVeK21111/retail_insights)",
    unsafe_allow_html=True
)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8501))
