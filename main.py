import streamlit as st
import math

# --------------------------
# 기본 설정
# --------------------------
st.set_page_config(page_title="수학 계산기", page_icon="🧮", layout="centered")
st.title("🧮 수학 계산기 (사칙·지수·로그·합동)")

st.write(
    """
기본적인 **사칙연산**, **지수**, **로그**, **합동(mod)** 연산을 지원하는
간단한 웹 계산기입니다.
"""
)

# --------------------------
# 연산 종류 선택
# --------------------------
calc_type = st.selectbox(
    "원하는 연산을 선택하세요.",
    ["사칙연산", "지수", "로그", "합동(mod)"],
)

st.divider()

# --------------------------
# 사칙연산
# --------------------------
if calc_type == "사칙연산":
    st.subheader("사칙연산 ( +, -, ×, ÷ )")

    a = st.number_input("첫 번째 수 (a)", value=0.0, format="%.10g")
    b = st.number_input("두 번째 수 (b)", value=0.0, format="%.10g")

    op = st.radio("연산자를 선택하세요.", ["+", "-", "×", "÷"], horizontal=True)

    if st.button("계산하기", key="basic"):
        try:
            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "×":
                result = a * b
            elif op == "÷":
                if b == 0:
                    st.error("0으로 나눌 수 없습니다.")
                    result = None
                else:
                    result = a / b
            else:
                result = None

            if result is not None:
                st.success(f"결과: {a} {op} {b} = {result}")
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
    base = st.number_input("밑 (b, 0보다 크고 1이 아니어야 함)", value=2.0, format="%.10g")

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
# 하단 설명
# --------------------------
st.divider()
st.caption(
    "이 앱은 Python과 Streamlit으로 작성된 예시입니다. "
    "코드를 수정하여 기능을 확장해 보세요!"
)
