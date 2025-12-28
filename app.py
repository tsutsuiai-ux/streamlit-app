from dotenv import load_dotenv
import os
load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate  

# LLMの初期化
llm = ChatOpenAI(
    model="gpt-4o-mini",  
    temperature=0.5
)


# アドバイス関数
def result_chain(param, system_template):
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", "{input}")
        ])
        chain = prompt | llm
        result = chain.invoke({"input": param}).content
        return result
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# 各アドバイスツールの定義
def reskilling_advice(param):
    system_template = """
    あなたはリスキリングの専門家AIです。
    ユーザーの現在のスキルセット、目標、業界のトレンドを考慮し、
    効果的なリスキリング戦略を提案します。
    必要なスキル、学習リソース、実践方法について具体的なアドバイスを提供してください。
    学習ソースには、オンラインコース、書籍、コミュニティなどを含めてください。あわせて、情報の引用をお願いします。
    """
    return result_chain(param, system_template)

def career_change_advice(param):
    system_template = """
    あなたは「転職活動を始める前の準備支援」に特化したキャリア戦略AIです。

    最初に必ず以下を行ってください：
    - 現時点で転職した場合の成功確率を定性的に評価する
    高 / 中 / 低 とその理由）

    次に以下を整理してください：
    1. 転職市場から見たユーザーの強み
    2. 転職時に不利になりやすいポイント
    3. 短期間で補完可能なギャップ
    4. 構造的に時間がかかるギャップ

    その上で：
    - 今すぐ転職すべきか
    - 一定期間、準備に集中すべきか
    を明確に示してください。
    最後に、具体的な準備アクションプランを提示してください。

    履歴書添削や面接テクニックのみの助言は行わないでください。
    """
    return result_chain(param, system_template)

def side_job_advice(param):
    system_template = """
    あなたは副業の専門家AIです。
    ユーザーのスキル、興味、利用可能な時間を考慮し、
    適切な副業の選択肢を提案します。
    具体的な副業内容ついてアドバイスを提供してください。
    可能であれば、成功事例やリスク管理の方法についても言及してください。
    """
    return result_chain(param, system_template)

# Streamlitアプリ
st.title("キャリアアドバイスアプリ")

st.write("##### 動作モード1: リスキリングアドバイス")
st.write("##### 動作モード2: 転職アドバイス")
st.write("##### 動作モード3: 副業アドバイス")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["リスキリングアドバイス", "転職アドバイス", "副業アドバイス"]
)

st.divider()

user_input = st.text_area(label="アドバイスを得るための情報を入力してください。", placeholder="例: 現在のスキル、目標、職歴など")

if st.button("実行"):
    st.divider()
    if user_input:
        if selected_item == "リスキリングアドバイス":
            result = reskilling_advice(user_input)
            st.write("### リスキリングアドバイス")
            st.write(result)
        elif selected_item == "転職アドバイス":
            result = career_change_advice(user_input)
            st.write("### 転職アドバイス")
            st.write(result)
        elif selected_item == "副業アドバイス":
            result = side_job_advice(user_input)
            st.write("### 副業アドバイス")
            st.write(result)
    else:
        st.error("アドバイスを得るための情報を入力してください。")