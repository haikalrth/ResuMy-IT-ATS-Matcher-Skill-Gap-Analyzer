import streamlit as st
import pandas as pd
import ast
import plotly.graph_objects as go

# Google Drive Files
FILE_ID_JD = "1X68LndJS98ZIefRLEi5cwv3pl4-UMsol"
FILE_ID_CV = "13LYhqvUZoIpWHGS1-ijs0aeSRnswl_PB"

def gdrive_url(file_id):
    return f"https://drive.google.com/uc?id={file_id}"

st.set_page_config(
    page_title="ResuMy",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark"

if st.session_state.theme_mode == "Dark":
    THEME = {
        "bg_app": "#111111",
        "bg_sidebar": "#1A1A1A",
        "bg_card": "#1A1A1A",
        "bg_gap_card": "#181818",
        "text_main": "#FFFFFF",
        "text_muted": "#AAAAAA",
        "text_subtitle": "#888888",
        "text_sec_title": "#666666",
        "border": "#2a2a2a",
        "btn_border": "#2e2e2e",
        "btn_text": "#CCCCCC",
        "header_text": "white",
        "accent": "#E4002B",
        "plotly_bg": "#161616"
    }
else:
    THEME = {
        "bg_app": "#FAFAFA",
        "bg_sidebar": "#F0F2F5",
        "bg_card": "#FFFFFF",
        "bg_gap_card": "#FFFFFF",
        "text_main": "#1A1A1A",
        "text_muted": "#555555",
        "text_subtitle": "#666666",
        "text_sec_title": "#888888",
        "border": "#E0E0E0",
        "btn_border": "#D0D0D0",
        "btn_text": "#444444",
        "header_text": "#1A1A1A",
        "accent": "#E4002B",
        "plotly_bg": "#F5F5F5"
    }

st.markdown(f"""
<style>
header[data-testid="stHeader"] {{
    background-color: {THEME["bg_app"]} !important;
    border-bottom: 1px solid {THEME["border"]} !important;
    box-shadow: none !important;
}}
header[data-testid="stHeader"]::before {{
    content: "IT Skill Trend Analysis";
    color: {THEME["header_text"]} !important;
    font-size: 1.5rem !important;
    font-family: sans-serif;
    font-weight: 600;
    letter-spacing: 0.05em;
    position: absolute;
    left: 4.5rem;
    top: 50%;
    transform: translateY(-50%);
    pointer-events: none;
}}
html, body, [data-testid="stApp"] {{
    background-color: {THEME["bg_app"]} !important;
    color: {THEME["text_main"]};
}}
[data-testid="stSidebar"] {{
    background-color: {THEME["bg_sidebar"]} !important;
    border-right: 1px solid {THEME["border"]};
}}
[data-testid="stAppViewContainer"] > .main > .block-container {{
    padding-top: 5rem !important;
}}
div[data-testid="stSidebar"] .stButton > button {{
    width: 100%;
    background: transparent;
    color: {THEME["btn_text"]};
    border: 1px solid {THEME["btn_border"]};
    border-radius: 6px;
    padding: 10px 14px;
    text-align: left;
    font-size: 0.85rem;
    letter-spacing: 0.02em;
    transition: all 0.2s ease;
    margin-bottom: 4px;
}}
div[data-testid="stSidebar"] .stButton > button:hover {{
    background: {THEME["accent"]}22;
    border-color: {THEME["accent"]};
    color: {THEME["text_main"]};
}}
div[data-testid="stSidebar"] .stButton > button[aria-pressed="true"],
div[data-testid="stSidebar"] .stButton > button:focus {{
    background: {THEME["accent"]} !important;
    border-color: {THEME["accent"]} !important;
    color: #FFFFFF !important;
}}
[data-testid="stMetric"] {{
    background: {THEME["bg_card"]};
    border: 1px solid {THEME["border"]};
    border-radius: 10px;
    padding: 16px 20px;
}}
[data-testid="stMetricLabel"] {{ color: {THEME["text_muted"]} !important; font-size: 0.78rem; }}
[data-testid="stMetricValue"] {{ color: {THEME["text_main"]} !important; font-size: 1.5rem; }}
[data-testid="stMetricDelta"] {{ color: {THEME["accent"]} !important; }}
hr {{ border-color: {THEME["border"]}; }}
.stSelectbox label, .stNumberInput label {{ color: {THEME["text_muted"]} !important; font-size: 0.82rem; }}
.section-title {{
    font-size: 0.72rem;
    font-weight: 600;
    color: {THEME["text_sec_title"]};
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 6px;
}}
.page-title {{
    font-size: 1.7rem;
    font-weight: 800;
    color: {THEME["text_main"]};
    letter-spacing: -0.01em;
}}
.page-subtitle {{
    color: {THEME["text_subtitle"]};
    font-size: 0.88rem;
    margin-top: 4px;
    margin-bottom: 20px;
    max-width: 820px;
}}
.gap-card {{
    background: {THEME["bg_gap_card"]};
    border: 1px solid {THEME["border"]};
    border-left: 3px solid {THEME["accent"]};
    border-radius: 8px;
    padding: 20px 24px;
    margin-top: 8px;
}}
.gap-card h4 {{
    color: {THEME["text_muted"]};
    font-size: 0.72rem;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    margin-bottom: 10px;
    margin-top: 14px;
}}
.gap-card h4:first-child {{ margin-top: 0; }}
.gap-card ul {{ color: {THEME["text_muted"]}; font-size: 0.86rem; line-height: 1.7; padding-left: 18px; }}
.gap-card li {{ color: {THEME["text_muted"]}; font-size: 0.86rem; line-height: 1.7; }}
.gap-card li strong {{ color: {THEME["text_main"]}; }}
</style>
""", unsafe_allow_html=True)


def parse_skills(val):
    if isinstance(val, list):
        return val
    if not isinstance(val, str):
        return []
    val = val.strip()
    if val.startswith("["):
        try:
            return ast.literal_eval(val)
        except Exception:
            pass
    return [s.strip() for s in val.split(",") if s.strip()]


@st.cache_data(show_spinner="Loading data…")
def load_data():
    import gdown, os

    # Load JD
    df_jd = pd.read_csv(gdrive_url(FILE_ID_JD))
    df_jd["require_skills"] = df_jd["require_skills"].apply(parse_skills)
    df_jd["skill_count"] = df_jd["require_skills"].apply(len)

    # Load CV
    cv_path = "cv_dashboard.csv"
    if not os.path.exists(cv_path):
        gdown.download(gdrive_url(FILE_ID_CV), cv_path, quiet=False)
    df_cv = pd.read_csv(cv_path)
    df_cv["skills"] = df_cv["skills"].apply(parse_skills)
    df_cv["skill_count"] = df_cv["skills"].apply(len)

    # Explode skills
    df_jd_skills = (
        df_jd[["job_role", "require_skills"]]
        .assign(skill=lambda x: x["require_skills"])
        .explode("skill")
    )
    df_jd_skills["skill"] = df_jd_skills["skill"].str.strip().str.lower()
    df_jd_skills = df_jd_skills[df_jd_skills["skill"].notna() & (df_jd_skills["skill"] != "")]

    df_cv_skills = (
        df_cv[["cv_role", "skills"]]
        .assign(skill=lambda x: x["skills"])
        .explode("skill")
    )
    df_cv_skills["skill"] = df_cv_skills["skill"].str.strip().str.lower()
    df_cv_skills = df_cv_skills[df_cv_skills["skill"].notna() & (df_cv_skills["skill"] != "")].reset_index(drop=True)

    # Domain avg JD
    domain_avg = (
        df_jd.groupby("job_role")["skill_count"]
        .mean().sort_values(ascending=True).round(1).reset_index()
        .rename(columns={"skill_count": "avg_skill"})
    )

    # Signature JD
    total_jd_freq = df_jd_skills["skill"].value_counts()
    domain_skill_freq = df_jd_skills.groupby(["job_role", "skill"]).size().reset_index(name="domain_count")
    domain_skill_freq["global_count"] = domain_skill_freq["skill"].map(total_jd_freq)
    domain_skill_freq["specificity"] = (domain_skill_freq["domain_count"] / domain_skill_freq["global_count"]).round(3)
    sig_jd = (
        domain_skill_freq[domain_skill_freq["domain_count"] >= 5]
        .sort_values("specificity", ascending=False)
        .groupby("job_role").first().reset_index()
        [["job_role", "skill", "domain_count", "specificity"]]
        .sort_values("specificity", ascending=True)
    )

    # Role avg CV
    role_avg = (
        df_cv.groupby("cv_role")["skill_count"]
        .mean().sort_values(ascending=True).round(1).reset_index()
        .rename(columns={"skill_count": "avg_skill"})
    )

    # Signature CV
    total_cv_freq = df_cv_skills["skill"].value_counts()
    role_skill_freq = df_cv_skills.groupby(["cv_role", "skill"]).size().reset_index(name="role_count")
    role_skill_freq["global_count"] = role_skill_freq["skill"].map(total_cv_freq)
    role_skill_freq["specificity"] = (role_skill_freq["role_count"] / role_skill_freq["global_count"]).round(3)
    sig_cv = (
        role_skill_freq[role_skill_freq["role_count"] >= 3]
        .sort_values("specificity", ascending=False)
        .groupby("cv_role").first().reset_index()
        [["cv_role", "skill", "role_count", "specificity"]]
        .sort_values("specificity", ascending=True)
    )

    # Gap
    jd_freq = df_jd_skills["skill"].value_counts().reset_index()
    jd_freq.columns = ["skill", "jd_count"]
    cv_freq = df_cv_skills["skill"].value_counts().reset_index()
    cv_freq.columns = ["skill", "cv_count"]
    gap_df = pd.merge(jd_freq, cv_freq, on="skill", how="inner")
    gap_df["jd_pct"] = (gap_df["jd_count"] / gap_df["jd_count"].sum()) * 100
    gap_df["cv_pct"] = (gap_df["cv_count"] / gap_df["cv_count"].sum()) * 100
    gap_df["gap_score"] = 100 - ((gap_df["cv_pct"] / gap_df["jd_pct"]).round(5)) * 100
    gap_df = gap_df[gap_df["gap_score"] > 0]

    return {
        "df_jd":        df_jd,
        "df_cv":        df_cv,
        "df_jd_skills": df_jd_skills,
        "df_cv_skills": df_cv_skills,
        "domain_avg":   domain_avg,
        "sig_jd":       sig_jd,
        "role_avg":     role_avg,
        "sig_cv":       sig_cv,
        "gap_df":       gap_df,
    }


PLOTLY_LAYOUT = dict(
    paper_bgcolor=THEME["plotly_bg"],
    plot_bgcolor=THEME["plotly_bg"],
    font=dict(color=THEME["text_muted"], family="Inter, sans-serif", size=12),
    margin=dict(l=0, r=0, t=40, b=0),
    xaxis=dict(gridcolor=THEME["border"], gridwidth=1, zeroline=False, showline=False, tickcolor=THEME["text_muted"]),
    yaxis=dict(gridcolor="rgba(0,0,0,0)", zeroline=False, showline=False, tickcolor=THEME["text_muted"]),
    hoverlabel=dict(bgcolor=THEME["bg_card"], bordercolor=THEME["accent"], font=dict(color=THEME["text_main"], size=12)),
)


def hbar_chart(y_labels, x_vals, title, text_labels=None, reversed_axis=False,
               bar_color=THEME["accent"], height=420, x_title=""):
    hover_text = [
        f"<b>{lbl.title()}</b><br>{txt}" if text_labels else f"<b>{lbl.title()}</b><br>{x:.2f}"
        for lbl, x, txt in zip(y_labels, x_vals, text_labels if text_labels else [""]*len(y_labels))
    ]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=y_labels, x=x_vals, orientation="h",
        marker=dict(color=bar_color, line=dict(width=0)),
        text=text_labels, textposition="outside",
        textfont=dict(color=THEME["text_main"], size=10),
        hovertemplate="%{customdata}<extra></extra>",
        customdata=hover_text,
    ))
    layout = {**PLOTLY_LAYOUT}
    layout["title"] = dict(text=f"<b>{title}</b>", font=dict(color=THEME["text_main"], size=14), x=0, xanchor="left")
    layout["height"] = height
    layout["xaxis"]["title"] = x_title
    layout["xaxis"]["title_font"] = dict(color=THEME["text_subtitle"], size=11)
    layout["bargap"] = 0.35
    if reversed_axis:
        layout["yaxis"]["side"] = "right"
        layout["xaxis"]["autorange"] = "reversed"
    fig.update_layout(**layout)
    return fig


