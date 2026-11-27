from __future__ import annotations

import io
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.eda import (  # noqa: E402
    build_eda_panel,
    complete_reporting_periods,
    load_wahis_source,
    prepare_state_detail_records,
    source_quality_summary,
    state_level_panel,
)

st.set_page_config(
    page_title="Poultry Disease Intelligence | Nigeria",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# A consistent, high-contrast palette is used across all views.
PALETTE = {
    "navy": "#102A43",
    "navy_2": "#163F5C",
    "teal": "#0F9D91",
    "teal_dark": "#087F78",
    "mint": "#56C5A8",
    "sky": "#3B82F6",
    "blue_light": "#7CC4F8",
    "gold": "#F2B84B",
    "coral": "#E27662",
    "purple": "#8B7CF6",
    "pink": "#E78AB7",
    "ink": "#17324D",
    "muted": "#60758A",
    "grid": "#E4ECF2",
    "paper": "#F4F7FA",
    "white": "#FFFFFF",
    "missing": "#D9E2EA",
}
DISEASE_COLORS = {
    "Newcastle disease virus (Inf. with)": PALETTE["sky"],
    "Infectious bursal disease (Gumboro disease)": PALETTE["gold"],
    "Fowl typhoid": PALETTE["teal"],
    "Avian infectious bronchitis": PALETTE["coral"],
    "Fowl pox (-2005)": PALETTE["purple"],
    "Fowl cholera": PALETTE["pink"],
}
DISEASE_SEQUENCE = list(DISEASE_COLORS)
COLORWAY = [
    PALETTE["teal"], PALETTE["sky"], PALETTE["gold"], PALETTE["coral"],
    PALETTE["purple"], PALETTE["mint"], PALETTE["pink"], PALETTE["navy_2"],
]

st.markdown(
    f"""
    <style>
      :root {{
        --ink:{PALETTE['ink']}; --navy:{PALETTE['navy']}; --teal:{PALETTE['teal']};
        --gold:{PALETTE['gold']}; --coral:{PALETTE['coral']}; --paper:{PALETTE['paper']};
      }}
      .stApp {{ background:var(--paper); color:var(--ink); }}
      [data-testid="stHeader"] {{ background:rgba(244,247,250,.93); }}
      [data-testid="stSidebar"] {{ background:linear-gradient(180deg,#102A43 0%,#163F5C 100%); }}
      [data-testid="stSidebar"] * {{ color:#F1F7FB !important; }}
      [data-testid="stSidebar"] [data-baseweb="select"] > div {{ background:#FFFFFF; }}
      [data-testid="stSidebar"] [data-baseweb="select"] * {{ color:#17324D !important; }}
      [data-testid="stMetric"] {{ background:#FFFFFF; padding:16px 18px; border-radius:14px;
        border:1px solid #E1EAF1; box-shadow:0 3px 12px rgba(16,42,67,.055); }}
      [data-testid="stMetricLabel"] {{ color:#526A80; font-weight:600; }}
      [data-testid="stMetricValue"] {{ color:#102A43; font-weight:750; }}
      .hero {{ background:linear-gradient(115deg,#102A43 0%,#174B68 58%,#0F9D91 100%);
        border-radius:20px; padding:28px 32px; color:#FFFFFF; margin:0 0 16px 0;
        box-shadow:0 8px 24px rgba(16,42,67,.12); }}
      .hero .eyebrow {{ color:#BCEDE4; font-size:.72rem; font-weight:800; letter-spacing:.16em;
        text-transform:uppercase; margin-bottom:8px; }}
      .hero h1 {{ color:#FFFFFF; font-size:2.05rem; line-height:1.2; margin:0 0 8px 0; }}
      .hero p {{ color:#E8F4F8; font-size:1rem; margin:0; max-width:940px; }}
      .hero .tag {{ display:inline-block; margin-top:13px; padding:4px 10px; border-radius:999px;
        background:rgba(255,255,255,.14); color:#FFFFFF; font-size:.76rem; }}
      .section-kicker {{ color:#0F9D91; font-size:.72rem; font-weight:800; letter-spacing:.12em;
        text-transform:uppercase; margin-bottom:3px; }}
      .section-note {{ color:#60758A; font-size:.91rem; margin-top:-4px; }}
      .insight {{ background:#E8F6F2; border-left:4px solid #0F9D91; padding:13px 16px;
        border-radius:9px; margin:8px 0 14px 0; color:#174B4C; }}
      .warning {{ background:#FFF4DF; border-left:4px solid #F2B84B; padding:13px 16px;
        border-radius:9px; margin:8px 0 14px 0; color:#674C1D; }}
      .risk {{ background:#FCEBE8; border-left:4px solid #E27662; padding:13px 16px;
        border-radius:9px; margin:8px 0 14px 0; color:#7D3429; }}
      .muted {{ color:#60758A; font-size:.82rem; }}
      div[data-testid="stExpander"] {{ border:1px solid #DCE6EE; border-radius:11px; background:#FFFFFF; }}
      div[data-testid="stTabs"] button[role="tab"] {{ font-weight:650; }}
      div[data-testid="stTabs"] button[aria-selected="true"] {{ color:#087F78; }}
      div[data-testid="stButton"] button {{ border-radius:10px; font-weight:650; }}
      h1,h2,h3 {{ color:#102A43; }}
      .small-caption {{ color:#60758A; font-size:.78rem; }}
      [data-testid="stDataFrame"] {{ border:1px solid #E1EAF1; border-radius:10px; }}
    </style>
    """,
    unsafe_allow_html=True,
)

RAW_PATH = ROOT / "data" / "raw" / "Quantitative data 2026-10-01.csv"
EVAL_PATH = ROOT / "artifacts" / "evaluation" / "model_evaluation_dataset.csv"
PRED_PATH = ROOT / "artifacts" / "evaluation" / "rolling_origin_oos_predictions.csv"


@st.cache_data(show_spinner="Preparing the WAHIS surveillance data…")
def get_source_data():
    raw = load_wahis_source(RAW_PATH)
    panel = build_eda_panel(raw)
    summary = source_quality_summary(raw, panel)
    return raw, panel, summary


@st.cache_data(show_spinner=False)
def get_model_relationship_data():
    if not EVAL_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(EVAL_PATH)


@st.cache_data(show_spinner=False)
def get_prediction_data():
    if not PRED_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(PRED_PATH)


def fmt(value, digits: int = 1) -> str:
    if value is None or pd.isna(value):
        return "Not available"
    return f"{value:,.{digits}f}"


def get_public_url() -> str:
    """Read the public deployment URL from Streamlit secrets or environment."""
    try:
        secret_url = st.secrets.get("APP_PUBLIC_URL", "")
    except Exception:
        secret_url = ""
    return str(secret_url or os.getenv("APP_PUBLIC_URL", "")).strip()


def chart_layout(fig, height: int = 390, title: str | None = None):
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=15, t=55, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.82)",
        font=dict(family="Inter, Arial, sans-serif", color=PALETTE["ink"], size=12),
        colorway=COLORWAY,
        hoverlabel=dict(bgcolor="#102A43", bordercolor="#102A43", font_color="#FFFFFF", font_size=12),
        legend=dict(bgcolor="rgba(255,255,255,.78)", bordercolor="#E4ECF2", borderwidth=1),
        hovermode="closest",
    )
    if title:
        fig.update_layout(title=dict(text=title, x=0.01, xanchor="left", font=dict(size=16, color=PALETTE["navy"])))
    fig.update_xaxes(showgrid=False, linecolor="#DCE5EC", zeroline=False, automargin=True)
    fig.update_yaxes(showgrid=True, gridcolor=PALETTE["grid"], zeroline=False, automargin=True)
    return fig


