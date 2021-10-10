from collections import defaultdict

import streamlit as st

dataset = (
    {
        'id': "50e157816b",
        'date': "2021-08-23",
        'product_id': 23356,
        'review': "Absolutely loved it.",
    },
    {
        'id': "113649fa84",
        'date': "2020-02-12",
        'product_id': 23356,
        'review': "Didn't work as I expected but happy anyway.",
    },
    {
        'id': "fc19cd0ba8",
        'date': "2020-01-26",
        'product_id': 34567,
        'review': "Seem to last just as long as other batteries I have paid more for.",
    },
    {
        'id': "b7edf6adab",
        'date': "2019-11-04",
        'product_id': 85403,
        'review': "Not the quality they describe. Absolute trash. Thumbs down.",
    },
)

initial_labels = [
    "positive",
    "negative",
    "neutral",
]

if 'idx' not in st.session_state:
    st.session_state.idx = 0

if 'annotations' not in st.session_state:
    st.session_state.annotations = defaultdict(lambda: "unknown")

if 'available_labels' not in st.session_state:
    st.session_state.available_labels = initial_labels


with st.form(key='add-label', clear_on_submit=True):
    new_label = st.text_input("Add new label to list", "")
    submitted = st.form_submit_button("Add label")
    if submitted and new_label != "" and new_label not in st.session_state.available_labels:
        st.session_state.available_labels.append(new_label)

def show_sample(container, idx):
    with container.container():
        st.markdown(f"Date: `{dataset[idx]['date']}`")
        st.markdown(f"Review: `{dataset[idx]['review']}`")

def set_label(label, idx):
    st.session_state.annotations[dataset[idx]['id']] = label

with st.form('labeling', clear_on_submit=True):

    data_container = st.empty()

    show_sample(data_container, st.session_state.idx)
    selected_label = st.radio("Select review sentiment label:", sorted(st.session_state.available_labels))

    submit_col, skip_col = st.columns(2)
    submit = submit_col.form_submit_button("submit")
    skip = skip_col.form_submit_button("skip")

    if submit:
        set_label(selected_label, st.session_state.idx)

    if submit or skip:
        st.session_state.idx += 1
        if st.session_state.idx < len(dataset):
            show_sample(data_container, st.session_state.idx)
        else:
            data_container.text("No more data to annotate")

st.write(st.session_state.annotations)
