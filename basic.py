import os
import pydicom as dicom


# DICOM画像を格納したディレクトリを指定するパス
DICOM_DIR_PATH = './dicom'


if __name__ == '__main__':

    # 最初のDICOMファイル (Image001.dcm) を指定するパス
    file_path = os.path.join(DICOM_DIR_PATH, 'image-000000.dcm')

    # pydicomライブラリを用いて最初のDICOMファイルを読み込む
    dcm = dicom.read_file(file_path)

    # 最初のDICOMファイルの内容を出力する
    print(dcm)
