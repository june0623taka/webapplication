# テスト用のアプリ

import streamlit as st
from log_Custom import log_user_action
from remote_ip import get_remote_ip
from CustomPrint import CustomPrint
import sys

# アプリの設定
st.title('テスト')

# 入力フィールド
app_name = st.text_input("アプリ名を入力してください。")
user_id = st.text_input("ユーザIDを入力してください。")
log_directory = st.text_input("保存先パスを入力してください。")
uploaded_file = st.file_uploader("Pythonスクリプトをアップロードしてください", type=["py"])



# 送信ボタンが押下されたときの処理
if st.button('送信'):
	if app_name and user_id and log_directory and uploaded_file:
		# UUIDとセッションIDを生成
		session = get_remote_ip()
		session_id = session[1]
  
  
  
		if not isinstance(sys.stdout, CustomPrint):
			sys.stdout = CustomPrint(user_id=user_id, session_id=session_id)
		else:
			# 既存のインスタンスがある場合は、user_idとsession_idを更新
			sys.stdout.user_id = user_id
			sys.stdout.session_id = session_id
		
		# サイドバーに表示
		st.sidebar.write(f'セッション:{session}')
		
		#sys.stdout = CustomPrint(user_id=user_id, session_id=session_id)
		
		#ログの設定と記録
		message = log_user_action(app_name, user_id, log_directory, session_id, uploaded_file)
	else:
		st.warning('すべてのフィールドを入力してください。')