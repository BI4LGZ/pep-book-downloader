#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import json
import argparse
import requests
from PIL import Image
import shutil


def load_custom_headers(headers_file):
    if not os.path.exists(headers_file):
        print(f"指定的请求头文件 {headers_file} 不存在。")
        sys.exit(1)
    with open(headers_file, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception as e:
            print(f"加载请求头文件失败: {e}")
            sys.exit(1)


def parse_url(input_url):
    code_match = re.search(r"book\.pep\.com\.cn/(\d+)", input_url)
    if not code_match:
        print("无法从 URL 中提取教材编码，请检查 URL 格式。")
        sys.exit(1)
    code = code_match.group(1)
    query = ""
    if "?" in input_url:
        query = "?" + input_url.split("?", 1)[1]
    return code, query


def download_image(session, url, save_path):
    try:
        response = session.get(url, timeout=15)
        if response.status_code == 200:
            if not response.content:
                print(f"下载的内容为空，URL: {url}")
                return False
            try:
                content = response.content.decode(errors="ignore")
                if "Page Verification" in content or "nocaptcha" in content:
                    print(f"检测到验证码页面内容，URL: {url}")
                    return False
            except Exception:
                pass
            with open(save_path, "wb") as f:
                f.write(response.content)
            if os.path.getsize(save_path) == 0:
                print(f"下载的文件大小为 0，URL: {url}")
                return False
            print(f"已下载: {save_path}")
            return True
        else:
            print(f"请求 {url} 返回状态码 {response.status_code}")
            return False
    except Exception as e:
        print(f"请求 {url} 失败: {e}")
        return False


def merge_images_to_pdf(image_files, output_pdf):
    if not image_files:
        print("没有可合并的图片！")
        return
    first_image = Image.open(image_files[0]).convert("RGB")
    target_size = first_image.size
    processed_images = [first_image]
    try:
        resample_method = Image.Resampling.LANCZOS
    except AttributeError:
        resample_method = Image.ANTIALIAS
    for img_path in image_files[1:]:
        img = Image.open(img_path).convert("RGB")
        img.thumbnail(target_size, resample_method)
        new_img = Image.new("RGB", target_size, (255, 255, 255))
        paste_x = (target_size[0] - img.width) // 2
        paste_y = (target_size[1] - img.height) // 2
        new_img.paste(img, (paste_x, paste_y))
        processed_images.append(new_img)
    processed_images[0].save(
        output_pdf, save_all=True, append_images=processed_images[1:]
    )
    print(f"PDF 文件已生成: {output_pdf}")


def clear_previous_files(images_dir, output_pdf):
    if os.path.exists(images_dir):
        try:
            for filename in os.listdir(images_dir):
                file_path = os.path.join(images_dir, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            print(f"已清空目录: {images_dir}")
        except Exception as e:
            print(f"清空目录 {images_dir} 时发生错误: {e}")
    else:
        os.makedirs(images_dir)
        print(f"创建目录: {images_dir}")
    if os.path.exists(output_pdf):
        try:
            os.remove(output_pdf)
            print(f"已删除旧的 PDF 文件: {output_pdf}")
        except Exception as e:
            print(f"删除旧的 PDF 文件 {output_pdf} 时发生错误: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="使用自定义请求头下载电子教材图片并合并成 PDF"
    )
    parser.add_argument(
        "url",
        help="教材的移动端 URL，例如：https://book.pep.com.cn/1311001202171/mobile/index.html",
    )
    parser.add_argument(
        "--headers_file",
        default="headers.json",
        help="自定义请求头的 JSON 文件路径（默认：headers.json）",
    )
    parser.add_argument(
        "--start_page", type=int, default=1, help="起始页码（默认从1开始下载）"
    )
    parser.add_argument(
        "--max_failures",
        type=int,
        default=3,
        help="连续下载失败次数达到设定值后停止（默认3）",
    )
    parser.add_argument("--output", default="output.pdf", help="生成的 PDF 文件名")
    args = parser.parse_args()

    images_dir = os.path.join(os.getcwd(), "images")
    clear_previous_files(images_dir, args.output)
    headers = load_custom_headers(args.headers_file)
    session = requests.Session()
    session.headers.update(headers)
    code, query = parse_url(args.url)
    print(f"教材编码：{code} 查询字符串：{query}")
    downloaded_files = []
    page = args.start_page
    consecutive_failures = 0
    while True:
        image_url = f"https://book.pep.com.cn/{code}/files/mobile/{page}.jpg{query}"
        image_path = os.path.join(images_dir, f"{page}.jpg")
        success = download_image(session, image_url, image_path)
        if success:
            downloaded_files.append(image_path)
            consecutive_failures = 0
        else:
            consecutive_failures += 1
            if consecutive_failures >= args.max_failures:
                print("连续失败次数达到设定值，停止下载。")
                break
        page += 1
        time.sleep(0.5)

    def sort_key(path):
        basename = os.path.basename(path)
        m = re.match(r"(\d+)", basename)
        return int(m.group(1)) if m else 0

    downloaded_files.sort(key=sort_key)
    merge_images_to_pdf(downloaded_files, args.output)


if __name__ == "__main__":
    main()