def add_explanation(title: str, body: str, method: str | None = None, limitation: str | None = None):
    with st.expander(f"ⓘ Understand this visual — {title}"):
        st.write(body)
        if method:
            st.caption(f"Calculation: {method}")
        if limitation:
            st.warning(limitation)
        st.caption("Tip: hover over a mark for detail, then click it to inspect the selected observation.")


def show_chart(fig, key: str, label: str, value_label: str = "value"):
    event = st.plotly_chart(
        fig,
        use_container_width=True,
        key=key,
        on_select="rerun",
        selection_mode="points",
        config={
            "displaylogo": False,
            "scrollZoom": True,
            "responsive": True,
            "modeBarButtonsToRemove": ["select2d", "lasso2d"],
        },
    )
    points = []
    try:
        points = event.selection.points
    except Exception:
        try:
            points = event["selection"]["points"]
        except Exception:
            points = []
    if points:
        point = points[0]
        x_value = point.get("x", "Selected observation")
        y_value = point.get("y", "")
        custom = point.get("customdata")
        context = ""
        if isinstance(custom, (list, tuple, np.ndarray)):
            context = " · ".join(str(x) for x in custom if x is not None and str(x) != "")
        elif custom is not None:
            context = str(custom)
        st.info(f"**Selected {label}:** {x_value}  ·  **{value_label}:** {y_value}" + (f"  ·  **Details:** {context}" if context else ""))
    return event


def disease_color_map(names):
    return {name: DISEASE_COLORS.get(name, COLORWAY[i % len(COLORWAY)]) for i, name in enumerate(names)}


def period_label_map(df: pd.DataFrame) -> dict[int, str]:
    pairs = df[["temporal_period", "year", "semester_half"]].dropna().drop_duplicates().sort_values("temporal_period")
    return {
        int(row.temporal_period): f"{row.semester_half} {int(row.year)}"
        for row in pairs.itertuples(index=False)
    }


def complete_period_frame(observed: pd.DataFrame, years: tuple[int, int], group_col: str | None = None) -> pd.DataFrame:
    """Keep every six-month period in chronological order without filling gaps with zero."""
    return complete_reporting_periods(observed, years[0], years[1], group_col)


def build_filters(panel: pd.DataFrame):
    state_panel = state_level_panel(panel)
    st.sidebar.markdown("## Explore the evidence")
    st.sidebar.caption("Selections update the surveillance charts throughout the dashboard.")
    diseases = ["All diseases"] + sorted(state_panel["disease"].dropna().unique().tolist())
    areas = ["All state-level areas"] + sorted(state_panel["admin_display"].dropna().unique().tolist())
    years = state_panel["year"].dropna().astype(int)
    min_year, max_year = int(years.min()), int(years.max())
    pilot = "Newcastle disease virus (Inf. with)"
    default_index = diseases.index(pilot) if pilot in diseases else 0
    disease = st.sidebar.selectbox("Disease", diseases, index=default_index)
    area = st.sidebar.selectbox("Administrative area", areas, index=0)
    year_range = st.sidebar.slider("Reporting years", min_year, max_year, (2020, max_year))
    filtered = state_panel.loc[state_panel["year"].between(year_range[0], year_range[1])].copy()
    if disease != "All diseases":
        filtered = filtered.loc[filtered["disease"].eq(disease)]
    if area != "All state-level areas":
        filtered = filtered.loc[filtered["admin_display"].eq(area)]
    st.sidebar.divider()
    st.sidebar.markdown("**How to read the data**")
    st.sidebar.caption("A missing WAHIS count is not zero. State rankings describe reported counts, not population-adjusted disease risk.")
    st.sidebar.markdown("**Current selection**")
    st.sidebar.caption(f"{len(filtered):,} grouped records in the selected period and scope.")
    return filtered, disease, area, year_range


