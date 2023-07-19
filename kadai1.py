import streamlit as st
import pandas as pd
from janome.tokenizer import Tokenizer
from io import StringIO
from janome.charfilter import RegexReplaceCharFilter
from janome.analyzer import Analyzer

tokenizer = Tokenizer()

# streamlit run kadai1.py のようにして実行する。


def main():
    st.title("課題1 形態素解析 完成版")
    string = "Pythonは1991年にオランダ人のグイド・ヴァン・ロッサム氏によって開発されたプログラミング言語です。"
    select = st.radio("どの入力方法で形態素解析しますか？", ("テキスト形式", "ファイル形式"))
    if select == "テキスト形式":
        string = fillin_file()
    if select == "ファイル形式":
        string = upload_file()
    st.header("入力文")
    st.text(string)
    st.header("分かち書き")
    # string 引数を形態素解析 t.で指定
    mk_table(string)


def upload_file():
    # ファイル形式での読み取り
    uploaded_file = st.file_uploader("形態素解析したいtxtファイルを読み込んでね", type="txt")
    if uploaded_file is not None:
        stringIo = StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_raw = stringIo.read()
        st.text(string_raw)
        string = string_raw.rstrip("\n")
        return string
    else:
        string = "ファイルを用意してね"
        return string


def fillin_file():
    # 文字入力形式での読み取り
    string = st.text_input(
        "形態素解析したい文章を入力してね", "Pythonは1991年にオランダ人のグイド・ヴァン・ロッサム氏によって開発されたプログラミング言語です。"
    )
    return string


def divide_str(string):
    char_filters = [
        # 改行と記号を除去する。
        RegexReplaceCharFilter("-/;:-! \n", ""),
        RegexReplaceCharFilter("\\s+", ""),
    ]
    token_filters = []
    divided_string = ""
    surface_list = []
    analyzer = Analyzer(char_filters=char_filters, token_filters=token_filters)
    for token in analyzer.analyze(string):
        divided_string += token.surface + " | "
        surface_list.append(token.surface)
    return surface_list


def mk_table(string):
    surface_list = []
    speech_list = []
    times_list = []
    read_list = []
    count = collections.Counter(divide_str(string))

    sorted_by_desc_list = count.most_common()
    # 文字と頻度をくっつけた
    surface_list = []
    for i in range(len(sorted_by_desc_list)):
        # print(sorted_by_desc_list[i][0])
        surface_list.append(sorted_by_desc_list[i][0])
        speech_list.append(
            tokenizer.tokenize(sorted_by_desc_list[i][0])
            .__next__()
            .part_of_speech.split(",")[0]
        )
        times_list.append(sorted_by_desc_list[i][1])
        read_list.append(
            tokenizer.tokenize(sorted_by_desc_list[i][0]).__next__().reading
        )
    df = pd.DataFrame(
        {"回数": times_list, "単語名": surface_list, "読み方": read_list, "品詞": speech_list}
    )
    select = st.radio("品詞の指定はしますか", ("指定なし", "名詞", "動詞", "形容詞", "記号", "助動詞"))
    if select == "指定なし" or select is None:
        st.header("形態素解析")
        st.table(df)
    else:
        st.header("形態素解析:{}".format(select))
        st.table(df[df["品詞"] == select])


if __name__ == "__main__":
    main()

