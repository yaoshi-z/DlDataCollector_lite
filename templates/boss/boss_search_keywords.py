# -*- coding: utf-8 -*-
'''
轻量级爬虫脚本，使用DrissionPage库实现
功能：爬取boss直聘网站的职位信息
字段名: 批次号/职位ID/职位名称/薪资/工作经验/学历要求/职位技能/城市/城市区域/业务领域/城市ID/公司名称/公司规模/公司福利
备注: 需要手动登录boss直聘网站，登录后按回车继续
'''

from DrissionPage import ChromiumPage
from urllib.parse import quote
from datetime import datetime
import pandas as pd
import pathlib
import random
import time

# 基础参数配置
dp = ChromiumPage() # 创建DrissionPage对象
spider_name = 'boss_search_keywords' # 爬虫名称
keywords = "python" # 搜索关键词
now = datetime.now().strftime('%Y%m%d%H%M%S') # 获取当前时间
keywords_quote = quote(keywords) # 对关键词进行URL编码
city_code = '101180100' # 城市代码，101180100代表郑州
start_url = f"https://www.zhipin.com/web/geek/jobs?query={keywords_quote}&city={city_code}"  # boss直聘
exports_dir = pathlib.Path(__file__).parent.parent.parent / 'exports' # 导出目录
exports_dir.mkdir(parents=True, exist_ok=True) # 创建导出目录，如果不存在则创建
export_file = exports_dir / f"{spider_name}_{now}.csv" # 导出文件路径
max_count = 300000 # 最大爬取数量
max_page = 10 # 最大页数
sleep_time = random.uniform(1, 3)
job_infos = [] # 用于存储职位信息


dp.listen.start('/search/joblist.json') # 启动监听器，监听职位列表数据

# 启动浏览器并访问页面
dp.get(start_url) # 访问51job,本示例仅限于51job

# 等待登录
input("请登录后按回车继续...") # 等待用户登录

for i in range(max_page):
    if len(job_infos) >= max_count: # 如果已获取的职位信息数量达到最大值，则停止爬取
        print(f"已获取 {len(job_infos)} 条职位信息，达到最大爬取数量 {max_count}，停止爬取")
        break

    # 等待数据加载,接收加载返回的对象
    try:
        r = dp.listen.wait(timeout=10)  # 设置10秒超时
        if not r:
            print("等待数据超时，可能已无新数据")
            break
    except Exception as e:
        print(f"等待数据异常: {e}")
        break

    # 获取响应数据
    json_data = r.response.body # 获取JSON数据
    # 解析JSON数据
    job_lists = json_data.get('zpData', {}).get('jobList', []) # 获取职位列表
    if not job_lists:
        print('没有职位信息,代码可能有误，请检查')
        break
    try:
        # 处理职位信息
        for job in job_lists:
            job_dict = {}
            batch_id = now
            job_id = job.get('encryptJobId', '') # 获取职位ID
            job_name = job.get('jobName', '') # 获取职位名称
            job_salary = job.get('salaryDesc', '') # 获取薪资
            job_experience = job.get('jobExperience', '') # 获取工作经验
            job_degree = job.get('jobDegree', '') # 获取学历要求
            job_skills = job.get('skills', '') # 获取职位技能
            job_city = job.get('cityName', '') # 获取城市
            job_area = job.get('areaDistrict', '') # 获取城市区域
            job_business = job.get('businessDistrict', '') # 获取业务领域
            city_id = job.get('city', '') # 获取城市ID
            company_name = job.get('brandName', '') # 获取公司名称
            company_size = job.get('brandScaleName', '') # 获取公司规模
            company_welfare = job.get('welfareList', '') # 获取公司福利 welfareList

            job_dict.update({
                'batch_id': batch_id,
                'job_id': job_id,
                'job_name': job_name,
                'job_salary': job_salary,
                'job_experience': job_experience,
                'job_degree': job_degree,
                'job_skills': job_skills,
                'job_city': job_city,
                'job_area': job_area,
                'job_business': job_business,
                'city_id': city_id,
                'company_name': company_name,
                'company_size': company_size,
                'company_welfare': company_welfare
            })
            print(job_dict) # 打印职位信息
            job_infos.append(job_dict) # 添加到职位列表
    except Exception as e:
        print(f"解析职位信息异常: {e}")

    # 打印获取的职位信息数量
    print(f"已获取 {len(job_infos)} 条职位信息") # 打印职位列表
    time.sleep(sleep_time) # 等待一段时间
    # 翻页操作
    dp.scroll.to_bottom() # 滚动到页面底部

df = pd.DataFrame(job_infos) # 将职位信息转换为DataFrame
df.to_csv(export_file, index=False, encoding='utf-8-sig') # 保存
