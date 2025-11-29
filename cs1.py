import requests

def upload_picgo(file_path, api_key):
    """
    上传图片到 picgo.net，并返回 (图片URL, 删除URL)
    :param file_path: 本地文件路径
    :param api_key: X-API-Key
    :return: (url, delete_url) 或 None
    """
    url = "https://www.picgo.net/api/1/upload"
    headers = {
        "X-API-Key": api_key
    }
    files = {
        "source": open(file_path, "rb")
    }

    try:
        resp = requests.post(url, headers=headers, files=files)
        resp.raise_for_status()
        data = resp.json()

        # 检查返回结构
        if "image" in data and "url" in data["image"] and "delete_url" in data["image"]:
            img_url = data["image"]["url"]
            delete_url = data["image"]["delete_url"]
            return img_url, delete_url
        else:
            print(f"⚠️ API 返回中缺少必要字段: {data}")
            return None
    except Exception as e:
        print(f"上传出错: {e}")
        return None
    finally:
        files["source"].close()
# 示例用法
if __name__ == "__main__":
    api_key = "chv_Sz5XA_2b5fe5041ad392c8fa66bb7be28d86a67c86599d327e7fb5fbcd14764900a97b56df206e550a78eb2051ea8ee1ec401df0c392d3f172a14370941ee37c4290be"
    result = upload_picgo("tset.jpeg", api_key)
    if result:
        img_url, del_url = result
        print(f"图片 URL: {img_url}")
        print(f"删除 URL: {del_url}")
