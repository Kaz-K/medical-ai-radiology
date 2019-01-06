import os
import vtk
import numpy as np
import pydicom as dicom

# DICOM画像を格納するフォルダのパスをグローバル変数として指定する
DICOM_DIR_PATH = 'sample_dicom'


if __name__ == '__main__':

    # DICOMフォーマットの基本
    # フォルダ中のDICOMファイルの一つを指定するパス
    file_path = os.path.join(DICOM_DIR_PATH, 'image-000000.dcm')

    # pydicomモジュールを用いてDICOMファイルを読み出す
    dcm_file = dicom.read_file(file_path)

    # DICOMファイルの内容を表示する
    print(dcm_file)

    # DICOMファイルから画像情報を取得して表示する
    # 圧縮形式かどうかを判別し、必要に応じて解凍する
    # 注意：環境によってはgdcmを別途インストールする必要あり
    transfer_syntax_uid = dcm_file.file_meta.TransferSyntaxUID
    if transfer_syntax_uid.is_compressed:
        dcm_file.decompress()

    print(dcm_file.pixel_array)
