import os
import requests
from bs4 import BeautifulSoup


def fetch_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        else:
            print(f"无法访问 {url}，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求 {url} 时发生错误: {e}")
        return None


def parse_content(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    article_title = soup.select_one('#title').get_text() if soup.select_one('#title') else "无标题"
    main_content = soup.select_one('.content#article')

    if not main_content:
        print("未找到正文内容")
        return "该网页无正文", article_title

    for img in main_content.find_all('img'):
        img.decompose()

    main_text = ""
    for p in main_content.find_all('p'):
        main_text += p.get_text() + "\n"

    return main_text, article_title


def save_to_txt(text, filename, title):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(title + "\n\n")
        f.write(text)


def get_pagination_links(base_url):
    html = fetch_page(base_url)
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    pagination_div = soup.find('div', class_='pages')
    if not pagination_div:
        return []

    links = [a['href'] for a in pagination_div.find_all('a', href=True)]
    return list(set(links))


def main():
    base_url = "https://h2.in-en.com/policy/"
    all_links = set()
    all_links.add(base_url)

    for page in range(2, 3):
        url = f"https://h2.in-en.com/policy/list3402-{page}.html"
        all_links.add(url)

    if not os.path.exists("policy"):
        os.makedirs("policy")

    for link in all_links:
        print(f"处理分页: {link}")
        html = fetch_page(link)
        if not html:
            continue

        soup = BeautifulSoup(html, 'html.parser')
        article_links = [a['href'] for a in soup.select('.listTxt h5 a')]

        if not article_links:
            print(f"在分页 {link} 中没有找到任何链接")
        else:
            for article_link in article_links:
                print(f"找到链接: {article_link}")
                page_html = fetch_page(article_link)
                if page_html:
                    main_text, article_title = parse_content(page_html, article_link)

                    safe_title = "".join(c for c in article_title if c.isalnum() or c in (' ', '_')).strip().replace(
                        ' ', '_')
                    output_filename = os.path.join("policy", f"{safe_title}.txt")
                    save_to_txt(main_text, output_filename, article_title)
                    print(f"已保存 {output_filename}")


if __name__ == "__main__":
    main()