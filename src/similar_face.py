import cv2
import pprint
import urllib.request

from modules.osyarista_test_lists import get_osyarista_lists

def get_osyarista_image(osyarista_lists):
    try:
        for osyarista in osyarista_lists:
            image_url = osyarista['プロフィール写真']
            with urllib.request.urlopen(url=image_url) as image_data:
                with open(f"images/osyarista/{osyarista['名前']}_{osyarista['身長'].replace('cm', '')}.png", mode='xb') as image_file:
                    image_file.write(image_data.read())
    except FileExistsError:
        print(f"{osyarista['名前']} は、既に存在します。")
        pass

if __name__ == '__main__':
    results = []
    osyarista_lists = get_osyarista_lists()

    target_image_data = cv2.imread('images/kawamura_yuka.jpg') # 画像データ（対象者）
    target_user = cv2.AKAZE_create().detectAndCompute(target_image_data, None)[1]

    for osyarista in osyarista_lists:
        comparator_file_name = f"images/osyarista/{osyarista['名前']}_{osyarista['身長'].replace('cm', '')}.png" # 画像データ（比較者）
        comparator_image_data = cv2.imread(comparator_file_name)
        comparator = cv2.AKAZE_create().detectAndCompute(comparator_image_data, cv2.IMREAD_GRAYSCALE, None)[1]

        try:
            dist = [m.distance for m in cv2.BFMatcher(cv2.NORM_HAMMING).match(target_user, comparator)]
            score = sum(dist) / len(dist)
        except cv2.error:
            score = 100000

        results.append({
            '名前': osyarista['名前'],
            '類似度': score,
            'プロフィール写真': osyarista['プロフィール写真']
        })

    results = pprint.pprint(sorted(results, key=lambda x: x['類似度']))
    print(results)
    print('処理が正常終了しました。')
