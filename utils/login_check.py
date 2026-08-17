import hmac
import streamlit as st


def check_password():
    """Returns True if the user entered the correct password."""

    users = {
        "IND_abc": st.secrets["users"]["IND_abc"]["password"],
        "IND_xyz": st.secrets["users"]["IND_xyz"]["password"],
    }

    def password_entered():
        username = st.session_state["username"]
        password = st.session_state["password"]

        if (
            username in users
            and hmac.compare_digest(password, users[username])
        ):
            st.session_state["password_correct"] = True
            st.session_state["username_logged_in"] = username
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    # Already logged in
    #if password_correct doesn't exist / is False, this part won't return True
    if st.session_state.get("password_correct", False):
        return True

    # Stylings for the login page
    st.markdown("""
    <style>
        .login-subtitle {
            text-align: center;
            color: #71858F;
            font-size: 20px;
            margin-top: 15px;
            margin-bottom: 35px;
        }

        .stTextInput label p {
            font-size: 18px;
            font-weight: 600;
            color: #39505C;
        }

       .stTextInput {
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 10px;
        }

        [data-testid="stAlert"] {
            text-align: center;
            margin-top: 15px;
            margin-left: auto;
            margin-right: auto;
            width: 80%;
        }

        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
        }

        div[data-testid="stButton"] button {
            width: 100px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # login form
    # appears if not login before / credentials incorrect
    left, center, right = st.columns([3.5, 3, 3.5])
    with center:
        st.image("assets/proj_logo.png")

        st.markdown(
            """
            <div class="login-subtitle">
                <i>Sign in to access the Objection Assistant</i>
            </div>
            """,
            unsafe_allow_html=True
        )

    _, input_center, _ = st.columns([4, 2, 4])
    with input_center:
        st.text_input(
            "Username",
            key="username",
            placeholder="Enter your username"
        )

        st.text_input(
            "Password",
            type="password",
            key="password",
            placeholder="Enter your password",
        )

        # centralise the Login button
        # button_left, button_center, button_right = st.columns([3, 2, 3])
        # with button_center:
        st.button(
            "Login",
            type="primary",
            on_click=password_entered,
            use_container_width=True
        )

        if "password_correct" in st.session_state:
            st.error("😕 Incorrect username or password")

    return False