def make_top_n_chart(skills_df, role_col, selected_role, top_n, df_raw, title):
    data = (
        skills_df[skills_df[role_col] == selected_role]
        .groupby("skill").size().reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    n = min(top_n, len(data))
    data = data.head(n).sort_values("count", ascending=True)
    n_records = df_raw[df_raw[role_col] == selected_role].shape[0]
    pct = (data["count"] / n_records * 100).round(1)
    text_labels = [f"{c} ({p:.0f}%)" for c, p in zip(data["count"], pct)]
    return hbar_chart(
        y_labels=data["skill"].str.title().tolist(),
        x_vals=data["count"].tolist(),
        title=title, text_labels=text_labels,
        height=max(320, n * 52 + 80),
    )


def make_jumlah_skill_chart(avg_df, role_col, avg_col, title, reversed_axis=False):
    labels = avg_df[role_col].tolist()
    values = avg_df[avg_col].tolist()
    return hbar_chart(
        y_labels=labels, x_vals=values, title=title,
        text_labels=[f"{v}" for v in values],
        reversed_axis=reversed_axis,
        height=max(400, len(labels) * 28 + 80),
    )


def make_signature_chart(sig_df, role_col, title, reversed_axis=False):
    labels = sig_df[role_col].tolist()
    values = sig_df["specificity"].tolist()
    skills = sig_df["skill"].str.title().tolist()
    return hbar_chart(
        y_labels=labels, x_vals=values, title=title,
        text_labels=[f'"{s}" ({v:.0%})' for s, v in zip(skills, values)],
        reversed_axis=reversed_axis,
        height=max(400, len(labels) * 28 + 80), x_title="Specificity Score",
    )


def make_gap_chart(gap_df, top_n, ascending=False):
    data = (
        gap_df.sort_values("gap_score", ascending=ascending)
        .head(top_n)
        .sort_values("gap_score", ascending=not ascending)
    )
    labels   = data["skill"].str.title().tolist()
    jd_vals  = data["jd_pct"].round(3).tolist()
    gap_vals = data["gap_score"].round(2).tolist()
    h        = max(360, top_n * 52 + 80)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels, x=jd_vals, orientation="h",
        marker=dict(color=THEME["accent"], line=dict(width=0)),
        text=[f"{v:.3f}  ▏Gap {g:.1f}%" for v, g in zip(jd_vals, gap_vals)],
        textposition="outside",
        textfont=dict(color=THEME["text_muted"], size=10),
        hovertemplate="<b>%{y}</b><br>Industry: %{x:.3f}%<extra></extra>",
    ))
    layout = {**PLOTLY_LAYOUT, "height": h, "bargap": 0.38,
              "title": dict(text="<b>Industry Skill Demand</b>",
                            font=dict(color=THEME["text_main"], size=14), x=0)}
    fig.update_layout(**layout)
    return fig


