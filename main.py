import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.express as px

# --------------------------
# 기본 설정
# --------------------------
st.set_page_config(page_title="수학 계산기 & 세계 인구 분석", page_icon="🧮", layout="wide")

st.sidebar.title("메뉴")
app_mode = st.sidebar.radio(
    "활동 선택",
    ["계산기", "연도별 세계인구분석"],
)

# ==========================================================
# 1. 계산기 앱
# ==========================================================
if app_mode == "계산기":
    st.title("🧮 수학 계산기 (사칙·지수·로그·합동·그래프)")

    st.write(
        """
    기본적인 **사칙연산**, **지수**, **로그**, **합동(mod)** 연산과  
    임의의 함수식 `y = f(x)`의 **그래프를 그려주는 기능**을 포함한 계산기입니다.
    """
    )

    # --------------------------
    # 연산 종류 선택
    # --------------------------
    calc_type = st.selectbox(
        "원하는 기능을 선택하세요.",
        ["사칙연산", "지수", "로그", "합동(mod)", "함수 그래프 (y = f(x))"],
    )

    st.divider()

    # --------------------------
    # 사칙연산
    # --------------------------
    if calc_type == "사칙연산":
        st.subheader("사칙연산 ( +, -, ×, ÷ )")

        a = st.number_input("첫 번째 수 (a)", value=0.0, format="%.10g")
        b = st.number_input("두 번째 수 (b)", value=0.0, format="%.10g")

        # +, - 가 공란처럼 보이는 문제 방지: 라벨을 길게 작성
        op = st.radio(
            "연산자를 선택하세요.",
            ["더하기 (+)", "빼기 (-)", "곱하기 (×)", "나누기 (÷)"],
            horizontal=True,
        )

        if st.button("계산하기", key="basic"):
            try:
                if op.startswith("더하기"):
                    result = a + b
                    symbol = "+"
                elif op.startswith("빼기"):
                    result = a - b
                    symbol = "-"
                elif op.startswith("곱하기"):
                    result = a * b
                    symbol = "×"
                elif op.startswith("나누기"):
                    symbol = "÷"
                    if b == 0:
                        st.error("0으로 나눌 수 없습니다.")
                        result = None
                    else:
                        result = a / b
                else:
                    result = None
                    symbol = "?"

                if result is not None:
                    st.success(f"결과: {a} {symbol} {b} = {result}")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

    # --------------------------
    # 지수 연산
    # --------------------------
    elif calc_type == "지수":
        st.subheader("지수 연산 (a^b)")

        base = st.number_input("밑 (a)", value=2.0, format="%.10g")
        exp = st.number_input("지수 (b)", value=3.0, format="%.10g")

        if st.button("계산하기", key="power"):
            try:
                result = base ** exp
                st.success(f"결과: {base} ^ {exp} = {result}")
            except OverflowError:
                st.error("수의 크기가 너무 커서 계산할 수 없습니다.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

    # --------------------------
    # 로그 연산
    # --------------------------
    elif calc_type == "로그":
        st.subheader("로그 연산 (log_b(a))")

        value = st.number_input("진수 (a, 0보다 커야 함)", value=8.0, format="%.10g")
        base = st.number_input(
            "밑 (b, 0보다 크고 1이 아니어야 함)", value=2.0, format="%.10g"
        )

        if st.button("계산하기", key="log"):
            try:
                if value <= 0:
                    st.error("진수 a는 0보다 커야 합니다.")
                elif base <= 0 or base == 1:
                    st.error("밑 b는 0보다 크고 1이 아니어야 합니다.")
                else:
                    result = math.log(value, base)
                    st.success(f"결과: log_{base}({value}) = {result}")
            except ValueError as e:
                st.error(f"정의역에 맞지 않습니다: {e}")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

    # --------------------------
    # 합동(mod) 연산
    # --------------------------
    elif calc_type == "합동(mod)":
        st.subheader("합동 연산 (mod)")

        mod_mode = st.radio(
            "합동 연산 방식을 선택하세요.",
            ["나머지 계산: a mod n", "합동 판정: a ≡ b (mod n)"],
            horizontal=False,
        )

        # 나머지 계산
        if mod_mode == "나머지 계산: a mod n":
            st.markdown("#### a mod n 계산")

            a = st.number_input("정수 a", value=10, step=1, format="%d")
            n = st.number_input("법 n (양의 정수)", value=3, min_value=1, step=1, format="%d")

            if st.button("계산하기", key="mod_remainder"):
                try:
                    r = int(a) % int(n)
                    st.success(f"결과: {a} mod {n} = {r}")
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

        # 합동 판정
        else:
            st.markdown("#### a ≡ b (mod n) 판정")

            a = st.number_input("정수 a", value=10, step=1, format="%d")
            b = st.number_input("정수 b", value=1, step=1, format="%d")
            n = st.number_input("법 n (양의 정수)", value=3, min_value=1, step=1, format="%d")

            if st.button("판정하기", key="mod_congruence"):
                try:
                    a_int = int(a)
                    b_int = int(b)
                    n_int = int(n)

                    is_cong = (a_int - b_int) % n_int == 0
                    ra = a_int % n_int
                    rb = b_int % n_int

                    if is_cong:
                        st.success(
                            f"{a_int} ≡ {b_int} (mod {n_int}) 가 참입니다. "
                            f"(a mod n = {ra}, b mod n = {rb})"
                        )
                    else:
                        st.error(
                            f"{a_int} ≡ {b_int} (mod {n_int}) 가 거짓입니다. "
                            f"(a mod n = {ra}, b mod n = {rb})"
                        )
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

    # --------------------------
    # 함수 그래프 (y = f(x))
    # --------------------------
    elif calc_type == "함수 그래프 (y = f(x))":
        st.subheader("함수 그래프 그리기 (y = f(x))")

        st.markdown(
            """
        x, y에 대한 **관계식** 중에서, y를 x의 함수 `y = f(x)`로 볼 수 있는 식을  
        Python 수식 형태로 입력하면, 해당 함수의 그래프를 그려줍니다.

        - 곱셈은 `*` (예: `2*x`, `x*(x-1)`)
        - 제곱은 `**` (예: `x**2`, `x**3`)
        - 사용 가능한 함수 예시: `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `abs` 등  
          (자연로그는 `log`, 밑이 10인 로그는 `log10` 사용 가능)
        """
        )

        expr = st.text_input(
            "함수식 f(x)를 입력하세요 (예: x**2 + 3*x - 1, sin(x), exp(-x**2) 등)",
            value="x**2",
        )

        col1, col2 = st.columns(2)
        with col1:
            x_min = st.number_input("x 최소값", value=-10.0, format="%.5g")
        with col2:
            x_max = st.number_input("x 최대값", value=10.0, format="%.5g")

        num_points = st.slider(
            "그래프 해상도 (샘플 개수)", min_value=100, max_value=2000, value=400, step=100
        )

        if st.button("그래프 그리기", key="plot"):
            if x_min >= x_max:
                st.error("x 최소값은 x 최대값보다 작아야 합니다.")
            else:
                try:
                    # x 값 배열 생성
                    x = np.linspace(x_min, x_max, num_points)

                    # eval에서 허용할 안전한 이름들만 따로 dict로 구성
                    allowed_names = {
                        "x": x,
                        "sin": np.sin,
                        "cos": np.cos,
                        "tan": np.tan,
                        "exp": np.exp,
                        "sqrt": np.sqrt,
                        "log": np.log,      # 자연로그
                        "log10": np.log10,  # 상용로그
                        "abs": np.abs,
                        "pi": math.pi,
                        "e": math.e,
                    }

                    # 안전한 eval 실행 (내장함수 차단)
                    y = eval(expr, {"__builtins__": None}, allowed_names)

                    # y가 스칼라(상수 함수)인 경우 처리
                    if np.isscalar(y):
                        y = np.full_like(x, float(y), dtype=float)

                    df = pd.DataFrame({"x": x, "y": y})
                    st.line_chart(df, x="x", y="y")

                    st.code(f"y = {expr}", language="python")
                    st.caption(
                        "입력한 식을 x ∈ [{:.3g}, {:.3g}] 구간에서 그린 그래프입니다.".format(
                            x_min, x_max
                        )
                    )

                except Exception as e:
                    st.error(f"식 해석/계산 중 오류가 발생했습니다: {e}")
                    st.info("식에 사용된 기호(곱셈 *, 제곱 **) 또는 지원하지 않는 함수가 있는지 확인해 보세요.")

    st.divider()
    st.caption(
        "이 앱의 계산기 부분은 Python과 Streamlit으로 작성된 예시입니다. "
        "코드를 수정하여 기능을 확장해 보세요!"
    )

# ==========================================================
# 2. 연도별 세계 인구 분석 앱
# ==========================================================
elif app_mode == "연도별 세계인구분석":
    st.title("🌍 연도별 세계 인구 분석")

    st.write(
        """
    CSV 파일(예: `world_population.csv`)을 업로드하면  
    **1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022년** 기준으로  
    세계 인구를 색으로 구분한 지도를 표시합니다.

    - 각 국가별 인구수 구간에 따라 색을 다르게 표시  
    - 선택한 연도에서 **세계 인구 대비 각 국가의 인구 비중(%)**을 기준으로 색을 칠하는 기능도 포함
    """
    )

    uploaded_file = st.file_uploader("세계 인구 데이터 CSV 파일을 업로드하세요.", type=["csv"])

    if uploaded_file is None:
        st.info("예: `Country`, `Year`, `Population` 처럼 국가/연도/인구 정보가 들어있는 CSV를 올려주세요.")
    else:
        # CSV 읽기
        df = pd.read_csv(uploaded_file)

        st.subheader("📄 데이터 미리 보기")
        st.dataframe(df.head())

        st.markdown("컬럼 매핑을 선택해 주세요. (데이터 형식에 맞게 지정)")

        # 컬럼 선택 (어떤 형식의 CSV든 쓸 수 있도록)
        col_country = st.selectbox("국가 컬럼 선택", options=df.columns, index=0)
        col_year = st.selectbox("연도 컬럼 선택", options=df.columns, index=1 if len(df.columns) > 1 else 0)
        col_pop = st.selectbox("인구수 컬럼 선택", options=df.columns, index=2 if len(df.columns) > 2 else 0)

        # 연도 선택: 문제에서 요구한 특정 연도만 사용
        target_years = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]

        # 연도 컬럼이 숫자형이 아니면 변환 시도
        df[col_year] = pd.to_numeric(df[col_year], errors="coerce")

        available_years = sorted(
            int(y) for y in df[col_year].dropna().unique() if int(y) in target_years
        )

        if len(available_years) == 0:
            st.error("데이터에 1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022 중 포함된 연도가 없습니다.")
        else:
            year = st.selectbox("지도를 그릴 연도 선택", options=available_years)

            # 색칠 기준: 절대 인구수 구간 vs 세계 인구 비중
            color_mode = st.radio(
                "색칠 기준을 선택하세요.",
                ["인구수 구간별 색", "세계 인구 비중(%)"],
                horizontal=True,
            )

            # 선택한 연도 데이터 필터링
            df_year = df[df[col_year] == year].copy()

            # 인구수 숫자형 변환
            df_year[col_pop] = pd.to_numeric(df_year[col_pop], errors="coerce")
            df_year = df_year.dropna(subset=[col_pop, col_country])

            if df_year.empty:
                st.error(f"{year}년 데이터가 비어 있습니다. 다른 연도를 선택해 보세요.")
            else:
                st.subheader(f"🗺 {year}년 세계 인구 지도")

                if color_mode == "인구수 구간별 색":
                    st.markdown("**1) 인구수 구간을 나누어 색으로 구별한 지도**")

                    # 인구수 기준 구간 설정 (원하면 여기 숫자를 수정해서 구간 조정 가능)
                    # 단위: 명
                    bins = [
                        0,
                        1_000_000,      # 100만 미만
                        5_000_000,      # 100만 ~ 500만
                        10_000_000,     # 500만 ~ 1,000만
                        50_000_000,     # 1,000만 ~ 5,000만
                        100_000_000,    # 5,000만 ~ 1억
                        500_000_000,    # 1억 ~ 5억
                        2_000_000_000,  # 5억 이상 (여유)
                    ]
                    labels = [
                        "< 1M",
                        "1M – 5M",
                        "5M – 10M",
                        "10M – 50M",
                        "50M – 100M",
                        "100M – 500M",
                        "≥ 500M",
                    ]

                    df_year["pop_bin"] = pd.cut(
                        df_year[col_pop],
                        bins=bins,
                        labels=labels,
                        include_lowest=True,
                        right=False,
                    )

                    fig = px.choropleth(
                        df_year,
                        locations=col_country,
                        locationmode="country names",  # 국가 이름 컬럼(영문)을 쓰는 것으로 가정
                        color="pop_bin",
                        hover_name=col_country,
                        hover_data={col_pop: ":,"},
                        title=f"{year}년 세계 인구 분포 (인구수 구간별 색)",
                        category_orders={"pop_bin": labels},
                    )
                    fig.update_layout(
                        legend_title_text="인구수 구간",
                        margin=dict(l=0, r=0, t=40, b=0),
                    )

                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.markdown("**2) 세계 인구 대비 각 국가의 인구 비중(%) 기준 지도**")

                    total_pop = df_year[col_pop].sum()
                    df_year["pop_share"] = df_year[col_pop] / total_pop * 100

                    fig = px.choropleth(
                        df_year,
                        locations=col_country,
                        locationmode="country names",
                        color="pop_share",
                        hover_name=col_country,
                        hover_data={
                            col_pop: ":,",
                            "pop_share": ":.2f",
                        },
                        title=f"{year}년 세계 인구 대비 국가별 인구 비중(%)",
                        color_continuous_scale="YlOrRd",
                        labels={"pop_share": "세계 인구 비중(%)"},
                    )
                    fig.update_layout(
                        margin=dict(l=0, r=0, t=40, b=0),
                        coloraxis_colorbar=dict(title="비중(%)"),
                    )

                    st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")
                st.caption(
                    "지도는 Plotly의 choropleth 기능을 사용했습니다. "
                    "CSV에서 국가 이름이 영어로 되어 있고, 세계 지도와 매칭 가능한 경우에 잘 표시됩니다."
                )
