import os
import vtk

from utils import decompress_dicom_files


# DICOM画像を格納するフォルダのパスをグローバル変数として指定する
DICOM_DIR_PATH = 'sample_dicom'


if __name__ == '__main__':

    # 前処理として圧縮されたDICOMファイルを全て解凍する
    decompress_dicom_files(DICOM_DIR_PATH)

    # vtkDICOMImageReaderでDICOM画像シリーズが格納されたフォルダを読み出す
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(DICOM_DIR_PATH)
    reader.Update()

    # vtkImageDataへと変換する
    image = reader.GetOutput()

    viewer = vtk.vtkImageViewer2()
    viewer.SetInputData(image)

    istyle = vtk.vtkInteractorStyleImage()
    iren = vtk.vtkRenderWindowInteractor()
    viewer.SetupInteractor(iren)
    iren.SetInteractorStyle(istyle)

    min_slice = viewer.GetSliceMin()
    max_slice = viewer.GetSliceMax()

    # 描画中の状態変数(slice番号等)を格納する
    actions = {'slice': min_slice}

    # マウス・ホイールに対するコールバック関数
    def mouse_wheel_forward_event(caller, event):
        if actions['slice'] > min_slice:
            actions['slice'] -= 1
            viewer.SetSlice(actions['slice'])
            viewer.Render()

    def mouse_wheel_backward_event(caller, event):
        if actions['slice'] < max_slice:
            actions['slice'] += 1
            viewer.SetSlice(actions['slice'])
            viewer.Render()

    istyle.AddObserver('MouseWheelForwardEvent', mouse_wheel_forward_event)
    istyle.AddObserver('MouseWheelBackwardEvent', mouse_wheel_backward_event)

    viewer.Render()
    iren.Initialize()
    iren.Start()
