import os
import feedparser
import telebot
import yfinance as yf

# GitHub Secrets에서 정보 불러오기
TOKEN = os.environ.get("8202610345:AAHOegOJo2OxnazBZR-FVJkiMkW490Rho_k")
CHAT_ID = os.environ.get("271408530")

bot = telebot.TeleBot(TOKEN)


def get_hot_news():
    """구글 뉴스 RSS 주요 뉴스 top 5"""
    rss_url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)

    news_text = "🔥 **오늘의 주요 이슈 뉴스**\n\n"
    for i, entry in enumerate(feed.entries[:5], 1):
        news_text += f"{i}. [{entry.title}]({entry.link})\n\n"
    return news_text


def get_market_report():
    """주요 증시 지수 조회"""
    tickers = {"코스피": "^KS11", "S&P 500": "^GSPC", "나스닥": "^IXIC"}
    market_text = "📊 **오늘의 주요 증시 요약**\n\n"

    for name, symbol in tickers.items():
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="2d")
            if len(hist) >= 2:
                prev_close = hist["Close"].iloc[-2]
                curr_close = hist["Close"].iloc[-1]
                change = curr_close - prev_close
                change_pct = (change / prev_close) * 100

                sign = "+" if change >= 0 else ""
                market_text += (
                    f"• **{name}**: {curr_close:,.2f} ({sign}{change_pct:.2f}%)\n"
                )
        except Exception:
            market_text += f"• **{name}**: 정보 조회 실패\n"

    return market_text


def send_daily_briefing():
    market_text = get_market_report()
    news_text = get_hot_news()
    full_message = f"{market_text}\n---\n\n{news_text}"

    try:
        bot.send_message(
            CHAT_ID,
            full_message,
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )
        print("전송 완료!")
    except Exception as e:
        print(f"전송 실패: {e}")


if __name__ == "__main__":
    send_daily_briefing()
