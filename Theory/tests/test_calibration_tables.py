from pathlib import Path

from sims.make_calibration_tables import generate_calibration_tables


def test_generate_calibration_tables(tmp_path):
    output_dir = tmp_path
    generate_calibration_tables(
        calibration_path='data/calibration.yaml',
        mrio_config='data/mrio_config.yaml',
        output_dir=str(output_dir),
    )

    calib_tex = Path(output_dir) / 'tables' / 'calibration_params.tex'
    sg_tex = Path(output_dir) / 'tables' / 'stone_geary_groups.tex'
    assert calib_tex.exists()
    assert sg_tex.exists()
    calib_text = calib_tex.read_text()
    assert 'Armington theta' in calib_text
