import os
import vtk
import numpy as np
from collections import defaultdict

from utils import decompress_dicom_files
from utils import make_rectangle
from utils import make_actor
from utils import translate_polydata


# DICOM画像を格納するフォルダのパスをグローバル変数として指定する
DICOM_DIR_PATH = 'sample_dicom'


class BasicAnnotator(object):

    def __init__(self):
        super().__init__()

    def show(self, image):
        viewer = vtk.vtkImageViewer2()
        viewer.SetInputData(image)

        istyle = vtk.vtkInteractorStyleImage()
        iren = vtk.vtkRenderWindowInteractor()
        viewer.SetupInteractor(iren)
        iren.SetInteractorStyle(istyle)

        min_slice = viewer.GetSliceMin()
        max_slice = viewer.GetSliceMax()

        # 描画中の状態変数(slice番号等)を格納する
        # temp_actorにおいて各スライス毎のBoundingBoxを保存する
        actions = {
            'slice': min_slice,
            'start_point': None,
            'temp_actor': defaultdict(lambda: None),
        }

        # マウス・ホイールに対するコールバック関数
        def mouse_wheel_forward_event(caller, event):
            if actions['slice'] > min_slice:

                # 前のスライスのBoundingBoxを消去する
                if not actions['temp_actor'][actions['slice']] is None:
                    viewer.GetRenderer().RemoveActor(
                        actions['temp_actor'][actions['slice']]
                    )

                actions['slice'] -= 1

                # 次のスライスに定義済みのBoundingBoxがあれば描画する
                if not actions['temp_actor'][actions['slice']] is None:
                    viewer.GetRenderer().AddActor(
                        actions['temp_actor'][actions['slice']]
                    )

                viewer.SetSlice(actions['slice'])
                viewer.Render()

        def mouse_wheel_backward_event(caller, event):
            if actions['slice'] < max_slice:

                # 前のスライスのBoundingBoxを消去する
                if not actions['temp_actor'][actions['slice']] is None:
                    viewer.GetRenderer().RemoveActor(
                        actions['temp_actor'][actions['slice']]
                    )

                actions['slice'] += 1

                # 次のスライスに定義済みのBoundingBoxがあれば描画する
                if not actions['temp_actor'][actions['slice']] is None:
                    viewer.GetRenderer().AddActor(
                        actions['temp_actor'][actions['slice']]
                    )

                viewer.SetSlice(actions['slice'])
                viewer.Render()

        # イベントが起きた場所の座標を取得する
        def pick_coordinate():
            pos = iren.GetEventPosition()
            picker = vtk.vtkPropPicker()
            picker.Pick(pos[0], pos[1], 0, viewer.GetRenderer())
            point = np.array(picker.GetPickPosition())
            return point

        def start_drawing():
            actions['start_point'] = pick_coordinate()

            # 当該スライスに定義済みのBoundingBoxがあれば一旦消去する
            if not actions['temp_actor'][actions['slice']] is None:
                viewer.GetRenderer().RemoveActor(
                    actions['temp_actor'][actions['slice']]
                )

        def continue_drawing():
            correction_value = 0.01

            start_point = actions['start_point']
            current_point = pick_coordinate()

            # start_pointとcurrent_pointを対角とする長方形を描く
            polydata = make_rectangle(start_point, current_point)
            polydata = translate_polydata(polydata, 0, 0, correction_value)
            actor = make_actor(polydata)

            # 当該スライスに定義済みのBoundingBoxがあれば一旦消去する
            if not actions['temp_actor'][actions['slice']] is None:
                viewer.GetRenderer().RemoveActor(
                    actions['temp_actor'][actions['slice']]
                )

            viewer.GetRenderer().AddActor(actor)
            viewer.Render()
            actions['temp_actor'][actions['slice']] = actor

        def stop_drawing():
            actions['start_point'] = None

        def button_event(caller, event):
            if event == 'LeftButtonPressEvent':
                start_drawing()

            elif event == 'LeftButtonReleaseEvent':
                stop_drawing()

        def mouse_move(caller, event):
            if not actions['start_point'] is None:
                continue_drawing()

        istyle.AddObserver('MouseWheelForwardEvent', mouse_wheel_forward_event)
        istyle.AddObserver('MouseWheelBackwardEvent', mouse_wheel_backward_event)

        # アノテーションを行うためのイベントを定義する
        istyle.AddObserver("LeftButtonPressEvent", button_event)
        istyle.AddObserver("LeftButtonReleaseEvent", button_event)
        iren.AddObserver("MouseMoveEvent", mouse_move)

        viewer.Render()
        iren.Initialize()
        iren.Start()


if __name__ == '__main__':

    # 前処理として圧縮されたDICOMファイルを全て解凍する
    # decompress_dicom_files(DICOM_DIR_PATH)

    # vtkDICOMImageReaderでDICOM画像シリーズが格納されたフォルダを読み出す
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(DICOM_DIR_PATH)
    reader.Update()

    # vtkImageDataへと変換する
    image = reader.GetOutput()

    annotator = BasicAnnotator()
    annotator.show(image)