def render_overview(panel: pd.DataFrame, summary: dict, filtered: pd.DataFrame, year_range: tuple[int, int]):
    st.markdown('<div class="section-kicker">Surveillance overview</div>', unsafe_allow_html=True)
    st.subheader("Research at a glance")
    st.caption("Start with the source evidence, then explore the selected disease, area and reporting years.")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Raw WAHIS records", f"{summary['raw_rows']:,}")
    k2.metric("Unique area–disease–period groups", f"{summary['panel_groups']:,}")
    k3.metric("Groups with observed outbreak counts", f"{summary['panel_observed_outbreak_groups']:,}")
    k4.metric("State-level areas", f"{summary['state_admin_areas_after_name_standardisation']:,}")
    with st.expander("What do these project-wide numbers mean?"):
        st.write(
            "These four figures describe the complete source and grouped analytical panel. They do not change when a sidebar filter is selected. "
            "The 1,180 raw rows are consolidated into 739 unique area–disease–semester groups. A group is counted as observed only when "
            "the source contains an unambiguous numeric new-outbreak count. Unavailable values are never converted to zero."
        )
    observed = filtered.loc[filtered["new_outbreaks"].notna()].copy()
    st.markdown("### What does the selected view contain?")
    a, b, c, d = st.columns(4)
    a.metric("Selected groups", f"{len(filtered):,}")
    b.metric("Observed outbreak counts", f"{len(observed):,}")
    c.metric("Unavailable counts", f"{filtered['new_outbreaks'].isna().sum():,}")
    c_pct = 100 * filtered["new_outbreaks"].notna().mean() if len(filtered) else np.nan
    d.metric("Count availability", f"{c_pct:.1f}%" if pd.notna(c_pct) else "Not available")
    if observed.empty:
        st.info("No numeric outbreak counts match the current filters.")
        return
    st.markdown("### Reported outbreak counts over time")
    trend = complete_period_frame(observed, year_range)
    fig = px.line(
        trend, x="temporal_period", y="new_outbreaks", markers=True,
        custom_data=["period_label"], labels={"temporal_period":"Six-month reporting period", "new_outbreaks":"Sum of observed reported counts"},
    )
    fig.update_traces(line=dict(color=PALETTE["teal"], width=3.5), marker=dict(size=9, color=PALETTE["teal"], line=dict(color="#FFFFFF", width=1.5)), connectgaps=False)
    fig.update_xaxes(tickmode="array", tickvals=trend["temporal_period"], ticktext=trend["period_label"], tickangle=-30)
    chart_layout(fig, 390, "Reported outbreak counts by six-month period")
    show_chart(fig, "overview-time", "reporting period", "reported count")
    add_explanation(
        "The time trend",
        "Each point is the sum of observed group-level new-outbreak counts for the selected disease and state scope. Periods are ordered by their numeric year/semester index. A gap means no numeric count is available for that selected period; it is not a zero.",
        "Sum the observed new_outbreaks values after grouping by area, disease and semester.",
        "These are reported counts, not a complete measure of all poultry disease events in Nigeria.",
    )
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("### Areas with the largest reported counts")
        area_counts = observed.groupby("admin_display", as_index=False).agg(
            reported_count=("new_outbreaks", "sum"), observed_groups=("new_outbreaks", "count")
        ).sort_values("reported_count", ascending=False).head(12)
        bar = px.bar(
            area_counts.sort_values("reported_count"), x="reported_count", y="admin_display", orientation="h",
            color="observed_groups", custom_data=["observed_groups"], color_continuous_scale="Tealgrn",
            labels={"reported_count":"Sum of observed reported counts", "admin_display":"State / area", "observed_groups":"Observed groups"},
        )
        chart_layout(bar, 410, "Leading areas in the selected view")
        show_chart(bar, "overview-areas", "administrative area", "reported count")
        add_explanation("Area comparison", "The ranking sums observed group counts by state. It is not a risk ranking; surveillance intensity, reporting completeness and poultry population can differ.", "Sum observed new-outbreak counts by area; count contributing groups separately.")
    with right:
        st.markdown("### Distribution of observed counts")
        log_bins = st.toggle("Use logarithmic count axis", value=False, key="overview-log-hist")
        hist = px.histogram(
            observed, x="new_outbreaks", nbins=30, log_x=log_bins,
            color_discrete_sequence=[PALETTE["gold"]],
            labels={"new_outbreaks":"Observed new-outbreak count", "count":"Number of groups"},
        )
        chart_layout(hist, 410, "How the reported counts are distributed")
        show_chart(hist, "overview-histogram", "outbreak-count range", "groups")
        add_explanation("Count distribution", f"The median observed count is {fmt(observed['new_outbreaks'].median())}; the maximum is {fmt(observed['new_outbreaks'].max(), 0)}. The optional log axis helps inspect a long right tail.", "Histogram of non-missing group-level new-outbreak counts.", "A log axis omits zero values if any are present; check the axis before comparing counts.")


