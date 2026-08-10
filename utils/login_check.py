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
        .login-title {
            text-align: center;
            color: #39505C;
            font-size: 40px;
            font-weight: 700;
            margin-top: 40px;
            margin-bottom: 5px;
        }

        .login-subtitle {
            text-align: center;
            color: #71858F;
            font-size: 22px;
            margin-bottom: 25px;
        }

        .stTextInput label p {
            font-size: 18px;
            font-weight: 600;
            color: #39505C;
        }

       .stTextInput {
            border-radius: 8px;
            font-size: 16px;
        }
    </style>
    """, unsafe_allow_html=True)

    # login form
    # appears if not login before / credentials incorrect
    left, center, right = st.columns([2.5, 5, 2.5])
    with center:
        st.markdown(
            """
            <div class="login-title">
                🏡 Property Tax Objection Assistant
            </div>

            <div class="login-subtitle">
                <i>Sign in to access the Objection Assistant</i>
            </div>
            """,
            unsafe_allow_html=True
        )

    left, center, right = st.columns([4, 2, 4])
    with center:
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
            on_change=password_entered
        )

        if "password_correct" in st.session_state:
            st.error("😕 Incorrect username or password")

    return False