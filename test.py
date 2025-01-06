import sys
import datetime

class CustomPrint:
    def __init__(self, user_id=None, session_id=None):
        self.original_stdout = sys.stdout  # 元の標準出力を保存
        self.user_id = user_id
        self.session_id = session_id

    def write(self, message):
        # メッセージが空行ではない場合のみ処理
        if message.strip():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_info = f"UserID: {self.user_id}" if self.user_id else "UserID: Unknown"
            session_info = f"SessionID: {self.session_id}" if self.session_id else "SessionID: Unknown"
            # カスタマイズされたフォーマットで出力
            self.original_stdout.write(f"{timestamp} | {user_info} | {session_info} - {message}\n")

    def flush(self):
        # 標準出力用にflushを定義する必要があるが、何も行わない
        pass

# CustomPrintを標準出力として使用
sys.stdout = CustomPrint(user_id="User123", session_id="Sess456")

# 通常のprint文と同じように使用
print("アプリが起動しました")
print("ユーザーが操作を実行しました")
print("エラーが発生しました")
