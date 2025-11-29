import streamlit as st
import math
import numpy as np
import pandas as pd

# --------------------------
# 기본 설정
# --------------------------
st.set_page_config(page_title="수학 계산기", page_icon="🧮", layout="centered")
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

    # 여기서 라벨을 좀 더 길게 적어서 +, -가 확실히 보이게 함
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
                if b == 0:
                    st.error("0으로 나눌 수 없습니다.")
                    result = None
                    symbol = "÷"
                else:
                    result = a / b
                    symbol = "÷"
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
  (자연로그는 `log`, 밑이 10인 로그는 `log10`을 사용할 수 있도록 아래에서 정의)
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

    num_points = st.slider("그래프 해상도 (샘플 개수)", min_value=100, max_value=2000, value=400, step=100)

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
                    # math 모듈의 주요 함수들
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

                # y가 스칼라로 나온 경우(상수 함수) 처리
                if np.isscalar(y):
                    y = np.full_like(x, float(y), dtype=float)

                # DataFrame으로 만들어서 line_chart로 그리기
                df = pd.DataFrame({"x": x, "y": y})
                st.line_chart(df, x="x", y="y")

                st.code(f"y = {expr}", language="python")
                st.caption("입력한 식을 x ∈ [{:.3g}, {:.3g}] 구간에서 그린 그래프입니다.".format(x_min, x_max))

            except Exception as e:
                st.error(f"식 해석/계산 중 오류가 발생했습니다: {e}")
                st.info("식에 사용된 기호(곱셈 *, 제곱 **) 또는 지원하지 않는 함수가 있는지 확인해 보세요.")

# --------------------------
# 하단 설명
# --------------------------
st.divider()
st.caption(
    "이 앱은 Python과 Streamlit으로 작성된 예시입니다. "
    "코드를 수정하여 기능을 확장해 보세요!"
)