def render_trends(filtered: pd.DataFrame, selected_disease: str, year_range: tuple[int, int]):
    st.markdown('<div class="section-kicker">Exploratory data analysis</div>', unsafe_allow_html=True)
    st.subheader("Disease and time patterns")
    st.caption("Compare the timing, distribution and amount of numerical evidence available across disease categories.")
    observed = filtered.loc[filtered["new_outbreaks"].notna()].copy()
    if observed.empty:
        st.info("No observed counts are available for the selected filters.")
        return
    if selected_disease == "All diseases":
        trend = complete_period_frame(observed, year_range, "disease")
        fig = px.line(
            trend, x="temporal_period", y="new_outbreaks", color="disease", markers=True,
            custom_data=["disease", "period_label"], color_discrete_map=disease_color_map(trend["disease"].dropna().unique()),
            labels={"temporal_period":"Six-month reporting period", "new_outbreaks":"Observed reported count", "disease":"Disease"},
        )
        fig.update_traces(connectgaps=False, line=dict(width=2.8), marker=dict(size=7))
    else:
        trend = complete_period_frame(observed, year_range)
        fig = px.line(trend, x="temporal_period", y="new_outbreaks", markers=True, custom_data=["period_label"],
                      labels={"temporal_period":"Six-month reporting period", "new_outbreaks":"Observed reported count"})
        fig.update_traces(connectgaps=False, line=dict(color=DISEASE_COLORS.get(selected_disease, PALETTE["teal"]), width=3.4), marker=dict(size=8))
    fig.update_xaxes(tickmode="array", tickvals=trend["temporal_period"].drop_duplicates().sort_values(), ticktext=[f"{'Jan–Jun' if p % 2 == 0 else 'Jul–Dec'} {p // 2}" for p in trend["temporal_period"].drop_duplicates().sort_values()], tickangle=-30)
    chart_layout(fig, 420, "Reported counts in chronological order")
    show_chart(fig, "disease-period-trend", "disease and period", "reported count")
    add_explanation("Disease trends", "The x-axis uses an ordered numeric semester index, not alphabetical labels. Missing periods are explicitly kept as gaps so the line does not imply an observed zero.", "Sum observed counts by disease and numeric semester index, then reindex to every semester in the selected date range.", "The trend shows changes in reported surveillance activity, not changes in true prevalence.")
    left, right = st.columns(2)
    with left:
        box = px.box(
            observed, x="disease", y="new_outbreaks", color="disease", points="outliers",
            color_discrete_map=disease_color_map(observed["disease"].dropna().unique()),
            labels={"disease":"Disease", "new_outbreaks":"Reported new-outbreak count"},
        )
        box.update_layout(showlegend=False)
        chart_layout(box, 420, "Spread of reported counts by disease")
        show_chart(box, "disease-count-box", "disease", "reported count")
        add_explanation("Spread by disease", "The box shows the middle half of observed counts; the centre line is the median. Points beyond whiskers are outliers. The groups have different sample sizes.", "Box plot of group-level observed outbreak counts by disease.")
    with right:
        disease_counts = observed.groupby("disease", as_index=False).agg(
            observed_groups=("new_outbreaks", "count"), reported_count_sum=("new_outbreaks", "sum")
        ).sort_values("observed_groups", ascending=True)
        coverage = px.bar(
            disease_counts, x="observed_groups", y="disease", orientation="h", color="disease",
            color_discrete_map=disease_color_map(disease_counts["disease"]),
            custom_data=["reported_count_sum"],
            labels={"observed_groups":"Groups with numeric counts", "disease":"Disease", "reported_count_sum":"Sum of reported counts"},
        )
        coverage.update_layout(showlegend=False)
        chart_layout(coverage, 420, "How much numeric evidence exists by disease")
        show_chart(coverage, "disease-coverage", "disease", "observed groups")
        add_explanation("Disease coverage", "Bar length is the number of area–disease–semester groups with a numeric outbreak count. Hover shows the sum of counts as a separate value; the colour simply identifies the disease.", "Count non-missing outbreak-count values by disease.", "A larger observed sample does not necessarily mean more disease; it can also reflect reporting coverage.")


def render_geography(filtered: pd.DataFrame):
    st.markdown('<div class="section-kicker">Spatial exploration</div>', unsafe_allow_html=True)
    st.subheader("Geographic surveillance patterns")
    st.caption("Compare observed reporting across Nigerian administrative areas. These are reporting summaries, not disease-risk estimates.")
    observed = filtered.loc[filtered["new_outbreaks"].notna()].copy()
    if observed.empty:
        st.info("No observed counts are available for the selected filters.")
        return
    area_summary = observed.groupby("admin_display", as_index=False).agg(
        reported_count=("new_outbreaks", "sum"), observed_groups=("new_outbreaks", "count"),
        diseases_reported=("disease", "nunique"), periods_observed=("temporal_period", "nunique"),
    ).sort_values("reported_count", ascending=False)
    top = area_summary.head(15)
    fig = px.bar(
        top.sort_values("reported_count"), x="reported_count", y="admin_display", orientation="h",
        color="observed_groups", custom_data=["observed_groups", "diseases_reported", "periods_observed"],
        color_continuous_scale="Tealgrn",
        labels={"reported_count":"Sum of observed reported counts", "admin_display":"Administrative area", "observed_groups":"Observed groups"},
    )
    chart_layout(fig, 500, "Administrative areas with the largest observed counts")
    event = show_chart(fig, "geography-ranked-areas", "administrative area", "reported count")
    add_explanation("Geographic comparison", "Bar length is the sum of observed new-outbreak counts. Colour represents how many groups contributed. This does not adjust for poultry population or reporting completeness.", "Sum group-level counts by state; count observed groups and distinct periods separately.", "Do not interpret this ranking as a map of future disease risk.")
    if len(area_summary):
        chosen = st.selectbox("Inspect an administrative area", area_summary["admin_display"].tolist(), key="geo-detail-state")
        detail = observed.loc[observed["admin_display"].eq(chosen)]
        x1, x2, x3, x4 = st.columns(4)
        x1.metric("Reported count sum", f"{detail['new_outbreaks'].sum():,.0f}")
        x2.metric("Observed groups", f"{len(detail):,}")
        x3.metric("Diseases represented", f"{detail['disease'].nunique():,}")
        x4.metric("Periods represented", f"{detail['temporal_period'].nunique():,}")
        detail_trend = detail.groupby(["temporal_period", "period_label"], as_index=False)["new_outbreaks"].sum().sort_values("temporal_period")
        dt = px.bar(detail_trend, x="temporal_period", y="new_outbreaks", custom_data=["period_label"],
                    color_discrete_sequence=[PALETTE["sky"]],
                    labels={"temporal_period":"Reporting period", "new_outbreaks":"Observed reported count"})
        dt.update_xaxes(tickmode="array", tickvals=detail_trend["temporal_period"], ticktext=detail_trend["period_label"], tickangle=-30)
        chart_layout(dt, 300, f"Reported counts over time — {chosen}")
        show_chart(dt, "geo-state-detail", "reporting period", "reported count")
        with st.expander(f"View the {chosen} records behind this summary"):
            records = prepare_state_detail_records(detail)
            st.dataframe(records, use_container_width=True, hide_index=True)
    matrix = observed.pivot_table(index="admin_display", columns="disease", values="new_outbreaks", aggfunc="sum", observed=True)
    matrix = matrix.reindex(top["admin_display"].tolist())
    heat = go.Figure(data=go.Heatmap(
        z=matrix.to_numpy(dtype=float), x=matrix.columns.tolist(), y=matrix.index.tolist(),
        colorscale=[[0, "#E9F6F4"], [0.35, "#8DD8C5"], [0.7, "#1C9A91"], [1, "#164E63"]],
        colorbar=dict(title="Reported<br>count"), hovertemplate="Area: %{y}<br>Disease: %{x}<br>Observed count sum: %{z}<extra></extra>",
        connectgaps=False,
    ))
    chart_layout(heat, 540, "Disease-by-area heatmap")
    heat.update_layout(xaxis_title="Disease", yaxis_title="Administrative area")
    show_chart(heat, "geography-heatmap", "area–disease cell", "reported count")
    add_explanation("Disease-by-area heatmap", "Each cell is the sum of observed counts for one disease and area. A blank cell means no numeric count was available in the selected records, not confirmed zero outbreaks.", "Pivot observed group-level counts by administrative area and disease.", "The heatmap is not adjusted for population size, poultry density or reporting completeness.")


