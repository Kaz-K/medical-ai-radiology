import os
import numpy as np
import pydicom as dicom
import matplotlib.pyplot as plt

from utils import scale_image


# DICOM画像を格納するフォルダのパスをグローバル変数として指定する
DICOM_DIR_PATH = 'sample_dicom'


if __name__ == '__main__':

    # 1.DICOMフォーマットの基本
    # フォルダ中のDICOMファイルの一つを指定するパス
    file_path = os.path.join(DICOM_DIR_PATH, 'image-000000.dcm')

    # pydicomモジュールを用いてDICOMファイルを読み出す
    dcm_file = dicom.read_file(file_path)

    # DICOMファイルの内容を表示する
    print(dcm_file)

    # 2.DICOMファイルから画像情報を取得して表示する
    # 圧縮形式かどうかを判別し、必要に応じて解凍する
    # 注意: 環境によってはgdcmを別途インストールする必要あり
    transfer_syntax_uid = dcm_file.file_meta.TransferSyntaxUID
    if transfer_syntax_uid.is_compressed:
        dcm_file.decompress()

    # pixel_arrayに格納されるピクセル情報を取得する
    pixel_array = dcm_file.pixel_array

    print('pixel_arrayの最大値: ', np.max(pixel_array))  # 2305
    print('pixel_arrayの最小値: ', np.min(pixel_array))  # 0

    # CT値に変換するための定型処理
    # 注意: グレースケールの方向を知りたい場合にはPhotometricInterpretationを参照する
    rescale_intercept = dcm_file.RescaleIntercept
    rescale_slope = dcm_file.RescaleSlope

    print('rescale_intercept: ', rescale_intercept)     # -1000
    print('rescale_slope: ', rescale_slope)             # 1

    image = rescale_slope * pixel_array + rescale_intercept

    print('imageの最大値: ', np.max(image))              # 1305.0
    print('imageの最小値: ', np.min(image))              # -1000.0

    print('image: ', image)                             # [[-1000, -1000, ...]]

    # 3.階調処理を施して画像として表示する
    image = scale_image(image, 2000, 400)

    print('階調処理後のimageの最大値: ', np.max(image))    # 242.88
    print('階調処理後のimageの最小値: ', np.min(image))    # 0.0

    # matplotlibを用いて画像を表示する
    plt.imshow(image, cmap='gray')
    plt.show()
