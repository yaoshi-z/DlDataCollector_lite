# -*- coding: utf-8 -*-
'''
轻量级爬虫脚本，使用DrissionPage库实现
功能：爬取51job网站的职位信息
字段名: 批次号/职位ID/标题/链接/公司名称/公司信息/城市/区域/经验/学历/薪资/发布时间/职位描述
备注: 本模板采用多线程爬取,线程数量控制在5个以内
'''

from DrissionPage import ChromiumPage
from urllib.parse import quote
from datetime import datetime
import json
import pandas as pd
import pathlib
import random
from threading import Thread,Lock

# 基础参数配置
spider_name = 'job51_search_keywords_dp' # 爬虫名称
keywords = ["python",'java','c++'] # 搜索关键词
now = datetime.now().strftime('%Y%m%d%H%M%S') # 获取当前时间
max_page = 3 # 最大页数
max_threads = 2 # 最大线程数
all_job_lists = [] # 用于存储所有职位信息


# 文件导出路径
exports_dir = pathlib.Path(__file__).parent.parent.parent / 'exports' # 导出目录
exports_dir.mkdir(parents=True, exist_ok=True) # 创建导出目录，如果不存在则创建
export_file = exports_dir / f"{spider_name}_{now}.csv" # 导出文件路径
export_lock = Lock()

def generate_keywords_quote(keywords,max_threads):
    keywords_quote = [quote(keyword) for keyword in keywords]
    # 如果关键词数量大于最大线程数，则将关键词进行分组, 每组数据不超过最大线程数
    if len(keywords_quote) > max_threads:
        keywords_quote = [keywords_quote[i:i+max_threads] for i in range(0, len(keywords_quote), max_threads)]
    return keywords_quote
def collect_data(tab,export_file):
    # 解析页面数据
    divs = tab.eles('css:.joblist-item') # 定位职位列表的div元素
    job_lists = [] # 用于存储职位信息
    current_page = 1
    while True: # 循环处理每一页的职位信息
        for div in divs:
            job_dict = {}
            info = div.ele('css:.joblist-item-job.sensors_exposure').attr('sensorsdata') # 获取职位信息属性
            info = json.loads(info) # 解析为JSON数据
            batch_id = now
            jb_id = info.get('jobId', '') # 获取职位ID
            jb_title = info.get('jobTitle', '') # 获取职位名称
            jb_salary = info.get('jobSalary', '') # 获取薪资
            area_info = info.get('jobArea', '').split('·')
            jb_city = area_info[0] # 获取城市
            jb_area = area_info[1] if len(area_info) > 1 else '' # 获取城市区域
            jb_year = info.get('jobYear', '') # 获取工作经验
            jb_degree = info.get('jobDegree', '无要求') # 获取学历要求
            commpany_name = div.ele('css:.cname').text.strip() # 获取公司名称
            commpany_info = [i.text for i in div.eles('css:.dc')] # 获取公司信息
            commpany_url = div.ele('css:.cname').attr('href') # 获取公司链接
            page_num = current_page # 获取页码

            job_dict.update({
                'batch_id': batch_id,
                'jb_id': jb_id,
                'jb_title': jb_title,
                'jb_salary': jb_salary,
                'jb_city': jb_city,
                'jb_area': jb_area,
                'jb_year': jb_year,
                'jb_degree': jb_degree,
                'commpany_name': commpany_name,
                'commpany_info': commpany_info,
                'commpany_url': commpany_url,
                'page_num': page_num
            })
        
            job_lists.append(job_dict)
        print(f"已获取 {len(job_lists)} 条职位信息") # 打印职位列表长度
        try:
            next_page = tab.ele('css:.el-icon.el-icon-arrow-right')
            next_page.scroll.to_see()
            if not next_page:
                break
            next_page.click() # 点击下一页按钮
            sleep_time = random.uniform(1, 3)
            tab.wait(sleep_time) # 随机休眠1-3秒
            current_page += 1
            if current_page > max_page:
                break
        except Exception as e:
            print(f"翻页逻辑异常: {e}")

    with export_lock:
        all_job_lists.extend(job_lists) # 将当前关键词的职位信息添加到总列表中
        # 保存职位信息到CSV文件
        df = pd.DataFrame(all_job_lists)
        df.to_csv(export_file, index=False, encoding='utf-8-sig')
        print(f"职位信息已保存到 {export_file}")

def main():
    keywords_quote = generate_keywords_quote(keywords,max_threads)
    for keywords_list in keywords_quote:
        page = ChromiumPage()
        start_urls = []
        threads = []
        for keyword in keywords_list:
            url = f"https://we.51job.com/pc/search?jobArea=170200&keyword={keyword}&searchType=2&keywordType="# 51job
            start_urls.append(url)
        page.get(start_urls[0])
        tab1 = page.get_tab()
        t1 = Thread(target=collect_data, args=(tab1, export_file))
        t1.start()
        threads.append(t1)

        # 循环创建线程
        for i in range(1, len(start_urls)):
            tab = page.new_tab(start_urls[i])
            tab = page.get_tab(tab)  
            t= Thread(target=collect_data, args=(tab, export_file))
            t.start()
            threads.append(t)
        # 等待所有线程结束,并释放资源
        for t in threads:
            t.join(timeout=30)
        page.quit()
  
if __name__ == '__main__':
    main()