def render_relationships(filtered: pd.DataFrame):
    st.markdown('<div class="section-kicker">Exploratory relationships</div>', unsafe_allow_html=True)
    st.subheader("Explore relationships in the surveillance data")
    st.caption("Choose another reported measure and inspect how it varies alongside new-outbreak counts.")
    options = {
        "Cases (animals reported as affected)": "cases",
        "Deaths": "deaths",
        "Vaccinated animals": "vaccinated",
        "Susceptible animals": "susceptible",
    }
    left, right = st.columns([0.9, 2.1])
    with left:
        label = st.selectbox("Compare new outbreaks with", list(options.keys()), key="relationship-measure")
        measure = options[label]
        log_x = st.checkbox("Use logarithmic x-axis", value=False, help="Useful when values span a wide range. Zero values cannot be plotted on a log axis.")
        trendline = st.checkbox("Show descriptive trend line", value=True)
        st.markdown("#### What is being compared?")
        st.write("Each dot is one area × disease × semester group with numeric values for both selected measures.")
    relation = filtered.loc[filtered["new_outbreaks"].notna() & filtered[measure].notna()].copy()
    if relation.empty:
        st.info("No groups have both selected measures under the current filters.")
        return
    omitted = 0
    if log_x:
        omitted = int((relation[measure] <= 0).sum())
        relation = relation.loc[relation[measure] > 0].copy()
    if relation.empty:
        st.warning("No positive x-values are available for a logarithmic axis. Turn off the log scale.")
        return
    rho = relation[["new_outbreaks", measure]].corr(method="spearman").iloc[0, 1]
    p1, p2, p3 = st.columns(3)
    p1.metric("Matched groups", f"{len(relation):,}")
    p2.metric("Spearman correlation", fmt(rho, 3))
    p3.metric("Median reported counts", fmt(relation["new_outbreaks"].median(), 1))
    with right:
        fig = px.scatter(
            relation, x=measure, y="new_outbreaks", color="disease", symbol="disease",
            color_discrete_map=disease_color_map(relation["disease"].dropna().unique()),
            hover_data={"admin_display": True, "period_label": True, "new_outbreaks": ":.2f", measure: ":.2f"},
            custom_data=["admin_display", "disease", "period_label", measure, "new_outbreaks"],
            labels={measure: label, "new_outbreaks":"Observed new-outbreak count", "disease":"Disease"},
        )
        if trendline and len(relation) >= 3 and relation[measure].nunique() > 1:
            x = relation[measure].to_numpy(dtype=float)
            y = relation["new_outbreaks"].to_numpy(dtype=float)
            try:
                coef = np.polyfit(np.log10(x) if log_x else x, y, 1)
                xx = np.linspace(float(x.min()), float(x.max()), 80)
                yy = coef[0] * (np.log10(xx) if log_x else xx) + coef[1]
                fig.add_trace(go.Scatter(x=xx, y=yy, mode="lines", name="Descriptive linear trend", line=dict(color=PALETTE["navy"], width=2, dash="dash")))
            except (ValueError, np.linalg.LinAlgError):
                pass
        if log_x:
            fig.update_xaxes(type="log")
        chart_layout(fig, 480, f"Reported outbreak count vs {label.lower()}")
        show_chart(fig, "relationship-explorer", "data point", "outbreak count")
    st.caption(f"Spearman rank correlation = {rho:.3f}. This describes a monotonic association, not causation." + (f" {omitted} zero/negative x-values were omitted for the log axis." if omitted else ""))
    by_disease = relation.groupby("disease").apply(lambda g: pd.Series({
        "matched_groups": len(g), "spearman_rho": g[["new_outbreaks", measure]].corr(method="spearman").iloc[0, 1]
        if len(g) >= 2 and g[measure].nunique() > 1 and g["new_outbreaks"].nunique() > 1 else np.nan
    }), include_groups=False).reset_index()
    st.markdown("### Relationship by disease")
    st.dataframe(by_disease, use_container_width=True, hide_index=True)
    add_explanation("Relationship explorer", "The scatter plot helps identify clusters, outliers and whether larger values of the selected measure tend to occur alongside larger outbreak counts. The dashed line is a simple descriptive linear fit.", "Spearman correlation is calculated only on rows where both selected measures are numeric. Disease-specific correlations are shown separately when there is enough variation.", "These relationships can reflect reporting practices and surveillance processes. They do not show that cases, deaths or vaccination caused the outbreak count.")


