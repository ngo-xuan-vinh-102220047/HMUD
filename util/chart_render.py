import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def display_percentage_bar(label, prob, class_names):
    import streamlit as st
    import matplotlib.pyplot as plt
    import numpy as np

    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(8, 4))
    y_pos = np.arange(len(class_names))
    ax.barh(y_pos, prob, align='center', color='skyblue')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(class_names)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Tỉ lệ dự đoán (%)')
    ax.set_title('Tỉ lệ dự đoán các lớp')

    # Highlight the predicted class
    for i, v in enumerate(prob):
        if class_names[i] == label:
            ax.barh(i, v, align='center', color='orange')

def display_prediction_charts(predicted_label, probs, class_names, title="Phân bố tỉ lệ phát hiện"):
    """
    Hiển thị 2 biểu đồ cạnh nhau:
      - Donut (pie with hole) hiển thị phần trăm cho từng class
      - Biểu đồ cột hiển thị phần trăm, highlight class dự đoán

    probs: list hoặc 1D array (giá trị 0-1 hoặc 0-100)
    class_names: list tên lớp (cùng độ dài)
    predicted_label: tên lớp được dự đoán (để highlight)
    """
    # chuẩn hóa probs về % nếu cần
    probs = list(probs)
    if max(probs) <= 1.0:
        pct = [p * 100.0 for p in probs]
    else:
        pct = [float(p) for p in probs]

    # màu (có thể tuỳ chỉnh)
    base_colors = px.colors.qualitative.Plotly
    # lặp màu đủ dài
    colors = [base_colors[i % len(base_colors)] for i in range(len(class_names))]
    # highlight màu khác cho predicted
    highlight_color = "#FFA500"  # cam
    colors_bar = [highlight_color if name == predicted_label else colors[i] for i, name in enumerate(class_names)]
    colors_pie = colors.copy()
    # làm màu của predicted đậm hơn trên donut
    for i, name in enumerate(class_names):
        if name == predicted_label:
            colors_pie[i] = highlight_color

    # Donut chart
    fig_pie = go.Figure(
        go.Pie(
            labels=class_names,
            values=pct,
            hole=0.5,
            marker=dict(colors=colors_pie, line=dict(color='#222222', width=1)),
            hovertemplate='%{label}: %{value:.2f}%<extra></extra>',
            textinfo='percent'
        )
    )
    fig_pie.update_layout(
        title=dict(text=title, x=0.5, xanchor='center'),
        showlegend=True,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation='v', x=1.02, y=0.5)
    )

    # Bar chart
    max_y = max(100, max(pct) + 5)
    fig_bar = go.Figure(
        go.Bar(
            x=class_names,
            y=pct,
            marker_color=colors_bar,
            text=[f"{v:.1f}%" for v in pct],
            textposition='auto',
            hovertemplate='%{x}: %{y:.1f}%<extra></extra>'
        )
    )
    fig_bar.update_layout(
        title=dict(text="Biểu đồ cột tỉ lệ (%)", x=0.5),
        yaxis=dict(title='Tỉ lệ (%)', range=[0, max_y]),
        xaxis=dict(tickangle=-15),
        margin=dict(l=20, r=10, t=40, b=20)
    )

    # Hiển thị trên Streamlit: 2 cột
    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)

    # trả về figures nếu cần dùng lại
    return fig_pie, fig_bar