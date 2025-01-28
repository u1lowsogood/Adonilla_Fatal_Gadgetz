from typing import List

class LogManager:
    def __init__(self, max_logs: int = 10):
        self.logs: List[str] = [" ", " ", "さあいよいよ始まりました！", "「第百回 アドン杯」！"]
        self.max_logs = max_logs
        self.log_index = 0

    def add(self, message: str):
        if message is None:
            return
        self.logs.append(message)
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
        
        self.log_index += 1

    def format_logs(self, turn) -> str:
        log_msg = f"```md\n# logs (turn: {turn})\n"
        for idx, log in enumerate(self.logs[-4:], start=1): 
            log_msg += f"{len(self.logs) - 4 + idx}. {log}\n"
        log_msg += "```"
        return log_msg