def render_model_performance():
    st.markdown('<div class="section-kicker">Model evaluation</div>', unsafe_allow_html=True)
    st.subheader("What the current model has demonstrated")
    st.caption("Project-wide development-stage temporal validation results. The sidebar filters affect surveillance exploration, not this saved model-evaluation sample. These results are not an untouched independent final test.")
    predictions = get_prediction_data()
    if predictions.empty:
        st.info("Saved out-of-sample predictions are not available in this checkout.")
        return
    y = predictions["target_outbreak_count"].astype(float)
    p = predictions["predicted_outbreak_count"].astype(float)
    error = p - y
    mae = float(np.mean(np.abs(error)))
    rmse = float(np.sqrt(np.mean(error**2)))
    bias = float(np.mean(error))
    median_ae = float(np.median(np.abs(error)))
    a, b, c, d = st.columns(4)
    a.metric("Pooled MAE", fmt(mae, 3), help="Average absolute error in reported outbreak-count units.")
    b.metric("Pooled RMSE", fmt(rmse, 3), help="Penalises large prediction errors more heavily.")
    c.metric("Mean signed error", f"{bias:+.3f}", help="Positive values indicate overprediction on average.")
    d.metric("Out-of-sample predictions", f"{len(predictions):,}")
    predictions = predictions.copy()
    predictions["residual"] = error
    predictions["absolute_error"] = np.abs(error)
    fig = px.scatter(
        predictions, x="target_outbreak_count", y="predicted_outbreak_count", color="fold",
        hover_data=["fold", "temporal_period", "residual", "absolute_error"],
        custom_data=["fold", "temporal_period", "target_outbreak_count", "predicted_outbreak_count"],
        color_continuous_scale="Turbo",
        labels={"target_outbreak_count":"Actual reported count", "predicted_outbreak_count":"Predicted reported count", "fold":"Validation fold"},
    )
    upper = max(float(y.max()), float(p.max())) * 1.03
    fig.add_trace(go.Scatter(x=[0, upper], y=[0, upper], mode="lines", name="Perfect prediction", line=dict(color=PALETTE["coral"], width=2.5, dash="dash")))
    chart_layout(fig, 470, "Actual versus predicted reported outbreak counts")
    show_chart(fig, "model-actual-predicted-v2", "prediction", "predicted count")
    add_explanation("Actual versus predicted", "Points close to the diagonal line have smaller errors. Points above it are overpredictions; points below it are underpredictions. The colour identifies the validation fold.", "Each point represents one rolling-origin out-of-sample prediction.", "These same folds were used during model selection. A new, untouched period is needed for independent evaluation.")
    left, right = st.columns(2)
    with left:
        hist = px.histogram(predictions, x="residual", nbins=30, color_discrete_sequence=[PALETTE["coral"]], labels={"residual":"Prediction error (predicted − actual)", "count":"Number of predictions"})
        hist.add_vline(x=0, line_dash="dash", line_color=PALETTE["navy"])
        chart_layout(hist, 370, "Distribution of prediction errors")
        show_chart(hist, "model-residual-hist", "error range", "predictions")
        add_explanation("Residual distribution", "Errors to the right of zero are overpredictions; errors to the left are underpredictions. A wide distribution indicates that prediction errors vary substantially between observations.", "Residual = predicted reported count − actual reported count.")
    with right:
        residual_fig = px.scatter(predictions, x="target_outbreak_count", y="residual", color="fold", color_continuous_scale="Turbo", hover_data=["temporal_period", "absolute_error"], labels={"target_outbreak_count":"Actual reported count", "residual":"Prediction error"})
        residual_fig.add_hline(y=0, line_dash="dash", line_color=PALETTE["navy"])
        chart_layout(residual_fig, 370, "Where do prediction errors increase?")
        show_chart(residual_fig, "model-residual-vs-actual", "actual count", "prediction error")
        add_explanation("Residuals versus actual counts", "This view helps reveal whether errors become larger for high-count observations or whether the model tends to overpredict or underpredict across the count range.", "Plot residuals against the actual target value.")
    if "fold" in predictions.columns:
        fold_summary = predictions.groupby("fold").apply(lambda g: pd.Series({
            "n_predictions": len(g), "MAE": g["absolute_error"].mean(), "RMSE": np.sqrt(np.mean(g["residual"]**2)), "Mean bias": g["residual"].mean()
        }), include_groups=False).reset_index()
        fold_long = fold_summary.melt(id_vars=["fold", "n_predictions"], value_vars=["MAE", "RMSE"], var_name="metric", value_name="error")
        ff = px.bar(fold_long, x="fold", y="error", color="metric", barmode="group", text_auto=".2f", color_discrete_map={"MAE":PALETTE["teal"], "RMSE":PALETTE["gold"]}, hover_data=["n_predictions"])
        chart_layout(ff, 360, "Performance across the eight chronological folds")
        show_chart(ff, "model-fold-errors", "validation fold", "error")
        with st.expander("View fold-level evaluation details"):
            st.dataframe(fold_summary.round(3), use_container_width=True, hide_index=True)
    st.markdown("### Matched benchmark finding")
    bm1, bm2 = st.columns(2)
    bm1.metric("Three-period historical mean MAE", "4.83", help="272 matched validation rows.")
    bm2.metric("Random Forest MAE on same rows", "6.58", help="Same 272 validation rows.")
    st.warning("The simple three-period historical mean performed better than Random Forest on this matched 272-row comparison. This is a development-stage result, not independent final testing.")


