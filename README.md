## ■ 2枚の顔写真から、類似度を測定する。

### ① 技術仕様

1. Python［Version: 3.11.3］
    - pip［Version: 23.0.1］
        - opencv-contrib-python［Version: 4.7.0.72］
2. Docker［Version: 20.10.17］

### ② 動作環境

```dockerfile
# $ docker build --tag 'Docker イメージ名':latest --no-cache .
# $ docker run --name 'Docker コンテナ名' --volume 'ホストOS':/usr/local/src --interactive --tty --detach --rm 'Docker イメージ名':latest

FROM python:3.11.3

COPY ./src /usr/local/src
WORKDIR /usr/local/src

RUN apt-get update \
    && apt-get install -y libgl1-mesa-dev

RUN pip install --upgrade pip \
    && pip install -r requirements.txt
```

### ③ 実装内容

```Python
import cv2
import pprint

if __name__ == '__main__':
    results = []

    target_image_data = cv2.imread('画像ファイル（顔を比較する対象者）')
    target_user = cv2.AKAZE_create().detectAndCompute(target_image_data, None)[1]

    for '比較者' in '比較者の一覧':
        comparator_file_name = f"画像ファイル（比較者の顔写真）"
        comparator_image_data = cv2.imread(comparator_file_name)
        comparator = cv2.AKAZE_create().detectAndCompute(comparator_image_data, cv2.IMREAD_GRAYSCALE, None)[1]

        try:
            dist = [m.distance for m in cv2.BFMatcher(cv2.NORM_HAMMING).match(target_user, comparator)]
            score = sum(dist) / len(dist)
        except cv2.error:
            score = 100000 # 比較に失敗した場合、一律で「100000」を設定

        results.append({
            '名前': '名前',
            '類似度': score,
            'プロフィール写真': '元の画像ファイル'
        })

    results = pprint.pprint(sorted(results, key=lambda x: x['類似度'])) # 類似度の値を昇順で並び替える。
    print(results)
    print('処理が正常終了しました。')
```

---

### ③ 処理結果

1. 今回 ユーザーデータとして使用した画像ファイル

    <img src='https://www.pakutaso.com/shared/img/thumb/yukayukaFTHG4550_TP_V4.jpg' width='25%' />

    > クリスマスのキャンペーンに呼び出された女子 | ぱくたそ  
    > → https://www.pakutaso.com/20181213354yukachristmas03.html

2. 今回 比較するデータとして使用した一覧

    - [おしゃリスタ | GU](https://www.gu-global.com/jp/ja/feature/contents/osharista) から抽出した 100名  
    → https://www.gu-global.com/jp/ja/feature/contents/osharista

3. 処理結果は、以下の通りです。

    - 顔付きが似ているおしゃリスタ 3名  
    ※ 左から類似度が高い（顔付きが似ている）順

        <img src='https://api.fastretailing.com/ugc/v1/uq/jp/SR_IMAGES/ugc_stylehint_user_3949955' width='25%' />
        <img src='https://api.fastretailing.com/ugc/v1/uq/jp/SR_IMAGES/ugc_stylehint_user_3949988' width='25%' />
        <img src='https://api.fastretailing.com/ugc/v1/uq/jp/SR_IMAGES/ugc_stylehint_user_3285687' width='25%' />

    - 顔付きが似ていないおしゃリスタ 3名  
    ※ 左から類似度が低い（顔付きが似ていない）順

        <img src='https://api.fastretailing.com/ugc/v1/uq/jp/SR_IMAGES/ugc_stylehint_user_3266951' width='25%' />
        <img src='https://api.fastretailing.com/ugc/v1/uq/jp/SR_IMAGES/ugc_stylehint_user_3266833' width='25%' />
        <img src='https://api.fastretailing.com/ugc/v1/uq/jp/SR_IMAGES/ugc_stylehint_user_3266884' width='25%' />
