import os
import vtk
import numpy as np
import pydicom as dicom


def scale_image(image, window_width, window_level):
    """
    画像の階調を変更する
    """
    max_value = window_level + window_width // 2      # 階調の最大
    min_value = window_level - window_width // 2      # 階調の最小

    # 最小値と最大値の間に収まる値以外をクリップする
    image = np.clip(image, min_value, max_value)

    image -= min_value                                # 階調の最小を0にする
    image /= window_width                             # 階調の最大を1にする
    image *= 255.0                                    # 階調の最大を255にする
    return image


def decompress_dicom_files(dir_path):
    """
    ディレクトリ内のDICOMファイルを読み出し、圧縮されたものを解凍して保存する
    """
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)

        dcm = dicom.read_file(file_path)
        transfer_syntax_uid = dcm.file_meta.TransferSyntaxUID
        if transfer_syntax_uid.is_compressed:
            dcm.decompress()
            dcm.save_as(file_path)


def make_rectangle(start_point, end_point):
    """
    start_pointとend_pointを対角とした長方形(vtkPolyData)を出力する
    """
    points = vtk.vtkPoints()
    points.SetNumberOfPoints(4)
    points.SetPoint(0, start_point[0], start_point[1], start_point[2])
    points.SetPoint(1, end_point[0], start_point[1], start_point[2])
    points.SetPoint(2, end_point[0], end_point[1], start_point[2])
    points.SetPoint(3, start_point[0], end_point[1], start_point[2])

    lines = vtk.vtkCellArray()
    lines.InsertNextCell(5)
    for i in range(4):
        lines.InsertCellPoint(i)
    lines.InsertCellPoint(0)

    rectangle = vtk.vtkPolyData()
    rectangle.SetPoints(points)
    rectangle.SetLines(lines)
    return rectangle


def make_actor(polydata, color=(1, 0, 0), width=2.0, opacity=1.0):
    """
    vtkPolyDataをvtkActorに変換する
    """
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetLineWidth(width)
    actor.GetProperty().SetOpacity(opacity)
    return actor


def translate_polydata(polydata, dx, dy, dz):
    """
    vtkPolyDataを平行移動させる
    """
    translate = vtk.vtkTransform()
    translate.Translate(dx, dy, dz)
    tf = vtk.vtkTransformPolyDataFilter()
    tf.SetInputData(polydata)
    tf.SetTransform(translate)
    tf.Update()
    polydata = tf.GetOutput()
    return polydata
