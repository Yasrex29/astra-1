import streamlit as st
import cv2
import numpy as np
from detector import process_frame
from auth import login, register

st.set_page_config(page_title="SafeCrowd AI",layout="wide")

st.title("SafeCrowd AI - Crowd Safety Platform")

menu = ["Login","Register"]

choice = st.sidebar.selectbox("Menu",menu)

if choice == "Register":

    st.subheader("Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password",type="password")

    if st.button("Register"):

        if register(username,password):
            st.success("Account created")
        else:
            st.error("User already exists")

if choice == "Login":

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password",type="password")

    if st.button("Login"):

        if login(username,password):

            st.success("Login successful")

            st.subheader("Crowd Monitoring Dashboard")

            video_file = st.file_uploader("Upload Video")

            if video_file:

                tfile = open("temp.mp4","wb")
                tfile.write(video_file.read())

                cap = cv2.VideoCapture("temp.mp4")

                frame_window = st.image([])

                while cap.isOpened():

                    ret,frame = cap.read()

                    if not ret:
                        break

                    frame,count = process_frame(frame)

                    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

                    frame_window.image(frame)

                    st.sidebar.metric("Crowd Count",count)

        else:
            st.error("Invalid login")