# Sidebar Layout
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding: 16px 0 8px 0;'>
        <div style='font-size:2.4rem; margin-bottom:4px; color:{THEME["header_text"]}'><b>ResuMy</b></div>
        <div style='font-size:1.1rem; font-weight:800; color:#E4002B;
                    letter-spacing:0.08em; text-transform:uppercase;'>
            CC26-PSU006
        </div>
    </div>
    <hr style='border-color:{THEME["border"]}; margin: 10px 0 16px 0;'>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='color:{THEME['text_sec_title']};font-size:0.72rem;letter-spacing:0.08em;"
                "text-transform:uppercase;margin-bottom:8px;'>Dashboard Pages</div>",
                unsafe_allow_html=True)

    if "page" not in st.session_state:
        st.session_state.page = "industri"

    pages = {
        "industri": "Industry Demand Trends",
        "kandidat": "Candidate Characteristics",
        "gap":      "Skill Gap Analysis",
    }
    for key, label in pages.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key

   # Mode
    st.markdown("<br>" * 5, unsafe_allow_html=True) 
    st.markdown(f"<hr style='border-color:{THEME['border']}; margin:16px 0 12px 0;'>", unsafe_allow_html=True)
    
    col_label, col_switch = st.columns([3, 1])
    with col_label:
        label_text = "🌙 Dark Mode" if st.session_state.theme_mode == "Dark" else "☀️ Light Mode"
        st.markdown(f"<div style='color:{THEME['text_main']}; font-size:0.9rem; padding-top:2px;'>{label_text}</div>", unsafe_allow_html=True)
        
    with col_switch:
        switch_state = st.toggle(
            "Toggle Theme", 
            value=(st.session_state.theme_mode == "Dark"),
            label_visibility="collapsed"
        )
    
    new_mode = "Dark" if switch_state else "Light"
    if new_mode != st.session_state.theme_mode:
        st.session_state.theme_mode = new_mode
        st.rerun()