def render_data_quality(raw: pd.DataFrame, panel: pd.DataFrame, summary: dict):
    st.markdown('<div class="section-kicker">Data quality and coverage</div>', unsafe_allow_html=True)
    st.subheader("Data completeness and reporting structure")
    st.caption("Project-wide source audit: understand where counts are available and where reporting information is incomplete. These visuals are not narrowed by the sidebar disease or area filters.")
    a, b, c, d = st.columns(4)
    a.metric("Raw rows without numeric count", f"{summary['raw_unavailable_outbreak_rows']:,}")
    b.metric("Groups without numeric count", f"{summary['panel_unavailable_outbreak_groups']:,}")
    c.metric("Groups with repeated source rows", f"{summary['multirow_groups']:,}")
    d.metric("Conflicting repeated outbreak counts", f"{summary['conflicting_outbreak_groups']:,}")
    st.info("The raw-row and grouped-row missing counts use different denominators. A dash or blank is unavailable reporting, not confirmed zero disease.")
    with st.expander("Why do the raw and grouped missing counts differ?"):
        st.write("Some area–disease–semester groups are represented by more than one source row. We consolidate each group conservatively. If at least one numeric outbreak count exists and repeated values do not conflict, the observed value is retained once. If every source row is missing that field, the group remains unavailable.")
    by_year = raw.groupby("year", dropna=False).agg(source_rows=("disease", "size"), rows_with_count=("new_outbreaks", "count")).reset_index()
    by_year["year"] = pd.to_numeric(by_year["year"], errors="coerce")
    by_year = by_year.sort_values("year")
    by_year["availability_pct"] = 100 * by_year["rows_with_count"] / by_year["source_rows"].replace(0, np.nan)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=by_year["year"], y=by_year["source_rows"], name="All source rows", marker_color=PALETTE["missing"], opacity=.9))
    fig.add_trace(go.Bar(x=by_year["year"], y=by_year["rows_with_count"], name="Rows with numeric count", marker_color=PALETTE["teal"], opacity=.95))
    chart_layout(fig, 390, "Source volume and numeric-count availability by year")
    fig.update_layout(barmode="group", yaxis_title="Number of source rows", xaxis_title="Reporting year")
    show_chart(fig, "quality-year-volume-v2", "year", "source rows")
    add_explanation("Reporting availability over time", "The grouped bars compare the number of original rows with the subset that has a numeric new-outbreak count. Numeric coverage is not uniform across years.", "Count raw source rows and non-missing New outbreaks values by year.", "A higher count of available records does not necessarily mean higher disease activity.")
    disease_quality = panel.groupby("disease", as_index=False).agg(
        total_groups=("disease", "size"), observed_groups=("new_outbreaks", "count")
    )
    disease_quality["unavailable_groups"] = disease_quality["total_groups"] - disease_quality["observed_groups"]
    disease_quality["availability_pct"] = 100 * disease_quality["observed_groups"] / disease_quality["total_groups"]
    long = disease_quality.melt(id_vars=["disease", "total_groups", "availability_pct"], value_vars=["observed_groups", "unavailable_groups"], var_name="count_status", value_name="groups")
    long["count_status"] = long["count_status"].map({"observed_groups":"Observed numeric count", "unavailable_groups":"Count unavailable"})
    fig2 = px.bar(long, x="disease", y="groups", color="count_status", barmode="stack",
                  color_discrete_map={"Observed numeric count":PALETTE["teal"], "Count unavailable":PALETTE["gold"]},
                  custom_data=["total_groups", "availability_pct"],
                  labels={"disease":"Disease", "groups":"Unique area–disease–semester groups", "count_status":"Count status"})
    chart_layout(fig2, 420, "Observed and unavailable counts by disease")
    show_chart(fig2, "quality-disease-status-v2", "disease", "groups")
    with st.expander("View availability percentages by disease"):
        st.dataframe(disease_quality[["disease", "total_groups", "observed_groups", "unavailable_groups", "availability_pct"]].round(1), use_container_width=True, hide_index=True)
    add_explanation("Availability by disease", "Each bar is a count of unique grouped observations. Teal means a numeric outbreak count was observed; amber means the count remains unavailable.", "Count unique area–disease–semester groups by availability status.", "This chart is about reporting completeness, not disease presence or absence.")
    # A transparent area-by-disease completeness matrix is more useful than a risk map.
    state_panel = state_level_panel(panel)
    coverage = state_panel.assign(count_available=state_panel["new_outbreaks"].notna().astype(int)).pivot_table(
        index="admin_display", columns="disease", values="count_available", aggfunc="mean"
    )
    coverage = coverage.reindex(coverage.mean(axis=1).sort_values(ascending=False).index).head(25)
    heat = go.Figure(data=go.Heatmap(
        z=coverage.to_numpy(dtype=float) * 100, x=coverage.columns.tolist(), y=coverage.index.tolist(),
        colorscale=[[0, "#FFF0D2"], [0.45, "#A9DDD1"], [1, "#0F817A"]], zmin=0, zmax=100,
        colorbar=dict(title="Observed<br>groups (%)"), hovertemplate="Area: %{y}<br>Disease: %{x}<br>Count availability: %{z:.1f}%<extra></extra>",
    ))
    chart_layout(heat, 560, "Where is numeric outbreak-count information available?")
    heat.update_layout(xaxis_title="Disease", yaxis_title="State / administrative area")
    show_chart(heat, "quality-completeness-heatmap", "area–disease availability", "availability (%)")
    add_explanation("Coverage heatmap", "Each cell is the percentage of grouped semester observations for an area and disease that contains a numeric new-outbreak count. Blank cells mean no group was present in the source for that combination.", "Mean of the binary observed-count flag within each area and disease, multiplied by 100.", "Availability is not a measure of disease burden. Areas with low reporting may still have disease activity that is not captured in these data.")
    with st.expander("How did we handle multiple source rows?"):
        st.write(f"The source contains {summary['multirow_groups']:,} groups with more than one row. The new-outbreak measure had no conflicting repeated numeric values in the audit. Conflicting repeated values for other measures (including cases) are withheld rather than added together.")


