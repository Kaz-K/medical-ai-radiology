import pydicom as dicom


def decompress_dicom(path):
    """Decompresses dicom file.

    This function overwrites dicom files as decompressed format.
    GDCM is requred to work.
    # WARNING: path should not contain any multi-byte character.

    Args:
        path: path of dicom file.
    """
    dcm = dicom.read_file(path)
    transfer_syntax_uid = dcm.file_meta.TransferSyntaxUID
    if transfer_syntax_uid.is_compressed:
        dcm.decompress()
        dcm.save_as(path)
