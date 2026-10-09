import requests
from bs4 import BeautifulSoup
import csv
import time

# 请求头，模拟浏览器，防止被网站直接拒绝
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def get_movies(page):
    """获取指定页面的电影信息"""
    url = f"https://movie.douban.com/top250?start={page * 25}"
    response = requests.get(url, headers=HEADERS, timeout=10)

    # 检查请求是否成功（状态码 200 表示成功）
    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    movie_list = []

    # 找到所有电影条目
    for item in soup.find_all("div", class_="item"):
        title = item.find("span", class_="title").text          # 电影名
        rating = item.find("span", class_="rating_num").text    # 评分
        quote_tag = item.find("span", class_="inq")             # 短评（可能没有）
        quote = quote_tag.text if quote_tag else ""

        movie_list.append({
            "title": title,
            "rating": rating,
            "quote": quote
        })

    return movie_list

def save_to_csv(movies, filename="douban_top250.csv"):
    """把数据保存到 CSV 文件"""
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "rating", "quote"])
        writer.writeheader()
        writer.writerows(movies)

if __name__ == "__main__":
    all_movies = []

    # 豆瓣 Top250 共 10 页，每页 25 条
    for page in range(10):
        print(f"正在爬取第 {page + 1} 页...")
        movies = get_movies(page)
        all_movies.extend(movies)
        time.sleep(1)  # 每爬一页休息 1 秒，避免请求过快被封

    save_to_csv(all_movies)
    print(f"爬取完成，共获取 {len(all_movies)} 条数据，已保存到 douban_top250.csv")