def render_how_it_works():
    st.markdown('<div class="section-kicker">Research journey</div>', unsafe_allow_html=True)
    st.subheader("Explore how the research was built")
    st.caption("Select a stage to see what was done, why it matters, what evidence supports it and what comes next.")
    stages = [
        ("1 · Surveillance data audit", "Completed", "We started with the WOAH/WAHIS quantitative poultry-disease export and inspected its fields, reporting years, disease labels, administrative areas and numeric-count availability.", "This establishes what the source can and cannot support. A dash or blank is unavailable, not evidence of zero disease.", "Source audit, record counts, field dictionary and missingness checks."),
        ("2 · Cleaning and analytical grouping", "Completed with limitations", "We standardised missing-value markers and field names, then constructed one group per year, six-month period, administrative area and disease.", "Repeated source rows are not blindly summed. Unambiguous values are retained once; conflicts are flagged.", "739 grouped observations from 1,180 source rows; 445 groups with observed outbreak counts."),
        ("3 · Exploratory analysis", "In progress / expanded", "We examine reporting coverage, distributions, disease patterns, time trends, geographic differences and relationships between reported measures.", "EDA identifies skew, outliers, missingness and coverage differences before model development.", "Interactive disease trends, box plots, correlation views and reporting-completeness visuals."),
        ("4 · Climate and geography integration", "Completed with limitations", "The research includes ERA5-Land climate summaries and Nigerian administrative reference boundaries.", "Climate and geography provide environmental context. An association is not evidence of causation.", "Climate variables, geographic standardisation and state-level summaries."),
        ("5 · Feature engineering and forecasting", "Requires refinement", "We constructed time, historical-outbreak, geography and climate features. The next version must ensure every predictor is available before the forecast semester.", "A genuine early-warning model must estimate a future period without using information from that period.", "Gap-aware lags and next-semester target design."),
        ("6 · Model comparison and evaluation", "Development validation completed", "The existing work compared regression models and historical baselines using chronological validation.", "The current Random Forest did not beat the three-period historical mean on the matched comparison. An untouched future test is still required.", "Fold metrics, residual diagnostics, matched benchmark and later-period holdout."),
        ("7 · Interactive decision-support prototype", "Prototype", "The dashboard brings surveillance analytics, geography, model evidence and plain-language explanations into one interface.", "The prototype is for exploration and decision support. It is not a veterinary diagnosis or an autonomous alert service.", "A pilot interface for discussion with animal-health professionals and poultry stakeholders."),
    ]
    left, right = st.columns([0.95, 2.05], gap="large")
    with left:
        labels = [s[0] for s in stages]
        selected = st.radio("Research stages", labels, index=0, key="research-stage-selector")
        st.markdown("### Journey status")
        st.caption("The research has progressed through data acquisition, cleaning, integration and development-stage evaluation. Prospective forecasting validation and stakeholder testing remain future work.")
    chosen = next(s for s in stages if s[0] == selected)
    with right:
        st.markdown(f"### {chosen[0]}")
        status_color = "success" if chosen[1] == "Completed" else "warning"
        if status_color == "success":
            st.success(chosen[1])
        else:
            st.warning(chosen[1])
        st.write(chosen[2])
        st.markdown("**Why this stage matters**")
        st.write(chosen[3])
        st.markdown("**Evidence / deliverable**")
        st.info(chosen[4])
    st.divider()
    st.markdown("### What the prototype currently represents")
    st.write("This is an exploratory research dashboard using the available WAHIS source data and saved model-evaluation artefacts. It is not connected to a live surveillance feed and does not issue operational disease alerts.")


def render_share():
    st.markdown('<div class="section-kicker">Public access</div>', unsafe_allow_html=True)
    st.subheader("Share the dashboard")
    st.caption("After deployment, this page can display a QR code that opens the complete dashboard on a phone or computer.")
    public_url = get_public_url()
    if not public_url:
        st.warning("The dashboard is currently running locally. A localhost address cannot be opened by other people scanning a QR code. Deploy the app first, then add APP_PUBLIC_URL to the app's Streamlit Cloud secrets.")
        st.markdown("**Deployment destination:** Streamlit Community Cloud · free public app hosting.")
        st.markdown("**Next:** Deploy the GitHub repository, copy the resulting `https://…streamlit.app` address, and set `APP_PUBLIC_URL` in the Streamlit app settings.")
        return
    st.success("A public dashboard address has been configured.")
    st.code(public_url, language=None)
    try:
        import qrcode
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=9, border=3)
        qr.add_data(public_url)
        qr.make(fit=True)
        image = qr.make_image(fill_color=PALETTE["navy"], back_color="white")
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        st.image(buffer.getvalue(), caption="Scan to open Poultry Disease Intelligence — Nigeria", width=270)
        st.download_button("Download dashboard QR code", data=buffer.getvalue(), file_name="poultry-disease-intelligence-qr.png", mime="image/png")
    except Exception as exc:
        st.error(f"QR code could not be generated: {exc}")


def main():
    st.markdown(
        "<div class='hero'><div class='eyebrow'>Surveillance · Analytics · Decision support</div>"
        "<h1>🐔 Poultry Disease Intelligence — Nigeria</h1>"
        "<p>Explore historical poultry-disease surveillance, investigate reporting patterns and understand the evidence behind the early-warning research.</p>"
        "<span class='tag'>Interactive research prototype · Not an operational alert service</span></div>",
        unsafe_allow_html=True,
    )
    if not RAW_PATH.exists():
        st.error(f"The WAHIS source file is missing: {RAW_PATH}")
        st.info("Run this app from the root of the project repository and confirm data/raw/ contains the source CSV.")
        st.stop()
    try:
        raw, panel, summary = get_source_data()
    except Exception as exc:
        st.error(f"Could not prepare the source data: {exc}")
        st.stop()
    filtered, selected_disease, selected_area, year_range = build_filters(panel)
    st.caption(f"Current view: {selected_disease} · {selected_area} · {year_range[0]}–{year_range[1]}. Hover for details, click chart marks to inspect and open the explanation under each visual.")
    # Use stateful tabs so only the active section executes. By default,
    # Streamlit computes every tab body on every rerun; a failure in one
    # section can otherwise prevent all other tabs from rendering.
    tabs = st.tabs(
        [
            "Overview", "Trends & disease", "Geography", "Relationships",
            "Model performance", "Data quality", "How it works", "Share / QR",
        ],
        on_change="rerun",
        key="poultry-disease-dashboard-tabs",
    )
    if tabs[0].open:
        with tabs[0]:
            render_overview(panel, summary, filtered, year_range)
    if tabs[1].open:
        with tabs[1]:
            render_trends(filtered, selected_disease, year_range)
    if tabs[2].open:
        with tabs[2]:
            render_geography(filtered)
    if tabs[3].open:
        with tabs[3]:
            render_relationships(filtered)
    if tabs[4].open:
        with tabs[4]:
            render_model_performance()
    if tabs[5].open:
        with tabs[5]:
            render_data_quality(raw, panel, summary)
    if tabs[6].open:
        with tabs[6]:
            render_how_it_works()
    if tabs[7].open:
        with tabs[7]:
            render_share()
    st.divider()
    st.caption(
        "Source: WOAH/WAHIS quantitative poultry-disease export included in this research repository. "
        "Displayed counts describe reported surveillance records. Missing values are not treated as zero. "
        "Historical summaries are not direct measures of true disease prevalence or future geographic risk."
    )


if __name__ == "__main__":
    main()