# Load data
try:
    D = load_data()
except Exception as e:
    st.error(f"**Error loading data:** {e}")
    st.stop()

page = st.session_state.page


# PAGE 1 Industry Demand Trends
if page == "industri":
    st.markdown(f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:has(div.page-title) {{
            position: -webkit-sticky; position: sticky; top: 0rem;
            background-color: {THEME["bg_app"]}; z-index: 999;
            padding-top: 4rem; padding-bottom: 1rem; margin-top: -4rem;
        }}
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="page-title">Industry Demand Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Business Question 1: What are the IT skill demand trends across various industrial roles, and which skills are universal versus specific to each role?</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Industry Roles", D["df_jd"]["job_role"].nunique())
    col2.metric("Total Job Postings",  f"{len(D['df_jd']):,}")
    col3.metric("Unique Skills",       D["df_jd_skills"]["skill"].nunique())

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="text-align:center">Top Skills</div>', unsafe_allow_html=True)

    ctrl1, ctrl2 = st.columns([3, 1])
    with ctrl1:
        selected_domain = st.selectbox("Select Industry Role",
                                       sorted(D["df_jd"]["job_role"].unique()),
                                       label_visibility="collapsed")
    with ctrl2:
        top_n_jd = st.selectbox("Top N", [3, 5, 10], index=1, label_visibility="collapsed")

    fig = make_top_n_chart(D["df_jd_skills"], "job_role", selected_domain, top_n_jd,
                           D["df_jd"], f"Top {top_n_jd} Skills for {selected_domain}")
    fig.update_layout(title_x=0.5, title_xanchor="center")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="text-align:center">All Roles Summary</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        fig_avg = make_jumlah_skill_chart(D["domain_avg"], "job_role", "avg_skill",
                                          "Average Number of Required Skills")
        fig_avg.update_layout(title_x=0.5, title_xanchor="center")
        st.plotly_chart(fig_avg, use_container_width=True)
    with col_right:
        fig_sig = make_signature_chart(D["sig_jd"], "job_role",
                                       "Signature Skills", reversed_axis=True)
        fig_sig.update_layout(title_x=0.5, title_xanchor="center")
        st.plotly_chart(fig_sig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="text-align:center">Conclusions & Recommendations</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="gap-card">
            <h4>Overall Dominant Skills</h4>
            <li>Python, SQL, Analytics, Reporting, and Excel are frequently found across many roles, indicating that these skills are universally required in various IT professions.</li>
            <br>
            <h4>Signature Role Skills</h4>
            <ul>
                <li>Artificial Intelligence → AI Engineer</li>
                <li>Machine Learning → Machine Learning Engineer</li>
                <li>Business Intelligence → BI Analyst</li>
                <li>Javascript → Web Developer</li>
                <li>Azure / AWS → Cloud Architect</li>
            </ul>
            <h4>Appearance Frequency vs Uniqueness</h4>
            <li>Python and Excel are ubiquitous across roles. Conversely, Artificial Intelligence and Machine Learning are highly specific and strongly tied to precise technical roles.</li>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="gap-card">
            <h4>Action Items</h4>
            <li>Signature skills unique to a role should serve as primary focus points in job postings. Meanwhile, universal skills found across multiple roles can be treated as baseline or supplementary requirements.</li>
        </div>
        """, unsafe_allow_html=True)


# PAGE 2 Candidate Characteristics
if page == "kandidat":
    st.markdown(f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:has(div.page-title) {{
            position: -webkit-sticky; position: sticky; top: 0rem;
            background-color: {THEME["bg_app"]}; z-index: 999;
            padding-top: 4rem; padding-bottom: 1rem; margin-top: -4rem;
        }}
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="page-title">Candidate Characteristics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Business Question 2: What are the skill ownership characteristics of candidates across various IT roles?</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Candidate Roles", D["df_cv"]["cv_role"].nunique())
    col2.metric("Total Candidates",      f"{len(D['df_cv']):,}")
    col3.metric("Unique Skills",       D["df_cv_skills"]["skill"].nunique())

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="text-align:center">Top Candidate Skills</div>', unsafe_allow_html=True)

    ctrl1, ctrl2 = st.columns([3, 1])
    with ctrl1:
        selected_role = st.selectbox("Select Candidate Role",
                                     sorted(D["df_cv"]["cv_role"].unique()),
                                     label_visibility="collapsed")
    with ctrl2:
        top_n_cv = st.selectbox("Top N", [3, 5, 10], index=1, label_visibility="collapsed")

    fig = make_top_n_chart(D["df_cv_skills"], "cv_role", selected_role, top_n_cv,
                           D["df_cv"], f"Top {top_n_cv} Skills for Candidate {selected_role}")
    fig.update_layout(title_x=0.5, title_xanchor="center")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="text-align:center">All Candidate Roles Summary</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        fig_avg = make_jumlah_skill_chart(D["role_avg"], "cv_role", "avg_skill",
                                          "Average Number of Candidate Skills")
        fig_avg.update_layout(title_x=0.5, title_xanchor="center")
        st.plotly_chart(fig_avg, use_container_width=True)
    with col_right:
        fig_sig = make_signature_chart(D["sig_cv"], "cv_role",
                                       "Candidate Signature Skills", reversed_axis=True)
        fig_sig.update_layout(title_x=0.5, title_xanchor="center")
        st.plotly_chart(fig_sig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="text-align:center">Conclusions & Recommendations</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="gap-card">
            <h4>Most Popular Skills</h4>
            <li>SQL and Testing are the most frequently appearing skills across all candidate profiles. Additionally, HTML and JavaScript are heavily populated within candidate resumes in several developer roles.</li>
            <br>
            <h4>Skill Count Variation per Role</h4>
            <li>Business Analysts possess the highest average number of listed skills (32.6 skills per CV), while Cloud Engineers maintain the lowest average profile breadth (8.1 skills per CV).</li>
            <h4>Candidate Signature Skill Patterns</h4>
            <li>Certain skills appear perfectly aligned with specific roles. For instance, A/B Testing appears on 100% of Data Scientist resumes, whereas ASP.NET is found on 77% of Business Analyst CVs.</li>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="gap-card">
            <h4>Action Items</h4>
            <li>Companies should deploy screening strategies oriented around signature skills to filter massive resume pipelines. Given the incredibly high baseline of universal skills like SQL and Testing listed by candidates across nearly all roles, focusing on role-specific skills with high uniqueness scores (e.g., "A/B Testing" for Data Scientists or "ASP.NET" for Business Analysts) will yield a significantly higher quality and more relevant candidate shortlist.</li>
        </div>
        """, unsafe_allow_html=True)


# PAGE 3 Skill Gap Analysis
elif page == "gap":
    st.markdown(f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:has(div.page-title) {{
            position: -webkit-sticky; position: sticky; top: 0rem;
            background-color: {THEME["bg_app"]}; z-index: 999;
            padding-top: 4rem; padding-bottom: 1rem; margin-top: -4rem;
        }}
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="page-title">Skill Gap Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Business Question 3: What is the skill gap between Industry Demand and Candidate availability?</div>', unsafe_allow_html=True)

    gap_df = D["gap_df"]
    high_gap_row = gap_df.sort_values("gap_score", ascending=False).iloc[0]
    low_gap_row  = gap_df.sort_values("gap_score", ascending=True).iloc[0]

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Tracked Skills", f"{len(gap_df):,}")
    m2.metric("Largest Discrepancy (Max Gap)",  f"{high_gap_row['gap_score']:.1f}%", f"{high_gap_row['skill'].title()}")
    m3.metric("Closest Alignment (Min Gap)", f"{low_gap_row['gap_score']:.1f}%",  f"{low_gap_row['skill'].title()}")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="text-align:center">Skill Discrepancy: Market Demand vs Talent Supply</div>', unsafe_allow_html=True)

    top_n_gap = st.selectbox("Display Top N Skill Gaps", [3, 5, 10], index=1, label_visibility="collapsed")

    col_l, col_r = st.columns(2)
    with col_l:
        fig_high = make_gap_chart(gap_df, top_n_gap, ascending=False)
        fig_high.update_layout(title=f"Top {top_n_gap} Largest Gaps",
                               title_x=0.5, title_xanchor="center")
        st.plotly_chart(fig_high, use_container_width=True)
    with col_r:
        fig_low = make_gap_chart(gap_df, top_n_gap, ascending=True)
        fig_low.update_layout(title=f"Top {top_n_gap} Smallest Gaps",
                              title_x=0.5, title_xanchor="center")
        st.plotly_chart(fig_low, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="text-align:center">Conclusions & Recommendations</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="gap-card">
            <h4>Highest Gaps</h4>
            <ul>
                <li><strong>Node.Js</strong> — gap 98.8%</li>
                <li><strong>A/B Testing</strong> — gap 98%</li>
                <li><strong>Looker</strong> — gap 97.3%</li>
                <li><strong>Operations Research</strong> — gap 96.8%</li>
                <li><strong>Artificial Intelligence</strong> — gap 96.7%</li>
            </ul>
            <br>
            <h4>Lowest Gaps</h4>
            <ul>
                <li><strong>Switching</strong> — gap 1.0%</li>
                <li><strong>Siem</strong> — gap 1.8%</li>
                <li><strong>Elasticsearch</strong> — gap 2.0%</li>
                <li><strong>Incident Management</strong> — gap 2.5%</li>
                <li><strong>C</strong> — gap 3.2%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="gap-card">
            <h4>Action Items for Candidates</h4>
            <ul>
                <li>Skills such as Node.js, A/B Testing, Looker, and Artificial Intelligence remain highly sought after by the industry but are significantly underrepresented in candidate profiles. Mastering these skills will maximize your competitive edge in the market.</li>
            </ul>
            <br>
            <h4>Action Items for Companies</h4>
            <ul>
                <li>High gap scores point to strict resource scarcity. Organizations should build specialized upskilling/training initiatives internally or restructure competitive acquisition pipelines specifically targetting talent with these high-deficit skills.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)